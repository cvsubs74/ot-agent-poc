import streamlit as st
from components.GraphVisualizer import GraphVisualizer
from components.ContextGraphGenerator import ContextGraphGenerator
from components.GraphChatbot import GraphChatbot
from repositories.ContextGraphRepository import ContextGraphRepository
from repositories.DatabaseManager import DatabaseManager


class GraphApp:
    def __init__(self):
        """Initialize the core components of the app."""
        self.database_manager = DatabaseManager()
        self.context_graph_repo = ContextGraphRepository(self.database_manager.connection)
        self.context_graph_generator = ContextGraphGenerator(self.context_graph_repo)
        self.graph_chatbot = GraphChatbot(self.context_graph_repo, self.context_graph_generator)
        self.graph_visualizer = GraphVisualizer()

    def configure_page(self):
        """Configure the Streamlit page settings."""
        st.set_page_config(page_title="Contextual Graph Generator and Explorer", layout="wide")

    def create_graph(self):
        """Handle the Create Graph functionality."""
        self.graph_chatbot.context_graph_generation_chatbot()

    def explore_graph(self):
        """Handle the Explore Graph functionality."""
        graphs = self.context_graph_generator.list_graphs()

        if not graphs:
            st.info("No graphs found. Please create a new graph in the 'Create Graph' tab.")
        else:
            # Prepare display names with graph type if needed
            graph_options = {f"{graph['name']}": graph for graph in graphs}
            graph_names = ["--Select a graph--"] + list(graph_options.keys())  # Add default option
            selected_graph_name = st.selectbox("Select a Graph", graph_names)

            # Check if a valid graph is selected
            if selected_graph_name != "--Select a graph--":
                selected_graph = graph_options.get(selected_graph_name)

                if selected_graph:
                    graph_id = selected_graph['id']

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
                        # Fetch the subgraph for the selected entity
                        subgraph_data = self.context_graph_repo.get_subgraph_for_entity(
                            graph_id, selected_entity_name)

                        if subgraph_data:
                            sub_entities = subgraph_data['entities']
                            sub_relationships = subgraph_data['relationships']

                            # Visualize the subgraph
                            subgraph_html = self.graph_visualizer.visualize(sub_entities, sub_relationships)
                            st.components.v1.html(subgraph_html, height=500, width=1000, scrolling=True)
                        else:
                            st.warning(f"No relationships found for entity: {selected_entity_name}")

                    # Display chatbot functionality below the graph with minimal spacing
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
        st.markdown("<h3 style='text-align: center;'>OT Explorer</h3>", unsafe_allow_html=True)

        # Step 3: Create tabs for "Create Graph" and "Explore Graph"
        tab1, tab2 = st.tabs(["Create Graph", "Explore Graph"])

        with tab1:
            self.create_graph()

        with tab2:
            self.explore_graph()


if __name__ == "__main__":
    app = GraphApp()
    app.run()
