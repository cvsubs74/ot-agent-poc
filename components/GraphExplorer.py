import streamlit as st

from components.GraphGenerator import ContextGraphGenerator
from components.GraphChatbot import GraphChatbot
from components.GraphVisualizer import GraphVisualizer
from repositories.ContextGraphRepository import ContextGraphRepository


class GraphExplorer:
    def __init__(self, context_graph_generator: ContextGraphGenerator,
                 graph_visualizer: GraphVisualizer,
                 context_graph_repo: ContextGraphRepository,
                 graph_chatbot: GraphChatbot):
        self.context_graph_repo = context_graph_repo
        self.context_graph_generator = context_graph_generator
        self.graph_visualizer = graph_visualizer
        self.graph_chatbot = graph_chatbot

    def explore(self, graph_id=None):
        """Handle the Explore Graph functionality."""
        st.markdown("""
        <div style='font-size: 1em; margin-bottom: 15px;'>
            Dive deep into existing scenarios, which represent the complex relationships between various entities such as vendors, assets, policies, risks, and more. 
            <br><br>
            Each scenario is a visual representation of how entities are interconnected, and it allows you to:
            <ul>
                <li>Visualize and explore the entire network of entities and relationships in a clear, interactive graph.</li>
                <li>Select specific entities to drill down into their relationships, revealing all their direct and indirect connections.</li>
                <li>Leverage the built-in chatbot to query the graph and receive context-driven answers, helping you analyze relationships and take context-sensitive actions.</li>
            </ul>
            Use this powerful tool to gain insights, identify potential risks, and monitor compliance across your organizational data in real time.
        </div>
        """, unsafe_allow_html=True)

        # Get graph list
        graphs = self.context_graph_generator.list_graphs()

        if not graphs:
            st.info("No scenarios found. Please create a new scenario in the 'Create Scenario' tab.")
        else:
            graph_options = {f"{graph['id']}-{graph['name']}": graph for graph in graphs}
            graph_names = ["--Select a Scenario--"] + list(graph_options.keys())  # Add default option

            # Retrieve the graph_id from session state or passed value
            if graph_id is None:
                graph_id = st.session_state.get('graph_id')  # Get from session state if not passed

            # Set default selected graph name from session if available
            if graph_id:
                selected_graph_name = next(
                    (name for name, graph in graph_options.items() if graph['id'] == graph_id),
                    "--Select a Scenario--"
                )
            else:
                selected_graph_name = "--Select a Scenario--"

            # Callback to update session state when graph selection changes
            def update_selected_graph():
                selected_graph_name = st.session_state['selected_graph_name']
                selected_graph = graph_options.get(selected_graph_name)
                if selected_graph:
                    st.session_state['graph_id'] = selected_graph['id']
                    st.session_state[
                        'selected_entity_name'] = "--Select an entity--"  # Reset entity selection when graph changes

            # Dropdown to select a graph, with an on_change callback
            st.selectbox("Select a Scenario", graph_names, index=graph_names.index(selected_graph_name),
                         key="selected_graph_name", on_change=update_selected_graph)

            # Continue only if a valid graph is selected
            if selected_graph_name != "--Select a Scenario--":
                selected_graph = graph_options[selected_graph_name]
                graph_id = selected_graph['id']
                st.session_state['graph_id'] = graph_id  # Update session state with selected graph_id

                # Visualize the full graph
                entities = []
                relationships = self.context_graph_repo.get_relationships_for_graph(graph_id)
                if relationships:
                    entity_set = set()
                    for rel in relationships:
                        entity_set.add((rel['source_entity_type'], rel['source_entity_name']))
                        entity_set.add((rel['target_entity_type'], rel['target_entity_name']))
                    entities = [{'name': name, 'type': etype} for etype, name in entity_set]
                    self.graph_visualizer.visualize(entities, relationships)
                else:
                    st.warning("No relationships found in this graph.")

                # Display dropdown for entity selection below the graph
                st.write("")
                entity_names = ["--Select an entity--"] + [entity['name'] for entity in entities]
                selected_entity_name = st.selectbox("Select an Entity to Explore", entity_names,
                                                    key="selected_entity_name")

                if selected_entity_name != "--Select an entity--":
                    subgraph_data = self.context_graph_repo.get_subgraph_for_entity(graph_id, selected_entity_name)

                    if subgraph_data:
                        sub_entities = subgraph_data['entities']
                        sub_relationships = subgraph_data['relationships']

                        # Visualize the subgraph
                        self.graph_visualizer.visualize(sub_entities, sub_relationships)
                    else:
                        st.warning(f"No relationships found for entity: {selected_entity_name}")

                # Display chatbot functionality below the graph
                st.markdown("<h3 style='text-align: center; font-size: 24px;'>Query Explorer</h3>",
                            unsafe_allow_html=True)
                self.graph_chatbot.context_graph_analyzer_chatbot(
                    graph_id, None if selected_entity_name == "--Select an entity--" else selected_entity_name)
