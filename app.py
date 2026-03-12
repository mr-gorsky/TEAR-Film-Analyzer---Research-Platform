"""
TEAR-Film Analyzer - Research Platform
TEAR-RG Compliant Data Collection for Tear Fluid Phenotyping
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Page config
st.set_page_config(
    page_title="TEAR-Film Analyzer",
    page_icon="🧪",
    layout="wide"
)

# Initialize session state for biomarkers and stored data
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👁️ Clinical Data", 
    "🧪 Tear Collection", 
    "🔬 Sample Processing",
    "📊 Biomarkers",
    "📈 Visualizations"
])

# TAB 1: Clinical Data (DODANI Schirmer with anesthesia i Phenol red)
with tab1:
    st.header("Clinical Phenotyping")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Symptoms")
        osdi_score = st.slider("OSDI Score (0-100)", 0, 100, 25)
        deq5_score = st.slider("DEQ-5 Score (0-22)", 0, 22, 8)
        
        st.subheader("Tear Film Stability")
        tbut = st.number_input("TBUT (seconds)", 0.0, 30.0, 10.0, 0.5)
        tbut_method = st.selectbox("TBUT Method", ["Fluorescein", "Non-invasive", "Keratograph", "Other"])
        nibut = st.number_input("NIBUT (seconds)", 0.0, 30.0, 10.0, 0.5)
        nibut_device = st.text_input("NIBUT Device", "Keratograph 5M")
    
    with col2:
        st.subheader("Ocular Surface Staining")
        staining_method = st.selectbox("Staining Method", ["Fluorescein", "Lissamine Green", "Rose Bengal", "None"])
        staining_scale = st.selectbox("Staining Scale", ["Oxford (0-5)", "NEI (0-15)", "Baylor (0-4)"])
        corneal_staining = st.selectbox("Corneal Staining", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"])
        conjunctival_staining = st.selectbox("Conjunctival Staining", ["0 - None", "1 - Mild", "2 - Moderate", "3 - Severe"])
        
        st.subheader("Tear Volume")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            schirmer = st.number_input("Schirmer I (mm/5min)", 0, 35, 15)
            schirmer_anesthesia = st.number_input("Schirmer with anesthesia (mm/5min)", 0, 35, 10)
        with col_v2:
            phenol_red = st.number_input("Phenol red thread (mm/15s)", 0, 30, 15)
            tmh = st.number_input("Tear Meniscus Height (mm)", 0.0, 1.0, 0.3, 0.05)

# TAB 2: Tear Collection (TEAR-RG Collection items)
with tab2:
    st.header("Tear Collection")
    st.caption("TEAR-RG Collection items C1-C12")
    
    col1, col2 = st.columns(2)
    
    with col1:
        collection_method = st.selectbox("Collection Method", ["Schirmer strip", "Capillary tube", "Sponge", "Flush", "Other"])
        anesthesia_used = st.radio("Anesthesia Used", ["Yes", "No"])
        tear_volume = st.number_input("Tear Volume Collected (μL)", 0, 100, 10)
        collection_time = st.time_input("Collection Time", datetime.now().time())
        
    with col2:
        cl_wear = st.radio("Contact Lens Wear", ["Yes", "No"])
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

# TAB 3: Sample Processing
with tab3:
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
        "nibut_device": nibut_device,
        "staining_method": staining_method,
        "staining_scale": staining_scale,
        "corneal_staining": corneal_staining,
        "conjunctival_staining": conjunctival_staining,
        "schirmer": schirmer,
        "schirmer_anesthesia": schirmer_anesthesia,
        "phenol_red": phenol_red,
        "tmh": tmh,
        
        # Collection
        "collection_method": collection_method,
        "anesthesia_used": anesthesia_used,
        "tear_volume": tear_volume,
        "collection_time": str(collection_time),
        "cl_wear": cl_wear,
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
            file_name=f"tear_rg_{patient_id}_visit{visit_number}.csv",
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
                file_name=f"tear_rg_{patient_id}_visit{visit_number}.xlsx",
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
                file_name=f"tear_rg_bulk_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No saved patients yet. Click 'Save Current Patient' to add.")
    
    # Preview
    with st.expander("Preview current patient data"):
        st.dataframe(df_current, use_container_width=True)

# TAB 5: Visualizations (NOVO)
with tab5:
    st.header("📈 Exploratory Data Analysis")
    st.caption("Upload your exported data for visualization")
    
    uploaded_file = st.file_uploader("Upload CSV or Excel file for analysis", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            # Učitaj podatke
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"Loaded {len(df)} records")
            
            # Osnovna statistika
            with st.expander("📊 Dataset Overview"):
                st.dataframe(df.describe(), use_container_width=True)
            
            # Vizualizacije u 2 kolone
            col_v1, col_v2 = st.columns(2)
            
            with col_v1:
                st.subheader("TBUT Distribution")
                if 'tbut' in df.columns:
                    fig_tbut = px.histogram(
                        df, 
                        x='tbut', 
                        nbins=20,
                        title='TBUT Distribution Across Patients',
                        labels={'tbut': 'TBUT (seconds)', 'count': 'Number of Patients'},
                        color_discrete_sequence=['#1f77b4']
                    )
                    fig_tbut.update_layout(showlegend=False)
                    st.plotly_chart(fig_tbut, use_container_width=True)
                    
                    # Basic stats
                    col_stats1, col_stats2, col_stats3 = st.columns(3)
                    with col_stats1:
                        st.metric("Mean TBUT", f"{df['tbut'].mean():.1f} s")
                    with col_stats2:
                        st.metric("Median", f"{df['tbut'].median():.1f} s")
                    with col_stats3:
                        st.metric("Std Dev", f"{df['tbut'].std():.1f} s")
                else:
                    st.warning("Column 'tbut' not found in data")
                
                st.subheader("OSDI Distribution")
                if 'osdi_score' in df.columns:
                    fig_osdi = px.box(
                        df,
                        y='osdi_score',
                        title='OSDI Score Distribution',
                        labels={'osdi_score': 'OSDI Score'},
                        color_discrete_sequence=['#ff7f0e']
                    )
                    st.plotly_chart(fig_osdi, use_container_width=True)
                else:
                    st.warning("Column 'osdi_score' not found")
            
            with col_v2:
                st.subheader("OSDI vs IL-6 Correlation")
                if 'osdi_score' in df.columns and 'IL6_value' in df.columns:
                    fig_corr = px.scatter(
                        df,
                        x='osdi_score',
                        y='IL6_value',
                        trendline='ols',
                        title='OSDI Score vs IL-6 Levels',
                        labels={'osdi_score': 'OSDI Score', 'IL6_value': 'IL-6 (pg/mL)'},
                        color_discrete_sequence=['#2ca02c']
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
                    
                    # Izračunaj korelaciju
                    corr = df['osdi_score'].corr(df['IL6_value'])
                    st.metric("Pearson Correlation", f"{corr:.3f}")
                else:
                    st.warning("Columns 'osdi_score' and 'IL6_value' required")
                
                st.subheader("Biomarker Heatmap")
                biomarker_cols = [col for col in df.columns if any(b in col for b in ['IL6', 'TNF', 'MMP9', 'Lactoferrin', 'Lysozyme'])]
                if len(biomarker_cols) >= 2:
                    biomarker_df = df[biomarker_cols].select_dtypes(include=['float64', 'int64'])
                    if not biomarker_df.empty and biomarker_df.shape[1] >= 2:
                        corr_matrix = biomarker_df.corr()
                        fig_heatmap = px.imshow(
                            corr_matrix,
                            text_auto=True,
                            aspect="auto",
                            title="Biomarker Correlation Matrix",
                            color_continuous_scale='RdBu_r'
                        )
                        st.plotly_chart(fig_heatmap, use_container_width=True)
                    else:
                        st.info("Not enough numeric biomarker data for heatmap")
                else:
                    st.info("Need at least 2 biomarker columns for heatmap")
            
            # Napredne vizualizacije
            st.markdown("---")
            st.subheader("Multi-Visit Analysis")
            
            if 'visit_number' in df.columns and 'patient_id' in df.columns:
                # Group by patient and visit
                pivot_tbut = df.pivot_table(
                    values='tbut', 
                    index='patient_id', 
                    columns='visit_number',
                    aggfunc='mean'
                ).reset_index()
                
                if not pivot_tbut.empty and pivot_tbut.shape[1] > 1:
                    fig_lines = px.line(
                        df,
                        x='visit_number',
                        y='tbut',
                        color='patient_id',
                        title='TBUT Progression by Visit',
                        labels={'visit_number': 'Visit Number', 'tbut': 'TBUT (seconds)'},
                        markers=True
                    )
                    st.plotly_chart(fig_lines, use_container_width=True)
                else:
                    st.info("Not enough multi-visit data for progression plot")
            else:
                st.info("Add 'visit_number' and 'patient_id' columns for multi-visit analysis")
            
        except Exception as e:
            st.error(f"Error loading file: {e}")
    else:
        st.info("👆 Upload your exported CSV or Excel file to see visualizations")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>TEAR-Film Analyzer v2.0</strong> | TEAR-RG Compliant | Delphi Consensus 2025</p>
    <p style="font-size: 0.8rem;">Based on: Schmeetz J, et al. Contact Lens and Anterior Eye 2025;48:102448</p>
    <p style="font-size: 0.8rem;">For research use only | WG1, WG2, WG3, WG8 ready</p>
</div>
""", unsafe_allow_html=True)
