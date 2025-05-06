import streamlit as st
import pandas as pd
import numpy as np
from components.JSONGenerator import JSONGenerator
from core.asset_policy_inference import AssetPolicyInference


class PolicyAuthoringPage:
    """Page for authoring and generating data governance policies."""
    
    def __init__(self, inventory_repository, glossary_repository, catalog_repository, sensitivity_inference, regulatory_metadata_repository, policy_repository):
        """Initialize the Policy Authoring page with required repositories."""
        self.inventory_repository = inventory_repository
        self.glossary_repository = glossary_repository
        self.catalog_repository = catalog_repository
        self.sensitivity_inference = sensitivity_inference
        self.regulatory_metadata_repository = regulatory_metadata_repository
        # Initialize asset_policy_inference with policy_repository
        self.asset_policy_inference = AssetPolicyInference(catalog_repository, regulatory_metadata_repository, glossary_repository, inventory_repository, policy_repository=policy_repository)
        self.json_generator = JSONGenerator(glossary_repository, catalog_repository, inventory_repository)
    
    def render(self):
        """Render the Policy Authoring page with selection controls and policy generation."""
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Authoring</div>", unsafe_allow_html=True)
        
        # Add CSS for styled components
        st.markdown("""
        <style>
        /* Target only the expander components */
        div[data-testid="stExpander"] {
            border: 1px solid #3498db !important;
            border-radius: 4px !important;
            margin-bottom: 10px !important;
            background-color: #eaf2f8 !important;
        }
        div[data-testid="stExpander"] > div:first-child {
            background-color: #eaf2f8 !important;
            border-bottom: 1px solid #3498db !important;
            padding: 0.5rem !important;
        }
        div[data-testid="stExpander"] details summary p {
            color: #3498db !important;
            font-weight: 600 !important;
        }
        
        /* Form styling */
        div[data-testid="stForm"] {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }
        
        /* Results container styling */
        .results-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #3498db;
        }
        
        /* Policy type badges */
        .policy-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 5px;
        }
        .security-badge {
            background-color: #e74c3c;
            color: white;
        }
        .usage-badge {
            background-color: #3498db;
            color: white;
        }
        .retention-badge {
            background-color: #2ecc71;
            color: white;
        }
        
        /* Data frame styling */
        div[data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #e9ecef;
        }
        
        /* Tab styling */
        button[data-baseweb="tab"] {
            border-radius: 4px 4px 0 0;
            padding: 10px 24px;
            font-weight: 600;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #eaf2f8;
            border-bottom: 3px solid #3498db;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section allows you to author and generate data governance policies based on:</p>
            <ul>
                <li><strong>Sensitivity-based policies</strong> - derived from data element sensitivity levels</li>
                <li><strong>Purpose-based policies</strong> - derived from specific business purposes</li>
                <li><strong>Regulatory context</strong> - including jurisdictions and data subject types</li>
            </ul>
            <p>The system will analyze your selections and generate appropriate policies for implementation.</p>
        </div>''', unsafe_allow_html=True)
        
        # Get all data elements
        data_elements = self.glossary_repository.get_data_elements()
        data_element_options = {de['id']: de['name'] for de in data_elements}
        
        # Get all purposes
        purposes = self.glossary_repository.get_purposes()
        purpose_options = {p['id']: p['name'] for p in purposes}
        
        # Get all policy types
        policy_types = ['security', 'usage', 'retention']
        policy_type_options = {pt: pt.capitalize() for pt in policy_types}
        
        # Get all jurisdictions
        jurisdictions = self.glossary_repository.get_jurisdictions()
        jurisdiction_options = {j['id']: j['name'] for j in jurisdictions}
        
        # Get all data subject types
        data_subject_types = self.glossary_repository.get_data_subject_types()
        data_subject_type_options = {dst['id']: dst['name'] for dst in data_subject_types}
        
        # Create form with full width layout
        st.markdown("<h3 style='color: #3498db;'><i class='fas fa-sliders-h'></i> Policy Selection Controls</h3>", unsafe_allow_html=True)
        
        with st.form("policy_authoring_form"):
            # Use columns for a better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h4 style='color: #2c3e50;'><i class='fas fa-database'></i> Data Elements</h4>", unsafe_allow_html=True)
                selected_data_elements = st.multiselect(
                    "Select Data Elements",
                    options=list(data_element_options.keys()),
                    format_func=lambda x: data_element_options[x],
                    help="Choose the data elements for which you want to generate policies"
                )
                
                st.markdown("<h4 style='color: #2c3e50;'><i class='fas fa-tags'></i> Policy Types</h4>", unsafe_allow_html=True)
                selected_policy_types = st.multiselect(
                    "Select Policy Types",
                    options=list(policy_type_options.keys()),
                    default=list(policy_type_options.keys()),
                    format_func=lambda x: policy_type_options[x],
                    help="Choose the types of policies you want to generate"
                )
                
                # Add an option to choose the inference method
                st.markdown("<h4 style='color: #2c3e50;'><i class='fas fa-cogs'></i> Inference Method</h4>", unsafe_allow_html=True)
                inference_method = st.radio(
                    "Select Policy Inference Method",
                    options=["Sensitivity-based", "Purpose-based", "Both"],
                    index=2,
                    horizontal=True,  # Display options horizontally to save space
                    help="Choose how policies should be inferred"
                )
            
            with col2:
                # Add styled container for context selection
                st.markdown("<h4 style='color: #2c3e50;'><i class='fas fa-globe'></i> Policy Context</h4>", unsafe_allow_html=True)
                
                # Add tabs for different policy contexts with custom styling
                context_tab, purpose_tab = st.tabs(["📋 Regulatory Context", "🎯 Purpose Context"])
                
                with context_tab:
                    st.markdown("<h5 style='color: #2c3e50;'>Jurisdictions</h5>", unsafe_allow_html=True)
                    selected_jurisdiction = st.selectbox(
                        "Select Jurisdiction",
                        options=[None] + list(jurisdiction_options.keys()),
                        format_func=lambda x: "All Jurisdictions" if x is None else jurisdiction_options.get(x, ""),
                        help="Select a specific jurisdiction for regulatory context"
                    )
                    
                    st.markdown("<h5 style='color: #2c3e50;'>Data Subject Types</h5>", unsafe_allow_html=True)
                    selected_data_subject_type = st.selectbox(
                        "Select Data Subject Type",
                        options=[None] + list(data_subject_type_options.keys()),
                        format_func=lambda x: "All Data Subject Types" if x is None else data_subject_type_options.get(x, ""),
                        help="Select a specific data subject type for regulatory context"
                    )
                
                with purpose_tab:
                    st.markdown("<h5 style='color: #2c3e50;'>Purposes</h5>", unsafe_allow_html=True)
                    selected_purposes = st.multiselect(
                        "Select Purposes",
                        options=list(purpose_options.keys()),
                        format_func=lambda x: purpose_options[x],
                        help="Select the business purposes for which you need policies"
                    )
            
            # Submit button - make it prominent
            st.markdown("")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("🚀 Generate Policies", use_container_width=True, type="primary")
        
        # Display the policy generation results in full width
        if submitted:
            if not selected_data_elements:
                st.warning("Please select at least one data element.")
                return
            
            # Store context information for display
            context_info = {}
            if selected_jurisdiction:
                jurisdiction = self.glossary_repository.get_jurisdiction_by_id(selected_jurisdiction)
                context_info['jurisdiction'] = jurisdiction['name'] if jurisdiction else 'Unknown'
                context_info['jurisdiction_id'] = selected_jurisdiction
            
            if selected_data_subject_type:
                data_subject_type = self.glossary_repository.get_data_subject_type_by_id(selected_data_subject_type)
                context_info['data_subject_type'] = data_subject_type['name'] if data_subject_type else 'Unknown'
                context_info['data_subject_type_id'] = selected_data_subject_type
            
            # Check which inference method to use
            if inference_method in ["Sensitivity-based", "Both"]:
                self.generate_sensitivity_based_policies(
                    selected_data_elements, 
                    selected_policy_types,
                    selected_jurisdiction,
                    selected_data_subject_type,
                    context_info
                )
            
            if inference_method in ["Purpose-based", "Both"] and selected_purposes:
                self.generate_purpose_based_policies(
                    selected_data_elements, 
                    selected_purposes, 
                    selected_policy_types, 
                    purpose_options,
                    policy_type_options
                )
            elif inference_method == "Purpose-based" and not selected_purposes:
                st.warning("Please select at least one purpose for purpose-based inference.")
                
            # Policy Implementation section removed as requested
    
    def generate_sensitivity_based_policies(self, selected_data_elements, selected_policy_types, jurisdiction_id=None, data_subject_type_id=None, context_info=None):
        """Generate sensitivity-based policies for the selected data elements."""
        st.markdown("<div class='results-container'><h3 style='color: #3498db;'><i class='fas fa-shield-alt'></i> Sensitivity-Based Policies</h3>", unsafe_allow_html=True)
        
        with st.spinner("Analyzing sensitivity-based policies..."):
            # Get policies based on data elements and sensitivity
            if jurisdiction_id or data_subject_type_id:
                df = self.asset_policy_inference.infer_policies_by_jurisdiction_data_subject_type_data_element(
                    selected_data_elements,
                    selected_policy_types if selected_policy_types else 'all',
                    jurisdiction_id,
                    data_subject_type_id
                )
            else:
                # This method only takes data_element_ids as a parameter
                df = self.asset_policy_inference.get_policies_by_data_elements_sensitivity(
                    selected_data_elements
                )
            
            if df.empty:
                st.info("No sensitivity-based policies found for the selected data elements.")
                st.markdown("</div>", unsafe_allow_html=True)
                return
            
            # Display context information if available
            if context_info:
                context_cols = st.columns(2)
                with context_cols[0]:
                    if 'jurisdiction' in context_info:
                        st.markdown(f"<div style='background-color: #eaf2f8; padding: 10px; border-radius: 5px;'><i class='fas fa-globe'></i> <b>Jurisdiction:</b> {context_info['jurisdiction']}</div>", unsafe_allow_html=True)
                with context_cols[1]:
                    if 'data_subject_type' in context_info:
                        st.markdown(f"<div style='background-color: #eaf2f8; padding: 10px; border-radius: 5px;'><i class='fas fa-user'></i> <b>Data Subject Type:</b> {context_info['data_subject_type']}</div>", unsafe_allow_html=True)
            
            # Format boolean columns as checkboxes
            df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Add colored indicators for policy types
            if 'policy_type' in df.columns and not df.empty:
                # Store the original policy_type values
                df['policy_type_original'] = df['policy_type']
                
                # Instead of using HTML, we'll use emoji indicators for different policy types
                def format_policy_type(policy_type):
                    policy_type_lower = policy_type.lower()
                    if policy_type_lower == 'security':
                        return '🔒 Security'
                    elif policy_type_lower == 'usage':
                        return '📊 Usage'
                    elif policy_type_lower == 'retention':
                        return '⏱️ Retention'
                    else:
                        return policy_type
                
                # Apply formatting directly to the policy_type column
                df['policy_type'] = df['policy_type'].apply(format_policy_type)
            
            # Display the results in a styled dataframe
            st.markdown("<h4 style='color: #2c3e50;'><i class='fas fa-table'></i> Policy Details</h4>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=400)
            
            # Policy Distribution section removed as requested
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def generate_purpose_based_policies(self, selected_data_elements, selected_purposes, selected_policy_types, 
                                       purpose_options, policy_type_options):
        """Generate purpose-based policies for the selected data elements and purposes."""
        st.markdown("<div class='results-container'><h3 style='color: #3498db;'><i class='fas fa-bullseye'></i> Purpose-Based Policies</h3>", unsafe_allow_html=True)
        
        with st.spinner("Analyzing purpose-based policies..."):
            # Get policies based on data elements and purposes
            df = self.asset_policy_inference.get_policies_by_data_elements_purpose(
                selected_data_elements,
                selected_purposes if selected_purposes else 'all',
                selected_policy_types if selected_policy_types else 'all',
                'all'  # Use 'all' for roles
            )
            
            if df.empty:
                st.info("No purpose-based policies found for the selected data elements and purposes.")
                st.markdown("</div>", unsafe_allow_html=True)
                return
            
            # Format boolean columns as checkboxes
            df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Add colored indicators for policy types
            if 'policy_type' in df.columns and not df.empty:
                # Store the original policy_type values
                df['policy_type_original'] = df['policy_type']
                
                # Instead of using HTML, we'll use emoji indicators for different policy types
                def format_policy_type(policy_type):
                    policy_type_lower = policy_type.lower()
                    if policy_type_lower == 'security':
                        return '🔒 Security'
                    elif policy_type_lower == 'usage':
                        return '📊 Usage'
                    elif policy_type_lower == 'retention':
                        return '⏱️ Retention'
                    else:
                        return policy_type
                
                # Apply formatting directly to the policy_type column
                df['policy_type'] = df['policy_type'].apply(format_policy_type)
            
            # Display the results in a styled dataframe
            st.markdown("<h4 style='color: #2c3e50;'><i class='fas fa-table'></i> Policy Details</h4>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=400)
            
            # Policy Distribution section removed as requested
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Policy Implementation Section removed as requested
