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
        st.title("Policy Authoring")
        
        # Use full width for the form
        st.subheader("Policy Selection Controls")
        
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
        with st.form("policy_authoring_form"):
            # Use columns for a better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Data Elements")
                selected_data_elements = st.multiselect(
                    "Select Data Elements",
                    options=list(data_element_options.keys()),
                    format_func=lambda x: data_element_options[x]
                )
                
                st.markdown("### Policy Types")
                selected_policy_types = st.multiselect(
                    "Select Policy Types",
                    options=list(policy_type_options.keys()),
                    default=list(policy_type_options.keys()),
                    format_func=lambda x: policy_type_options[x]
                )
            
            with col2:
                # Add tabs for different policy contexts
                context_tab, purpose_tab = st.tabs(["Regulatory Context", "Purpose Context"])
                
                with context_tab:
                    st.markdown("### Jurisdictions")
                    selected_jurisdiction = st.selectbox(
                        "Select Jurisdiction",
                        options=[None] + list(jurisdiction_options.keys()),
                        format_func=lambda x: "All Jurisdictions" if x is None else jurisdiction_options.get(x, "")
                    )
                    
                    st.markdown("### Data Subject Types")
                    selected_data_subject_type = st.selectbox(
                        "Select Data Subject Type",
                        options=[None] + list(data_subject_type_options.keys()),
                        format_func=lambda x: "All Data Subject Types" if x is None else data_subject_type_options.get(x, "")
                    )
                
                with purpose_tab:
                    st.markdown("### Purposes")
                    selected_purposes = st.multiselect(
                        "Select Purposes",
                        options=list(purpose_options.keys()),
                        format_func=lambda x: purpose_options[x]
                    )
            
            # Add an option to choose the inference method
            st.markdown("### Inference Method")
            inference_method = st.radio(
                "Select Policy Inference Method",
                options=["Sensitivity-based", "Purpose-based", "Both"],
                index=2,
                horizontal=True  # Display options horizontally to save space
            )
            
            # Submit button - make it prominent
            st.markdown("")
            submitted = st.form_submit_button("Generate Policies", use_container_width=True)
        
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
            
            # Generate JSON if both methods were used
            if inference_method == "Both" and selected_data_elements:
                # Check if we have either context or purpose information
                has_context = selected_jurisdiction or selected_data_subject_type
                has_purpose = selected_purposes and len(selected_purposes) > 0
                
                if has_context or has_purpose:
                    self.render_json(
                        selected_data_elements,
                        selected_purposes,
                        selected_policy_types,
                        purpose_options,
                        policy_type_options,
                        selected_jurisdiction,
                        selected_data_subject_type,
                        context_info
                    )
                else:
                    st.warning("Please select either a jurisdiction/data subject type or at least one purpose to generate implementation details.")
    
    def generate_sensitivity_based_policies(self, selected_data_elements, selected_policy_types, jurisdiction_id=None, data_subject_type_id=None, context_info=None):
        """Generate sensitivity-based policies for the selected data elements."""
        st.subheader("Sensitivity-Based Policies")
        
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
                df = self.asset_policy_inference.get_policies_by_data_elements_sensitivity(
                    selected_data_elements,
                    selected_policy_types if selected_policy_types else 'all'
                )
            
            if df.empty:
                st.info("No sensitivity-based policies found for the selected data elements.")
                return
            
            # Display context information if available
            if context_info:
                context_cols = st.columns(2)
                with context_cols[0]:
                    if 'jurisdiction' in context_info:
                        st.info(f"Jurisdiction: {context_info['jurisdiction']}")
                with context_cols[1]:
                    if 'data_subject_type' in context_info:
                        st.info(f"Data Subject Type: {context_info['data_subject_type']}")
            
            # Format boolean columns as checkboxes
            df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Display the results
            st.dataframe(df)
            
            # Create a pivot table for visualization
            if 'data_element_name' in df.columns and 'policy_type' in df.columns:
                pivot_df = pd.pivot_table(
                    df, 
                    values='policy_name', 
                    index='data_element_name',
                    columns='policy_type', 
                    aggfunc='count',
                    fill_value=0
                )
                
                st.subheader("Policy Distribution by Data Element")
                st.bar_chart(pivot_df)
    
    def generate_purpose_based_policies(self, selected_data_elements, selected_purposes, selected_policy_types, 
                                       purpose_options, policy_type_options):
        """Generate purpose-based policies for the selected data elements and purposes."""
        st.subheader("Purpose-Based Policies")
        
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
                return
            
            # Format boolean columns as checkboxes
            df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Display the results
            st.dataframe(df)
            
            # Create a pivot table for visualization
            if 'data_element_name' in df.columns and 'purpose_name' in df.columns and 'policy_type' in df.columns:
                # Pivot by purpose and policy type
                pivot_df = pd.pivot_table(
                    df, 
                    values='policy_name', 
                    index=['data_element_name', 'purpose_name'],
                    columns='policy_type', 
                    aggfunc='count',
                    fill_value=0
                )
                
                st.subheader("Policy Distribution by Data Element and Purpose")
                st.dataframe(pivot_df)
                
                # Simplified pivot for visualization
                simple_pivot = pd.pivot_table(
                    df, 
                    values='policy_name', 
                    index='data_element_name',
                    columns='policy_type', 
                    aggfunc='count',
                    fill_value=0
                )
                
                st.subheader("Policy Distribution by Data Element")
                st.bar_chart(simple_pivot)
                
                # Create a purpose-policy count for visualization
                purpose_policy_counts = df.groupby(['purpose_name', 'policy_type']).size().reset_index(name='Count')
                purpose_policy_counts.rename(columns={'purpose_name': 'Purpose', 'policy_type': 'Policy Type'}, inplace=True)
                
                st.subheader("Policy Distribution by Purpose")
                pivot_df = purpose_policy_counts.pivot(index='Purpose', columns='Policy Type', values='Count').fillna(0)
                st.bar_chart(pivot_df)
    
    def render(self):
        """Render the Policy Authoring page with selection controls and policy generation."""
        st.title("Policy Authoring")
        
        # Use full width for the form
        st.subheader("Policy Selection Controls")
        
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
        with st.form("policy_authoring_form"):
            # Use columns for a better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Data Elements")
                selected_data_elements = st.multiselect(
                    "Select Data Elements",
                    options=list(data_element_options.keys()),
                    format_func=lambda x: data_element_options[x]
                )
                
                st.markdown("### Policy Types")
                selected_policy_types = st.multiselect(
                    "Select Policy Types",
                    options=list(policy_type_options.keys()),
                    default=list(policy_type_options.keys()),
                    format_func=lambda x: policy_type_options[x]
                )
            
            with col2:
                # Add tabs for different policy contexts
                context_tab, purpose_tab = st.tabs(["Regulatory Context", "Purpose Context"])
                
                with context_tab:
                    st.markdown("### Jurisdictions")
                    selected_jurisdiction = st.selectbox(
                        "Select Jurisdiction",
                        options=[None] + list(jurisdiction_options.keys()),
                        format_func=lambda x: "All Jurisdictions" if x is None else jurisdiction_options.get(x, "")
                    )
                    
                    st.markdown("### Data Subject Types")
                    selected_data_subject_type = st.selectbox(
                        "Select Data Subject Type",
                        options=[None] + list(data_subject_type_options.keys()),
                        format_func=lambda x: "All Data Subject Types" if x is None else data_subject_type_options.get(x, "")
                    )
                
                with purpose_tab:
                    st.markdown("### Purposes")
                    selected_purposes = st.multiselect(
                        "Select Purposes",
                        options=list(purpose_options.keys()),
                        format_func=lambda x: purpose_options[x]
                    )
            
            # Add an option to choose the inference method
            st.markdown("### Inference Method")
            inference_method = st.radio(
                "Select Policy Inference Method",
                options=["Sensitivity-based", "Purpose-based", "Both"],
                index=2,
                horizontal=True  # Display options horizontally to save space
            )
            
            # Submit button - make it prominent
            st.markdown("")
            submitted = st.form_submit_button("Generate Policies", use_container_width=True)
        
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
    
    def generate_sensitivity_based_policies(self, selected_data_elements, selected_policy_types, jurisdiction_id=None, data_subject_type_id=None, context_info=None):
        """Generate sensitivity-based policies for the selected data elements."""
        st.subheader("Sensitivity-Based Policies")
        
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
                df = self.asset_policy_inference.get_policies_by_data_elements_sensitivity(
                    selected_data_elements,
                    selected_policy_types if selected_policy_types else 'all'
                )
            
            if df.empty:
                st.info("No sensitivity-based policies found for the selected data elements.")
                return
            
            # Display context information if available
            if context_info:
                context_cols = st.columns(2)
                with context_cols[0]:
                    if 'jurisdiction' in context_info:
                        st.info(f"Jurisdiction: {context_info['jurisdiction']}")
                with context_cols[1]:
                    if 'data_subject_type' in context_info:
                        st.info(f"Data Subject Type: {context_info['data_subject_type']}")
            
            # Format boolean columns as checkboxes
            df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Display the results
            st.dataframe(df)
            
            # Create a pivot table for visualization
            if 'data_element_name' in df.columns and 'policy_type' in df.columns:
                pivot_df = pd.pivot_table(
                    df, 
                    values='policy_name', 
                    index='data_element_name',
                    columns='policy_type', 
                    aggfunc='count',
                    fill_value=0
                )
                
                st.subheader("Policy Distribution by Data Element")
                st.bar_chart(pivot_df)
    
    def generate_purpose_based_policies(self, selected_data_elements, selected_purposes, selected_policy_types, 
                                       purpose_options, policy_type_options):
        """Generate purpose-based policies for the selected data elements and purposes."""
        st.subheader("Purpose-Based Policies")
        
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
                return
            
            # Format boolean columns as checkboxes
            df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Display the results
            st.dataframe(df)
            
            # Create a pivot table for visualization
            if 'data_element_name' in df.columns and 'purpose_name' in df.columns and 'policy_type' in df.columns:
                # Pivot by purpose and policy type
                pivot_df = pd.pivot_table(
                    df, 
                    values='policy_name', 
                    index=['data_element_name', 'purpose_name'],
                    columns='policy_type', 
                    aggfunc='count',
                    fill_value=0
                )
                
                st.subheader("Policy Distribution by Data Element and Purpose")
                st.dataframe(pivot_df)
                
                # Simplified pivot for visualization
                simple_pivot = pd.pivot_table(
                    df, 
                    values='policy_name', 
                    index='data_element_name',
                    columns='policy_type', 
                    aggfunc='count',
                    fill_value=0
                )
                
                st.subheader("Policy Distribution by Data Element")
                st.bar_chart(simple_pivot)
    
    def render(self):
        """Render the Policy Authoring page with selection controls and policy generation."""
        st.title("Policy Authoring")
        
        # Use full width for the form
        st.subheader("Policy Selection Controls")
        
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
        with st.form("policy_authoring_form"):
            # Use columns for a better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Data Elements")
                selected_data_elements = st.multiselect(
                    "Select Data Elements",
                    options=list(data_element_options.keys()),
                    format_func=lambda x: data_element_options[x]
                )
                
                st.markdown("### Policy Types")
                selected_policy_types = st.multiselect(
                    "Select Policy Types",
                    options=list(policy_type_options.keys()),
                    default=list(policy_type_options.keys()),
                    format_func=lambda x: policy_type_options[x]
                )
            
            with col2:
                # Add tabs for different policy contexts
                context_tab, purpose_tab = st.tabs(["Regulatory Context", "Purpose Context"])
            
                with context_tab:
                    st.markdown("### Jurisdictions")
                    selected_jurisdiction = st.selectbox(
                        "Select Jurisdiction",
                        options=[None] + list(jurisdiction_options.keys()),
                        format_func=lambda x: "All Jurisdictions" if x is None else jurisdiction_options.get(x, "")
                    )
                    
                    st.markdown("### Data Subject Types")
                    selected_data_subject_type = st.selectbox(
                        "Select Data Subject Type",
                        options=[None] + list(data_subject_type_options.keys()),
                        format_func=lambda x: "All Data Subject Types" if x is None else data_subject_type_options.get(x, "")
                    )
                
                with purpose_tab:
                    st.markdown("### Purposes")
                    selected_purposes = st.multiselect(
                        "Select Purposes",
                        options=list(purpose_options.keys()),
                        format_func=lambda x: purpose_options[x]
                    )
            
            # Add an option to choose the inference method
            st.markdown("### Inference Method")
            inference_method = st.radio(
                "Select Policy Inference Method",
                options=["Sensitivity-based", "Purpose-based", "Both"],
                index=2,
                horizontal=True  # Display options horizontally to save space
            )
            
            # Submit button - make it prominent
            st.markdown("")
            submitted = st.form_submit_button("Generate Policies", use_container_width=True)
        
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
            
    def generate_sensitivity_based_policies(self, selected_data_elements, selected_policy_types, jurisdiction_id=None, data_subject_type_id=None, context_info=None):
        """Generate sensitivity-based policies for the selected data elements."""
        # Create a title with context information if available
        title = "Sensitivity-Based Policies"
        if context_info:
            context_parts = []
            if 'jurisdiction' in context_info:
                context_parts.append(f"Jurisdiction: {context_info['jurisdiction']}")
            if 'data_subject_type' in context_info:
                context_parts.append(f"Data Subject Type: {context_info['data_subject_type']}")
            
            if context_parts:
                title += f" ({', '.join(context_parts)})"
        
        st.subheader(title)
        
        with st.spinner("Analyzing sensitivity-based policies..."):
            # Get policies based on data element sensitivities with jurisdiction and data subject type if provided
            if jurisdiction_id or data_subject_type_id:
                df = self.asset_policy_inference.get_policies_by_jurisdiction_data_subject_type_data_elements_sensitivity(
                    selected_data_elements,
                    jurisdiction_id=jurisdiction_id,
                    data_subject_type_id=data_subject_type_id
                )
                if jurisdiction_id and data_subject_type_id:
                    st.info(f"Policies are based on jurisdiction and data subject type specific sensitivity inference.")
                elif jurisdiction_id:
                    st.info(f"Policies are based on jurisdiction specific sensitivity inference.")
                elif data_subject_type_id:
                    st.info(f"Policies are based on data subject type specific sensitivity inference.")
            else:
                # Use standard method without jurisdiction and data subject type
                df = self.asset_policy_inference.get_policies_by_data_elements_sensitivity(selected_data_elements)
            
            if df.empty:
                if jurisdiction_id or data_subject_type_id:
                    st.warning("No sensitivity-based policies found for the selected data elements with the specified jurisdiction and data subject type.")
                else:
                    st.info("No sensitivity-based policies found for the selected data elements.")
                return
            
            # Filter by policy types if specified
            if selected_policy_types and 'all' not in selected_policy_types and 'policy_type' in df.columns:
                # Convert policy_type column to lowercase for case-insensitive comparison
                df['policy_type_lower'] = df['policy_type'].str.lower()
                
                # Create a list of lowercase policy types to filter by
                policy_types_lower = [pt.lower() for pt in selected_policy_types]
                
                # Filter the DataFrame
                df = df[df['policy_type_lower'].isin(policy_types_lower)]
                
                # Remove the temporary column
                df = df.drop('policy_type_lower', axis=1)
            
            # Format boolean columns as checkboxes
            formatted_df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Display the results
            st.dataframe(formatted_df, use_container_width=True)
            
            # Add a download button for the results
            csv = df.to_csv(index=False)
            filename = "sensitivity_based_policies"
            if jurisdiction_id:
                filename += f"_jurisdiction_{jurisdiction_id}"
            if data_subject_type_id:
                filename += f"_data_subject_type_{data_subject_type_id}"
            
            st.download_button(
                label="Download Sensitivity-Based Policies",
                data=csv,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
            
            # Group by sensitivity and display summary
            if 'sensitivity' in df.columns:
                sensitivity_counts = df['sensitivity'].value_counts().reset_index()
                sensitivity_counts.columns = ['Sensitivity', 'Policy Count']
                
            # Show additional context-specific visualizations if available
            if jurisdiction_id and 'jurisdiction_name' in df.columns:
                st.subheader(f"Policies for Jurisdiction: {context_info.get('jurisdiction', 'Selected')}")
                if 'policy_type' in df.columns:
                    policy_type_counts = df['policy_type'].value_counts().reset_index()
                    policy_type_counts.columns = ['Policy Type', 'Count']
                    st.bar_chart(policy_type_counts.set_index('Policy Type'))
                    
            if data_subject_type_id and 'data_subject_type_name' in df.columns:
                st.subheader(f"Policies for Data Subject Type: {context_info.get('data_subject_type', 'Selected')}")
                if 'policy_type' in df.columns and 'sensitivity' in df.columns:
                    # Create a crosstab of policy types and sensitivities
                    pivot_df = pd.crosstab(df['sensitivity'], df['policy_type'])
                    st.write("Policy Types by Sensitivity:")
                    st.dataframe(pivot_df)
    
    def generate_purpose_based_policies(self, selected_data_elements, selected_purposes, selected_policy_types, 
                                       purpose_options, policy_type_options):
        """Generate purpose-based policies for the selected data elements and purposes."""
        st.subheader("Purpose-Based Policies")
        
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
                return
            
            # Format boolean columns as checkboxes
            formatted_df = self.asset_policy_inference.format_boolean_as_checkbox(df)
            
            # Display the results
            st.dataframe(formatted_df, use_container_width=True)
            
            # Add a download button for the results
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Purpose-Based Policies",
                data=csv,
                file_name="purpose_based_policies.csv",
                mime="text/csv"
            )
            
            # Group by purpose and policy type and display summary
            if 'purpose_name' in df.columns and 'policy_type' in df.columns:
                purpose_policy_counts = df.groupby(['purpose_name', 'policy_type']).size().reset_index()
                purpose_policy_counts.columns = ['Purpose', 'Policy Type', 'Count']
                
                
                
    
    def render_json(self, selected_data_elements, selected_purposes, selected_policy_types, 
                           purpose_options, policy_type_options,
                           jurisdiction_id=None, data_subject_type_id=None, context_info=None):
        """Generate and display JSON for the policies."""
        st.subheader("Policy Implementation")
        
        with st.container():
            st.markdown("### JSON for Policy Implementation")
            
            # Get policies for JSON generation based on available parameters
            policies_dfs = []
            
            # Get purpose-based policies if purposes are selected
            if selected_purposes:
                purpose_policies_df = self.asset_policy_inference.get_policies_by_data_elements_purpose(
                    selected_data_elements,
                    selected_purposes,
                    selected_policy_types,
                    'all'  # Use 'all' for roles
                )
                if not purpose_policies_df.empty:
                    policies_dfs.append(purpose_policies_df)
            
            # Get jurisdiction/data subject type based policies if specified
            if jurisdiction_id or data_subject_type_id:
                sensitivity_policies_df = self.asset_policy_inference.infer_policies_by_jurisdiction_data_subject_type_data_element(
                    selected_data_elements,
                    selected_policy_types,
                    jurisdiction_id,
                    data_subject_type_id
                )
                if not sensitivity_policies_df.empty:
                    policies_dfs.append(sensitivity_policies_df)
            else:
                # Get standard sensitivity-based policies if no jurisdiction/data subject type is specified
                sensitivity_policies_df = self.asset_policy_inference.get_policies_by_data_elements_sensitivity(
                    selected_data_elements,
                    selected_policy_types
                )
                if not sensitivity_policies_df.empty:
                    policies_dfs.append(sensitivity_policies_df)
            
            if not policies_dfs:
                st.info("No policies available for JSON generation.")
                return
            
            # Combine all policy dataframes
            combined_df = pd.concat(policies_dfs, ignore_index=True)
            
            # Generate JSON output
            json_output = self.json_generator.generate_json(combined_df)
            
            # Combine the policies
            combined_policies = {
                "sensitivity_based": sensitivity_policies_df.to_dict(orient="records") if not sensitivity_policies_df.empty else [],
                "purpose_based": purpose_policies_df.to_dict(orient="records") if not purpose_policies_df.empty else [],
                "data_elements": [self.catalog_repository.get_data_element_by_id(de_id) for de_id in selected_data_elements],
                "purposes": [self.glossary_repository.get_purpose_by_id(p_id) for p_id in selected_purposes] if selected_purposes else []
            }
            
            # Add note about purpose-based roles for DDL generation
            combined_policies["ddl_preferences"] = {
                "use_purpose_based_roles": True,
                "masking_policy_naming": "data_element",  # Name masking policies based on data element names
                "use_role_in_session": True  # Use IS_ROLE_IN_SESSION() in masking policies
            }
            
            # Add jurisdiction if specified
            if jurisdiction_id:
                jurisdiction = self.glossary_repository.get_jurisdiction_by_id(jurisdiction_id)
                if jurisdiction:
                    combined_policies["jurisdiction"] = jurisdiction
            
            # Add data subject type if specified
            if data_subject_type_id:
                data_subject_type = self.glossary_repository.get_data_subject_type_by_id(data_subject_type_id)
                if data_subject_type:
                    combined_policies["data_subject_type"] = data_subject_type
            
            # Generate JSON
            json_output = self.json_generator.generate_json(combined_policies)
            
            # Display the JSON
            st.json(json_output)
            
            # Add a download button for the JSON
            filename = "policy_implementation"
            if jurisdiction_id:
                filename += f"_jurisdiction_{jurisdiction_id}"
            if data_subject_type_id:
                filename += f"_data_subject_type_{data_subject_type_id}"
                
            st.download_button(
                label="Download JSON",
                data=json_output,
                file_name=f"{filename}.json",
                mime="application/json"
            )
    
    
