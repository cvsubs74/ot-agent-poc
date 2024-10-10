import streamlit as st
from pyvis.network import Network
import json

from components.ContextGraphGenerator import ContextGraphGenerator
from components.GraphChatbot import GraphChatbot
from enums.EntityType import EntityType
from repositories.ContextGraphRepository import ContextGraphRepository
from repositories.DatabaseManager import DatabaseManager

# Configure Streamlit page
st.set_page_config(page_title="Contextual Graph Generator and Explorer", layout="wide")
database_manager = DatabaseManager()
context_graph_repo = ContextGraphRepository(database_manager.connection)
context_graph_generator = ContextGraphGenerator(context_graph_repo)
graph_chatbot = GraphChatbot(context_graph_repo, context_graph_generator)


def visualize_graph(entities, relationships, type_color_map):
    """
    Generates an interactive graph visualization using PyVis.

    :param entities: List of dictionaries with 'name' and 'type' keys.
    :param relationships: List of dictionaries with relationship details.
    :param type_color_map: Dictionary mapping EntityType to colors.
    :return: HTML string of the generated graph.
    """
    # Initialize PyVis Network with white background
    net = Network(height='490px', width='100%', directed=True, bgcolor='#FFFFFF', font_color='black')

    # Define the options as a Python dictionary with updated node size, font size, and spring length
    options = {
        "edges": {
            "font": {
                "size": 12,  # Font size for edge labels
                "align": "middle"
            },
            "arrows": {
                "to": {
                    "enabled": True
                }
            },
            "color": {
                "color": "#000000"
            },
            "smooth": False
        },
        "nodes": {
            "font": {
                "size": 12,  # Font size for node labels
                "color": "#000000"
            },
            "shape": "dot",
            "size": 16,  # Node size
            "scaling": {
                "min": 20,  # Minimum node size
                "max": 40  # Maximum node size
            }
        },
        "physics": {
            "enabled": True,
            "barnesHut": {
                "gravitationalConstant": -8000,  # Increase attraction
                "centralGravity": 0.8,  # Reduce node spacing
                "springLength": 130,  # Space nodes further apart
                "springConstant": 0.05,
                "damping": 0.09
            },
            "minVelocity": 0.75
        },
        "layout": {
            "randomSeed": 2
        }
    }

    # Serialize the options dictionary to a JSON string
    net.set_options(json.dumps(options))

    # Add nodes with color coding based on EntityType
    for entity in entities:
        color = type_color_map.get(EntityType(entity['type']), '#000000')  # Default to black if type not found
        net.add_node(
            entity['name'],
            label=entity['name'],
            color=color,
            size=20,  # Node size
            title=f"Type: {entity['type']}"  # Tooltip with entity type
        )

    # Add edges with labels
    for rel in relationships:
        net.add_edge(
            rel['source_entity_name'],
            rel['target_entity_name'],
            label=rel['relationship_type'],
            font={'align': 'horizontal'},  # Align labels horizontally
            arrows='to'  # Add arrow to indicate direction
        )

    # Generate network with physics layout and return HTML
    return net.generate_html()


# Define color mapping for visualization
type_color_map = {
    EntityType.VENDOR: 'red',
    EntityType.ASSET: 'blue',
    EntityType.ENTITY: 'green',
    EntityType.PROCESSING_ACTIVITY: 'orange',
    EntityType.CONTRACT: 'purple',
    EntityType.ENGAGEMENT: 'cyan',
    EntityType.POLICY: 'magenta',
    EntityType.EXCEPTION: 'yellow',
    EntityType.CONTROL: 'pink',
    EntityType.EVIDENCE_TASK: 'grey',
    EntityType.RISK: 'brown',
}

# Application Title
st.markdown("<h3 style='text-align: center;'>Context Graph Explorer</h3>", unsafe_allow_html=True)

# Create tabs for "Create Graph" and "Explore Graph"
tab1, tab2 = st.tabs(["Create Graph", "Explore Graph"])

with tab1:
    # Create Graph Tab
    graph_chatbot.context_graph_generation_chatbot()

with tab2:
    # Retrieve list of graphs
    graphs = context_graph_generator.list_graphs()

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

                # Visualize the graph
                relationships = context_graph_generator.context_graph_repo.get_relationships_for_graph(graph_id)
                if relationships:
                    entity_set = set()
                    for rel in relationships:
                        entity_set.add((rel['source_entity_type'], rel['source_entity_name']))
                        entity_set.add((rel['target_entity_type'], rel['target_entity_name']))
                    entities = [{'name': name, 'type': etype} for etype, name in entity_set]
                    graph_html = visualize_graph(entities, relationships, type_color_map)
                    st.components.v1.html(graph_html, height=500, width=1000, scrolling=True)
                else:
                    st.warning("No relationships found in this graph.")

                # Display chatbot functionality below the graph with minimal spacing
                st.markdown("<h3 style='text-align: center; font-size: 24px;'>Query Explorer</h3>",
                            unsafe_allow_html=True)
                graph_chatbot.context_graph_analyzer_chatbot(graph_id)
        else:
            st.info("Please select a valid graph to visualize.")
