import streamlit as st
from UX.decision_tree_renderer import DecisionTreeRenderer
from core.legal_basis_inference import LegalBasisInference

class LegalBasisInferencePage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.legal_basis_inference = LegalBasisInference(
            self.regulatory_metadata_repository,
            self.glossary_repository
        )

    def render(self):
        """Implement a legal basis inference API based on regulatory metadata.
        This allows users to input processing parameters and get legal basis recommendations.
        """
        st.markdown("<div class='page-header'><i class='fas fa-balance-scale'></i> &nbsp;Legal Basis Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            This API helps determine the appropriate legal basis for processing personal data based on regulatory metadata.<br><br>
            <ul>
                <li>Recommends suitable legal bases according to applicable regulations</li>
                <li>Considers processing purpose, data sensitivity, and jurisdiction</li>
                <li>Ranks recommendations by regulatory preference</li>
                <li>Provides implementation guidance for each legal basis</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Purpose-Based Analysis:</strong> Finds legal bases for specific law and purpose combinations</li>
                <li><strong>Preference Ordering:</strong> Ranks legal bases by regulatory preference (lower numbers = higher preference)</li>
                <li><strong>Sensitivity Refinement:</strong> Adjusts recommendations based on data sensitivity level</li>
                <li><strong>Fallback Mechanism:</strong> Uses general legal bases if no purpose-specific ones are found</li>
                <li><strong>Compliance Guidance:</strong> Provides specific requirements and implementation steps</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
            
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options)
        
        # Get jurisdictions
        jurisdictions = self.glossary_repository.get_jurisdictions()
        if jurisdictions:
            jurisdiction_options = [j["name"] for j in jurisdictions]
            selected_jurisdiction = st.selectbox("Select Jurisdiction", options=jurisdiction_options)
        else:
            selected_jurisdiction = None
        
        # Get purpose categories (new)
        purpose_categories = self.glossary_repository.get_purpose_categories()
        if purpose_categories:
            purpose_category_options = [pc["name"] for pc in purpose_categories]
            selected_purpose_category = st.selectbox("Select Purpose Category", options=purpose_category_options)
        else:
            st.warning("No purpose categories available.")
            return
                                    
        # Add sensitivity level selection
        sensitivities = self.glossary_repository.get_sensitivities()
        if sensitivities:
            sensitivity_options = [s["name"] for s in sensitivities]
            selected_sensitivity = st.selectbox("Select Data Sensitivity", options=sensitivity_options)
        else:
            sensitivity_options = ["Low", "Medium", "High"]
            selected_sensitivity = st.selectbox("Select Data Sensitivity", options=sensitivity_options)
        
        # Add a button to trigger inference
        infer_button = st.button("Recommend Legal Basis")
        
        if infer_button:
            # Display a spinner while "processing"
            with st.spinner("Analyzing regulatory metadata..."):
                # Get legal bases using LegalBasisInference
                legal_bases = self.legal_basis_inference.get_legal_bases(
                    selected_law, 
                    selected_jurisdiction,
                    selected_sensitivity,
                    selected_purpose_category
                )
            
            if legal_bases:
                # Display the recommended legal bases with appropriate styling
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                    <h3 style="color: #3498db;">Recommended Legal Bases</h3>
                    <p>Based on the selected parameters, the following legal bases are recommended for processing under {selected_law}:</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display each legal basis with its description and compliance requirements
                for i, legal_basis in enumerate(legal_bases):
                    with st.expander(f"{i+1}. {legal_basis['name']}", expanded=True if i == 0 else False):
                        st.markdown(f"**Description**: {legal_basis.get('description', 'No description available')}")
                        
                        # Add compliance requirements from the repository
                        st.markdown("#### Compliance Requirements:")
                        
                        if "compliance_requirements" in legal_basis and legal_basis["compliance_requirements"]:
                            requirements_list = "\n".join([f"- {req}" for req in legal_basis["compliance_requirements"]])
                            st.markdown(requirements_list)
                        else:
                            st.markdown("No specific compliance requirements available for this legal basis.")
                        
                        # Add compatibility with sensitivity level
                        compatibility = "High" if selected_sensitivity.lower() == "low" else \
                                        "Medium" if selected_sensitivity.lower() == "medium" else \
                                        "Low"
                        
                        st.markdown(f"**Compatibility with {selected_sensitivity} sensitivity data**: {compatibility}")
                
                # Display the reasoning
                st.markdown("### Reasoning")
                st.markdown(f"""
                The legal basis recommendations were determined based on the following factors:
                - **Law**: {selected_law}
                - **Jurisdiction**: {selected_jurisdiction if selected_jurisdiction else 'Not specified'}
                - **Purpose Category**: {selected_purpose_category}
                - **Sensitivity Level**: {selected_sensitivity}
                
                According to the regulatory metadata, when processing {selected_sensitivity} data under {selected_law} for the purpose category of {selected_purpose_category}, 
                the recommended legal bases are listed above in order of preference.
                """)
                
                # Add general compliance notes
                st.markdown("### General Compliance Notes")
                st.markdown("""
                1. **Documentation**: Always document your legal basis assessment and decision process.
                2. **Transparency**: Clearly communicate the legal basis to data subjects in your privacy notice.
                3. **Purpose Limitation**: Only use the data for the purpose specified under the chosen legal basis.
                4. **Data Minimization**: Only process the data necessary for the specified purpose.
                5. **Regular Review**: Periodically review your legal basis to ensure it remains appropriate.
                6. **Special Categories**: For sensitive data, ensure you also have an appropriate condition for processing.
                """)
            else:
                st.warning("No specific legal basis recommendations found for the selected parameters.")
                st.markdown("""
                This could be because:
                1. The specific combination of parameters is not defined in the regulatory metadata
                2. The selected law does not specify legal bases for this scenario
                3. Additional context may be needed for proper recommendations
                
                Consider consulting with a privacy professional for further guidance.
                """)
                
                # Provide general legal basis information
                st.markdown("### General Legal Basis Information")
                st.markdown("""
                Here are the common legal bases for processing personal data under major privacy regulations:
                
                1. **Consent**: The data subject has given clear consent for processing their personal data for a specific purpose.
                2. **Contract**: Processing is necessary for a contract with the data subject or to take steps at their request before entering a contract.
                3. **Legal Obligation**: Processing is necessary to comply with a legal obligation.
                4. **Vital Interests**: Processing is necessary to protect someone's life or vital interests.
                5. **Public Task**: Processing is necessary for a task carried out in the public interest or in the exercise of official authority.
                6. **Legitimate Interests**: Processing is necessary for legitimate interests pursued by the controller or a third party, except where overridden by the interests or rights of the data subject.
                
                The appropriate legal basis depends on your specific circumstances, the nature of the data, and the purpose of processing.
                """)
                
            # Define nodes for the decision tree
            nodes = [
                {"id": "processing", "label": "Processing Activity", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "law", "label": "Law", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "purpose", "label": "Purpose Category", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "sensitivity", "label": "Data Sensitivity", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Legal Basis Lookup", "color": "#2ecc71", "shape": "box", "size": 25,
                    "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #2ecc71;'>
                        <h3>Legal Basis Lookup Process</h3>
                        <p>This lookup process determines appropriate legal bases by:</p>
                        <ol>
                            <li>Querying the <b>Law Purpose Category Legal Basis</b> table for matches</li>
                            <li>Filtering results based on the selected law, purpose, and data sensitivity</li>
                            <li>Ranking legal bases by appropriateness for the specific scenario</li>
                            <li>Considering sensitivity thresholds for each legal basis type</li>
                            <li>Providing implementation requirements for each recommended basis</li>
                        </ol>
                        <p>The algorithm prioritizes more protective legal bases for higher sensitivity data and considers purpose-specific requirements defined in each law.</p>
                    </div>
                """}},
                {"id": "consent", "label": "Consent", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "contract", "label": "Contract", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "legitimate", "label": "Legitimate Interest", "color": "#2ecc71", "shape": "box", "size": 25},
                {"id": "legal", "label": "Legal Obligation", "color": "#3498db", "shape": "box", "size": 25}
            ]
            
            # Define edges for the decision tree
            edges = [
                {"source": "processing", "target": "law", "label": "Governed by"},
                {"source": "processing", "target": "purpose", "label": "Has purpose"},
                {"source": "processing", "target": "sensitivity", "label": "Involves data"},
                {"source": "law", "target": "lookup", "label": ""},
                {"source": "purpose", "target": "lookup", "label": ""},
                {"source": "sensitivity", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "consent", "label": "High sensitivity"},
                {"source": "lookup", "target": "contract", "label": "Low sensitivity"},
                {"source": "lookup", "target": "legitimate", "label": "Medium sensitivity"},
                {"source": "lookup", "target": "legal", "label": "Compliance"}
            ]
                
            # Render the decision tree
            DecisionTreeRenderer.render(nodes, edges, "Legal Basis Inference Process", 700)
