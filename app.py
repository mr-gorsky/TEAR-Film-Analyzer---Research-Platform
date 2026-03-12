"""
TEAR-Film Analyzer - Research Platform
TEAR-RG Compliant Data Collection for Tear Fluid Phenotyping
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Page config
st.set_page_config(
    page_title="TEAR-Film Analyzer",
    page_icon="🧪",
    layout="wide"
)

# Initialize session state for biomarkers
if 'biomarker_data' not in st.session_state:
    st.session_state.biomarker_data = {
        "IL-6": 0.0,
        "TNF-α": 0.0,
        "MMP-9": 0.0,
        "Lactoferrin": 0.0,
        "Lysozyme": 0.0
    }

# Header
st.title("🧪 TEAR-Film Analyzer")
st.markdown("### Research Platform for Tear Fluid Phenotyping")
st.markdown("---")

# Sidebar - Study Info (uvijek vidljivo)
with st.sidebar:
    st.header("📋 Study Information")
    
    study_id = st.text_input("Study ID", value="TP-2025-001")
    site_id = st.text_input("Site ID", value="SITE-01")
    patient_id = st.text_input("Patient ID", value="P-001")
    visit_number = st.number_input("Visit Number", min_value=1, max_value=10, value=1)
    eye_examined = st.selectbox("Eye Examined", ["OD", "OS", "Both"])
    exam_date = st.date_input("Examination Date", datetime.now())
    
    st.markdown("---")
    st.caption("TEAR-RG v1.0 | Delphi Consensus 2025")

# Glavni tabovi
tab1, tab2, tab3, tab4 = st.tabs([
    "👁️ Clinical Data", 
    "🧪 Tear Collection", 
    "🔬 Sample Processing",
    "📊 Biomarkers & Export"
])

# TAB 1: Clinical Data
with tab1:
    st.header("Clinical Phenotyping")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Symptoms")
        osdi_score = st.slider("OSDI Score (0-100)", 0, 100, 25)
        deq5_score = st.slider("DEQ-5 Score (0-22)", 0, 22, 8)
        
        st.subheader("Tear Film Stability")
        tbut = st.number_input("TBUT (seconds)", 0.0, 30.0, 10.0, 0.5)
        tbut_method = st.selectbox("TBUT Method", ["Fluorescein", "Non-invasive", "Keratograph"])
        nibut = st.number_input("NIBUT (seconds)", 0.0, 30.0, 10.0, 0.5)
    
    with col2:
        st.subheader("Ocular Surface Staining")
        staining_method = st.selectbox("Staining Method", ["Fluorescein", "Lissamine Green", "Rose Bengal"])
        staining_scale = st.selectbox("Staining Scale", ["Oxford (0-5)", "NEI (0-15)"])
        corneal_staining = st.selectbox("Corneal Staining", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"])
        conjunctival_staining = st.selectbox("Conjunctival Staining", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"])
        
        st.subheader("Tear Volume")
        schirmer = st.number_input("Schirmer I (mm/5min)", 0, 35, 15)
        tmh = st.number_input("Tear Meniscus Height (mm)", 0.0, 1.0, 0.3, 0.05)

# TAB 2: Tear Collection (TEAR-RG Collection items)
with tab2:
    st.header("Tear Collection")
    st.caption("TEAR-RG Collection items C1-C12")
    
    col1, col2 = st.columns(2)
    
    with col1:
        collection_method = st.selectbox("Collection Method", ["Schirmer strip", "Capillary tube", "Sponge", "Flush"])
        anesthesia_used = st.radio("Anesthesia Used", ["Yes", "No"])
        tear_volume = st.number_input("Tear Volume Collected (μL)", 0, 100, 10)
        collection_time = st.time_input("Collection Time", datetime.now().time())
        
    with col2:
        cl_wear = st.radio("Contact Lens Wear", ["Yes", "No"])
        if cl_wear == "Yes":
            cl_type = st.text_input("Lens Type", "")
        
        eye_status = st.multiselect("Eye Status", ["Healthy", "Dry Eye", "MGD", "Blepharitis", "Allergy"])
        collection_site = st.selectbox("Collection Site", ["Lower fornix", "Lateral canthus", "Medial canthus"])
        
    st.subheader("Sample Details")
    col3, col4 = st.columns(2)
    with col3:
        num_strips = st.number_input("Number of strips/tubes", 1, 5, 1)
        collection_duration = st.number_input("Collection duration (seconds)", 10, 300, 60)
    with col4:
        pooling = st.selectbox("Pooling of samples", ["No", "Yes - both eyes", "Yes - multiple strips"])
        blood_contamination = st.selectbox("Blood contamination", ["None", "Trace", "Visible"])

# TAB 3: Sample Processing
with tab3:
    st.header("Sample Storage & Processing")
    st.caption("TEAR-RG Storage S1-S3 and Processing P1-P6")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Storage")
        time_to_freezing = st.number_input("Time to freezing (minutes)", 0, 240, 30)
        storage_temp = st.selectbox("Storage temperature", ["-80°C", "-20°C", "4°C", "Liquid N2"])
        transport = st.text_input("Transport conditions", "Dry ice")
        
        st.subheader("Centrifugation")
        centrifugation = st.radio("Centrifugation performed", ["Yes", "No"])
        if centrifugation == "Yes":
            centrifuge_speed = st.number_input("Speed (g)", 0, 20000, 10000)
            centrifuge_time = st.number_input("Time (minutes)", 0, 60, 10)
    
    with col2:
        st.subheader("Elution")
        elution_buffer = st.text_input("Elution buffer", "PBS + 0.05% Tween")
        elution_volume = st.number_input("Elution volume (μL)", 50, 1000, 200)
        elution_time = st.number_input("Elution time (minutes)", 1, 120, 30)
        dilution_factor = st.number_input("Dilution factor", 1.0, 100.0, 1.0)
        
        st.subheader("Processing")
        protease_inhibitors = st.radio("Protease inhibitors", ["Yes", "No"])
        freeze_thaw = st.number_input("Freeze-thaw cycles", 0, 10, 1)

# TAB 4: Biomarkers & Export
with tab4:
    st.header("Biomarker Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Biomarker Panel")
        
        # Input za svaki biomarker
        for biomarker in ["IL-6", "TNF-α", "MMP-9", "Lactoferrin", "Lysozyme"]:
            units = {"IL-6": "pg/mL", "TNF-α": "pg/mL", "MMP-9": "ng/mL", 
                    "Lactoferrin": "mg/mL", "Lysozyme": "μg/mL"}
            
            value = st.number_input(
                f"{biomarker} ({units[biomarker]})",
                value=st.session_state.biomarker_data[biomarker],
                format="%.2f",
                key=f"input_{biomarker}"
            )
            st.session_state.biomarker_data[biomarker] = value
    
    with col2:
        st.subheader("Analysis Method")
        analytical_method = st.selectbox("Method", ["ELISA", "MS", "Luminex"])
        lod = st.number_input("LOD", 0.0, 100.0, 1.0)
        loq = st.number_input("LOQ", 0.0, 100.0, 3.0)
    
    # EXPORT SEKCIJA
    st.markdown("---")
    st.header("📥 Data Export")
    
    # Prikupi sve podatke u jedan dictionary
    all_data = {
        # Study info
        "study_id": study_id,
        "site_id": site_id,
        "patient_id": patient_id,
        "visit_number": visit_number,
        "eye_examined": eye_examined,
        "exam_date": str(exam_date),
        
        # Clinical
        "osdi_score": osdi_score,
        "deq5_score": deq5_score,
        "tbut": tbut,
        "tbut_method": tbut_method,
        "nibut": nibut,
        "staining_method": staining_method,
        "staining_scale": staining_scale,
        "corneal_staining": corneal_staining,
        "conjunctival_staining": conjunctival_staining,
        "schirmer": schirmer,
        "tmh": tmh,
        
        # Collection
        "collection_method": collection_method,
        "anesthesia_used": anesthesia_used,
        "tear_volume": tear_volume,
        "collection_time": str(collection_time),
        "cl_wear": cl_wear,
        "eye_status": ", ".join(eye_status) if eye_status else "",
        "collection_site": collection_site,
        "num_strips": num_strips,
        "collection_duration": collection_duration,
        "pooling": pooling,
        "blood_contamination": blood_contamination,
        
        # Storage & Processing
        "time_to_freezing": time_to_freezing,
        "storage_temp": storage_temp,
        "transport": transport,
        "centrifugation": centrifugation,
        "centrifuge_speed": centrifuge_speed if centrifugation == "Yes" else "",
        "centrifuge_time": centrifuge_time if centrifugation == "Yes" else "",
        "elution_buffer": elution_buffer,
        "elution_volume": elution_volume,
        "elution_time": elution_time,
        "dilution_factor": dilution_factor,
        "protease_inhibitors": protease_inhibitors,
        "freeze_thaw": freeze_thaw,
        
        # Analysis
        "analytical_method": analytical_method,
        "lod": lod,
        "loq": loq,
        
        # Biomarkers
        "IL6_value": st.session_state.biomarker_data["IL-6"],
        "TNFa_value": st.session_state.biomarker_data["TNF-α"],
        "MMP9_value": st.session_state.biomarker_data["MMP-9"],
        "Lactoferrin_value": st.session_state.biomarker_data["Lactoferrin"],
        "Lysozyme_value": st.session_state.biomarker_data["Lysozyme"]
    }
    
    df = pd.DataFrame([all_data])
    
    # CSV Export
    col_csv, col_excel = st.columns(2)
    
    with col_csv:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"tear_rg_{patient_id}_visit{visit_number}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_excel:
        try:
            # Probaj Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='TEAR-RG_Data')
            excel_data = output.getvalue()
            
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"tear_rg_{patient_id}_visit{visit_number}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except:
            st.warning("Excel export zahtijeva 'openpyxl'. Instaliraj: pip install openpyxl")
            st.download_button(
                label="📊 Download CSV (Excel alternative)",
                data=csv,
                file_name=f"tear_rg_{patient_id}_visit{visit_number}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Preview
    with st.expander("Preview data"):
        st.dataframe(df, use_container_width=True)
    
    # TEAR-RG info
    st.info("✅ This dataset includes all TEAR-RG recommended items from the Delphi consensus (34 items)")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>TEAR-Film Analyzer v2.0</strong> | For research use only</p>
    <p style="font-size: 0.8rem;">Based on: Schmeetz J, et al. Contact Lens and Anterior Eye 2025;48:102448</p>
</div>
""", unsafe_allow_html=True)
