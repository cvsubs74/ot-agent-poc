import streamlit as st
import pandas as pd

class LawLegalBasisPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown("""
            <div class="card">
                <h3>Law Legal Basis</h3>
                <p>This section maps data protection laws to their applicable legal bases for processing personal data.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Get law legal basis data from repository
        law_legal_bases = self.regulatory_metadata_repository.get_law_legal_bases()
        if law_legal_bases:
            law_legal_basis_data = {
                "Law": [],
                "Legal Basis": [],
                "Description": []
            }
            for llb in law_legal_bases:
                law_legal_basis_data["Law"].append(llb["law_name"])
                law_legal_basis_data["Legal Basis"].append(llb["legal_basis_name"])
                law_legal_basis_data["Description"].append(llb["legal_basis_description"])
    
            # Create a DataFrame
            df = pd.DataFrame(law_legal_basis_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_legal_basis_law_filter")
            
            with col2:
                legal_bases = sorted(df["Legal Basis"].unique())
                selected_legal_basis = st.selectbox("Filter by Legal Basis", ["All"] + list(legal_bases), key="law_legal_basis_lb_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_legal_basis != "All":
                filtered_df = filtered_df[filtered_df["Legal Basis"] == selected_legal_basis]
            
            # Sort by Law and Legal Basis
            filtered_df = filtered_df.sort_values(by=["Law", "Legal Basis"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")

class LawJurisdictionPage:
    def __init__(self, regulatory_metadata_repository):
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        st.markdown("""
            <div class="card">
                <h3>Law to Jurisdiction Mapping</h3>
                <p>This section maps data protection laws to their applicable jurisdictions, helping organizations 
                understand which laws apply in which geographic areas.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Get law jurisdiction data from repository
        law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
        if law_jurisdictions:
            law_jurisdiction_data = {
                "Law": [],
                "Jurisdiction": []
            }
            for lj in law_jurisdictions:
                law_jurisdiction_data["Law"].append(lj["law_name"])
                law_jurisdiction_data["Jurisdiction"].append(lj["jurisdiction_name"])
    
            # Create a DataFrame
            df = pd.DataFrame(law_jurisdiction_data)
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                laws = sorted(df["Law"].unique())
                selected_law = st.selectbox("Filter by Law", ["All"] + list(laws), key="law_jurisdiction_law_filter")
            
            with col2:
                jurisdictions = sorted(df["Jurisdiction"].unique())
                selected_jurisdiction = st.selectbox("Filter by Jurisdiction", ["All"] + list(jurisdictions), key="law_jurisdiction_jurisdiction_filter")
    
            # Apply filters
            filtered_df = df.copy()
            if selected_law != "All":
                filtered_df = filtered_df[filtered_df["Law"] == selected_law]
            if selected_jurisdiction != "All":
                filtered_df = filtered_df[filtered_df["Jurisdiction"] == selected_jurisdiction]
            
            # Sort by Law and Jurisdiction
            filtered_df = filtered_df.sort_values(by=["Law", "Jurisdiction"])
            
            # Display the filtered data
            st.dataframe(filtered_df)
        else:
            st.warning("No data available in the database.")
