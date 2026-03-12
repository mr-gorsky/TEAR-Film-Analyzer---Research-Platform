"""
TEAR-Film Analyzer - Research Platform
TEAR-RG Compliant Data Collection for Tear Fluid Phenotyping
Maastricht UMC - TEAR-Precision Version
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time
import io

# Page config
st.set_page_config(
    page_title="TEAR-Film Analyzer - Maastricht UMC",
    page_icon="🧪",
    layout="wide"
)

# Initialize session state
if 'biomarker_data' not in st.session_state:
    st.session_state.biomarker_data = {
        "IL-6": 0.0,
        "TNF-α": 0.0,
        "MMP-9": 0.0,
        "Lactoferrin": 0.0,
        "Lysozyme": 0.0
    }

if 'all_patients' not in st.session_state:
    st.session_state.all_patients = []

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
    
if 'user_site' not in st.session_state:
    st.session_state.user_site = None
    
# Custom CSS za pozicioniranje loga
st.markdown("""
<style>
    .logo-container {
        position: fixed;
        top: 10px;
        right: 20px;
        z-index: 1000;
        background-color: white;
        padding: 5px 15px;
        border-radius: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .logo-container img {
        height: 40px;
        width: auto;
    }
    @media print {
        .logo-container {
            display: none;
        }
    }
</style>

<div class="logo-container">
    <img src="https://i.postimg.cc/Kjsbj7xY/Phantasmed-logo.png" alt="Phantasmed Logo">
</div>
""", unsafe_allow_html=True)
# Header
st.title("🧪 TEAR-Film Analyzer")
st.markdown("### Maastricht UMC - TEAR-Precision Research Platform")
st.markdown("---")

# ============================================
# 2️⃣ USER LOGIN SYSTEM - MAASTRICHT VERSION
# ============================================
with st.sidebar:
    if not st.session_state.authenticated:
        st.header("🔐 Login")
        
        # Site selection - Maastricht fokus
        site = st.selectbox("Select Site", [
            "Maastricht UMC - Core Lab",
            "Maastricht UMC - Clinic",
            "External Collaborator"
        ])
        
        # Role selection
        role = st.selectbox("Role", [
            "Principal Investigator",
            "Clinician",
            "Lab Technician",
            "Researcher",
            "Study Coordinator"
        ])
        
        # Simple login with Maastricht password
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            # Maastricht password for TEAR-Precision
            if password == "tear2025":  # Pilot password - change for production
                st.session_state.authenticated = True
                st.session_state.user_site = site
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Invalid password. For TEAR-Precision pilot use: tear2025")
    else:
        st.header(f"✅ Logged In")
        st.write(f"**Site:** {st.session_state.user_site}")
        st.write(f"**Role:** {st.session_state.user_role}")
        st.write(f"**Institution:** Maastricht UMC")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.user_site = None
            st.rerun()

# Only show main app if authenticated
if st.session_state.authenticated:
    
    # Sidebar - Study Info (uvijek vidljivo)
    with st.sidebar:
        st.markdown("---")
        st.header("📋 Study Information")
        
        study_id = st.text_input("Study ID", value="TP-2025-001")
        # Site ID automatski iz logina
        site_id = "MUMC"
        st.info(f"**Site ID:** {site_id}")
        
        patient_id = st.text_input("Patient ID", value="P-001")
        visit_number = st.number_input("Visit Number", min_value=1, max_value=10, value=1)
        
        # Eye selection - sada za oba oka
        st.subheader("👁️ Eyes Examined")
        eyes_to_examine = st.multiselect(
            "Select eyes for this visit",
            ["OD", "OS"],
            default=["OD", "OS"]
        )
        
        exam_date = st.date_input("Examination Date", datetime.now())
        
        st.markdown("---")
        st.caption("TEAR-RG v1.0 | Delphi Consensus 2025")
    
    # Glavni tabovi
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👤 Demographics", 
        "👁️ Clinical Data", 
        "🧪 Tear Collection", 
        "🔬 Sample Processing",
        "📊 Biomarkers",
        "📈 Visualizations"
    ])
    
    # ============================================
    # 3️⃣ PATIENT DEMOGRAPHICS
    # ============================================
    with tab1:
        st.header("Patient Demographics")
        st.caption("Important confounders for biomarker analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=50)
            sex = st.selectbox("Sex", ["Male", "Female", "Other", "Prefer not to say"])
            
            st.subheader("Systemic Diseases")
            st.caption("Select all that apply")
            systemic_diseases = st.multiselect(
                "Systemic conditions",
                ["None", "Diabetes", "Hypertension", "Rheumatoid Arthritis", 
                 "Sjögren's Syndrome", "Thyroid disease", "Allergies", "Other"]
            )
            
        with col2:
            st.subheader("Current Medications")
            st.caption("Medications that may affect tear film")
            medications = st.multiselect(
                "Medications",
                ["None", "Antihistamines", "Antidepressants", "Beta-blockers",
                 "Diuretics", "Hormone therapy", "Immunosuppressants", "Other"]
            )
            
            st.subheader("Other Factors")
            smoking = st.radio("Smoking status", ["Never", "Former", "Current"])
            cl_wear_general = st.radio("Contact lens wearer", ["Yes", "No"])
    
    # ============================================
    # 4️⃣ EYE-SPECIFIC CLINICAL DATA
    # ============================================
    with tab2:
        st.header("Clinical Phenotyping")
        st.caption("Separate measurements for each eye")
        
        # OD Data
        if "OD" in eyes_to_examine:
            with st.expander("👁️ Right Eye (OD)", expanded=True):
                col_od1, col_od2 = st.columns(2)
                
                with col_od1:
                    st.subheader("Tear Film Stability")
                    tbut_od = st.number_input("TBUT OD (seconds)", 0.0, 30.0, 10.0, 0.5, key="tbut_od")
                    tbut_method_od = st.selectbox("TBUT Method OD", ["Fluorescein", "Non-invasive", "Keratograph", "Other"], key="tbut_method_od")
                    nibut_od = st.number_input("NIBUT OD (seconds)", 0.0, 30.0, 10.0, 0.5, key="nibut_od")
                    
                with col_od2:
                    st.subheader("Staining")
                    corneal_staining_od = st.selectbox("Corneal Staining OD", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"], key="corneal_od")
                    conjunctival_staining_od = st.selectbox("Conjunctival Staining OD", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"], key="conj_od")
                    
                    st.subheader("Tear Volume")
                    schirmer_od = st.number_input("Schirmer I OD (mm/5min)", 0, 35, 15, key="schirmer_od")
                    tmh_od = st.number_input("Tear Meniscus Height OD (mm)", 0.0, 1.0, 0.3, 0.05, key="tmh_od")
        
        # OS Data
        if "OS" in eyes_to_examine:
            with st.expander("👁️ Left Eye (OS)", expanded=True):
                col_os1, col_os2 = st.columns(2)
                
                with col_os1:
                    st.subheader("Tear Film Stability")
                    tbut_os = st.number_input("TBUT OS (seconds)", 0.0, 30.0, 10.0, 0.5, key="tbut_os")
                    tbut_method_os = st.selectbox("TBUT Method OS", ["Fluorescein", "Non-invasive", "Keratograph", "Other"], key="tbut_method_os")
                    nibut_os = st.number_input("NIBUT OS (seconds)", 0.0, 30.0, 10.0, 0.5, key="nibut_os")
                    
                with col_os2:
                    st.subheader("Staining")
                    corneal_staining_os = st.selectbox("Corneal Staining OS", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"], key="corneal_os")
                    conjunctival_staining_os = st.selectbox("Conjunctival Staining OS", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"], key="conj_os")
                    
                    st.subheader("Tear Volume")
                    schirmer_os = st.number_input("Schirmer I OS (mm/5min)", 0, 35, 15, key="schirmer_os")
                    tmh_os = st.number_input("Tear Meniscus Height OS (mm)", 0.0, 1.0, 0.3, 0.05, key="tmh_os")
        
        # Common staining parameters
        st.subheader("Staining Details")
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            staining_method = st.selectbox("Staining Method", ["Fluorescein", "Lissamine Green", "Rose Bengal", "None"])
        with col_st2:
            staining_scale = st.selectbox("Staining Scale", ["Oxford (0-5)", "NEI (0-15)", "Baylor (0-4)"])
    
    # ============================================
    # 5️⃣ TEAR COLLECTION WITH TIMESTAMP
    # ============================================
    with tab3:
        st.header("Tear Collection")
        st.caption("TEAR-RG Collection items C1-C12")
        
        # 6️⃣ SAMPLING TIMESTAMP - circadian variation
        st.subheader("⏰ Collection Time")
        st.caption("Critical for circadian variation in tear proteins")
        
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            collection_date = st.date_input("Collection Date", datetime.now(), key="collection_date")
        with col_time2:
            collection_time = st.time_input("Exact Collection Time", datetime.now().time(), key="collection_time")
        
        # Automatska kategorizacija doba dana
        hour = collection_time.hour
        if 5 <= hour < 12:
            time_category = "Morning"
        elif 12 <= hour < 17:
            time_category = "Afternoon"
        elif 17 <= hour < 21:
            time_category = "Evening"
        else:
            time_category = "Night"
        
        st.info(f"**Time category:** {time_category} - important for circadian variation")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            collection_method = st.selectbox("Collection Method", ["Schirmer strip", "Capillary tube", "Sponge", "Flush", "Other"])
            anesthesia_used = st.radio("Anesthesia Used", ["Yes", "No"])
            tear_volume = st.number_input("Tear Volume Collected (μL)", 0, 100, 10)
            
        with col2:
            cl_wear = st.radio("Contact Lens Wear at Collection", ["Yes", "No"])
            if cl_wear == "Yes":
                cl_type = st.text_input("Lens Type", "")
                cl_duration = st.text_input("Wear duration", "")
            
            eye_status = st.multiselect("Eye Status", ["Healthy", "Dry Eye", "MGD", "Blepharitis", "Allergy", "Other"])
            collection_site = st.selectbox("Collection Site", ["Lower fornix", "Lateral canthus", "Medial canthus", "Whole meniscus"])
            
        st.subheader("Sample Details")
        col3, col4 = st.columns(2)
        with col3:
            num_strips = st.number_input("Number of strips/tubes", 1, 5, 1)
            collection_duration = st.number_input("Collection duration (seconds)", 10, 300, 60)
        with col4:
            pooling = st.selectbox("Pooling of samples", ["No", "Yes - both eyes", "Yes - multiple strips", "Yes - other"])
            blood_contamination = st.selectbox("Blood contamination", ["None", "Trace", "Visible", "Not assessed"])
    
    # TAB 4: Sample Processing
    with tab4:
        st.header("Sample Storage & Processing")
        st.caption("TEAR-RG Storage S1-S3 and Processing P1-P6")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Storage")
            time_to_freezing = st.number_input("Time to freezing (minutes)", 0, 240, 30)
            storage_temp = st.selectbox("Storage temperature", ["-80°C", "-20°C", "4°C", "Liquid N2", "Room temp"])
            transport = st.text_input("Transport conditions", "Dry ice, overnight")
            
            st.subheader("Centrifugation")
            centrifugation = st.radio("Centrifugation performed", ["Yes", "No"])
            if centrifugation == "Yes":
                centrifuge_speed = st.number_input("Speed (g)", 0, 20000, 10000)
                centrifuge_time = st.number_input("Time (minutes)", 0, 60, 10)
                centrifuge_temp = st.number_input("Temperature (°C)", -10, 30, 4)
        
        with col2:
            st.subheader("Elution")
            elution_buffer = st.text_input("Elution buffer", "PBS + 0.05% Tween")
            elution_volume = st.number_input("Elution volume (μL)", 50, 1000, 200)
            elution_time = st.number_input("Elution time (minutes)", 1, 120, 30)
            dilution_factor = st.number_input("Dilution factor", 1.0, 100.0, 1.0)
            
            st.subheader("Processing")
            protease_inhibitors = st.radio("Protease inhibitors", ["Yes", "No"])
            if protease_inhibitors == "Yes":
                inhibitor_type = st.text_input("Inhibitor type", "Complete™")
            freeze_thaw = st.number_input("Freeze-thaw cycles", 0, 10, 1)
    
    # ============================================
    # 5️⃣ BIOMARKERS WITH UNIT VALIDATION
    # ============================================
    with tab5:
        st.header("Biomarker Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Biomarker Panel")
            st.caption("Values must be positive numbers")
            
            # Input za svaki biomarker s validacijom
            for biomarker in ["IL-6", "TNF-α", "MMP-9", "Lactoferrin", "Lysozyme"]:
                units = {"IL-6": "pg/mL", "TNF-α": "pg/mL", "MMP-9": "ng/mL", 
                        "Lactoferrin": "mg/mL", "Lysozyme": "μg/mL"}
                
                col_b1, col_b2 = st.columns([3, 1])
                with col_b1:
                    value = st.number_input(
                        f"{biomarker} ({units[biomarker]})",
                        value=st.session_state.biomarker_data[biomarker],
                        min_value=0.0,  # SPRJEČAVA NEGATIVNE VRIJEDNOSTI
                        format="%.2f",
                        key=f"input_{biomarker}"
                    )
                    st.session_state.biomarker_data[biomarker] = value
                
                with col_b2:
                    st.caption(f"Unit: {units[biomarker]}")
                    
                    # Unit validation warnings
                    if biomarker in ["IL-6", "TNF-α"] and value > 1000:
                        st.warning("⚠️ >1000 pg/mL - verify value")
                    elif biomarker == "MMP-9" and value > 500:
                        st.warning("⚠️ >500 ng/mL - verify value")
        
        with col2:
            st.subheader("Analysis Method")
            analytical_method = st.selectbox("Method", ["ELISA", "MS", "Luminex", "Western Blot", "Other"])
            assay_validation = st.text_input("Validation", "CV% < 10%")
            lod = st.number_input("LOD", 0.0, 100.0, 1.0)
            loq = st.number_input("LOQ", 0.0, 100.0, 3.0)
            qc_used = st.radio("QC samples", ["Yes", "No"])
        
        # EXPORT SEKCIJA
        st.markdown("---")
        st.header("📥 Data Export")
        
        # Prikupi sve podatke u jedan dictionary
        current_patient = {
            # Study info
            "study_id": study_id,
            "site_id": site_id,
            "site_full": st.session_state.user_site,
            "user_role": st.session_state.user_role,
            "institution": "Maastricht UMC",
            "patient_id": patient_id,
            "visit_number": visit_number,
            "exam_date": str(exam_date),
            "eyes_examined": ", ".join(eyes_to_examine),
            
            # Demographics
            "age": age,
            "sex": sex,
            "systemic_diseases": ", ".join(systemic_diseases) if systemic_diseases else "",
            "medications": ", ".join(medications) if medications else "",
            "smoking": smoking,
            "cl_wearer": cl_wear_general,
            
            # Clinical - OD
            "tbut_od": tbut_od if "OD" in eyes_to_examine else None,
            "tbut_method_od": tbut_method_od if "OD" in eyes_to_examine else None,
            "nibut_od": nibut_od if "OD" in eyes_to_examine else None,
            "corneal_staining_od": corneal_staining_od if "OD" in eyes_to_examine else None,
            "conjunctival_staining_od": conjunctival_staining_od if "OD" in eyes_to_examine else None,
            "schirmer_od": schirmer_od if "OD" in eyes_to_examine else None,
            "tmh_od": tmh_od if "OD" in eyes_to_examine else None,
            
            # Clinical - OS
            "tbut_os": tbut_os if "OS" in eyes_to_examine else None,
            "tbut_method_os": tbut_method_os if "OS" in eyes_to_examine else None,
            "nibut_os": nibut_os if "OS" in eyes_to_examine else None,
            "corneal_staining_os": corneal_staining_os if "OS" in eyes_to_examine else None,
            "conjunctival_staining_os": conjunctival_staining_os if "OS" in eyes_to_examine else None,
            "schirmer_os": schirmer_os if "OS" in eyes_to_examine else None,
            "tmh_os": tmh_os if "OS" in eyes_to_examine else None,
            
            # Common staining
            "staining_method": staining_method,
            "staining_scale": staining_scale,
            
            # Collection with timestamp
            "collection_date": str(collection_date),
            "collection_time": str(collection_time),
            "time_category": time_category,
            "collection_method": collection_method,
            "anesthesia_used": anesthesia_used,
            "tear_volume": tear_volume,
            "cl_wear_at_collection": cl_wear,
            "cl_type": cl_type if cl_wear == "Yes" else "",
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
            "centrifuge_temp": centrifuge_temp if centrifugation == "Yes" else "",
            "elution_buffer": elution_buffer,
            "elution_volume": elution_volume,
            "elution_time": elution_time,
            "dilution_factor": dilution_factor,
            "protease_inhibitors": protease_inhibitors,
            "inhibitor_type": inhibitor_type if protease_inhibitors == "Yes" else "",
            "freeze_thaw": freeze_thaw,
            
            # Analysis
            "analytical_method": analytical_method,
            "assay_validation": assay_validation,
            "lod": lod,
            "loq": loq,
            "qc_used": qc_used,
            
            # Biomarkers
            "IL6_value": st.session_state.biomarker_data["IL-6"],
            "TNFa_value": st.session_state.biomarker_data["TNF-α"],
            "MMP9_value": st.session_state.biomarker_data["MMP-9"],
            "Lactoferrin_value": st.session_state.biomarker_data["Lactoferrin"],
            "Lysozyme_value": st.session_state.biomarker_data["Lysozyme"]
        }
        
        # Spremi u session state za bulk export
        if st.button("💾 Save Current Patient to Session"):
            st.session_state.all_patients.append(current_patient)
            st.success(f"Saved patient {patient_id} (Total: {len(st.session_state.all_patients)})")
        
        df_current = pd.DataFrame([current_patient])
        
        # Export opcije
        col_csv, col_excel, col_bulk = st.columns(3)
        
        with col_csv:
            csv = df_current.to_csv(index=False)
            st.download_button(
                label="📥 Download Current as CSV",
                data=csv,
                file_name=f"tear_rg_{site_id}_{patient_id}_visit{visit_number}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_excel:
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_current.to_excel(writer, index=False, sheet_name='TEAR-RG_Data')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📊 Download Current as Excel",
                    data=excel_data,
                    file_name=f"tear_rg_{site_id}_{patient_id}_visit{visit_number}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except:
                st.warning("Excel export zahtijeva openpyxl")
        
        with col_bulk:
            if len(st.session_state.all_patients) > 0:
                df_bulk = pd.DataFrame(st.session_state.all_patients)
                bulk_csv = df_bulk.to_csv(index=False)
                
                st.download_button(
                    label=f"📦 Bulk Export ({len(st.session_state.all_patients)} patients)",
                    data=bulk_csv,
                    file_name=f"tear_rg_{site_id}_bulk_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No saved patients yet. Click 'Save Current Patient' to add.")
        
        # Preview
        with st.expander("Preview current patient data"):
            st.dataframe(df_current, use_container_width=True)

    # TAB 6: Visualizations
    with tab6:
        st.header("📈 Exploratory Data Analysis")
        st.caption("Upload your exported data for visualization")
        
        uploaded_file = st.file_uploader("Upload CSV or Excel file for analysis", type=['csv', 'xlsx'])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"Loaded {len(df)} records from Maastricht UMC dataset")
                
                with st.expander("📊 Dataset Overview"):
                    st.dataframe(df.describe(), use_container_width=True)
                
                col_v1, col_v2 = st.columns(2)
                
                with col_v1:
                    st.subheader("TBUT Distribution")
                    tbut_cols = [col for col in df.columns if 'tbut' in col.lower()]
                    if tbut_cols:
                        for col in tbut_cols[:2]:
                            if col in df.columns:
                                fig_tbut = px.histogram(
                                    df, x=col, nbins=20,
                                    title=f'{col} Distribution - Maastricht Cohort',
                                    labels={col: col, 'count': 'Number of Patients'}
                                )
                                st.plotly_chart(fig_tbut, use_container_width=True)
                
                with col_v2:
                    st.subheader("Biomarker Correlations")
                    biomarker_cols = [col for col in df.columns if any(b in col for b in ['IL6', 'TNF', 'MMP9'])]
                    if len(biomarker_cols) >= 2:
                        corr_matrix = df[biomarker_cols].corr()
                        fig_heatmap = px.imshow(
                            corr_matrix,
                            text_auto=True,
                            aspect="auto",
                            title="Biomarker Correlations - Maastricht Data"
                        )
                        st.plotly_chart(fig_heatmap, use_container_width=True)
                        
            except Exception as e:
                st.error(f"Error loading file: {e}")
        else:
            st.info("👆 Upload your exported CSV or Excel file to see visualizations")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>TEAR-Film Analyzer v3.0</strong> | Maastricht UMC - TEAR-Precision</p>
        <p style="font-size: 0.8rem;">Based on: Schmeetz J, et al. Contact Lens and Anterior Eye 2025;48:102448</p>
        <p style="font-size: 0.8rem;">For research use only | WG1, WG2, WG3, WG8 ready</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # Show login prompt
    st.info("👈 Please log in using the sidebar to access the TEAR-Precision platform")
    st.image("https://www.maastrichtuniversity.nl/sites/default/files/styles/medium/public/logo_maastricht_university.png", width=300)
