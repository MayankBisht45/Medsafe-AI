import streamlit as st
from matcher import load_medicine_data, match_medicine_name, check_drug_interactions
from ocr_engine import extract_text_from_image
from llm_engine import explain_interaction_with_llm, parse_prescription_ocr, assess_symptoms_with_rules_and_llm

db = load_medicine_data()

st.set_page_config(page_title="MedSafe AI - Healthcare Dashboard", page_icon="🏥", layout="wide")
st.title("🏥 MedSafe AI")
st.caption("⚠️ **Educational Tool Only**: MedSafe AI provides preventive information and does not replace professional medical diagnosis.")
st.divider()

tab1, tab2, tab3 = st.tabs(["💊 Medicine Interaction", "📄 Prescription OCR", "🩺 Symptom Risk Assessment"])

# --- SCENARIO 1: INTERACTION ANALYSIS ---
with tab1:
    st.header("Scenario 1: Medicine Interaction Analysis")
    raw_input = st.text_input("Medication names (separated by commas):", value="Aspirne, Warfren")
    
    if st.button("Analyze Interactions", type="primary"):
        input_list = [item.strip() for item in raw_input.split(",") if item.strip()]
        matched_meds = []
        
        st.markdown("### 🔎 Recognized Medicines")
        for item in input_list:
            canonical_name, score = match_medicine_name(item, db["medicines"])
            if canonical_name:
                matched_meds.append(canonical_name)
                st.write(f"✅ Input: `{item}` ➡️ **{canonical_name}** ({score}% match)")
            else:
                st.write(f"❌ Input: `{item}` ➡️ *Not found*")
        
        unique_matched = list(set(matched_meds))
        if len(unique_matched) >= 2:
            results = check_drug_interactions(unique_matched, db["interactions"])
            st.markdown("---")
            st.markdown("### ⚠️ Safety Alerts")
            
            if not results:
                st.success("No known interactions found in local database.")
            else:
                for alert in results:
                    st.error(f"🚨 **{alert['severity']} Risk:** {' + '.join(alert['pair'])}")
                    with st.spinner("LLaMA 3 generating plain-language guidance..."):
                        ai_explanation = explain_interaction_with_llm(unique_matched, alert["description"])
                        st.markdown(f"**🤖 AI Explanation:**\n{ai_explanation}")

# --- SCENARIO 2: PRESCRIPTION OCR ---
with tab2:
    st.header("Scenario 2: Prescription OCR & AI Structuring")
    uploaded_file = st.file_uploader("Upload Prescription Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        col_img, col_ocr = st.columns(2)
        with col_img:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
        with col_ocr:
            if st.button("Extract & Process Prescription", type="primary"):
                with st.spinner("Running Tesseract OCR & LLaMA 3..."):
                    raw_text = extract_text_from_image(uploaded_file)
                    structured_data = parse_prescription_ocr(raw_text)
                    
                st.markdown("### 📋 Extracted Medications")
                if "medications" in structured_data:
                    st.table(structured_data["medications"])
                else:
                    st.json(structured_data)

# --- SCENARIO 3: SYMPTOM RISK ASSESSMENT ---
with tab3:
    st.header("Scenario 3: Symptom Guidance & Risk Assessment")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Patient Age", min_value=1, max_value=120, value=30)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
    symptoms = st.text_area(
        "Describe your symptoms in detail:",
        placeholder="e.g., I have a slight headache, fever, and chest pain when taking deep breaths."
    )
    
    if st.button("Assess Symptoms & Evaluate Risk", type="primary"):
        if not symptoms.strip():
            st.warning("Please describe your symptoms first.")
        else:
            with st.spinner("Analyzing risk indicators and generating guidance..."):
                assessment = assess_symptoms_with_rules_and_llm(age, gender, symptoms)
                
            st.markdown("---")
            st.markdown("### 📊 Emergency Risk Assessment")
            
            # Display Risk Score Meter
            score = assessment["risk_score"]
            if score >= 7:
                st.error(f"🚨 **Emergency Risk Score: {score}/10 ({assessment['risk_level']})**")
            else:
                st.success(f"🟢 **Emergency Risk Score: {score}/10 ({assessment['risk_level']})**")
                
            if assessment["red_flags"]:
                st.warning(f"⚠️ **Red Flag Keywords Detected:** {', '.join(assessment['red_flags'])}")
                
            st.markdown("### 🤖 Educational Guidance")
            st.markdown(assessment["guidance"])