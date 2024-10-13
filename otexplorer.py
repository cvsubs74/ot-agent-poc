import streamlit as st
from components.GraphVisualizer import GraphVisualizer
from components.ContextGraphGenerator import ContextGraphGenerator
from components.GraphChatbot import GraphChatbot
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
            self.context_graph_repo, self.context_graph_generator, self.graph_visualizer)


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
        # Add small font introduction for the "Create Graph" tab
        graph_id = self.graph_chatbot.context_graph_generation_chatbot()
        return graph_id

    def explore_graph(self, graph_id=None):
        """Handle the Explore Graph functionality."""

        # Add small font introduction for the "Explore Graph" tab
        st.markdown(
            """
            <div style='font-size: 1em; margin-bottom: 15px;'>
                Dive deep into existing scenarios, which represent the complex relationships between various entities such as vendors, assets, policies, risks, and more. 
                <br><br>
                Each scenario is a visual representation of how entities are interconnected, and it allows you to:
                <ul>
                    <li>Visualize and explore the entire network of entities and relationships in a clear, interactive graph.</li>
                    <li>Select specific entities to drill down into their relationships, revealing all their direct and indirect connections.</li>
                    <li>Leverage the built-in chatbot to query the graph and receive context-driven answers, helping you analyze relationships and take context sensitive actions.</li>
                </ul>
                Use this powerful tool to gain insights, identify potential risks, and monitor compliance across your organizational data in real time.
            </div>
            """, unsafe_allow_html=True)

        # Get graph list
        graphs = self.context_graph_generator.list_graphs()

        if not graphs:
            st.info("No scenarios found. Please create a new scenario in the 'Create Scenario' tab.")
        else:
            graph_options = {f"{graph['name']}": graph for graph in graphs}
            graph_names = ["--Select a Scenario--"] + list(graph_options.keys())  # Add default option

            # Store the graph_id in session state if provided or retrieved from session state
            if graph_id:
                st.session_state['graph_id'] = graph_id
            elif 'graph_id' in st.session_state:
                graph_id = st.session_state['graph_id']

            # Preselect the graph if a valid graph_id is present in session state
            if graph_id:
                selected_graph_name = next((name for name, graph in graph_options.items() if graph['id'] == graph_id),
                                           None)
                if selected_graph_name:
                    selected_graph_name = st.selectbox("Select a Scenario", graph_names,
                                                       index=graph_names.index(selected_graph_name))
                else:
                    selected_graph_name = st.selectbox("Select a Scenario", graph_names)
            else:
                selected_graph_name = st.selectbox("Select a Scenario", graph_names)

            if selected_graph_name != "--Select a Scenario--":
                selected_graph = graph_options.get(selected_graph_name)

                if selected_graph:
                    graph_id = selected_graph['id']
                    st.session_state['graph_id'] = graph_id  # Update session state with selected graph_id

                    # Visualize the full graph
                    entities = []
                    relationships = self.context_graph_generator.context_graph_repo.get_relationships_for_graph(
                        graph_id)
                    if relationships:
                        entity_set = set()
                        for rel in relationships:
                            entity_set.add((rel['source_entity_type'], rel['source_entity_name']))
                            entity_set.add((rel['target_entity_type'], rel['target_entity_name']))
                        entities = [{'name': name, 'type': etype} for etype, name in entity_set]
                        graph_html = self.graph_visualizer.visualize(entities, relationships)
                        st.components.v1.html(graph_html, height=500, width=1000, scrolling=True)
                    else:
                        st.warning("No relationships found in this graph.")

                    # Display dropdown for entity selection below the graph
                    entity_names = ["--Select an entity--"] + [entity['name'] for entity in entities]
                    selected_entity_name = st.selectbox("Select an Entity to Explore", entity_names)

                    if selected_entity_name != "--Select an entity--":
                        subgraph_data = self.context_graph_repo.get_subgraph_for_entity(graph_id, selected_entity_name)

                        if subgraph_data:
                            sub_entities = subgraph_data['entities']
                            sub_relationships = subgraph_data['relationships']

                            # Visualize the subgraph
                            subgraph_html = self.graph_visualizer.visualize(sub_entities, sub_relationships)
                            st.components.v1.html(subgraph_html, height=500, width=1000, scrolling=True)
                        else:
                            st.warning(f"No relationships found for entity: {selected_entity_name}")

                    # Display chatbot functionality below the graph
                    st.markdown("<h3 style='text-align: center; font-size: 24px;'>Query Explorer</h3>",
                                unsafe_allow_html=True)
                    self.graph_chatbot.context_graph_analyzer_chatbot(
                        graph_id, None if selected_entity_name == "--Select an entity--" else selected_entity_name)
            else:
                st.info("Please select a valid graph to visualize.")

    def run(self):
        """Main function to run the Streamlit app."""
        # Step 1: Configure the page
        self.configure_page()

        # Step 2: Application Title
        st.markdown("<h3 style='text-align: center;'>OT Explorer - A New Paradigm in Contextual Intelligence</h3>", unsafe_allow_html=True)

        # Step 3: Introduction Section
        st.write(f"""
            #### **Welcome to OT Explorer**

            **Unlock the Power of Context-Driven Insights and Actionable Intelligence**

            OT Explorer revolutionizes how organizations explore and manage their data by offering an interactive, context-driven graph platform. Whether you're looking to understand risks, manage vendor relationships, or ensure compliance, OT Explorer brings clarity to your complex data landscape:

            - **Visualize & Analyze**: Create dynamic scenarios that represent the relationships between vendors, assets, policies, risks, and more, allowing you to see the full context of your data.
            - **Interact & Act**: Explore your scenario through a chatbot interface that allows you to ask complex business questions and receive detailed, contextually relevant answers. Take action directly within the interface by triggering risk assessments, audits, and more.
            - **Monitor & Mitigate**: OT Explorer ensures you stay ahead of risks with real-time insights and actions. Visualize how entities are connected, spot potential issues, and take proactive measures.

            #### Why OT Explorer? 🌟

            - **Contextual Intelligence**: OT Explorer leverages the power of context graphs, allowing you to explore the full spectrum of relationships between your organizational entities.
            - **Actionable Insights**: Move beyond analysis. OT Explorer not only answers your questions but also provides actionable recommendations based on the data in your graph.
            - **Real-Time Interaction**: Use the chatbot to query your data in real-time, getting answers on risks, compliance, and much more, instantly.
            - **Dynamic Graph Generation**: Easily create and modify graphs as your business evolves, ensuring you always have an accurate, up-to-date view of your organization's data.
            - **Entity-Centric Actions**: Take real-world actions—like initiating a compliance check, triggering an audit, or reviewing risk exposure—directly from the graph interface.
            - **Comprehensive Visualization**: See your data and its relationships like never before, with interactive, high-level visualizations that simplify even the most complex data ecosystems.

            With OT Explorer, you can track and analyze complex relationships between entities, identify risks, and act on the information—all in one seamless platform. Visualize your organizational ecosystem with entities and relationships mapped across multiple systems. 

            Ready to explore and take action? **Create a scenario** or **explore existing scenarios** to see how OT Explorer can transform your decision-making process.
        """, unsafe_allow_html=True)

        # Step 4: Create tabs for "Create Graph" and "Explore Graph"
        tab1, tab2 = st.tabs(["Create Scenarios", "Explore Scenarios"])

        with tab1:
            graph_id = self.create_graph()

        with tab2:
            self.explore_graph(graph_id)


if __name__ == "__main__":
    app = OTExplorer()
    app.run()
