import streamlit as st
import tempfile
import os
from pyvis.network import Network
import streamlit.components.v1 as components

class OntologyGraphPage:
    def __init__(self):
        pass

    def render(self):
        """Visualize the regulatory ontology and association rules as a decision tree using PyVis."""
        st.markdown("<div class='page-header'><i class='fas fa-sitemap'></i> &nbsp;Ontology Visualization</div>", unsafe_allow_html=True)
        st.markdown('''<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section visualizes the regulatory ontology and association rules as an interactive graph.</p>
            <ul>
                <li>Shows the conceptual relationships between different entity types in the regulatory framework</li>
                <li>Displays association rules that define how entities relate to each other</li>
                <li>Provides a high-level view of the data model without showing specific instances</li>
            </ul>
        </div>''', unsafe_allow_html=True)

        st.subheader("Visualization Options")
        col1, col2 = st.columns(2)
        with col1:
            show_core_entities = st.checkbox("Show Core Entities", value=True)
            show_regulatory_metadata = st.checkbox("Show Regulatory Metadata", value=True)
            show_inference_rules = st.checkbox("Show Inference Rules", value=True)
        with col2:
            show_compliance_entities = st.checkbox("Show Compliance Entities", value=True)
            show_inventory_entities = st.checkbox("Show Inventory Entities", value=True)

        net = Network(height="800px", width="100%", directed=True)
        net.set_options("""
        var options = {
        "physics": {
            "enabled": true,
            "stabilization": {
            "enabled": true,
            "iterations": 1000,
            "updateInterval": 25,
            "onlyDynamicEdges": false
            },
            "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.3,
            "springLength": 150,
            "springConstant": 0.04,
            "damping": 0.09,
            "avoidOverlap": 0.2
            }
        },
        "interaction": {
            "dragNodes": true,
            "zoomView": true
        },
        "edges": {
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            },
            "smooth": {
                "enabled": true,
                "type": "dynamic"
            }
        },
        "nodes": {
            "shape": "box",
            "font": {
                "size": 14,
                "face": "Arial"
            }
        }
        }
        """)

        if show_core_entities:
            net.add_node("Law", label="Law", size=30, color="#3498db", shape="box")
            net.add_node("Jurisdiction", label="Jurisdiction", size=25, color="#2ecc71", shape="box")
            net.add_node("Legal Basis", label="Legal Basis", size=25, color="#e74c3c", shape="box")
            net.add_node("Data Subject Type", label="Data Subject Type", size=25, color="#f39c12", shape="box")
            net.add_node("Data Element", label="Data Element", size=25, color="#9b59b6", shape="box")
            net.add_node("Data Category", label="Data Category", size=25, color="#1abc9c", shape="box")
            net.add_node("Sensitivity", label="Sensitivity", size=25, color="#e67e22", shape="box")
            net.add_node("Purpose", label="Purpose", size=25, color="#34495e", shape="box")
            net.add_edge("Law", "Jurisdiction", title="applies to", label="applies to")
            net.add_edge("Law", "Legal Basis", title="defines", label="defines")
            net.add_edge("Law", "Data Subject Type", title="protects", label="protects")
            net.add_edge("Data Subject Type", "Data Element", title="has", label="has")
            net.add_edge("Data Element", "Data Category", title="belongs to", label="belongs to")
            net.add_edge("Data Element", "Sensitivity", title="has level", label="has level")
            net.add_edge("Data Category", "Sensitivity", title="has level", label="has level")
            net.add_edge("Purpose", "Legal Basis", title="requires", label="requires")

        if show_regulatory_metadata:
            net.add_node("Obligation", label="Obligation", size=25, color="#8e44ad", shape="box")
            net.add_node("Risk", label="Risk", size=25, color="#c0392b", shape="box")
            net.add_node("Control", label="Control", size=25, color="#16a085", shape="box")
            net.add_node("Framework", label="Framework", size=25, color="#2980b9", shape="box")
            net.add_node("Policy", label="Policy", size=25, color="#27ae60", shape="box")
            net.add_edge("Law", "Obligation", title="imposes", label="imposes")
            net.add_edge("Obligation", "Risk", title="mitigates", label="mitigates")
            net.add_edge("Control", "Risk", title="mitigates", label="mitigates")
            net.add_edge("Framework", "Control", title="includes", label="includes")
            net.add_edge("Policy", "Control", title="implements", label="implements")
            net.add_edge("Law", "Policy", title="requires", label="requires")

        if show_compliance_entities:
            net.add_node("Compliance Status", label="Compliance Status", size=25, color="#f1c40f", shape="box")
            net.add_node("Breach Notification", label="Breach Notification", size=25, color="#d35400", shape="box")
            net.add_node("Data Subject Right", label="Data Subject Right", size=25, color="#7f8c8d", shape="box")
            net.add_node("Transfer Mechanism", label="Transfer Mechanism", size=25, color="#3498db", shape="box")
            net.add_edge("Law", "Compliance Status", title="measures", label="measures")
            net.add_edge("Law", "Breach Notification", title="requires", label="requires")
            net.add_edge("Law", "Data Subject Right", title="grants", label="grants")
            net.add_edge("Law", "Transfer Mechanism", title="permits", label="permits")
            net.add_edge("Data Subject Type", "Data Subject Right", title="has", label="has")

        if show_inventory_entities:
            net.add_node("Asset", label="Asset", size=25, color="#95a5a6", shape="box")
            net.add_node("Processing Activity", label="Processing Activity", size=25, color="#bdc3c7", shape="box")
            net.add_node("Legal Entity", label="Legal Entity", size=25, color="#7f8c8d", shape="box")
            net.add_node("Vendor", label="Vendor", size=25, color="#34495e", shape="box")
            net.add_edge("Asset", "Data Element", title="contains", label="contains")
            net.add_edge("Processing Activity", "Purpose", title="has", label="has")
            net.add_edge("Processing Activity", "Legal Basis", title="requires", label="requires")
            net.add_edge("Legal Entity", "Processing Activity", title="performs", label="performs")
            net.add_edge("Vendor", "Processing Activity", title="supports", label="supports")
            net.add_edge("Legal Entity", "Jurisdiction", title="subject to", label="subject to")

        if show_inference_rules:
            net.add_node("Sensitivity Inference", label="Sensitivity Inference", size=25, color="#e74c3c", shape="ellipse")
            net.add_node("Legal Basis Inference", label="Legal Basis Inference", size=25, color="#e74c3c", shape="ellipse")
            net.add_node("Breach Notification Inference", label="Breach Notification Inference", size=25, color="#e74c3c", shape="ellipse")
            net.add_node("Transfer Mechanism Inference", label="Transfer Mechanism Inference", size=25, color="#e74c3c", shape="ellipse")
            net.add_node("Control Inference", label="Control Inference", size=25, color="#e74c3c", shape="ellipse")
            net.add_node("Risk Inference", label="Risk Inference", size=25, color="#e74c3c", shape="ellipse")
            net.add_edge("Sensitivity Inference", "Data Element", title="analyzes", label="analyzes")
            net.add_edge("Sensitivity Inference", "Data Category", title="analyzes", label="analyzes")
            net.add_edge("Sensitivity Inference", "Sensitivity", title="determines", label="determines")
            net.add_edge("Legal Basis Inference", "Purpose", title="analyzes", label="analyzes")
            net.add_edge("Legal Basis Inference", "Data Category", title="analyzes", label="analyzes")
            net.add_edge("Legal Basis Inference", "Legal Basis", title="determines", label="determines")
            net.add_edge("Breach Notification Inference", "Sensitivity", title="analyzes", label="analyzes")
            net.add_edge("Breach Notification Inference", "Jurisdiction", title="analyzes", label="analyzes")
            net.add_edge("Breach Notification Inference", "Breach Notification", title="determines", label="determines")
            net.add_edge("Transfer Mechanism Inference", "Jurisdiction", title="analyzes", label="analyzes")
            net.add_edge("Transfer Mechanism Inference", "Transfer Mechanism", title="determines", label="determines")
            net.add_edge("Control Inference", "Risk", title="analyzes", label="analyzes")
            net.add_edge("Control Inference", "Policy", title="analyzes", label="analyzes")
            net.add_edge("Control Inference", "Framework", title="analyzes", label="analyzes")
            net.add_edge("Control Inference", "Control", title="recommends", label="recommends")
            net.add_edge("Risk Inference", "Obligation", title="analyzes", label="analyzes")
            net.add_edge("Risk Inference", "Risk", title="identifies", label="identifies")

        tmp_dir = tempfile.gettempdir()
        path = os.path.join(tmp_dir, "pyvis_network.html")
        net.show(path, notebook=False)
        with open(path, "r", encoding="utf-8") as html_file:
            components.html(html_file.read(), height=800, width=1000)

        legend_html = """
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px;">
            <h3 style="width: 100%;">Entity Types</h3>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #3498db; border-radius: 0; margin-right: 5px;"></div>
                <span>Law</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #2ecc71; border-radius: 0; margin-right: 5px;"></div>
                <span>Jurisdiction</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #e74c3c; border-radius: 0; margin-right: 5px;"></div>
                <span>Legal Basis</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #f39c12; border-radius: 0; margin-right: 5px;"></div>
                <span>Data Subject Type</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #9b59b6; border-radius: 0; margin-right: 5px;"></div>
                <span>Data Element</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #1abc9c; border-radius: 0; margin-right: 5px;"></div>
                <span>Data Category</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #e67e22; border-radius: 0; margin-right: 5px;"></div>
                <span>Sensitivity</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #34495e; border-radius: 0; margin-right: 5px;"></div>
                <span>Purpose</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #8e44ad; border-radius: 0; margin-right: 5px;"></div>
                <span>Obligation</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #c0392b; border-radius: 0; margin-right: 5px;"></div>
                <span>Risk</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #16a085; border-radius: 0; margin-right: 5px;"></div>
                <span>Control</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #2980b9; border-radius: 0; margin-right: 5px;"></div>
                <span>Framework</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #27ae60; border-radius: 0; margin-right: 5px;"></div>
                <span>Policy</span>
            </div>
            <h3 style="width: 100%; margin-top: 15px;">Inference Rules</h3>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #e74c3c; border-radius: 50%; margin-right: 5px;"></div>
                <span>Inference Rules (shown as ellipses)</span>
            </div>
        </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)
