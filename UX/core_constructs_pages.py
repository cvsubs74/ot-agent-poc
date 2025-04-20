import streamlit as st
import pandas as pd

class LawPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository, obligation_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.obligation_repository = obligation_repository

    def render(self):
        st.subheader("Law Definitions")
        st.markdown("""
        <div class="card">
            <p>A law is a system of rules created and enforced through social or governmental institutions to regulate behavior. 
            In the context of data protection, laws establish the legal framework for how organizations must handle personal data.</p>
        </div>
        """, unsafe_allow_html=True)
        laws = self.glossary_repository.get_laws()
        if laws:
            law_data = {
                "Law Name": [],
                "Description": [],
                "Scope": []
            }
            for law in laws:
                law_data["Law Name"].append(law["name"])
                law_data["Description"].append(law["description"])
                law_data["Scope"].append(law["scope"])
            st.dataframe(pd.DataFrame(law_data))
        else:
            st.warning("No data available in the database.")

class JurisdictionsPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Jurisdictions")
        st.markdown("""
        <div class="card">
            <p>Jurisdictions are geographical areas with specific legal authority. In data protection, different jurisdictions may have different laws and regulations governing how personal data must be handled.</p>
        </div>
        """, unsafe_allow_html=True)
        jurisdictions = self.glossary_repository.get_jurisdictions()
        if jurisdictions:
            jurisdiction_data = {
                "Jurisdiction": []
            }
            for jurisdiction in jurisdictions:
                jurisdiction_data["Jurisdiction"].append(jurisdiction["name"])
            st.dataframe(pd.DataFrame(jurisdiction_data))
        else:
            st.warning("No data available in the database.")

class LegalBasisPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Legal Basis")
        st.markdown("""
        <div class="card">
            <p>A legal basis is the lawful ground for processing personal data. Data protection laws typically require organizations to have a valid legal basis before they can process personal data.</p>
        </div>
        """, unsafe_allow_html=True)
        legal_bases = self.glossary_repository.get_legal_bases()
        if legal_bases:
            legal_basis_data = {
                "Legal Basis": [],
                "Description": []
            }
            for legal_basis in legal_bases:
                legal_basis_data["Legal Basis"].append(legal_basis["name"])
                legal_basis_data["Description"].append(legal_basis["description"])
            st.dataframe(pd.DataFrame(legal_basis_data))
        else:
            st.warning("No data available in the database.")

class DataElementsPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Data Elements")
        st.markdown("""
        <div class="card">
            <p>Data elements are specific pieces of information that can be collected about individuals. They are the building blocks of personal data.</p>
        </div>
        """, unsafe_allow_html=True)
        data_elements = self.glossary_repository.get_data_elements()
        if data_elements:
            data_element_data = {
                "Data Element": [],
                "Description": []
            }
            for element in data_elements:
                data_element_data["Data Element"].append(element["name"])
                data_element_data["Description"].append(element["description"])
            st.dataframe(pd.DataFrame(data_element_data))
        else:
            st.warning("No data available in the database.")

class DataSubjectTypesPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Data Subject Types")
        st.markdown("""
        <div class="card">
            <p>Data subject types refer to the categories of individuals whose data is being processed, such as employees, customers, or patients.</p>
        </div>
        """, unsafe_allow_html=True)
        types = self.glossary_repository.get_data_subject_types()
        if types:
            type_data = {
                "Data Subject Type": [],
                "Description": []
            }
            for t in types:
                type_data["Data Subject Type"].append(t["name"])
                type_data["Description"].append(t["description"])
            st.dataframe(pd.DataFrame(type_data))
        else:
            st.warning("No data available in the database.")

class DataCategoriesPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Data Categories")
        st.markdown("""
        <div class="card">
            <p>Data categories classify the types of personal data being processed, such as contact information, financial data, or health data.</p>
        </div>
        """, unsafe_allow_html=True)
        categories = self.glossary_repository.get_data_categories()
        if categories:
            category_data = {
                "Data Category": [],
                "Description": []
            }
            for c in categories:
                category_data["Data Category"].append(c["name"])
                category_data["Description"].append(c["description"])
            st.dataframe(pd.DataFrame(category_data))
        else:
            st.warning("No data available in the database.")

class SensitivityPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Sensitivity")
        st.markdown("""
        <div class="card">
            <p>Sensitivity refers to the level of risk or impact associated with processing different types of personal data.</p>
        </div>
        """, unsafe_allow_html=True)
        sensitivities = self.glossary_repository.get_sensitivities()
        if sensitivities:
            sensitivity_data = {
                "Sensitivity": [],
                "Description": []
            }
            for s in sensitivities:
                sensitivity_data["Sensitivity"].append(s["name"])
                sensitivity_data["Description"].append(s["description"])
            st.dataframe(pd.DataFrame(sensitivity_data))
        else:
            st.warning("No data available in the database.")

class PurposeCategoriesPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Purpose Categories")
        st.markdown("""
        <div class="card">
            <p>Purpose categories describe the reasons for processing personal data, such as marketing, HR, or compliance.</p>
        </div>
        """, unsafe_allow_html=True)
        purposes = self.glossary_repository.get_purpose_categories()
        if purposes:
            purpose_data = {
                "Purpose Category": [],
                "Description": []
            }
            for p in purposes:
                purpose_data["Purpose Category"].append(p["name"])
                purpose_data["Description"].append(p["description"])
            st.dataframe(pd.DataFrame(purpose_data))
        else:
            st.warning("No data available in the database.")

class BreachTypesPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Breach Types")
        st.markdown("""
        <div class="card">
            <p>Breach types refer to the different kinds of data breaches that can occur, such as unauthorized access, loss, or disclosure.</p>
        </div>
        """, unsafe_allow_html=True)
        breaches = self.glossary_repository.get_breach_types()
        if breaches:
            breach_data = {
                "Breach Type": [],
                "Description": []
            }
            for b in breaches:
                breach_data["Breach Type"].append(b["name"])
                breach_data["Description"].append(b["description"])
            st.dataframe(pd.DataFrame(breach_data))
        else:
            st.warning("No data available in the database.")

class ObligationsPage:
    def __init__(self, obligation_repository):
        self.obligation_repository = obligation_repository

    def render(self):
        st.subheader("Obligations")
        st.markdown("""
        <div class="card">
            <p>Obligations are the legal or regulatory requirements that organizations must fulfill when processing personal data.</p>
        </div>
        """, unsafe_allow_html=True)
        # Create columns for filters and actions
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Open", "In Progress", "Implemented", "Accepted Risk"],
                key="obligation_status_filter"
            )
        
        with col2:
            control_filter = st.selectbox(
                "Filter by Control Type",
                ["All", "Encryption", "Access Control", "Masking", "Monitoring", "Retention", "General"],
                key="obligation_control_filter"
            )
        
        with col3:
            policy_filter = st.selectbox(
                "Filter by Policy Status",
                ["All", "Linked to Policy", "No Policy"],
                key="obligation_policy_filter"
            )
        
        # Apply filters
        status = None if status_filter == "All" else status_filter
        control_type = None if control_filter == "All" else control_filter
        policy_linked = None
        if policy_filter == "Linked to Policy":
            policy_linked = True
        elif policy_filter == "No Policy":
            policy_linked = False
        
        # Get obligations from repository with filters
        obligations = self.obligation_repository.get_obligations(status, control_type, policy_linked)
        
        if obligations:
            # Convert to DataFrame for display
            df = pd.DataFrame(obligations)
            # Rename columns for better display
            df = df.rename(columns={
                "id": "ID",
                "name": "Obligation",
                "description": "Description",
                "source": "Source",
                "control_type": "Control Type",
                "status": "Status",
                "policy_name": "Policy",
                "risk_accepted": "Risk Accepted",
                "created_at": "Created At"
            })
            
            # Reorder columns for better display
            display_columns = ["ID", "Obligation", "Description", "Source", "Control Type", "Status", "Policy", "Risk Accepted"]
            df = df[display_columns]
            
            # Display the dataframe
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No obligations found with the selected filters.")

class RisksPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Risks")
        st.markdown("""
        <div class="card">
            <p>Risks are potential threats or vulnerabilities that could impact the security or privacy of personal data.</p>
        </div>
        """, unsafe_allow_html=True)
        risks = self.glossary_repository.get_risks()
        if risks:
            risk_data = {
                "Risk": [],
                "Description": []
            }
            for r in risks:
                risk_data["Risk"].append(r["name"])
                risk_data["Description"].append(r["description"])
            st.dataframe(pd.DataFrame(risk_data))
        else:
            st.warning("No data available in the database.")

class FrameworksPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Frameworks")
        st.markdown("""
        <div class="card">
            <p>Frameworks are structured sets of guidelines or best practices for managing data privacy and security.</p>
        </div>
        """, unsafe_allow_html=True)
        frameworks = self.glossary_repository.get_frameworks()
        if frameworks:
            framework_data = {
                "Framework": [],
                "Description": []
            }
            for f in frameworks:
                framework_data["Framework"].append(f["name"])
                framework_data["Description"].append(f["description"])
            st.dataframe(pd.DataFrame(framework_data))
        else:
            st.warning("No data available in the database.")

class ControlsPage:
    def __init__(self, glossary_repository):
        self.glossary_repository = glossary_repository

    def render(self):
        st.subheader("Controls")
        st.markdown("""
        <div class="card">
            <p>Controls are measures put in place to mitigate risks and ensure compliance with data protection requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        controls = self.glossary_repository.get_controls()
        if controls:
            control_data = {
                "Control": [],
                "Description": []
            }
            for c in controls:
                control_data["Control"].append(c["name"])
                control_data["Description"].append(c["description"])
            st.dataframe(pd.DataFrame(control_data))
        else:
            st.warning("No data available in the database.")
