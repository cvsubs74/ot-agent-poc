import streamlit as st

from UX.decision_tree_renderer import DecisionTreeRenderer

class PolicyInferencePage:
    def __init__(self, glossary_repository, policy_compliance_page):
        self.glossary_repository = glossary_repository
        self.policy_compliance_page = policy_compliance_page

    def render(self):
        """Implement the Policy Inference API for access governance.
        This helps determine whether access to data is permitted based on purpose limitation principles.
        """
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Inference API</div>", unsafe_allow_html=True)
        
        # Description
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p><strong>Policy Inference API</strong> determines whether access to data is permitted based on purpose limitation principles and organizational policies.</p>
            <p>This API helps enforce purpose-based access control and ensures data is only used for approved purposes in compliance with privacy regulations.</p>
            <br>
            <ul>
                <li>Enforces purpose limitation principles</li>
                <li>Determines data access permissions based on business purpose</li>
                <li>Applies policy-based restrictions on data usage</li>
                <li>Provides clear decision rationale</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        # Get purposes for dropdown selection
        try:
            purposes = self.glossary_repository.get_purposes()
            purpose_options = [purpose["name"] for purpose in purposes] if purposes else ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
        except Exception as e:
            st.warning(f"Error loading purposes: {e}")
            purpose_options = ["Customer Support", "Fraud Detection", "Marketing Campaigns", "Product Analytics", "User Authentication"]
            
        selected_purpose = st.selectbox("Select Business Purpose", options=purpose_options, key="policy_purpose")
        
        # Get data elements for multiselect
        try:
            data_elements = self.glossary_repository.get_data_elements()
            data_element_options = [de["name"] for de in data_elements] if data_elements else ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
        except Exception as e:
            st.warning(f"Error loading data elements: {e}")
            data_element_options = ["Full Name", "Email Address", "Phone Number", "Customer ID", "Purchase History", "Social Security Number", "Credit Card Number"]
            
        selected_data_elements = st.multiselect("Select Data Elements", options=data_element_options, key="policy_data_elements")
        
        # Operation selection
        operations = ["read", "write", "share"]
        selected_operation = st.selectbox("Select Operation", options=operations, key="policy_operation")
        
        try:
            jurisdictions = self.glossary_repository.get_jurisdictions()
            jurisdiction_options = ["Any"] + [j["name"] for j in jurisdictions] if jurisdictions else ["Any", "California", "European Union", "United Kingdom", "Canada"]
        except Exception as e:
            jurisdiction_options = ["Any", "California", "European Union", "United Kingdom", "Canada"]
            
        selected_jurisdiction = st.selectbox("Select Jurisdiction (Optional)", options=jurisdiction_options, key="policy_jurisdiction")
        
        analyze_button = st.button("Analyze Policy Compliance", key="policy_analysis_btn")
        
        # Define nodes for the decision tree
        nodes = [
            {"id": "request", "label": "Access Request", "color": "#3498db", "shape": "ellipse", "size": 30},
            {"id": "purpose", "label": "Business Purpose", "color": "#e74c3c", "shape": "box", "size": 25},
            {"id": "policy", "label": "Applicable Policy", "color": "#9b59b6", "shape": "box", "size": 25},
            {"id": "data_elements", "label": "Data Elements", "color": "#f39c12", "shape": "box", "size": 25},
            {"id": "operation", "label": "Operation Type", "color": "#2ecc71", "shape": "box", "size": 25},
            {"id": "lookup", "label": "Policy Compliance Check", "color": "#1abc9c", "shape": "box", "size": 25},
            {"id": "allowed", "label": "Access Decision", "color": "#3498db", "shape": "box", "size": 25},
            {"id": "restrictions", "label": "Usage Restrictions", "color": "#f39c12", "shape": "box", "size": 25},
            {"id": "rationale", "label": "Decision Rationale", "color": "#e74c3c", "shape": "box", "size": 25}
        ]
        
        # Define edges for the decision tree
        edges = [
            {"source": "request", "target": "purpose", "arrows": "to", "label": "has"},
            {"source": "purpose", "target": "policy", "arrows": "to", "label": "governed by"},
            {"source": "request", "target": "data_elements", "arrows": "to", "label": "requests"},
            {"source": "request", "target": "operation", "arrows": "to", "label": "performs"},
            {"source": "purpose", "target": "lookup", "arrows": "to"},
            {"source": "data_elements", "target": "lookup", "arrows": "to"},
            {"source": "operation", "target": "lookup", "arrows": "to"},
            {"source": "policy", "target": "lookup", "arrows": "to"},
            {"source": "lookup", "target": "allowed", "arrows": "to"},
            {"source": "lookup", "target": "restrictions", "arrows": "to"},
            {"source": "lookup", "target": "rationale", "arrows": "to"}
        ]
        
        if analyze_button:
            if not selected_purpose or not selected_data_elements:
                st.warning("Please select both Purpose and at least one Data Element")
            else:
                self.policy_compliance_page.analyze_policy_compliance(
                    selected_purpose, 
                    selected_data_elements,
                    selected_operation,
                    selected_jurisdiction if selected_jurisdiction != "Any" else None
                )

                # Render the decision tree
                self._render_decision_tree(nodes, edges, title="Policy Decision Tree")
        else:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h3 style="color: #7F8C8D;">Sample Result</h3>
                <p>Policy compliance analysis will appear here after analysis...</p>
            </div>
            """, unsafe_allow_html=True)

    def _render_decision_tree(self, nodes, edges, title="Policy Decision Tree"):
        # This method should delegate to the main app's decision tree rendering logic if possible
        # For now, assume it is implemented elsewhere or provide a placeholder
        st.markdown(f"#### {title}")
        DecisionTreeRenderer.render_decision_tree(nodes, edges)
