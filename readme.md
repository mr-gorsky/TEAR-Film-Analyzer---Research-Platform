# TEAR-Film Analyzer - Research Platform

A standardized data collection platform for tear film phenotyping, developed for TEAR-Precision Working Groups 1,2,3,8.

## 🎯 Purpose

This platform enables standardized clinical data collection and integration with tear fluid biomarker analysis for multicenter studies. It is fully compliant with TEAR Reporting Guidelines (TEAR-RG) based on the Delphi consensus published in Contact Lens and Anterior Eye (2025).

## 🔬 Key Features

- **TEAR-RG Compliant** - All 34 Delphi consensus items included
- **Multicenter Support** - Study ID, Site ID, Visit tracking
- **Clinical Phenotyping** - OSDI, DEQ-5, TBUT, NIBUT, staining, tear volume
- **Tear Collection Metadata** - Method, anesthesia, time, contact lens wear
- **Sample Processing** - Storage, centrifugation, elution, freeze-thaw
- **Biomarker Integration** - IL-6, TNF-α, MMP-9, Lactoferrin, Lysozyme
- **Visualization** - Distributions, correlations, multi-visit tracking

## 📊 Data Export

All data can be exported as:
- Individual patient CSV/Excel
- Bulk CSV for all patients in session
- Compatible with SPSS, R, Python analysis

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py

📚 Citation
Based on: Schmeetz J, et al. International reporting guidelines for tear fluid research: A Delphi consensus. Contact Lens and Anterior Eye 2025;48:102448.

👥 TEAR-Precision Working Groups
WG1: Biomarker standardization

WG2: Terminology and reporting

WG3: Clinical phenotyping

WG8: Data integration

📄 License
For research use only. Contact corresponding author for collaboration.
