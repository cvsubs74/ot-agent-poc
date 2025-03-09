import streamlit as st

from components.ContextGrammar import ContextGrammar
from components.EntityActions import EntityActions
from components.EvidenceValidator import EvidenceValidator
from components.GraphExplorer import GraphExplorer
from components.GraphVisualizer import GraphVisualizer
from components.GraphGenerator import ContextGraphGenerator
from components.GraphChatbot import GraphChatbot
from components.ControlFinder import ControlFinder
from repositories.ContextGraphRepository import ContextGraphRepository
from repositories.DatabaseManager import DatabaseManager


class OTExplorer:
    def __init__(self):
        """Initialize the core components of the app."""
        self.database_manager = DatabaseManager()
        self.context_graph_repo = ContextGraphRepository(self.database_manager.connection)
        self.context_graph_generator = ContextGraphGenerator(self.context_graph_repo)
        self.graph_visualizer = GraphVisualizer(self.context_graph_generator)
        self.graph_chatbot = GraphChatbot(
            self.context_graph_repo, self.context_graph_generator, self.graph_visualizer
        )

    @staticmethod
    def divider(height=1):
        """Utility function to create a divider with specified height."""
        st.markdown(
            f"<hr style='height:{height}px; margin-top: 0; margin-bottom: 0; border-width:0; background: lightblue;'>",
            unsafe_allow_html=True
        )

    def configure_page(self):
        """Configure the Streamlit page settings."""
        st.set_page_config(page_title="OT Explorer - Contextual Graph Generator and Explorer", layout="wide")

        # Inject custom CSS for styling tabs
        st.markdown("""
        <style>
        .stTabs [role="tablist"] {
            background-color: #f4f4f4; /* Tab background color */
            padding: 5px;
            border-radius: 10px;
        }
        .stTabs [role="tab"] {
            background-color: #0e76a8; /* Individual tab background color */
            color: white;
            font-size: 18px;
            margin-right: 0px;
            padding: 20px;
            border-radius: 5px;
        }
        .stTabs [role="tab"]:hover {
            background-color: #005682; /* Hover color for tabs */
            color: #f4f4f4;
        }
        .stTabs [role="tab"]:active {
            background-color: #003f5c; /* Active tab background color */
        }
        .intro-text {
            font-size: 18px; 
            color: #318283; 
            margin-bottom: 15px;
        }
        </style>
        """, unsafe_allow_html=True)

    def create_graph(self):
        """Handle the Create Graph functionality."""
        graph_id = self.graph_chatbot.context_graph_generation_chatbot()
        if graph_id:
            st.session_state['graph_id'] = graph_id  # Store in session state for access across tabs
        return graph_id

    def explore_graph(self, graph_id=None):
        GraphExplorer(
            self.context_graph_generator,
            self.graph_visualizer,
            self.context_graph_repo,
            self.graph_chatbot
        ).explore()

    def context_grammar(self):
        ContextGrammar(self.context_graph_repo).rules()

    def entity_actions(self):
        EntityActions(self.context_graph_repo).actions()

    def chatbot(self):
        """Handle the AI Insights functionality."""
        st.markdown("""
        <div style='font-size: 1em; margin-bottom: 15px;'>
            Welcome to the AI Insights section, where you can unlock the full power of AI-driven analysis across your organizational data. 
            <br><br>
            Use this feature to:
            <ul>
                <li>Ask complex, context-specific questions about relationships, risks, compliance, and entity attributes.</li>
                <li>Receive real-time, AI-generated insights that are grounded in the relationships and data within your organization.</li>
                <li>Leverage the chatbot to explore data flows, identify compliance issues, assess risks, and even trigger corrective actions directly from the chat interface.</li>
                <li>Automatically tailor responses to your organization's unique graph structure, providing actionable intelligence that can inform decision-making.</li>
            </ul>
            The AI Insights section is your go-to resource for understanding and managing the intricate web of data, vendors, policies, and risks that define your organization.
        </div>
        """, unsafe_allow_html=True)
        self.graph_chatbot.ai_insights_context_graph_analyzer_chatbot()

    def evidence_validator(self):
        """Handle the Evidence Validator functionality."""
        EvidenceValidator().validate_evidence()

    def control_finder(self):
        """Handle the Control Finder functionality."""
        ControlFinder().render()

    def run(self):
        """Main function to run the Streamlit app."""
        # Step 1: Configure the page
        self.configure_page()

        # Step 2: Application Title
        st.markdown(
            "<h3 style='text-align: center;'>OT Explorer - A New Paradigm in Contextual Intelligence</h3>",
            unsafe_allow_html=True
        )

        # Step 3: Introduction Section
        st.write("""
            #### **Welcome to OT Explorer**

            **Unlock the Power of Context-Driven Insights and Actionable Intelligence**

            OT Explorer revolutionizes how organizations explore and manage their data by offering an interactive, context-driven graph platform. Whether you're looking to understand risks, manage vendor relationships, or ensure compliance, OT Explorer brings clarity to your complex data landscape:

            - 🗺️ **Visualize & Analyze**: Create dynamic scenarios that represent the relationships between vendors, assets, policies, risks, and more, allowing you to see the full context of your data.
            - 💬 **Interact & Act**: Explore your scenario through a chatbot interface that allows you to ask complex business questions and receive detailed, contextually relevant answers. Take action directly within the interface by triggering risk assessments, audits, and more.
            - 📊 **Monitor & Mitigate**: OT Explorer ensures you stay ahead of risks with real-time insights and actions. Visualize how entities are connected, spot potential issues, and take proactive measures.
            - ⚙️ **Customize & Enhance**: Define your own context rules and actions to tailor the platform to your organization's unique needs. Watch as the recommendation engine dynamically adapts to your custom rules, providing personalized insights and actionable suggestions.

            Ready to explore and take action? **Create a scenario**, **explore existing scenarios**, or manage **business rules** to see how OT Explorer can transform your decision-making process.
        """)

        # Step 4: Create tabs for all functionalities
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
            ["Create Scenarios", "Explore Scenarios", "Rules", "Actions", "AI Insights", "Evidence Validator", "Control Finder"]
        )

        with tab1:
            graph_id = self.create_graph()

        with tab2:
            self.explore_graph(graph_id)

        with tab3:
            self.context_grammar()

        with tab4:
            self.entity_actions()

        with tab5:
            self.chatbot()

        with tab6:
            self.evidence_validator()
            
        with tab7:
            self.control_finder()


if __name__ == "__main__":
    app = OTExplorer()
    app.run()
