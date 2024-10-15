from pyvis.network import Network
import json
import streamlit as st
from enums.EntityType import EntityType


class GraphVisualizer:
    def __init__(self, context_graph_generator):
        self.context_graph_generator = context_graph_generator
        # Define color mapping for visualization
        self.type_color_map = {
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

    def visualize_graph(self, graph_id):
        # Visualize the full graph
        relationships = self.context_graph_generator.context_graph_repo.get_relationships_for_graph(
            graph_id)
        if relationships:
            entity_set = set()
            for rel in relationships:
                entity_set.add((rel['source_entity_type'], rel['source_entity_name']))
                entity_set.add((rel['target_entity_type'], rel['target_entity_name']))
            entities = [{'name': name, 'type': etype} for etype, name in entity_set]
            self.visualize(entities, relationships)

    def visualize(self, entities, relationships):
        """
        Generates an interactive graph visualization using PyVis.

        :param entities: List of dictionaries with 'name' and 'type' keys.
        :param relationships: List of dictionaries with relationship details.
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
            },
            "interaction": {
                "navigationButtons": True,  # Add zoom controls
                "keyboard": True,  # Allow keyboard controls
                "multiselect": False,  # Disable multiselect
                "zoomView": True,  # Prevent zooming in too much
            }
        }

        # Serialize the options dictionary to a JSON string
        net.set_options(json.dumps(options))

        # Add nodes with color coding based on EntityType
        for entity in entities:
            try:
                # Map the entity['type'] string to the correct EntityType enum
                entity_type = EntityType.from_value(entity['type'])
                color = self.type_color_map.get(entity_type, '#000000')  # Default to black if type not found
            except ValueError:
                color = '#000000'  # Default to black if the entity type is invalid

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
        graph_html = net.generate_html()

        # Display the graph in one column and the legend in another
        col1, col2 = st.columns([4, 1])  # Adjust column widths as needed

        # Display the graph
        with col1:
            st.components.v1.html(graph_html, height=500, scrolling=True)

        # Display the color legend
        with col2:
            st.markdown("<h4 style='text-align: left;'>Legend</h4>", unsafe_allow_html=True)

            for entity_type, color in self.type_color_map.items():
                # Use a horizontal layout with color box and label
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <div style="width: 20px; height: 20px; background-color: {color}; margin-right: 10px; border: 1px solid black;"></div>
                        <span>{entity_type.value}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

