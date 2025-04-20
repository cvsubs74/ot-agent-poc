import streamlit as st
import time
from core.law_inference import LawInference
from UX.decision_tree_renderer import DecisionTreeRenderer

class DataSubjectRightsPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.law_inference = LawInference(
            self.regulatory_metadata_repository,
            self.glossary_repository
        )

    def render(self):
        """Implement a data subject rights inference API based on regulatory metadata.
        This helps users determine appropriate responses to data subject rights requests.
        """
        st.markdown("<div class='page-header'><i class='fas fa-user-shield'></i> &nbsp;Data Subject Rights Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            This API helps determine appropriate responses to data subject rights requests based on regulatory metadata.<br><br>
            <ul>
                <li>Identifies applicable rights under different regulations</li>
                <li>Determines response timeframes and requirements</li>
                <li>Provides guidance on verification and exemptions</li>
                <li>Offers implementation steps for fulfilling requests</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Jurisdictional Analysis:</strong> Determines applicable laws based on data subject location</li>
                <li><strong>Right Identification:</strong> Maps request types to specific legal rights</li>
                <li><strong>Exemption Evaluation:</strong> Checks for applicable exemptions or limitations</li>
                <li><strong>Response Planning:</strong> Provides timeframes and implementation steps</li>
                <li><strong>Documentation Guidance:</strong> Offers templates and record-keeping requirements</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options, key="dsr_law")
        
        # Get jurisdictions
        jurisdictions = self.glossary_repository.get_jurisdictions()
        if jurisdictions:
            jurisdiction_options = [j["name"] for j in jurisdictions]
            selected_jurisdiction = st.selectbox("Select Data Subject's Jurisdiction", options=jurisdiction_options, key="dsr_jurisdiction")
        else:
            selected_jurisdiction = None
        
        # Get data subject types
        data_subject_types = self.glossary_repository.get_data_subject_types()
        if data_subject_types:
            dst_options = [dst["name"] for dst in data_subject_types]
            selected_dst = st.selectbox("Select Data Subject Type", options=dst_options, key="dsr_subject_type")
        else:
            st.warning("No data subject types available.")
            return
        
        # Add right type selection
        right_types = [
            "Access",
            "Rectification",
            "Erasure",
            "Restriction of Processing",
            "Data Portability",
            "Objection",
            "Automated Decision Making",
            "Withdraw Consent"
        ]
        selected_right = st.selectbox("Select Requested Right", options=right_types, key="dsr_right_type")
        
        # Add request complexity
        request_complexity = st.select_slider(
            "Request Complexity",
            options=["Simple", "Moderate", "Complex"],
            value="Moderate",
            key="dsr_complexity"
        )
        
        # Add a button to trigger inference
        analyze_button = st.button("Analyze Rights Request")
        
        # Define nodes for the decision tree
        nodes = [
            {"id": "request", "label": "DSR Request", "color": "#3498db", "shape": "ellipse", "size": 30},
            {"id": "jurisdiction", "label": "Jurisdiction", "color": "#e74c3c", "shape": "box", "size": 25},
            {"id": "law", "label": "Applicable Law", "color": "#9b59b6", "shape": "box", "size": 25},
            {"id": "subject_type", "label": "Data Subject Type", "color": "#f39c12", "shape": "box", "size": 25},
            {"id": "right_type", "label": "Right Type", "color": "#2ecc71", "shape": "box", "size": 25},
            {"id": "lookup", "label": "Rights Requirements Lookup", "color": "#1abc9c", "shape": "box", "size": 25},
            {"id": "timeframe", "label": "Response Timeframe", "color": "#3498db", "shape": "box", "size": 25},
            {"id": "steps", "label": "Implementation Steps", "color": "#f39c12", "shape": "box", "size": 25},
            {"id": "exemptions", "label": "Potential Exemptions", "color": "#e74c3c", "shape": "box", "size": 25},
            {"id": "verification", "label": "Verification Requirements", "color": "#9b59b6", "shape": "box", "size": 25}
        ]
        edges = [
            {"source": "request", "target": "jurisdiction", "label": "From"},
            {"source": "jurisdiction", "target": "law", "label": "Governed by"},
            {"source": "request", "target": "subject_type", "label": "Made by"},
            {"source": "request", "target": "right_type", "label": "Requests"},
            {"source": "law", "target": "lookup", "label": ""},
            {"source": "subject_type", "target": "lookup", "label": ""},
            {"source": "right_type", "target": "lookup", "label": ""},
            {"source": "lookup", "target": "timeframe", "label": "Determines"},
            {"source": "lookup", "target": "steps", "label": "Provides"},
            {"source": "lookup", "target": "exemptions", "label": "Identifies"},
            {"source": "lookup", "target": "verification", "label": "Requires"}
        ]
        if analyze_button:
            with st.spinner("Analyzing rights requirements..."):
                time.sleep(1)
                rights_guidance = self._get_rights_guidance(selected_law, selected_right)
            if rights_guidance:
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                    <h3 style="color: #3498db;">Right to {selected_right} under {selected_law}</h3>
                    <p>The following guidance applies to {selected_dst}s in {selected_jurisdiction} making a {selected_right} request:</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                    <h4>Response Timeframe</h4>
                    <p><strong>Standard timeframe:</strong> {rights_guidance['timeframe']} days</p>
                    <p><strong>Extension possible:</strong> {rights_guidance['extension_possible']}</p>
                    {f'<p><strong>Extension conditions:</strong> {rights_guidance["extension_conditions"]}</p>' if rights_guidance['extension_possible'] == 'Yes' else ''}
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                    <h4>Verification Requirements</h4>
                    <p>{rights_guidance['verification_requirements']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                    <h4>Implementation Steps</h4>
                    <ol>
                """, unsafe_allow_html=True)
                for step in rights_guidance['implementation_steps']:
                    st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                st.markdown("""
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                if rights_guidance['exemptions']:
                    st.markdown("""
                    <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa; margin: 10px 0;">
                        <h4>Potential Exemptions</h4>
                        <ul>
                    """, unsafe_allow_html=True)
                    for exemption in rights_guidance['exemptions']:
                        st.markdown(f"<li>{exemption}</li>", unsafe_allow_html=True)
                    st.markdown("""
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                if analyze_button and selected_jurisdiction:
                    applicable_laws = self.law_inference.get_applicable_laws(selected_jurisdiction)
                    if applicable_laws:
                        st.markdown(f"""
                        <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                            <h3 style="color: #3498db;">Laws Applicable to {selected_jurisdiction}</h3>
                            <p>The following laws apply to activities in this jurisdiction:</p>
                        </div>
                        """, unsafe_allow_html=True)
                        for i, law in enumerate(applicable_laws):
                            with st.expander(f"{i+1}. {law['name']}", expanded=True):
                                st.markdown(f"**Full Name:** {law['full_name']}")
                                st.markdown(f"**Description:** {law['description']}")
                                st.markdown(f"**Effective Date:** {law['effective_date']}")
                    else:
                        st.markdown("""
                        <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                            <h3 style="color: #7F8C8D;">No Applicable Laws Found</h3>
                            <p>No specific data protection laws were found for the selected jurisdiction in our database.</p>
                            <p>This may be due to:</p>
                            <ul>
                                <li>The jurisdiction may not have comprehensive data protection legislation</li>
                                <li>The jurisdiction may be covered by regional laws not specifically mapped in the database</li>
                                <li>The database may need to be updated with the latest regulatory information</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                DecisionTreeRenderer.render(nodes, edges, "Decision Tree", 700)
            else:
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">No Rights Guidance Found</h3>
                    <p>No specific guidance was found for the selected parameters. This may be due to:</p>
                    <ul>
                        <li>The selected right may not be explicitly recognized under the chosen law</li>
                        <li>The combination of parameters may not match any defined rights scenarios</li>
                        <li>The data subject type may have special considerations not covered in the database</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    def _get_rights_guidance(self, law, right_type):
        """Internal method to get guidance for data subject rights based on regulatory metadata.
        
        Args:
            law (str): The name of the selected law
            right_type (str): The type of right requested
            
        Returns:
            dict: A dictionary containing guidance for the requested right or None if not found
        """
        # Use the repository method to get guidance
        return self.regulatory_metadata_repository.get_data_subject_right_implementation_steps(law, right_type)
