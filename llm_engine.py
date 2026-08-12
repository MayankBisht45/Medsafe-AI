import json
import re
import ollama

MODEL_NAME = "llama3"

def explain_interaction_with_llm(med_list, interaction_details):
    """Generates user-friendly explanations for flagged drug interactions."""
    prompt = f"""
    You are a clinical educational AI assistant.
    The user is taking these medications: {', '.join(med_list)}.
    
    A known interaction was flagged:
    {interaction_details}
    
    In clear, empathetic, and simple non-medical terms:
    1. Explain why taking these medications together can be unsafe.
    2. List 2-3 specific symptoms or side effects the user should monitor.
    3. State clearly that they should consult their doctor before changing doses.
    
    Keep your response concise (under 150 words).
    """
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Could not connect to Ollama: {str(e)}. Make sure Ollama is running."

def parse_prescription_ocr(ocr_text):
    """Uses LLaMA 3 to extract structured JSON data with robust string extraction."""
    prompt = f"""
    Extract medication names, dosages, and frequencies from the following raw OCR text:
    
    \"\"\"{ocr_text}\"\"\"
    
    You MUST output valid JSON ONLY with a root key named "medications" containing an array of objects.
    Each object must have these exact keys: "name", "dosage", "frequency".
    If a field is missing, set its value to "Not specified".
    Do NOT include any introduction, explanations, or markdown blocks.
    
    Example response format:
    {{"medications": [{{"name": "Diclofenac", "dosage": "40mg", "frequency": "0-0-1"}}]}}
    """
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_response = response["message"]["content"].strip()
        
        # Use regex to extract JSON content
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            clean_json_str = json_match.group(0)
            return json.loads(clean_json_str)
        else:
            return json.loads(raw_response)
            
    except Exception as e:
        return {"error": f"Failed to structure OCR text: {str(e)}", "raw": ocr_text}

def assess_symptoms_with_rules_and_llm(age, gender, symptom_text):
    """
    Evaluates symptoms using rule-based red flag checking combined with LLaMA 3 educational guidance.
    """
    # Rule-Based Red Flag Engine
    red_flags = [
        "chest pain", "shortness of breath", "difficulty breathing", 
        "fainting", "severe bleeding", "sudden paralysis", "confusion", 
        "coughing blood", "stiff neck with high fever"
    ]
    
    found_flags = [flag for flag in red_flags if flag in symptom_text.lower()]
    
    # Calculate emergency risk score
    if len(found_flags) >= 2:
        risk_score = 9
        risk_level = "CRITICAL / EMERGENCY"
    elif len(found_flags) == 1:
        risk_score = 7
        risk_level = "HIGH RISK"
    else:
        risk_score = 3
        risk_level = "MODERATE / LOW RISK"

    # LLaMA 3 Prompting
    prompt = f"""
    You are an educational AI healthcare assistant.
    Patient Demographics: Age {age}, Gender {gender}.
    Reported Symptoms: "{symptom_text}".
    Calculated Emergency Risk Score: {risk_score}/10 ({risk_level}).
    Identified Red Flag Symptoms: {', '.join(found_flags) if found_flags else 'None detected'}.
    
    Provide an educational response strictly formatted as follows:
    1. **Possible Causes**: List 2-3 non-definitive educational possibilities.
    2. **Home-Care & Comfort Measures**: 2 simple suggestions (e.g., hydration, rest).
    3. **Warning Indicators**: Specific signs that mean they must go to an Emergency Room immediately.
    
    Keep the tone empathetic, clear, and under 200 words. Always include an ethical medical disclaimer.
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        ai_guidance = response["message"]["content"]
    except Exception as e:
        ai_guidance = f"Unable to generate AI guidance: {str(e)}"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "red_flags": found_flags,
        "guidance": ai_guidance
    }