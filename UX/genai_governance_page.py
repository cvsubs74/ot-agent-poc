import streamlit as st
import pandas as pd
import os
import json
import re
import vertexai
from vertexai.generative_models import GenerativeModel
from core.asset_policy_inference import AssetPolicyInference

class AIGovernancePage:
    """Page for demonstrating AI Governance with policy-based redaction."""
    
    def __init__(self, glossary_repository, regulatory_metadata_repository, policy_repository, asset_policy_inference=None, catalog_repository=None, inventory_repository=None):
        """Initialize the AI Governance page with required repositories.
        
        Args:
            glossary_repository: Repository for accessing glossary data
            regulatory_metadata_repository: Repository for accessing regulatory metadata
            policy_repository: Repository for accessing policy data
            asset_policy_inference: Optional pre-initialized AssetPolicyInference instance
            catalog_repository: Optional repository for accessing catalog data (needed if asset_policy_inference not provided)
            inventory_repository: Optional repository for accessing inventory data (needed if asset_policy_inference not provided)
        """
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.policy_repository = policy_repository
        
        # Use provided asset_policy_inference or initialize a new one if all required repositories are available
        if asset_policy_inference:
            self.asset_policy_inference = asset_policy_inference
        elif catalog_repository and inventory_repository:
            self.asset_policy_inference = AssetPolicyInference(
                catalog_repository,
                regulatory_metadata_repository,
                glossary_repository,
                inventory_repository,
                policy_repository
            )
        else:
            # Log a warning but don't fail - we'll handle missing asset_policy_inference in _get_policies_for_purpose
            self.asset_policy_inference = None
        
        # Initialize VertexAI for document Q&A and policy evaluation
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]
            vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
            self.model = GenerativeModel(os.environ["MODEL"])
        except Exception as e:
            st.warning(f"VertexAI initialization failed: {e}. AI functionality may not work.")
            self.model = None
            
        # Sample documents path
        self.documents_path = os.path.join(os.getcwd(), "sample_documents")
        
        # Initialize session state for document content
        if "document_content" not in st.session_state:
            st.session_state.document_content = {}
            
        # Initialize session state for AI responses
        if "raw_response" not in st.session_state:
            st.session_state.raw_response = ""
        if "governed_response" not in st.session_state:
            st.session_state.governed_response = ""
            
        # Load document content if not already loaded
        self._load_documents()
    
    def _load_documents(self):
        """Load all documents from the sample_documents directory."""
        if not os.path.exists(self.documents_path):
            st.error(f"Sample documents directory not found: {self.documents_path}")
            return
            
        for filename in os.listdir(self.documents_path):
            if filename.endswith(".md"):
                file_path = os.path.join(self.documents_path, filename)
                if filename not in st.session_state.document_content:
                    with open(file_path, 'r') as file:
                        st.session_state.document_content[filename] = file.read()
    
    def render(self):
        """Render the AI Governance page with document Q&A and policy-based redaction."""
        st.markdown("<div class='page-header'><i class='fas fa-robot'></i> &nbsp;AI Governance</div>", unsafe_allow_html=True)
        
        # Add CSS for styled components
        st.markdown("""
        <style>
        /* Information box styling */
        .info-box {
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #2196F3;
        }
        
        /* Response container styling */
        .response-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #4CAF50;
        }
        
        /* Raw response container styling */
        .raw-response-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #FF9800;
        }
        
        /* Governed response container styling */
        .governed-response-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #4CAF50;
        }
        
        /* Redacted text styling */
        .redacted {
            background-color: #000;
            color: #000;
            border-radius: 3px;
            padding: 0 3px;
            user-select: none;
        }
        
        /* Generalized text styling */
        .generalized {
            background-color: #FFC107;
            color: #000;
            border-radius: 3px;
            padding: 0 3px;
        }
        
        /* Conditional text styling */
        .conditional {
            background-color: #2196F3;
            color: #fff;
            border-radius: 3px;
            padding: 0 3px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Information box
        st.markdown("""
        <div class="info-box">
            <h3>AI Governance</h3>
            <p>This page demonstrates how to apply data governance policies to AI-generated responses. 
            Select a document, choose a business purpose, and ask a question. The system will generate 
            a response based on the document content and then apply appropriate governance policies 
            based on the selected purpose.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for document selection and purpose selection
        col1, col2 = st.columns(2)
        
        with col1:
            # Document selection
            document_options = list(st.session_state.document_content.keys())
            selected_document = st.selectbox(
                "Select a document to query",
                options=document_options,
                index=0 if document_options else None,
                key="document_selector"
            )
        
        with col2:
            # Purpose selection
            purposes = self.glossary_repository.get_purposes()
            purpose_options = [(p["id"], p["name"]) for p in purposes]
            selected_purpose_tuple = st.selectbox(
                "Select a business purpose",
                options=purpose_options,
                format_func=lambda x: x[1],
                key="purpose_selector"
            )
            selected_purpose_id, selected_purpose_name = selected_purpose_tuple
        
        # Display document preview
        if selected_document:
            with st.expander("Document Preview", expanded=False):
                st.markdown(st.session_state.document_content[selected_document])
        
        # Question input
        st.subheader("Ask a question about the document")
        
        # Suggested questions based on the selected document
        suggested_questions = self._get_suggested_questions(selected_document)
        
        # Display suggested questions as buttons
        st.markdown("**Suggested Questions:**")
        cols = st.columns(3)
        for i, question in enumerate(suggested_questions):
            col_index = i % 3
            if cols[col_index].button(question, key=f"q_{i}"):
                st.session_state.user_question = question
        
        # Text area for user question
        user_question = st.text_area(
            "Enter your question",
            value=st.session_state.get("user_question", ""),
            height=100,
            key="question_input"
        )
        
        # Submit button
        if st.button("Submit Question", key="submit_button"):
            if user_question and selected_document:
                with st.spinner("Generating response..."):
                    # Generate raw response
                    raw_response = self._generate_response(
                        document_content=st.session_state.document_content[selected_document],
                        question=user_question
                    )
                    st.session_state.raw_response = raw_response
                    
                    # Get policies for the selected purpose
                    policies_json = self._get_policies_for_purpose(selected_purpose_id)
                    
                    # Evaluate response against policies
                    governed_response = self._evaluate_response(
                        raw_response=raw_response,
                        policies_json=policies_json,
                        purpose_name=selected_purpose_name
                    )
                    st.session_state.governed_response = governed_response
        
        # Display responses if available
        if st.session_state.raw_response:
            # Create tabs for raw and governed responses
            tabs = st.tabs(["Raw Response", "Governed Response", "Policy Explanation"])
            
            # Raw response tab
            with tabs[0]:
                st.markdown("""
                <div class="raw-response-container">
                    <h3>Raw AI Response</h3>
                    <p><em>This is the unfiltered response from the AI model before governance policies are applied.</em></p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(st.session_state.raw_response)
            
            # Governed response tab
            with tabs[1]:
                st.markdown("""
                <div class="governed-response-container">
                    <h3>Governed AI Response</h3>
                    <p><em>This is the response after governance policies have been applied based on the selected purpose.</em></p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(st.session_state.governed_response, unsafe_allow_html=True)
            
            # Policy explanation tab
            with tabs[2]:
                st.markdown("""
                <div class="info-box">
                    <h3>Policy Application Explanation</h3>
                    <p>This tab explains how governance policies were applied to the AI-generated response.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### Applied Redaction Types")
                st.markdown("""
                - <span class="redacted">Complete Redaction</span>: Information is fully redacted due to policy restrictions.
                - <span class="generalized">Generalization</span>: Specific details are replaced with more general information.
                - <span class="conditional">Conditional Access</span>: Access is provided based on specific conditions.
                """, unsafe_allow_html=True)
                
                st.markdown("### Policy Evaluation Process")
                st.markdown("""
                1. **Content Generation**: The AI generates a response based on the document and question.
                2. **Policy Retrieval**: Policies associated with the selected purpose are retrieved.
                3. **Content Analysis**: The response is analyzed for sensitive information based on policies.
                4. **Policy Application**: Appropriate redaction techniques are applied based on policy requirements.
                5. **Response Delivery**: The governed response is delivered to the user.
                """)
                
                # Display the policies used for governance
                st.markdown("### Policies Applied")
                policies_json = self._get_policies_for_purpose(selected_purpose_id)
                if policies_json:
                    st.json(policies_json)
                else:
                    st.info("No specific policies were applied for this purpose.")
    
    def _get_suggested_questions(self, document_name):
        """Get suggested questions based on the selected document."""
        questions = {
            "customer_data_analysis.md": [
                "What are the demographics of our customers?",
                "What is the personally identifiable information of our high-value customers?",
                "What payment methods do our customers use?",
                "How do our customers compare to competitors' customers?",
                "What are the recommendations for improving customer experience?"
            ],
            "product_roadmap.md": [
                "What are our strategic initiatives for the next 18 months?",
                "What is our competitive advantage in AI analytics?",
                "What is our market expansion strategy?",
                "What are our acquisition targets?",
                "What technical innovations are in our roadmap?"
            ],
            "financial_performance.md": [
                "How did we perform in Q1 2025?",
                "What is the breakdown of revenue by business unit?",
                "What is the executive compensation structure?",
                "What are our strategic investments?",
                "What is our financial outlook for the rest of 2025?"
            ]
        }
        
        return questions.get(document_name, ["What is this document about?"])
    
    def _generate_response(self, document_content, question):
        """Generate a response to the user's question based on the document content."""
        if not self.model:
            return "Error: VertexAI model is not available. Please check the configuration."
        
        prompt = f"""
        You are an AI assistant tasked with answering questions about a document.
        
        DOCUMENT CONTENT:
        {document_content}
        
        USER QUESTION:
        {question}
        
        Please provide a comprehensive and accurate answer based solely on the information in the document.
        If the document doesn't contain information to answer the question, state that clearly.
        Format your response using markdown for better readability.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                return response.text.strip()
            else:
                return "Error: Failed to generate a response. Please try again."
        except Exception as e:
            return f"Error generating response: {e}"
    
    def _get_policies_for_purpose(self, purpose_id):
        """Get policies associated with the selected purpose using AssetPolicyInference."""
        # Convert purpose_id to integer if it's not already an integer
        if not isinstance(purpose_id, int):
            try:
                purpose_id_int = int(purpose_id)
            except (ValueError, TypeError):
                # If purpose_id can't be converted to int, use it as is
                purpose_id_int = purpose_id
        else:
            purpose_id_int = purpose_id
            
        # Get all data elements to pass to the policy inference engine
        data_elements = self.glossary_repository.get_data_elements()
        data_element_ids = [element["id"] for element in data_elements]
        
        # Use the AssetPolicyInference to get policies by data elements and purpose
        # This returns a DataFrame with all policy details
        policy_df = self.asset_policy_inference.get_policies_by_data_elements_purpose(
            data_element_ids=data_element_ids,
            purpose_id=purpose_id_int,
            policy_type='all'
        )
        
        # Convert DataFrame to a list of dictionaries
        if not policy_df.empty:
            policy_data = policy_df.to_dict('records')
        else:
            policy_data = []
            
        # Add additional policy metadata if needed
        for policy in policy_data:
            # Ensure all required fields are present
            if 'policy_id' not in policy and 'id' in policy:
                policy['policy_id'] = policy['id']
            if 'policy_name' not in policy and 'name' in policy:
                policy['policy_name'] = policy['name']
            if 'policy_type' not in policy:
                policy['policy_type'] = 'Unknown'
                
        # Convert to JSON
        return json.dumps(policy_data, indent=2)
    
    def _evaluate_response(self, raw_response, policies_json, purpose_name):
        """Evaluate the raw response against policies and apply governance."""
        if not self.model:
            return "Error: VertexAI model is not available. Please check the configuration."
        
        prompt = f"""
        You are an AI governance assistant tasked with evaluating an AI-generated response against data governance policies.
        
        RAW RESPONSE:
        {raw_response}
        
        POLICIES (JSON):
        {policies_json}
        
        BUSINESS PURPOSE:
        {purpose_name}
        
        Your task is to:
        1. Analyze the raw response for any sensitive information covered by the policies.
        2. Apply appropriate governance actions based on the policies:
           - For data elements with "allowed": false in usage policies, completely redact the information.
           - For data elements requiring masking in security policies, generalize the information.
           - For data elements with restrictions, apply conditional access based on the restrictions.
        3. Return a modified version of the response with HTML markup for redacted content:
           - Use <span class="redacted">REDACTED</span> for completely redacted information.
           - Use <span class="generalized">generalized information</span> for masked information.
           - Use <span class="conditional">conditional information</span> for restricted information.
        
        Make sure to:
        - Preserve the overall structure and flow of the original response.
        - Only modify content that violates the policies.
        - Be thorough in identifying all sensitive information covered by the policies.
        - Explain your reasoning for each redaction in comments at the end of your response.
        
        Return ONLY the modified response with HTML markup, not your explanation.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                governed_response = response.text.strip()
                
                # Clean up the response if it contains markdown code blocks
                if governed_response.startswith("```html"):
                    governed_response = governed_response.replace("```html", "", 1)
                elif governed_response.startswith("```"):
                    governed_response = governed_response.replace("```", "", 1)
                if governed_response.endswith("```"):
                    governed_response = governed_response.replace("```", "", 1)
                
                return governed_response.strip()
            else:
                return "Error: Failed to evaluate the response against policies. Please try again."
        except Exception as e:
            return f"Error evaluating response: {e}"
