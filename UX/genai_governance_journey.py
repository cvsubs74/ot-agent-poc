import streamlit as st
import pandas as pd
from UX.genai_governance_page import AIGovernancePage

class AIGovernanceJourney:
    """Class to render the AI Governance Journey page."""
    
    def __init__(self, glossary_repository, regulatory_metadata_repository, policy_repository, asset_policy_inference=None, catalog_repository=None, inventory_repository=None):
        """Initialize with repositories.
        
        Args:
            glossary_repository: Repository for accessing glossary data
            regulatory_metadata_repository: Repository for accessing regulatory metadata
            policy_repository: Repository for accessing policy data
            asset_policy_inference: Optional pre-initialized AssetPolicyInference instance
            catalog_repository: Optional repository for accessing catalog data
            inventory_repository: Optional repository for accessing inventory data
        """
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.policy_repository = policy_repository
        self.asset_policy_inference = asset_policy_inference
        self.catalog_repository = catalog_repository
        self.inventory_repository = inventory_repository
    
    def render(self):
        """Render the AI Governance Journey page."""
        st.markdown("<div class='page-header'><i class='fas fa-robot'></i> &nbsp;AI Governance Journey</div>", unsafe_allow_html=True)
        
        # Add CSS for styled components
        st.markdown("""
        <style>
        /* Section styling */
        .section-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #3498db;
        }
        
        /* Challenge section styling */
        .challenge-container {
            background-color: #fff3e0;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #ff9800;
        }
        
        /* Solution section styling */
        .solution-container {
            background-color: #e8f5e9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #4caf50;
        }
        
        /* Example section styling */
        .example-container {
            background-color: #f3e5f5;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #9c27b0;
        }
        
        /* Flowchart styling */
        .flowchart-container {
            background-color: #fafafa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
            text-align: center;
        }
        
        /* Card styling */
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 16px;
            margin-bottom: 16px;
        }
        
        /* Icon styling */
        .icon {
            font-size: 24px;
            margin-right: 10px;
            vertical-align: middle;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create tabs for different sections of the journey
        tabs = st.tabs([
            "Overview",
            "Challenges",
            "Solution",
            "Try It Out"
        ])
        
        # Overview tab
        with tabs[0]:
            self._render_overview()
            
        # Challenges tab
        with tabs[1]:
            self._render_challenges()
            
        # Solution tab
        with tabs[2]:
            self._render_solution()
            
        # Try It Out tab
        with tabs[3]:
            AIGovernancePage(
                self.glossary_repository,
                self.regulatory_metadata_repository,
                self.policy_repository,
                asset_policy_inference=self.asset_policy_inference,
                catalog_repository=self.catalog_repository,
                inventory_repository=self.inventory_repository
            ).render()
    
    def render_embedded(self):
        """Render the AI Governance Journey page embedded in another page."""
        # Create tabs for different sections of the journey
        tabs = st.tabs([
            "Overview",
            "Challenges",
            "Solution",
            "Try It Out"
        ])
        
        # Overview tab
        with tabs[0]:
            self._render_overview()
            
        # Challenges tab
        with tabs[1]:
            self._render_challenges()
            
        # Solution tab
        with tabs[2]:
            self._render_solution()
            
        # Try It Out tab
        with tabs[3]:
            AIGovernancePage(
                self.glossary_repository,
                self.regulatory_metadata_repository,
                self.policy_repository,
                asset_policy_inference=self.asset_policy_inference,
                catalog_repository=self.catalog_repository,
                inventory_repository=self.inventory_repository
            ).render()
    
    def _render_overview(self):
        """Render the overview of AI Governance."""
        st.markdown("""
        <div class="section-container">
            <h2><i class="fas fa-info-circle icon"></i>What is AI Governance?</h2>
            <p>AI Governance is the practice of applying data governance principles and policies to AI-generated content. 
            As organizations increasingly rely on generative AI to process, analyze, and provide insights from sensitive data, 
            ensuring that AI outputs comply with data governance policies becomes critical.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Why AI Governance Matters section using native Streamlit components
        st.subheader("🎯 Why AI Governance Matters")
        st.write(
            "When users interact with AI systems that have access to sensitive corporate data, there's a risk that the AI might "
            "inadvertently disclose information that should be protected. AI Governance ensures that AI-generated responses "
            "adhere to the same data governance policies that human users would be expected to follow."
        )
        
        st.markdown("### Key Benefits")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Regulatory Compliance**")
            st.write("Ensures AI outputs comply with data protection regulations like GDPR, CCPA, and industry-specific requirements")
            
            st.markdown("**Risk Mitigation**")
            st.write("Reduces the risk of data breaches and unauthorized disclosure of sensitive information")
            
            st.markdown("**Consistent Governance**")
            st.write("Applies the same governance standards to AI outputs as to human-generated content")
        
        with col2:
            st.markdown("**Purpose-Based Access**")
            st.write("Ensures AI responses are tailored to the user's legitimate business purpose")
            
            st.markdown("**Auditability**")
            st.write("Provides a clear record of how governance policies were applied to AI outputs")
        
        # How AI Governance Works section using native Streamlit components
        st.subheader("⚙️ How AI Governance Works")
        st.write(
            "AI Governance works by intercepting AI-generated responses before they reach the user, evaluating them against "
            "applicable data governance policies, and applying appropriate redaction or modification techniques to ensure compliance."
        )
        
        st.markdown("### AI Governance Flow")
        
        # Create a simple flow diagram using columns
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # User Request
            st.markdown("""<div style='background-color:#f0f2f6;padding:10px;border-radius:5px;text-align:center;margin-bottom:10px'>
                        <b>1. User Request</b><br>
                        User selects document and business purpose, then asks a question
                        </div>""", unsafe_allow_html=True)
            
            # Down arrow
            st.markdown("""<div style='text-align:center;font-size:20px'>↓</div>""", unsafe_allow_html=True)
            
            # AI Response Generation
            st.markdown("""<div style='background-color:#e1f5fe;padding:10px;border-radius:5px;text-align:center;margin-bottom:10px'>
                        <b>2. AI Response Generation</b><br>
                        Vertex AI generates a response based on document content
                        </div>""", unsafe_allow_html=True)
            
            # Down arrow
            st.markdown("""<div style='text-align:center;font-size:20px'>↓</div>""", unsafe_allow_html=True)
            
            # Policy Evaluation
            st.markdown("""<div style='background-color:#fff8e1;padding:10px;border-radius:5px;text-align:center;margin-bottom:10px'>
                        <b>3. Policy Evaluation</b><br>
                        Response is evaluated against applicable governance policies
                        </div>""", unsafe_allow_html=True)
            
            # Down arrow
            st.markdown("""<div style='text-align:center;font-size:20px'>↓</div>""", unsafe_allow_html=True)
            
            # Redaction & Modification
            st.markdown("""<div style='background-color:#e8f5e9;padding:10px;border-radius:5px;text-align:center;margin-bottom:10px'>
                        <b>4. Redaction & Modification</b><br>
                        Sensitive information is redacted based on policies and purpose
                        </div>""", unsafe_allow_html=True)
            
            # Down arrow
            st.markdown("""<div style='text-align:center;font-size:20px'>↓</div>""", unsafe_allow_html=True)
            
            # Governed Response
            st.markdown("""<div style='background-color:#f3e5f5;padding:10px;border-radius:5px;text-align:center'>
                        <b>5. Governed Response</b><br>
                        Policy-compliant response is presented to the user
                        </div>""", unsafe_allow_html=True)
            
    def _render_challenges(self):
        """Render the challenges of AI and data governance."""
        st.subheader("⚠️ Challenges with Uncontrolled AI")
        st.write("Organizations face significant challenges when deploying generative AI solutions without proper governance controls:")
        
        # Data Privacy Violations
        with st.expander("Data Privacy Violations", expanded=True):
            st.write(
                "Without governance, AI models might inadvertently disclose personally identifiable information (PII), "
                "protected health information (PHI), or other sensitive data in their responses, potentially violating "
                "regulations like GDPR, HIPAA, or CCPA."
            )
            
            st.markdown("**Example Scenario:**")
            st.info(
                "A financial analyst asks an AI assistant about customer spending patterns. The AI response includes "
                "specific customer names, account numbers, and transaction details that should be anonymized or redacted."
            )
        
        # Intellectual Property Exposure
        with st.expander("Intellectual Property Exposure", expanded=True):
            st.write(
                "AI systems with access to proprietary documents might reveal trade secrets, confidential business "
                "strategies, or other intellectual property that should remain protected."
            )
            
            st.markdown("**Example Scenario:**")
            st.info(
                "A product manager asks an AI about market trends, and the response includes confidential details about "
                "an unreleased product, its pricing strategy, and competitive positioning that should not be widely shared."
            )
        
        # Purpose Limitation Violations
        with st.expander("Purpose Limitation Violations", expanded=True):
            st.write(
                "AI responses might provide information beyond what's necessary for the user's stated business purpose, "
                "violating the principle of data minimization and purpose limitation."
            )
            
            st.markdown("**Example Scenario:**")
            st.info(
                "A marketing analyst asks about customer demographics for a campaign, and the AI provides detailed "
                "individual customer profiles with sensitive attributes that aren't necessary for the marketing purpose."
            )
        
        # Inconsistent Policy Application
        with st.expander("Inconsistent Policy Application", expanded=True):
            st.write(
                "Without governance, AI systems might apply data policies inconsistently or not at all, leading to "
                "unpredictable and potentially non-compliant outputs."
            )
            
            st.markdown("**Example Scenario:**")
            st.info(
                "Two employees ask similar questions about customer data, but the AI provides different levels of detail "
                "in each response, creating inconsistency in how sensitive information is handled."
            )
    
    def _render_solution(self):
        """Render the solution for AI Governance."""
        st.subheader("💡 The AI Governance Solution")
        st.write(
            "Our AI Governance solution addresses these challenges by integrating data governance policies directly "
            "into the AI response generation process. This ensures that all AI-generated content complies with the same "
            "governance standards that apply to human-generated content."
        )
        
        # Solution Components
        st.markdown("### Key Components")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Purpose-Based Access Control
            st.markdown("**Purpose-Based Access Control**")
            st.write(
                "Requires users to specify a legitimate business purpose when interacting with AI, ensuring that "
                "responses are tailored to that purpose and comply with relevant policies."
            )
            
            # Policy Evaluation Engine
            st.markdown("**Policy Evaluation Engine**")
            st.write(
                "Evaluates AI-generated responses against applicable data governance policies to identify sensitive "
                "information that should be protected."
            )
        
        with col2:
            # Intelligent Redaction
            st.markdown("**Intelligent Redaction**")
            st.write(
                "Applies appropriate redaction techniques to sensitive information based on the user's purpose, "
                "the applicable policies, and the context of the information."
            )
            
            # Audit Trail
            st.markdown("**Audit Trail**")
            st.write(
                "Maintains a record of all AI interactions, including the user's purpose, the policies applied, "
                "and any redactions or modifications made to the response."
            )
        
        # How It Works
        st.markdown("### How It Works")
        
        st.write(
            "1. **User Selection**: The user selects a document and specifies their business purpose."
        )
        st.write(
            "2. **Question Input**: The user asks a question about the document content."
        )
        st.write(
            "3. **AI Response Generation**: The system uses Vertex AI to generate a response based on the document content."
        )
        st.write(
            "4. **Policy Evaluation**: The response is evaluated against applicable data governance policies."
        )
        st.write(
            "5. **Redaction Application**: Sensitive information is redacted or modified based on the policies and purpose."
        )
        st.write(
            "6. **Response Delivery**: The governed response is presented to the user alongside the original response for comparison."
        )
        
        # Benefits
        st.markdown("### Benefits")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Compliance**")
            st.write("Ensures AI outputs comply with data protection regulations and internal policies")
        
        with col2:
            st.markdown("**Consistency**")
            st.write("Applies the same governance standards to AI outputs as to human-generated content")
        
        with col3:
            st.markdown("**Confidence**")
            st.write("Builds trust in AI systems by ensuring they handle sensitive information appropriately")
