from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components
import tempfile

class DecisionTreeRenderer:
    @staticmethod
    def render(nodes, edges, title="Decision Tree", height=700):
        """Renders a decision tree visualization using PyVis in Streamlit.
        Args:
            nodes (list): List of node dicts with id, label, color, etc.
            edges (list): List of edge dicts with source, target, label, etc.
            title (str): Title for the decision tree
            height (int): Height of the visualization in pixels
        """
        # Create a network with larger dimensions
        net = Network(height=f"{height}px", width="100%", directed=True, notebook=True)
        net.toggle_hide_edges_on_drag(False)
        net.barnes_hut()

        # Add nodes
        for node in nodes:
            node_title = node.get("title", node["label"])
            if isinstance(node_title, dict) and "html" in node_title:
                formatted_title = node_title["html"]
            else:
                formatted_title = node_title
            net.add_node(
                node["id"],
                label=node["label"],
                color=node.get("color", "#3498db"),
                shape=node.get("shape", "box"),
                title=formatted_title,
                size=node.get("size", 25),
                font=node.get("font", {"size": 14, "color": "black", "face": "Arial"})
            )

        # Add edges
        for edge in edges:
            net.add_edge(
                edge["source"],
                edge["target"],
                title=edge.get("label", ""),
                label=edge.get("label", ""),
                color=edge.get("color", "#7F8C8D"),
                width=edge.get("width", 2),
                arrows=edge.get("arrows", "to")
            )

        # Configure physics for hierarchical layout
        net.set_options("""
        {
          "physics": {
            "hierarchicalRepulsion": {
              "centralGravity": 0.0,
              "springLength": 100,
              "springConstant": 0.01,
              "nodeDistance": 120,
              "damping": 0.09
            },
            "solver": "hierarchicalRepulsion",
            "stabilization": {
              "iterations": 100
            }
          },
          "layout": {
            "hierarchical": {
              "enabled": true,
              "levelSeparation": 150,
              "nodeSpacing": 100,
              "treeSpacing": 200,
              "blockShifting": true,
              "edgeMinimization": true,
              "parentCentralization": true,
              "direction": "UD",
              "sortMethod": "directed"
            }
          },
          "interaction": {
            "navigationButtons": true,
            "keyboard": true
          }
        }
        """)

        # Generate the visualization
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
            net.save_graph(tmpfile.name)
            with open(tmpfile.name, "r", encoding="utf-8") as f:
                html = f.read()
            # Fix HTML in tooltips by modifying the HTML directly
            html = html.replace('</head>', '''
            <style>
                div.vis-tooltip {
                    position: absolute;
                    visibility: hidden;
                    padding: 5px;
                    white-space: normal !important;
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    color: #000000;
                    background-color: #ffffff;
                    border-radius: 5px;
                    border: 1px solid #d3d3d3;
                    box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
                    max-width: 400px;
                    word-wrap: break-word;
                    z-index: 9999;
                    overflow: auto;
                    max-height: 400px;
                }
            </style>
            <script>
                // Override the default tooltip rendering to support HTML
                document.addEventListener("DOMContentLoaded", function() {
                    setTimeout(function() {
                        if (typeof network !== 'undefined') {
                            network.on("hoverNode", function(params) {
                                var nodeId = params.node;
                                var node = network.body.nodes[nodeId];
                                if (node && node.options && node.options.title) {
                                    var tooltip = document.querySelector(".vis-tooltip");
                                    if (tooltip) {
                                        tooltip.innerHTML = node.options.title;
                                    }
                                }
                            });
                        }
                    }, 1000);
                });
            </script>
            </head>''')
        st.subheader(title)
        components.html(html, height=height)
