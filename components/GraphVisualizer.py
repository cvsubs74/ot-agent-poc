from pyvis.network import Network
import json

from enums.EntityType import EntityType


class GraphVisualizer:
    def __init__(self):
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
            }
        }

        # Serialize the options dictionary to a JSON string
        net.set_options(json.dumps(options))

        # Add nodes with color coding based on EntityType
        for entity in entities:
            color = self.type_color_map.get(EntityType(entity['type']), '#000000')  # Default to black if type not found
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