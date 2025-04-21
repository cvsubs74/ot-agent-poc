import streamlit as st

from UX.decision_tree_renderer import DecisionTreeRenderer
from core.sensitivity_inference import SensitivityInference

class SensitivityInferencePage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.sensitivity_inference = SensitivityInference(
            self.glossary_repository,
            self.regulatory_metadata_repository
        )

    @staticmethod
    def explain():
        st.markdown(
            """
            <div style=\"background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;\">
                <h4 style=\"margin-top: 0;\">How Data Sensitivity Inference Works</h4>
                <p>The Data Sensitivity Inference API uses multiple sensitivity mapping tables to determine the sensitivity level of data elements in different contexts:</p>
                <ul>
                    <li><strong>Data Category Data Element</strong>: Maps data elements to their categories, establishing hierarchical relationships.</li>
                    <li><strong>Law/Data Subject Type/Data Element Sensitivity</strong>: Determines sensitivity levels for specific data elements under different laws and for different data subject types.</li>
                    <li><strong>Law/Data Subject Type/Data Category Sensitivity</strong>: Provides higher-level sensitivity determinations for data categories.</li>
                    <li><strong>Context Sensitivity</strong>: Adjusts sensitivity based on processing context (e.g., healthcare vs. marketing).</li>
                </ul>
                <p>The system considers multiple factors to determine data sensitivity, which then influences other decisions like legal basis selection, security requirements, and risk assessments.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    def render(self):
        """Implement a sensitivity inference API based on regulatory metadata.
        This allows users to input data attributes and get sensitivity predictions.
        """
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Sensitivity Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                This API determines the sensitivity level of data based on regulatory metadata.<br><br>
                <ul>
                    <li>Analyzes data attributes against regulatory requirements</li>
                    <li>Provides sensitivity classification (high, medium, low)</li>
                    <li>Offers compliance recommendations based on sensitivity level</li>
                    <li>Helps implement appropriate data protection safeguards</li>
                </ul>
                <strong>How the Algorithm Works:</strong><br><br>
                <ul>
                    <li><strong>Parameter-Based Lookup:</strong> Checks for sensitivity classifications matching all input parameters</li>
                    <li><strong>Fallback Mechanism:</strong> Uses more general classifications if no specific match is found</li>
                    <li><strong>Hierarchical Classification:</strong> Understands relationships between data elements and categories</li>
                    <li><strong>Regulatory Alignment:</strong> Derives classifications from regulatory mappings</li>
                    <li><strong>Compliance Guidance:</strong> Provides specific safeguard recommendations by sensitivity level</li>
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
        
        # Get data subject types
        data_subject_types = self.glossary_repository.get_data_subject_types()
        if data_subject_types:
            dst_options = [dst["name"] for dst in data_subject_types]
            selected_dst = st.selectbox("Select Data Subject Type", options=dst_options)
        else:
            st.warning("No data subject types available.")
            return
        
        # Option to select either data element or data category
        data_type = st.radio("Select Data Type", ["Data Element", "Data Category"])
        
        if data_type == "Data Element":
            data_elements = self.glossary_repository.get_data_elements()
            if data_elements:
                de_options = [de["name"] for de in data_elements]
                selected_data = st.selectbox("Select Data Element", options=de_options)
            else:
                st.warning("No data elements available.")
                return
        else:  # Data Category
            data_categories = self.glossary_repository.get_data_categories()
            if data_categories:
                dc_options = [dc["name"] for dc in data_categories]
                selected_data = st.selectbox("Select Data Category", options=dc_options)
            else:
                st.warning("No data categories available.")
                return
        
        # Add a button to trigger inference
        infer_button = st.button("Infer Sensitivity")
        
        # Show results below the button
        if infer_button:
            st.subheader("Sensitivity Results")
            # Display a spinner while "processing"
            with st.spinner("Analyzing regulatory metadata..."):
                # Get the sensitivity based on the selected parameters
                sensitivity = self.sensitivity_inference.infer_sensitivity(
                    selected_law, 
                    selected_dst, 
                    selected_data, 
                    data_type
                )
            
            if sensitivity:
                # Display the result with appropriate styling based on sensitivity level
                color = "#e74c3c" if sensitivity.lower() == "high" else \
                       "#f39c12" if sensitivity.lower() == "medium" else \
                       "#2ecc71"
                
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: {color}25; border: 2px solid {color}; margin-top: 20px;">
                    <h3 style="color: {color};">Sensitivity Level: {sensitivity}</h3>
                    <p>Based on the selected parameters, the data is classified as <strong>{sensitivity} sensitivity</strong> 
                    under {selected_law}.</p>
                </div>
                """, unsafe_allow_html=True)
                    
                # Display the reasoning
                st.markdown("### Reasoning")
                
                if data_type == "Data Element":
                    st.markdown(f"""
                    The sensitivity level was determined based on the following factors:
                    - **Law**: {selected_law}
                    - **Data Subject Type**: {selected_dst}
                    - **Data Element**: {selected_data}
                    
                    According to the regulatory metadata, when processing the data element '{selected_data}' 
                    for a '{selected_dst}' under '{selected_law}', the appropriate sensitivity classification is '{sensitivity}'.
                    """)
                else:
                    st.markdown(f"""
                    The sensitivity level was determined based on the following factors:
                    - **Law**: {selected_law}
                    - **Data Subject Type**: {selected_dst}
                    - **Data Category**: {selected_data}
                    
                    According to the regulatory metadata, when processing data from the '{selected_data}' category 
                    for a '{selected_dst}' under '{selected_law}', the appropriate sensitivity classification is '{sensitivity}'.
                    """)
                    
                # Add compliance recommendations based on sensitivity
                st.markdown("### Compliance Recommendations")
                
                if sensitivity.lower() == "high":
                    st.markdown("""
                    #### High Sensitivity Data Handling Requirements:
                    - Implement strong encryption for storage and transmission
                    - Conduct a Data Protection Impact Assessment (DPIA)
                    - Implement strict access controls and authentication
                    - Ensure explicit consent is obtained where required
                    - Maintain detailed processing records
                    - Consider data minimization and pseudonymization techniques
                    """)
                elif sensitivity.lower() == "medium":
                    st.markdown("""
                    #### Medium Sensitivity Data Handling Requirements:
                    - Implement standard encryption for storage and transmission
                    - Consider whether a DPIA is necessary
                    - Implement appropriate access controls
                    - Ensure appropriate legal basis for processing
                    - Maintain processing records
                    - Apply data minimization principles
                    """)
                else:  # Low
                    st.markdown("""
                    #### Low Sensitivity Data Handling Requirements:
                    - Follow standard security practices
                    - Implement basic access controls
                    - Ensure appropriate legal basis for processing
                    - Apply data minimization principles
                    - Maintain basic processing records
                    """)
                    
                # Define nodes for the decision tree
                nodes = [
                    {"id": "data", "label": "Data Element/Category", "color": "#3498db", "shape": "ellipse", "size": 30},
                    {"id": "law", "label": "Law", "color": "#e74c3c", "shape": "box", "size": 25},
                    {"id": "dst", "label": "Data Subject Type", "color": "#f39c12", "shape": "box", "size": 25},

                    {"id": "lookup", "label": "Sensitivity Lookup", "color": "#2ecc71", "shape": "box", "size": 25, 
                     "title": {"html": """
                        <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #2ecc71;'>
                            <h3>Sensitivity Lookup Process</h3>
                            <p>This lookup process determines data sensitivity by:</p>
                            <ol>
                                <li>Checking the <b>Law Data Subject Type Data Element Sensitivity</b> table for exact matches</li>
                                <li>If no match, checking the <b>Law Data Subject Type Data Category Sensitivity</b> table</li>

                                <li>Applying law-specific sensitivity rules and thresholds</li>
                                <li>Returning the appropriate sensitivity level with confidence score</li>
                            </ol>
                            <p>The algorithm prioritizes specific element matches over category matches and considers the most restrictive interpretation when multiple laws apply.</p>
                        </div>
                    """}},
                    {"id": "high", "label": "High Sensitivity", "color": "#e74c3c", "shape": "box", "size": 25},
                    {"id": "medium", "label": "Medium Sensitivity", "color": "#f39c12", "shape": "box", "size": 25},
                    {"id": "low", "label": "Low Sensitivity", "color": "#2ecc71", "shape": "box", "size": 25}
                ]
                
                # Define edges for the decision tree
                edges = [
                    {"source": "data", "target": "law", "label": "Regulated by"},
                    {"source": "data", "target": "dst", "label": "Relates to"},

                    {"source": "law", "target": "lookup", "label": ""},
                    {"source": "dst", "target": "lookup", "label": ""},

                    {"source": "lookup", "target": "high", "label": "If sensitive PII"},
                    {"source": "lookup", "target": "medium", "label": "If general PII"},
                    {"source": "lookup", "target": "low", "label": "If non-PII"}
                ]
                
                # Render the decision tree
                DecisionTreeRenderer.render(nodes, edges, "Sensitivity Inference Process", 700)
            else:
                st.warning("No sensitivity classification found for the selected parameters.")
                st.markdown("""
                This could be because:
                1. The specific combination of parameters is not defined in the regulatory metadata
                2. The selected law does not regulate this specific data type for this subject type
                3. Additional context may be needed for proper classification
                
                Consider consulting with a privacy professional for further guidance.
                """)
