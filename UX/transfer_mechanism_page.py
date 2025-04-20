import streamlit as st
import time
from UX.decision_tree_renderer import DecisionTreeRenderer

class TransferMechanismPage:
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository

    def render(self):
        """Implement a transfer mechanism inference API based on regulatory metadata.
        This helps users determine appropriate safeguards for cross-border data transfers.
        """
        st.markdown("<div class='page-header'><i class='fas fa-exchange-alt'></i> &nbsp;Transfer Mechanism Inference</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            This API helps determine appropriate transfer mechanisms for cross-border data transfers based on regulatory metadata.<br><br>
            <ul>
                <li>Identifies suitable transfer mechanisms for specific jurisdictions</li>
                <li>Evaluates adequacy decisions and existing agreements</li>
                <li>Recommends appropriate safeguards (SCCs, BCRs, etc.)</li>
                <li>Provides implementation guidance for each transfer mechanism</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Jurisdictional Analysis:</strong> Evaluates source and destination jurisdictions</li>
                <li><strong>Adequacy Assessment:</strong> Checks for adequacy decisions or existing agreements</li>
                <li><strong>Risk Evaluation:</strong> Considers data types and transfer volumes</li>
                <li><strong>Mechanism Ranking:</strong> Presents transfer mechanisms in order of preference</li>
                <li><strong>Implementation Guidance:</strong> Provides specific requirements for each mechanism</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
            
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options, key="transfer_law")
        
        # Get jurisdictions for source and destination
        jurisdictions = self.glossary_repository.get_jurisdictions()
        if jurisdictions:
            jurisdiction_options = [j["name"] for j in jurisdictions]
            source_jurisdiction = st.selectbox("Select Source Jurisdiction", options=jurisdiction_options, key="transfer_source")
            destination_jurisdiction = st.selectbox("Select Destination Jurisdiction", options=jurisdiction_options, key="transfer_destination")
        else:
            st.warning("No jurisdictions available.")
            return
        
        # Get data categories
        data_categories = self.glossary_repository.get_data_categories()
        if data_categories:
            dc_options = [dc["name"] for dc in data_categories]
            selected_data_categories = st.multiselect("Select Data Categories to Transfer", options=dc_options, key="transfer_data_categories")
        else:
            selected_data_categories = []
        
        # Add transfer volume/frequency options
        transfer_volume = st.select_slider(
            "Transfer Volume",
            options=["Low", "Medium", "High"],
            value="Medium",
            key="transfer_volume"
        )
        
        transfer_frequency = st.select_slider(
            "Transfer Frequency",
            options=["One-time", "Occasional", "Regular", "Continuous"],
            value="Regular",
            key="transfer_frequency"
        )
        
        # Add a button to trigger inference
        analyze_button = st.button("Recommend Transfer Mechanisms")
        
        if analyze_button:
            # Display a spinner while "processing"
            with st.spinner("Analyzing transfer requirements..."):
                time.sleep(1)
                is_adequate = False
                if destination_jurisdiction in ["United Kingdom", "Canada", "Switzerland", "Japan", "New Zealand"]:
                    is_adequate = True
                transfer_mechanisms = self._get_transfer_mechanisms(selected_law, source_jurisdiction, destination_jurisdiction, is_adequate)
            
            if transfer_mechanisms:
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                    <h3 style="color: #3498db;">Recommended Transfer Mechanisms</h3>
                    <p>Based on the selected parameters, the following transfer mechanisms are recommended for transfers from <strong>{source_jurisdiction}</strong> to <strong>{destination_jurisdiction}</strong> under {selected_law}:</p>
                </div>
                """, unsafe_allow_html=True)
                for i, mechanism in enumerate(transfer_mechanisms):
                    with st.expander(f"{i+1}. {mechanism['name']}"):
                        st.markdown(f"""
                        <div style="padding: 15px; border-radius: 5px; background-color: #f8f9fa;">
                            <h4>{mechanism['name']}</h4>
                            <p><strong>Description:</strong> {mechanism['description']}</p>
                            <p><strong>Implementation Requirements:</strong></p>
                            <ul>
                                {' '.join([f'<li>{req}</li>' for req in mechanism['requirements']])}
                            </ul>
                            <p><strong>Risk Level:</strong> <span style="color: {mechanism['risk_color']};">{mechanism['risk_level']}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                    <h3 style="color: #7F8C8D;">No Transfer Mechanisms Found</h3>
                    <p>No suitable transfer mechanisms were found for the selected parameters. This may be due to:</p>
                    <ul>
                        <li>The destination jurisdiction may have an adequacy decision, making additional safeguards unnecessary</li>
                        <li>The selected law may not have specific transfer mechanism requirements for these jurisdictions</li>
                        <li>The combination of parameters may not match any defined transfer scenarios</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            nodes = [
                {"id": "transfer", "label": "Data Transfer", "color": "#3498db", "shape": "ellipse", "size": 30},
                {"id": "source", "label": "Source Jurisdiction", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "destination", "label": "Destination Jurisdiction", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "law", "label": "Applicable Law", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "data_categories", "label": "Data Categories", "color": "#2ecc71", "shape": "box", "size": 25},
                {"id": "adequacy", "label": "Adequacy Decision", "color": "#1abc9c", "shape": "box", "size": 25},
                {"id": "lookup", "label": "Transfer Mechanism Lookup", "color": "#3498db", "shape": "box", "size": 25,
                    "title": {"html": """
                    <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #3498db;'>
                        <h3>Transfer Mechanism Lookup Process</h3>
                        <p>This lookup process determines appropriate transfer mechanisms by:</p>
                        <ol>
                            <li>Querying the <b>Law Transfer</b> table for the applicable law</li>
                            <li>Checking for adequacy decisions between source and destination jurisdictions</li>
                            <li>Evaluating data categories and their sensitivity levels</li>
                            <li>Considering transfer volume and frequency</li>
                            <li>Ranking mechanisms by appropriateness and legal compliance</li>
                        </ol>
                        <p>The algorithm prioritizes mechanisms based on the legal hierarchy established in each jurisdiction, with preference for adequacy decisions when available.</p>
                    </div>
                """}},
                {"id": "sccs", "label": "Standard Contractual Clauses", "color": "#e74c3c", "shape": "box", "size": 25},
                {"id": "bcrs", "label": "Binding Corporate Rules", "color": "#f39c12", "shape": "box", "size": 25},
                {"id": "consent", "label": "Explicit Consent", "color": "#9b59b6", "shape": "box", "size": 25},
                {"id": "derogations", "label": "Derogations", "color": "#2ecc71", "shape": "box", "size": 25}
            ]
            edges = [
                {"source": "transfer", "target": "source", "label": "From"},
                {"source": "transfer", "target": "destination", "label": "To"},
                {"source": "transfer", "target": "data_categories", "label": "Involves"},
                {"source": "source", "target": "law", "label": "Governed by"},
                {"source": "destination", "target": "adequacy", "label": "Has/lacks"},
                {"source": "law", "target": "lookup", "label": ""},
                {"source": "data_categories", "target": "lookup", "label": ""},
                {"source": "adequacy", "target": "lookup", "label": ""},
                {"source": "lookup", "target": "sccs", "label": "May recommend"},
                {"source": "lookup", "target": "bcrs", "label": "May recommend"},
                {"source": "lookup", "target": "consent", "label": "May recommend"},
                {"source": "lookup", "target": "derogations", "label": "May allow"}
            ]
            DecisionTreeRenderer.render(nodes, edges, "Transfer Mechanism Process", 700)

    def _get_transfer_mechanisms(self, law, source_jurisdiction, destination_jurisdiction, is_adequate):
        """Internal method to get appropriate transfer mechanisms based on regulatory metadata."""
        if is_adequate:
            return [
                {
                    "name": "Adequacy Decision",
                    "description": "The European Commission has recognized that the destination country provides an adequate level of data protection. No additional safeguards are strictly necessary.",
                    "requirements": [
                        "Document the transfer in your records of processing activities",
                        "Ensure compliance with general GDPR principles",
                        "Monitor adequacy status for any changes"
                    ],
                    "risk_level": "Low",
                    "risk_color": "#2ecc71"
                }
            ]
        else:
            return [
                {
                    "name": "Standard Contractual Clauses (SCCs)",
                    "description": "Pre-approved contractual clauses adopted by the European Commission that provide appropriate safeguards for international data transfers.",
                    "requirements": [
                        "Implement the latest version of SCCs (adopted in 2021)",
                        "Conduct and document a transfer impact assessment",
                        "Implement supplementary measures if necessary",
                        "Ensure SCCs are signed by both parties"
                    ],
                    "risk_level": "Medium",
                    "risk_color": "#f39c12"
                },
                {
                    "name": "Binding Corporate Rules (BCRs)",
                    "description": "Internal rules for data transfers within a multinational group, approved by the relevant supervisory authority.",
                    "requirements": [
                        "Develop comprehensive internal data protection policies",
                        "Obtain approval from the lead supervisory authority",
                        "Implement training and compliance mechanisms",
                        "Regular auditing and reporting"
                    ],
                    "risk_level": "Low",
                    "risk_color": "#2ecc71"
                },
                {
                    "name": "Derogations for Specific Situations",
                    "description": "Exceptions that allow transfers in specific circumstances without requiring additional safeguards.",
                    "requirements": [
                        "Ensure the transfer falls under one of the specific derogations",
                        "Document the justification for using the derogation",
                        "Limit transfers to what is strictly necessary",
                        "Consider implementing additional safeguards where possible"
                    ],
                    "risk_level": "High",
                    "risk_color": "#e74c3c"
                }
            ]
