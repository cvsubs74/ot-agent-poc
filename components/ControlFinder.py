import json
import os
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

class ControlFinder:
    """
    A component that helps find and match security controls based on user input.
    Uses Vertex AI to analyze and compare controls with a base set of controls.
    """
    def __init__(self):
        # Initialize Vertex AI
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]
        vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
        self.model = GenerativeModel(os.environ["MODEL"])
        
        # Load base controls from JSON file
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'base_controls_1.json'), 'r') as f:
                controls_data = json.load(f)
                self.base_controls = controls_data['controls']
        except Exception as e:
            st.error(f"Error loading base controls: {str(e)}")
            self.base_controls = []
            
        # Load sample test controls
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_test_controls.json'), 'r') as f:
                self.test_controls = json.load(f)['test_controls']
        except Exception as e:
            st.error(f"Error loading test controls: {str(e)}")
            self.test_controls = []

    def find_matching_controls(self, input_control, expected_matches=None):
        """Find matching controls from the base set using Vertex AI."""
        prompt = f"""
        You are a security control expert. Analyze the following security control description and identify matches from our base control set.
        Focus on these key aspects:
        1. **Cross-Framework Mapping:** Identify equivalent or related controls across different frameworks (e.g., NIST 800-53, ISO 27001, CIS).
        2. **Control Intent:** Emphasize the underlying security objective rather than relying solely on terminology.
        3. **Implementation Hierarchy:** Evaluate both high-level policies and specific technical controls.
        4. **Control Dependencies:** Recognize controls that function together across frameworks.
        5. **Framework-Specific Context:** Understand how each framework uniquely approaches the security objective.
    
        **Input Control Description:**
        {input_control}
    
        **Base Controls:**
        {json.dumps(self.base_controls, indent=2)}
        // Each control in the base data follows this format:
        // {{
        //   "body": "A) There shall be a written report or document demonstrating that the data processing ...",
        //   "id": 9687,
        //   "title": "Lawfulness Assessment of the Processing"
        // }}
    
        **Expected Matches (if any):**
        {expected_matches if expected_matches else 'None specified'}
    
        **Additional Requirement:**
        Only include and analyze matching controls that have a similarity score above 50.
    
        For each matching control, please provide an analysis with the following details:
    
        ### Match [Number]
        - **Control ID:** [ID]
        - **Control Name:** [Name]
        - **Framework:** [Framework Name]
        - **Similarity Score:** [0-100]
        - **Match Type:** [Primary/Supporting/Related]
        - **Cross-Framework Equivalents:**
          * List equivalent controls from other frameworks.
        - **Key Alignments:**
          * **Security Objective:** Explain how the control addresses the core security need.
          * **Implementation Approach:** Describe how the control achieves the objective.
        - **Framework Context:**
          * Explain how this control fits within its framework’s approach.
          * Note any framework-specific considerations.
    
        **Rules:**
        1. Always search for matches across all frameworks (NIST, ISO, CIS).
        2. Prioritize security objectives over exact terminology matches.
        3. Consider each framework’s specific implementation approaches.
        4. Include both policy-level and technical controls from each framework.
        5. Clarify relationships between controls across different frameworks.
        6. Only include controls with a similarity score over 50.
        7. If expected matches are provided, explain their relevance or why they might not be the best matches.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text if hasattr(response, "text") else "No matches found."
        except Exception as e:
            return f"Error analyzing controls: {str(e)}"


    def render(self):
        """Render the control finder interface."""
        st.markdown("""
        This tool helps you find existing security controls that match your requirements.
        Enter a description of the control you're looking for, and we'll find similar controls
        from our base control set, along with similarity scores and detailed analysis.
        """)

        # Add tabs for manual input and sample testing
        tab1, tab2 = st.tabs(["Manual Input", "Sample Controls"])

        with tab1:
            # Input for control description
            control_description = st.text_area(
                "Enter Control Description",
                help="Describe the security control you're looking for. Include its purpose, requirements, and expected outcomes."
            )

            if st.button("Find Matching Controls"):
                if not control_description:
                    st.error("Please enter a control description.")
                    return

                with st.spinner("Analyzing control and finding matches..."):
                    matches = self.find_matching_controls(control_description)
                    st.markdown("### Analysis Results")
                    st.markdown(matches)

        with tab2:
            st.markdown("### Sample Controls for Testing")
            st.markdown("""
            Select a sample control to test the matching functionality. Each sample includes expected matches
            for validation purposes.
            """)
            
            if not self.test_controls:
                st.warning("No sample controls available for testing.")
                return
                
            # Create a selectbox with sample control names
            selected_control = st.selectbox(
                "Select a Sample Control",
                options=range(len(self.test_controls)),
                format_func=lambda x: self.test_controls[x]['name']
            )
            
            # Display selected control details
            control = self.test_controls[selected_control]
            st.markdown("#### Selected Control Details")
            st.markdown(f"**Name:** {control['name']}")
            st.markdown(f"**Description:** {control['description']}")
            st.markdown(f"**Expected Matches:** {', '.join(control['expected_matches'])}")
            st.markdown(f"**Test Scenario:** {control['test_scenario']}")
            
            if st.button("Test with Sample Control"):
                with st.spinner("Analyzing control and finding matches..."):
                    matches = self.find_matching_controls(
                        control['description'],
                        expected_matches=control['expected_matches']
                    )
                    st.markdown(matches)
