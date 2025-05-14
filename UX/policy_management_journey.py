import streamlit as st
import pandas as pd
import json
from datetime import datetime

class PolicyManagementJourney:
    """A user journey for managing policies, policy groups, and context-specific overrides."""
    
    def __init__(self, policy_definition_repository, glossary_repository, regulatory_metadata_repository):
        """Initialize the Policy Management Journey with required repositories."""
        self.policy_definition_repository = policy_definition_repository
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
    
    def render(self):
        """Render the Policy Management Journey page."""
        st.markdown("<div class='page-header'><i class='fas fa-shield-alt'></i> &nbsp;Policy Management Journey</div>", unsafe_allow_html=True)
        
        # Introduction with standard Streamlit components
        st.markdown("This journey demonstrates how to manage policies based on purposes, ensuring data is protected according to its sensitivity and intended use.")
        
        # Create tabs for different sections of the journey using standard Streamlit tabs
        tabs = st.tabs(["Overview", "Policy Types", "Define Policies", "Policy Groups & Overrides", "FAQ"])
        
        # Render content based on selected tab
        with tabs[0]:  # Overview
            self._render_overview()
        with tabs[1]:  # Policy Types
            self._render_policy_types()
        with tabs[2]:  # Define Policies
            self._render_define_policies()
        with tabs[3]:  # Policy Groups & Overrides
            self._render_policy_groups()
        with tabs[4]:  # FAQ
            self._render_faq()
    
    def _render_overview(self):
        """Render the overview of policy management."""
        # Header with custom styling - light blue background
        st.markdown("""
        <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #1565C0;">
            <h2 style="color: #1565C0; text-align: center; margin: 0;">Policy Management Journey</h2>
            <p style="color: #1565C0; text-align: center; margin-top: 10px;">A comprehensive approach to data governance and protection</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Introduction with custom styling
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #1565C0; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 16px;">Policy management is a critical component of data governance, allowing organizations to define and enforce rules 
            for how data can be accessed, used, and retained. This journey provides a comprehensive approach to managing policies 
            with a focus on purpose-based access control and data protection.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step-by-step guide with visual header
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="background-color: #1565C0; color: white; padding: 10px; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                <span style="font-size: 20px;">📋</span>
            </div>
            <h3 style="margin: 0; color: #1565C0;">Policy Management Step-by-Step Guide</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Define steps with rich styling
        steps = [
            {
                "title": "Understand Policy Types",
                "description": """
                <div style="padding: 10px; border-radius: 5px;">
                    <p>Start by understanding the different types of policies available:</p>
                    <ul>
                        <li><span style="color: #1565C0; font-weight: bold;">Access Control Policies</span>: Define who can access what data and under what conditions</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Security Policies</span>: Specify how data should be protected through masking, encryption, and other security measures</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Retention Policies</span>: Determine how long data should be kept and when it should be deleted</li>
                    </ul>
                    <p>Each policy type serves a specific purpose in your data governance framework.</p>
                </div>
                """,
                "icon": "🔍",
                "color": "#E3F2FD"
            },
            {
                "title": "Create Data-Element Specific Policies",
                "description": """
                <div style="padding: 10px; border-radius: 5px;">
                    <p>Create policies for specific data elements, categories, or sensitivity levels:</p>
                    <ul>
                        <li><span style="color: #1565C0; font-weight: bold;">Target Selection</span>: Choose whether the policy applies to a specific data element, category, or sensitivity level</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Configuration</span>: Set up policy-specific settings such as access permissions, masking rules, or retention periods</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Per-Element Settings</span>: Configure detailed settings for each data element to ensure appropriate protection</li>
                    </ul>
                    <p>This granular approach ensures that each piece of data is governed according to its specific requirements.</p>
                </div>
                """,
                "icon": "✏️",
                "color": "#E8F5E9"
            },
            {
                "title": "Organize Policies into Groups",
                "description": """
                <div style="padding: 10px; border-radius: 5px;">
                    <p>Group related policies together for easier management:</p>
                    <ul>
                        <li><span style="color: #1565C0; font-weight: bold;">Create Policy Groups</span>: Organize policies that serve a common purpose or apply to related data</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Add Multiple Policies</span>: Select multiple policies to add to a group in a single operation</li>
                        <li><span style="color: #1565C0; font-weight: bold;">View Group Contents</span>: Use the dropdown to see which policies are included in each group</li>
                    </ul>
                    <p>Policy groups simplify management and provide a foundation for context-based application.</p>
                </div>
                """,
                "icon": "📋",
                "color": "#FFF8E1"
            },
            {
                "title": "Define Context Overrides",
                "description": """
                <div style="padding: 10px; border-radius: 5px;">
                    <p>Create context-specific overrides to apply policies based on business context:</p>
                    <ul>
                        <li><span style="color: #1565C0; font-weight: bold;">Select Policy Group</span>: Choose which policy group to apply in a specific context</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Define Context</span>: Specify the purpose, role, region, or other context factors</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Set Priority</span>: Determine the priority of this override relative to others</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Set Effective Dates</span>: Specify when the override should take effect and expire</li>
                    </ul>
                    <p>Context overrides ensure that policies are applied appropriately based on legitimate business purposes.</p>
                </div>
                """,
                "icon": "🔄",
                "color": "#F3E5F5"
            },
            {
                "title": "Implementation and Enforcement",
                "description": """
                <div style="padding: 10px; border-radius: 5px;">
                    <p>The final step is implementing and enforcing the policies:</p>
                    <ul>
                        <li><span style="color: #1565C0; font-weight: bold;">Generate DDL</span>: Convert policies into database-specific code (e.g., Snowflake DDL)</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Deploy Policies</span>: Apply the policies to your data infrastructure</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Monitor Compliance</span>: Track policy application and effectiveness</li>
                        <li><span style="color: #1565C0; font-weight: bold;">Iterate and Improve</span>: Refine policies based on feedback and changing requirements</li>
                    </ul>
                    <p>This ensures that your governance rules are effectively protecting your data in production environments.</p>
                </div>
                """,
                "icon": "🚀",
                "color": "#FFEBEE"
            }
        ]
        
        # Display steps in an interactive way with custom styling
        for i, step in enumerate(steps):
            with st.expander(f"{step['icon']} Step {i+1}: {step['title']}", expanded=i==0):
                st.markdown(f"""
                <div style="background-color: {step['color']}; border-radius: 10px; padding: 15px; border-left: 5px solid #1565C0;">
                    {step['description']}
                </div>
                """, unsafe_allow_html=True)
        
        # Key components and benefits with visual header
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 30px 0 20px 0;">
            <div style="background-color: #1565C0; color: white; padding: 10px; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                <span style="font-size: 20px;">🔑</span>
            </div>
            <h3 style="margin: 0; color: #1565C0;">Key Components and Benefits</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Components and benefits in styled cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; height: 100%; border-left: 5px solid #1565C0;">
                <h4 style="color: #1565C0; margin-top: 0;">Key Components</h4>
                <ul style="margin-bottom: 0;">
                    <li><span style="font-weight: bold;">Policy Types</span>: Define categories of policies (Access Control, Security, Retention)</li>
                    <li><span style="font-weight: bold;">Policies</span>: Create specific rules targeting data elements, categories, or sensitivity levels</li>
                    <li><span style="font-weight: bold;">Policy Groups</span>: Organize related policies for easier management</li>
                    <li><span style="font-weight: bold;">Context Overrides</span>: Apply different policies based on purpose, role, or region</li>
                    <li><span style="font-weight: bold;">Per-Element Settings</span>: Configure specific protections for each data element</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; height: 100%; border-left: 5px solid #2E7D32;">
                <h4 style="color: #2E7D32; margin-top: 0;">Benefits</h4>
                <ul style="margin-bottom: 0;">
                    <li><span style="font-weight: bold;">Consistent Governance</span>: Apply standardized rules across your data landscape</li>
                    <li><span style="font-weight: bold;">Purpose-Based Access</span>: Ensure data is only used for legitimate purposes</li>
                    <li><span style="font-weight: bold;">Compliance</span>: Meet regulatory requirements for data protection</li>
                    <li><span style="font-weight: bold;">Flexibility</span>: Adapt policies to different contexts and requirements</li>
                    <li><span style="font-weight: bold;">Granular Control</span>: Apply appropriate protections based on data sensitivity</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Best practices with visual header
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 30px 0 20px 0;">
            <div style="background-color: #1565C0; color: white; padding: 10px; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                <span style="font-size: 20px;">⭐</span>
            </div>
            <h3 style="margin: 0; color: #1565C0;">Best Practices</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Best practices in a styled card
        st.markdown("""
        <div style="background-color: #FFF8E1; padding: 20px; border-radius: 10px; border-left: 5px solid #FF8F00;">
            <ol style="margin-bottom: 0;">
                <li><span style="font-weight: bold;">Start with Data Classification</span>: Understand your data elements and their sensitivity before creating policies</li>
                <li><span style="font-weight: bold;">Use Purpose-Based Roles</span>: Organize access around business purposes rather than individual roles</li>
                <li><span style="font-weight: bold;">Standardize Naming Conventions</span>: Use consistent naming for policies to improve maintainability</li>
                <li><span style="font-weight: bold;">Document Policy Decisions</span>: Keep track of why certain policy choices were made</li>
                <li><span style="font-weight: bold;">Regular Review</span>: Periodically review and update policies to ensure they remain effective</li>
                <li><span style="font-weight: bold;">Layer Your Defenses</span>: Use multiple policy types together for comprehensive protection</li>
                <li><span style="font-weight: bold;">Test Before Deployment</span>: Validate policies in a test environment before applying them to production</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation info
        st.markdown("""
        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; margin: 30px 0; text-align: center; border: 1px solid #1565C0;">
            <p style="margin: 0; color: #1565C0;"><i>Navigate through the tabs above to explore and implement each aspect of policy management.</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual diagram header
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 30px 0 20px 0;">
            <div style="background-color: #1565C0; color: white; padding: 10px; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                <span style="font-size: 20px;">📊</span>
            </div>
            <h3 style="margin: 0; color: #1565C0;">Policy Management Flow</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Simplified visual flow with styled cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("""
            <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; text-align: center; height: 100%; border-top: 4px solid #1565C0;">
                <div style="font-size: 24px; margin-bottom: 10px;">1️⃣</div>
                <div style="font-weight: bold; color: #1565C0;">Define Policy Types</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; text-align: center; height: 100%; border-top: 4px solid #2E7D32;">
                <div style="font-size: 24px; margin-bottom: 10px;">2️⃣</div>
                <div style="font-weight: bold; color: #2E7D32;">Create Policies</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: #FFF8E1; padding: 15px; border-radius: 10px; text-align: center; height: 100%; border-top: 4px solid #FF8F00;">
                <div style="font-size: 24px; margin-bottom: 10px;">3️⃣</div>
                <div style="font-weight: bold; color: #FF8F00;">Organize into Groups</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background-color: #F3E5F5; padding: 15px; border-radius: 10px; text-align: center; height: 100%; border-top: 4px solid #7B1FA2;">
                <div style="font-size: 24px; margin-bottom: 10px;">4️⃣</div>
                <div style="font-weight: bold; color: #7B1FA2;">Define Context Overrides</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div style="background-color: #FFEBEE; padding: 15px; border-radius: 10px; text-align: center; height: 100%; border-top: 4px solid #C62828;">
                <div style="font-size: 24px; margin-bottom: 10px;">5️⃣</div>
                <div style="font-weight: bold; color: #C62828;">Deploy & Monitor</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Flow arrows
        st.markdown("""
        <div style="text-align: center; margin: 10px 0 20px 0;">
            <span style="font-size: 24px; color: #1565C0;">➡️ ➡️ ➡️ ➡️</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Call to action
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-top: 30px; text-align: center; border: 1px solid #2E7D32;">
            <h4 style="color: #2E7D32; margin: 0;">Ready to start?</h4>
            <p style="margin: 10px 0 0 0;">Begin by exploring the Policy Types tab and then proceed through the journey step by step.</p>
        </div>
        """, unsafe_allow_html=True)

    
    def _render_policy_types(self):
        """Render the policy types section."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policy Types</h3>
        <p>Understand the different types of policies available in the system.</p>
        """, unsafe_allow_html=True)
        
        # Policy types
        policy_types = [
            {
                "name": "Access Control",
                "description": "Defines who can access what data and under what conditions",
                "schema": {
                    "type": "Access Control",
                    "read": "boolean",
                    "write": "boolean",
                    "share": "boolean"
                },
                "icon": "🔒"
            },
            {
                "name": "Security",
                "description": "Specifies security measures like encryption and masking",
                "schema": {
                    "encryption_required": "boolean",
                    "encryption_algorithm": "string (optional)",
                    "masking_required": "boolean",
                    "masking_format": "string (optional)",
                    "access_logging": "boolean"
                },
                "icon": "🛡️"
            },
            {
                "name": "Retention",
                "description": "Defines how long data should be kept and when it should be deleted",
                "schema": {
                    "retention_period": "string (e.g., '7 years')",
                    "retention_trigger": "string (e.g., 'creation_date', 'last_accessed')",
                    "retention_basis": "string (e.g., 'Legal Requirement')",
                    "exceptions": "string (optional)"
                },
                "icon": "⏱️"
            }
        ]
        
        # Display policy types in expandable sections
        for policy_type in policy_types:
            with st.expander(f"{policy_type['icon']} {policy_type['name']}", expanded=True):
                st.markdown(f"**Description**: {policy_type['description']}")
                st.markdown("**Schema**:")
                schema_df = pd.DataFrame(
                    [[k, v] for k, v in policy_type['schema'].items()],
                    columns=["Property", "Type"]
                )
                st.table(schema_df)
                
                # Example JSON
                st.markdown("**Example JSON**:")
                
                # Create realistic example JSON based on policy type
                if policy_type['name'] == "Access Control":
                    example_json = json.dumps({
                        "type": "Access Control",
                        "read": True,
                        "write": False,
                        "share": False,
                        "target": {
                            "type": "data_element",
                            "id": "DE12345",
                            "name": "Customer PII"
                        },
                        "purpose": "Marketing",
                        "effective_from": "2025-01-01"
                    }, indent=2)
                elif policy_type['name'] == "Security":
                    example_json = json.dumps({
                        "type": "Security",
                        "encryption_required": True,
                        "encryption_algorithm": "AES-256",
                        "masking_required": True,
                        "masking_format": "XXXX-XXXX-XXXX-####",
                        "access_logging": True,
                        "target": {
                            "type": "sensitivity_level",
                            "id": "SL789",
                            "name": "Highly Confidential"
                        },
                        "effective_from": "2025-01-01"
                    }, indent=2)
                elif policy_type['name'] == "Retention":
                    example_json = json.dumps({
                        "type": "Retention",
                        "retention_period": "7 years",
                        "retention_trigger": "creation_date",
                        "retention_basis": "Legal Requirement",
                        "exceptions": "Litigation hold may extend retention period",
                        "target": {
                            "type": "data_category",
                            "id": "DC456",
                            "name": "Financial Records"
                        },
                        "effective_from": "2025-01-01",
                        "effective_to": "2030-01-01"
                    }, indent=2)
                
                st.code(example_json, language="json")
    
    def _render_define_policies(self):
        """Render the policy definition section."""
        st.markdown("""
        <h3 style="color: #1565C0;">Define Policies</h3>
        <p>Create and manage policies of different types to protect your data assets.</p>
        """, unsafe_allow_html=True)
        
        # Policy creation form
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                policy_name = st.text_input("Policy Name")
                effective_from = st.date_input("Effective From", value=datetime.now().date())
            
            with col2:
                policy_description = st.text_area("Description (Optional)")
                effective_to = st.date_input("Effective To (Optional)", value=None)
            
            # Get policy types for dropdown
            policy_types = self.policy_definition_repository.get_all_policy_types() if self.policy_definition_repository else []
            
            if not policy_types:
                st.warning("No policy types available. Please define policy types first.")
                return
                
            policy_type_options = {pt["id"]: pt["name"] for pt in policy_types}
            
            # Policy type selection
            selected_policy_type_id = st.selectbox(
                "Select Policy Type",
                options=list(policy_type_options.keys()),
                format_func=lambda x: policy_type_options.get(x, "Unknown")
            )
            
            policy_type_name = policy_type_options.get(selected_policy_type_id)
            
            # Update policy name based on policy type
            if not policy_name and policy_type_name:
                policy_name = f"{policy_type_name} Policy"
            
            # Target selection tabs
            target_tab = st.radio(
                "Target Type",
                ["Data Element", "Data Category", "Sensitivity Level"],
                horizontal=True
            )
            
            # Target selection based on tab
            selected_targets = []
            selected_target_names = []
            
            if target_tab == "Data Element":
                data_elements = self.glossary_repository.get_data_elements() if self.glossary_repository else []
                
                if not data_elements:
                    st.warning("No data elements available. Please define data elements first.")
                else:
                    data_element_options = {de["id"]: de["name"] for de in data_elements}
                    
                    # Multi-select for data elements
                    selected_target_ids = st.multiselect(
                        "Select Data Elements",
                        options=list(data_element_options.keys()),
                        format_func=lambda x: data_element_options.get(x, "Unknown")
                    )
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "data_element",
                            "id": target_id,
                            "name": data_element_options.get(target_id)
                        })
                        selected_target_names.append(data_element_options.get(target_id))
            
            elif target_tab == "Data Category":
                data_categories = self.glossary_repository.get_data_categories() if self.glossary_repository else []
                
                if not data_categories:
                    st.warning("No data categories available. Please define data categories first.")
                else:
                    data_category_options = {dc["id"]: dc["name"] for dc in data_categories}
                    
                    # Multi-select for data categories
                    selected_target_ids = st.multiselect(
                        "Select Data Categories",
                        options=list(data_category_options.keys()),
                        format_func=lambda x: data_category_options.get(x, "Unknown")
                    )
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "data_category",
                            "id": target_id,
                            "name": data_category_options.get(target_id)
                        })
                        selected_target_names.append(data_category_options.get(target_id))
            
            elif target_tab == "Sensitivity Level":
                sensitivity_levels = self.glossary_repository.get_sensitivities() if self.glossary_repository else []
                
                if not sensitivity_levels:
                    st.warning("No sensitivity levels available. Please define sensitivity levels first.")
                else:
                    sensitivity_options = {sl["id"]: sl["name"] for sl in sensitivity_levels}
                    
                    # Multi-select for sensitivity levels
                    selected_target_ids = st.multiselect(
                        "Select Sensitivity Levels",
                        options=list(sensitivity_options.keys()),
                        format_func=lambda x: sensitivity_options.get(x, "Unknown")
                    )
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "sensitivity_level",
                            "id": target_id,
                            "name": sensitivity_options.get(target_id)
                        })
                        selected_target_names.append(sensitivity_options.get(target_id))
            
            # Update policy name based on selected targets
            if selected_target_names and (not policy_name or policy_name == f"{policy_type_name} Policy"):
                if len(selected_target_names) == 1:
                    policy_name = f"{policy_type_name} Policy for {selected_target_names[0]}"
                else:
                    target_type = target_tab.replace(" Level", "")
                    policy_name = f"{policy_type_name} Policy for {len(selected_target_names)} {target_type}s"
            
            # Dynamic policy configuration based on selected policy type
            policy_config = {}
            
            if policy_type_name == "Access Control" and selected_targets:
                st.write("Set specific permissions for each selected target:")
                
                # Create a dictionary to store permissions for each target
                target_permissions = {}
                
                # Create a table-like interface for setting permissions
                for i, target in enumerate(selected_targets):
                    st.markdown(f"**{i+1}. {target['name']} ({target['type']}):**")
                    
                    cols = st.columns([3, 2, 2, 2])
                    with cols[1]:
                        read = st.checkbox("Read", value=True, key=f"read_{target['id']}", help="Allow reading/viewing the data")
                    with cols[2]:
                        write = st.checkbox("Write", value=False, key=f"write_{target['id']}", help="Allow modifying the data")
                    with cols[3]:
                        share = st.checkbox("Share", value=False, key=f"share_{target['id']}", help="Allow sharing the data with others")
                    
                    # Store permissions for this target
                    target_permissions[target['id']] = {
                        "read": read,
                        "write": write,
                        "share": share
                    }
                    
                    # Add a separator between targets
                    st.markdown("---")
                
                # Update the policy config to include per-target permissions
                policy_config = {
                    "type": "Access Control",
                    "target_permissions": target_permissions
                }
            
            elif policy_type_name == "Security":
                # Initialize default security settings
                global_encryption_required = True
                global_masking_required = False
                access_logging = True
                global_encryption_algorithm = "AES-256"
                global_masking_format = "XXXX-XXXX-XXXX-####"
                
                # Define appropriate masking formats for different data element types
                masking_formats = {
                    "Email Address": "****@****.com",
                    "Phone Number": "(XXX) XXX-####",
                    "Social Security Number": "XXX-XX-####",
                    "Credit Card Number": "XXXX-XXXX-XXXX-####",
                    "Date of Birth": "XXXX-XX-DD",
                    "Address": "*** ****** ****",
                    "Name": "**** *****",
                    "IP Address": "XXX.XXX.XXX.XXX",
                    "Bank Account Number": "XXXXXXXX####"
                }
                
                # Initialize target_security dictionary to store per-target security settings
                policy_config["target_security"] = {}
                
                # Per-target security settings
                if selected_targets:
                    st.markdown("---")
                    st.subheader("Security Settings")
                    st.write("Configure security settings for each selected target.")
                    
                    # For each target, create an expander with security settings
                    for target in selected_targets:
                        with st.expander(f"Security settings for {target['name']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                target_encryption = st.checkbox(
                                    "Encryption Required", 
                                    value=global_encryption_required,
                                    key=f"encrypt_{target['id']}"
                                )
                                
                                target_masking = st.checkbox(
                                    "Masking Required", 
                                    value=global_masking_required,
                                    key=f"mask_{target['id']}"
                                )
                            
                            # Encryption algorithm if encryption is required
                            if target_encryption:
                                encryption_algo = st.text_input(
                                    "Encryption Algorithm", 
                                    value=global_encryption_algorithm or "AES-256",
                                    key=f"algo_{target['id']}"
                                )
                            else:
                                encryption_algo = None
                            
                            # Masking format if masking is required
                            if target_masking:
                                # Use data element-specific masking format if available
                                default_format = masking_formats.get(target['name'], global_masking_format)
                                masking_format = st.text_input(
                                    "Masking Format", 
                                    value=default_format,
                                    key=f"format_{target['id']}"
                                )
                            else:
                                masking_format = None
                            
                            # Store the target's security settings
                            policy_config["target_security"][target["id"]] = {
                                "encryption_required": target_encryption,
                                "encryption_algorithm": encryption_algo,
                                "masking_required": target_masking,
                                "masking_format": masking_format
                            }
                
                # Global settings (applied to targets without specific settings)
                policy_config.update({
                    "encryption_required": global_encryption_required,
                    "encryption_algorithm": global_encryption_algorithm,
                    "masking_required": global_masking_required,
                    "masking_format": global_masking_format,
                    "access_logging": access_logging
                })
            
            elif policy_type_name == "Retention":
                # Initialize default retention settings
                global_retention_period = "7 years"
                global_retention_basis = "Legal Requirement"
                global_retention_trigger = "creation_date"
                global_exceptions = ""
                
                # Initialize target_retention dictionary to store per-target retention settings
                policy_config = {"target_retention": {}}
                
                # Per-target retention settings
                if selected_targets:
                    st.markdown("---")
                    st.subheader("Retention Settings")
                    st.write("Configure retention settings for each selected target.")
                    
                    # For each target, create an expander with retention settings
                    for target in selected_targets:
                        with st.expander(f"Retention settings for {target['name']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                target_retention_period = st.text_input(
                                    "Retention Period", 
                                    value=global_retention_period,
                                    key=f"period_{target['id']}"
                                )
                                
                                target_retention_basis = st.text_input(
                                    "Retention Basis", 
                                    value=global_retention_basis,
                                    key=f"basis_{target['id']}"
                                )
                            
                            with col2:
                                target_retention_trigger = st.selectbox(
                                    "Retention Trigger",
                                    options=["creation_date", "last_modified", "last_accessed", "custom_event"],
                                    key=f"trigger_{target['id']}"
                                )
                            
                            target_exceptions = st.text_area(
                                "Exceptions (Optional)", 
                                value=global_exceptions,
                                key=f"exceptions_{target['id']}"
                            )
                            
                            # Store the target's retention settings
                            policy_config["target_retention"][target["id"]] = {
                                "retention_period": target_retention_period,
                                "retention_trigger": target_retention_trigger,
                                "retention_basis": target_retention_basis,
                                "exceptions": target_exceptions
                            }
                
                # Global settings (applied to targets without specific settings)
                policy_config.update({
                    "retention_period": global_retention_period,
                    "retention_trigger": global_retention_trigger,
                    "retention_basis": global_retention_basis,
                    "exceptions": global_exceptions
                })
            
            # Preview policy before submission
            if selected_targets:
                with st.expander("Preview Policy", expanded=True):
                    
                    # Optimized JSON preview
                    st.subheader("Policy Preview")
                    
                    # Create a more concise policy representation
                    if policy_type_name == "Access Control":
                        # Determine the target type (all targets should be of the same type)
                        if selected_targets:
                            target_type = selected_targets[0]['type']
                        else:
                            target_type = "unknown"
                            
                        # For Access Control, show a simplified version with target permissions
                        optimized_json = {
                            "name": policy_name,
                            "type": policy_type_name,
                            "target_type": target_type,  # Specify target type once
                            "effective_dates": {
                                "from": str(effective_from),
                                "to": str(effective_to) if effective_to else "indefinite"
                            }
                        }
                        
                        # Add description only if provided
                        if policy_description and policy_description.strip():
                            optimized_json["description"] = policy_description
                        
                        # Add target permissions in a more readable format
                        target_permissions = {}
                        for target in selected_targets:
                            perms = policy_config.get("target_permissions", {}).get(target['id'], {})
                            # Only include ID and permissions, not type (since it's specified at the top level)
                            target_permissions[target['name']] = {
                                "id": target['id'],
                                "read": perms.get("read", False),
                                "write": perms.get("write", False),
                                "share": perms.get("share", False)
                            }
                        
                        optimized_json["permissions"] = target_permissions
                    elif policy_type_name == "Security" or policy_type_name == "Retention":
                        # Determine the target type (all targets should be of the same type)
                        if selected_targets:
                            target_type = selected_targets[0]['type']
                        else:
                            target_type = "unknown"
                            
                        # For Security/Retention policies, show a simplified version with target-specific settings
                        optimized_json = {
                            "name": policy_name,
                            "type": policy_type_name,
                            "target_type": target_type,  # Specify target type once
                            "effective_dates": {
                                "from": str(effective_from),
                                "to": str(effective_to) if effective_to else "indefinite"
                            }
                        }
                        
                        # Add description only if provided
                        if policy_description and policy_description.strip():
                            optimized_json["description"] = policy_description
                        
                        if policy_type_name == "Security":
                            # Add security settings in a more readable format
                            security_settings = {}
                            for target in selected_targets:
                                target_security = policy_config.get("target_security", {}).get(target['id'], {})
                                
                                # Create attribute-based security settings
                                target_settings = {
                                    "id": target['id'],
                                    "encryption": {
                                        "required": target_security.get("encryption_required", False),
                                        "algorithm": target_security.get("encryption_algorithm") if target_security.get("encryption_required", False) else None
                                    },
                                    "masking": {
                                        "required": target_security.get("masking_required", False),
                                        "format": target_security.get("masking_format") if target_security.get("masking_required", False) else None
                                    }
                                }
                                
                                security_settings[target['name']] = target_settings
                            
                            optimized_json["security_settings"] = security_settings
                        elif policy_type_name == "Retention":
                            # Add retention settings in a more readable format
                            retention_settings = {}
                            for target in selected_targets:
                                target_retention = policy_config.get("target_retention", {}).get(target['id'], {})
                                
                                # Create attribute-based retention settings
                                target_settings = {
                                    "id": target['id'],
                                    "period": target_retention.get("retention_period", policy_config.get("retention_period")),
                                    "basis": target_retention.get("retention_basis", policy_config.get("retention_basis")),
                                    "trigger": target_retention.get("retention_trigger", policy_config.get("retention_trigger")),
                                    "exceptions": target_retention.get("exceptions", policy_config.get("exceptions"))
                                }
                                
                                retention_settings[target['name']] = target_settings
                            
                            optimized_json["retention_settings"] = retention_settings
                    else:
                        # Determine the target type (all targets should be of the same type)
                        if selected_targets:
                            target_type = selected_targets[0]['type']
                        else:
                            target_type = "unknown"
                            
                        # For other policy types, use a similar structure but with the specific config
                        optimized_json = {
                            "name": policy_name,
                            "type": policy_type_name,
                            "target_type": target_type,  # Specify target type once
                            "targets": [
                                {
                                    "id": t["id"],
                                    "name": t["name"]
                                    # No type field here since it's specified at the top level
                                } for t in selected_targets
                            ],
                            "effective_dates": {
                                "from": str(effective_from),
                                "to": str(effective_to) if effective_to else "indefinite"
                            },
                            "config": policy_config
                        }
                        
                        # Add description only if provided
                        if policy_description and policy_description.strip():
                            optimized_json["description"] = policy_description
                    
                    # Display the optimized JSON
                    st.json(optimized_json)
            else:
                st.warning("Please select at least one target to create a policy.")
            
            # Submit button
            if st.button("Create Policy", type="primary"):
                # Validate inputs
                validation_errors = []
                
                if not policy_name or policy_name.strip() == "":
                    validation_errors.append("Policy name is required.")
                
                if not selected_targets:
                    validation_errors.append("At least one data element, category, or sensitivity level must be selected.")
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(error)
                else:
                    created_policies = []
                    failed_policies = []
                    
                    # Create a policy for each target
                    for target in selected_targets:
                        try:
                            # Determine target type and ID
                            data_element_id = None
                            data_category_id = None
                            sensitivity_id = None
                            
                            if target['type'] == 'data_element':
                                data_element_id = target['id']
                            elif target['type'] == 'data_category':
                                data_category_id = target['id']
                            elif target['type'] == 'sensitivity_level':
                                sensitivity_id = target['id']
                                
                            # Convert dates to string format
                            effective_from_str = effective_from.strftime('%Y-%m-%d') if effective_from else None
                            effective_to_str = effective_to.strftime('%Y-%m-%d') if effective_to else None
                                
                            # Generate a specific policy name for this target
                            target_policy_name = policy_name
                            
                            # If we're creating multiple policies, append the target name to make each unique
                            if len(selected_targets) > 1:
                                # Different naming patterns based on policy type
                                if policy_type_name == "Access Control":
                                    # For Access Control, include the permissions in the name
                                    perms = policy_config.get("target_permissions", {}).get(target['id'], {})
                                    operations = []
                                    if perms.get("read", False):
                                        operations.append("Read")
                                    if perms.get("write", False):
                                        operations.append("Write")
                                    if perms.get("share", False):
                                        operations.append("Share")
                                    
                                    operations_str = "/".join(operations) if operations else "No Access"
                                    target_policy_name = f"{policy_name} - {target['name']} ({operations_str})"
                                elif policy_type_name == "Security":
                                    # For Security, include the security measures in the name
                                    security_settings = policy_config.get("target_security", {}).get(target['id'], {})
                                    measures = []
                                    if security_settings.get("encryption_required", False):
                                        measures.append("Encrypted")
                                    if security_settings.get("masking_required", False):
                                        measures.append("Masked")
                                    
                                    measures_str = "/".join(measures) if measures else "No Security"
                                    target_policy_name = f"{policy_name} - {target['name']} ({measures_str})"
                                elif policy_type_name == "Retention":
                                    # For Retention, include the retention period in the name
                                    retention_settings = policy_config.get("target_retention", {}).get(target['id'], {})
                                    retention_period = retention_settings.get("retention_period", policy_config.get("retention_period", "7 years"))
                                    target_policy_name = f"{policy_name} - {target['name']} ({retention_period})"
                                else:
                                    # For other policy types, just append the target name
                                    target_policy_name = f"{policy_name} - {target['name']}"
                            
                            # Create policy in repository
                            policy_id = self.policy_definition_repository.create_policy(
                                policy_type_id=selected_policy_type_id,
                                data_element_id=data_element_id,
                                data_category_id=data_category_id,
                                sensitivity_id=sensitivity_id,
                                policy_config=policy_config,
                                effective_from=effective_from_str,
                                effective_to=effective_to_str,
                                name=target_policy_name
                            )
                                
                            if policy_id:
                                created_policies.append({
                                    'id': policy_id,
                                    'target_name': target['name'],
                                    'target_type': target['type']
                                })
                            else:
                                failed_policies.append({
                                    'target_name': target['name'],
                                    'target_type': target['type']
                                })
                        except Exception as e:
                            st.error(f"Error creating policy for {target['name']}: {str(e)}")
                            failed_policies.append({
                                'target_name': target['name'],
                                'target_type': target['type'],
                                'error': str(e)
                            })
                    
                    # Show results
                    if created_policies:
                        st.success(f"Successfully created {len(created_policies)} policies!")
                        
                        # Show created policies in a table
                        created_df = pd.DataFrame(
                            [[p['id'], p['target_name'], p['target_type']] for p in created_policies],
                            columns=["Policy ID", "Target Name", "Target Type"]
                        )
                        st.dataframe(created_df, use_container_width=True)
                    
                    if failed_policies:
                        st.error(f"Failed to create {len(failed_policies)} policies.")
                        for failed in failed_policies:
                            st.write(f"- {failed['target_name']} ({failed['target_type']}): {failed.get('error', 'Unknown error')}")
                    
                    # Refresh the policy list
                    st.rerun()
        
        # Existing policies section
        st.markdown("---")
        st.subheader("Existing Policies")
        
        # Get policies
        policies = self.policy_definition_repository.get_all_policies() if self.policy_definition_repository else []
        
        if not policies:
            st.info("No policies defined yet.")
        else:
            # Display policies as expandable JSON objects
            for i, policy in enumerate(policies):
                # Get policy name (use the dedicated name field if available)
                policy_name = policy.get("name")
                
                # Determine target name and type
                target_name = policy.get("data_element_name") or policy.get("data_category_name") or policy.get("sensitivity_name") or "Global"
                target_type = "data_element" if policy.get("data_element_name") else \
                             "data_category" if policy.get("data_category_name") else \
                             "sensitivity_level" if policy.get("sensitivity_name") else "global"
                
                # Parse policy config to extract read/write/share settings
                policy_config = {}
                if policy.get("policy_config"):
                    try:
                        if isinstance(policy.get("policy_config"), str):
                            policy_config = json.loads(policy.get("policy_config"))
                        else:
                            policy_config = policy.get("policy_config")
                    except:
                        policy_config = {}
                
                # Create a clean policy representation
                policy_json = {
                    "id": policy.get("id"),
                    "name": policy.get("name", "Unknown"),
                    "type": policy.get("policy_type_name", "Unknown"),
                    "target_type": target_type,
                    "target": {
                        "id": policy.get("data_element_id") or policy.get("data_category_id") or policy.get("sensitivity_id"),
                        "name": target_name
                    },
                    "effective_dates": {
                        "from": str(policy.get("effective_from", "Immediately")),
                        "to": str(policy.get("effective_to", "Indefinite"))
                    }
                }
                
                # Add permissions for Access Control policies
                if policy.get("policy_type_name") == "Access Control":
                    # Extract permissions from policy config
                    permissions = {
                        "read": policy_config.get("read", False),
                        "write": policy_config.get("write", False),
                        "share": policy_config.get("share", False)
                    }
                    
                    # If using target_permissions structure
                    target_id = policy.get("data_element_id") or policy.get("data_category_id") or policy.get("sensitivity_id")
                    if policy_config.get("target_permissions") and policy_config["target_permissions"].get(target_id):
                        target_perms = policy_config["target_permissions"].get(target_id)
                        permissions = {
                            "read": target_perms.get("read", False),
                            "write": target_perms.get("write", False),
                            "share": target_perms.get("share", False)
                        }
                    
                    policy_json["permissions"] = permissions
                # Add security settings for Security policies
                elif policy.get("policy_type_name") == "Security":
                    # Extract global security settings
                    security_settings = {
                        "encryption_required": policy_config.get("encryption_required", False),
                        "encryption_algorithm": policy_config.get("encryption_algorithm"),
                        "masking_required": policy_config.get("masking_required", False),
                        "masking_format": policy_config.get("masking_format"),
                        "access_logging": policy_config.get("access_logging", False)
                    }
                    
                    # If using target_security structure
                    target_id = policy.get("data_element_id") or policy.get("data_category_id") or policy.get("sensitivity_id")
                    if policy_config.get("target_security") and policy_config["target_security"].get(target_id):
                        target_security = policy_config["target_security"].get(target_id)
                        security_settings = {
                            "encryption_required": target_security.get("encryption_required", False),
                            "encryption_algorithm": target_security.get("encryption_algorithm"),
                            "masking_required": target_security.get("masking_required", False),
                            "masking_format": target_security.get("masking_format"),
                            "access_logging": policy_config.get("access_logging", False)  # Global setting
                        }
                    
                    policy_json["security_settings"] = security_settings
                else:
                    # For other policy types, include the full config
                    policy_json["config"] = policy_config
                
                # Display the policy with an expander
                with st.expander(f"{policy_json['name']} ({target_name})", expanded=i==0):
                    st.json(policy_json)
    
    def _render_faq(self):
        """Render the FAQ section with common scenarios and solutions."""
        # Header with custom styling
        st.markdown("""
        <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #1565C0;">
            <h2 style="color: #1565C0; text-align: center; margin: 0;">Frequently Asked Questions</h2>
            <p style="color: #1565C0; text-align: center; margin-top: 10px;">Common scenarios and how to implement them</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Introduction
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #1565C0; margin-bottom: 20px;">
            <p style="margin: 0;">This FAQ provides step-by-step guidance for common policy management scenarios. Each scenario includes a visual walkthrough of the necessary steps to accomplish specific tasks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Define scenarios
        scenarios = [
            {
                "title": "Overriding Policies for Specific Data Elements",
                "question": "I have a default policy group assigned to a purpose. How do I override policies for a few specific data elements?",
                "description": """
                <p>This scenario demonstrates how to create exceptions to your default policies for specific data elements while maintaining the default policies for everything else.</p>
                
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p style="margin-top: 0; font-weight: bold; color: #2E7D32;">Use Case Example:</p>
                    <p>You have a default security policy group for the "Marketing" purpose that applies standard masking to all PII. However, you need stricter masking for email addresses and phone numbers when used for this purpose.</p>
                </div>
                """,
                "steps": [
                    {
                        "title": "Create Specific Policies for the Data Elements",
                        "content": """
                        <ol>
                            <li>Navigate to the <span style="color: #1565C0; font-weight: bold;">Define Policies</span> tab</li>
                            <li>Select the appropriate policy type (e.g., <span style="color: #1565C0; font-weight: bold;">Security</span>)</li>
                            <li>Choose <span style="color: #1565C0; font-weight: bold;">Data Element</span> as the target type</li>
                            <li>Select the specific data elements you want to override (e.g., <span style="color: #1565C0; font-weight: bold;">Email Address</span> and <span style="color: #1565C0; font-weight: bold;">Phone Number</span>)</li>
                            <li>Configure stricter masking settings for these elements</li>
                            <li>Name these policies descriptively (e.g., <span style="color: #1565C0; font-weight: bold;">Marketing - Strict Email Masking</span>)</li>
                            <li>Save the new policies</li>
                        </ol>
                        """,
                        "icon": "✏️"
                    },
                    {
                        "title": "Create a New Policy Group for the Overrides",
                        "content": """
                        <ol>
                            <li>Go to the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Create New Policy Group</span></li>
                            <li>Name it something like <span style="color: #1565C0; font-weight: bold;">Marketing - PII Overrides</span></li>
                            <li>Add a description explaining these are overrides for specific data elements</li>
                            <li>Set the version and mark it as active</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Group</span></li>
                        </ol>
                        """,
                        "icon": "📋"
                    },
                    {
                        "title": "Add Your Override Policies to the New Group",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Manage Policy Groups</span> section, find your newly created override group</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Add Policies to this Group</span></li>
                            <li>Use the multi-select to choose your data element-specific policies</li>
                            <li>Optionally specify a target system if needed</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Add Policies</span></li>
                        </ol>
                        """,
                        "icon": "➕"
                    },
                    {
                        "title": "Create a Context Override for the Specific Purpose",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab, find the <span style="color: #1565C0; font-weight: bold;">Create New Override</span> expander</li>
                            <li>Select your override policy group from the dropdown</li>
                            <li>Select the <span style="color: #1565C0; font-weight: bold;">Marketing</span> purpose</li>
                            <li>Leave the role and region fields empty (unless you want to further restrict the override)</li>
                            <li>Set a <span style="color: #1565C0; font-weight: bold;">higher priority number</span> than your default policy group (higher numbers take precedence)</li>
                            <li>Set effective dates if the override should be temporary</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Override</span></li>
                        </ol>
                        """,
                        "icon": "🔄"
                    }
                ],
                "result": """
                <div style="background-color: #FFF8E1; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 5px solid #FF8F00;">
                    <p style="margin-top: 0; font-weight: bold; color: #FF8F00;">How It Works:</p>
                    <p>When the system evaluates which policies to apply:</p>
                    <ol>
                        <li>It identifies all context policy groups that match the current purpose (Marketing)</li>
                        <li>It selects the one with the highest priority (your override group)</li>
                        <li>For Email Address and Phone Number, it applies the stricter masking policies</li>
                        <li>For all other data elements, it falls back to the policies in your default Marketing policy group</li>
                    </ol>
                    <p>This approach allows you to maintain default policies while creating exceptions for specific data elements that need different treatment.</p>
                </div>
                """,
                "color": "#E3F2FD"
            },
            {
                "title": "Creating Role-Based Policy Variations",
                "question": "How do I apply different policies based on user roles?",
                "description": """
                <p>This scenario shows how to create role-specific policy variations that override your default policies when accessed by specific user roles.</p>
                
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p style="margin-top: 0; font-weight: bold; color: #2E7D32;">Use Case Example:</p>
                    <p>You have standard access control policies for customer data, but you want to provide expanded access for Customer Support representatives while maintaining stricter controls for everyone else.</p>
                </div>
                """,
                "steps": [
                    {
                        "title": "Create Role-Specific Policies",
                        "content": """
                        <ol>
                            <li>Navigate to the <span style="color: #1565C0; font-weight: bold;">Define Policies</span> tab</li>
                            <li>Select <span style="color: #1565C0; font-weight: bold;">Access Control</span> as the policy type</li>
                            <li>Create policies with expanded access permissions for customer data</li>
                            <li>Name these policies descriptively (e.g., <span style="color: #1565C0; font-weight: bold;">Customer Support - Enhanced Access</span>)</li>
                            <li>Save the new policies</li>
                        </ol>
                        """,
                        "icon": "✏️"
                    },
                    {
                        "title": "Create a Policy Group for Support Staff",
                        "content": """
                        <ol>
                            <li>Go to the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Create New Policy Group</span></li>
                            <li>Name it <span style="color: #1565C0; font-weight: bold;">Customer Support Access</span></li>
                            <li>Add a description explaining this is for support staff</li>
                            <li>Set the version and mark it as active</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Group</span></li>
                        </ol>
                        """,
                        "icon": "📋"
                    },
                    {
                        "title": "Add Policies to the Support Group",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Manage Policy Groups</span> section, find your Customer Support group</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Add Policies to this Group</span></li>
                            <li>Select all the enhanced access policies you created</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Add Policies</span></li>
                        </ol>
                        """,
                        "icon": "➕"
                    },
                    {
                        "title": "Create a Role-Based Context Override",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab, find the <span style="color: #1565C0; font-weight: bold;">Create New Override</span> expander</li>
                            <li>Select your Customer Support policy group</li>
                            <li>Select the appropriate purpose (e.g., <span style="color: #1565C0; font-weight: bold;">Customer Service</span>)</li>
                            <li>Select <span style="color: #1565C0; font-weight: bold;">Customer Support</span> from the role dropdown</li>
                            <li>Set a high priority to ensure it overrides default policies</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Override</span></li>
                        </ol>
                        """,
                        "icon": "🔄"
                    }
                ],
                "result": """
                <div style="background-color: #FFF8E1; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 5px solid #FF8F00;">
                    <p style="margin-top: 0; font-weight: bold; color: #FF8F00;">How It Works:</p>
                    <p>When a user accesses the system:</p>
                    <ol>
                        <li>The system identifies their role (Customer Support)</li>
                        <li>It finds context policy groups that match both the purpose and role</li>
                        <li>It applies the enhanced access policies for Customer Support staff</li>
                        <li>Other users with different roles will still get the default, more restrictive policies</li>
                    </ol>
                    <p>This role-based approach ensures that users only get the access they need to perform their specific job functions.</p>
                </div>
                """,
                "color": "#F3E5F5"
            },
            {
                "title": "Applying Region-Specific Policies",
                "question": "How do I implement different policies for different geographic regions?",
                "description": """
                <p>This scenario shows how to create region-specific policy variations to comply with different regulatory requirements across geographic regions.</p>
                
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p style="margin-top: 0; font-weight: bold; color: #2E7D32;">Use Case Example:</p>
                    <p>You need to apply stricter data retention policies for users in the European Union to comply with GDPR, while maintaining different retention periods for users in other regions.</p>
                </div>
                """,
                "steps": [
                    {
                        "title": "Create Region-Specific Policies",
                        "content": """
                        <ol>
                            <li>Navigate to the <span style="color: #1565C0; font-weight: bold;">Define Policies</span> tab</li>
                            <li>Select <span style="color: #1565C0; font-weight: bold;">Retention</span> as the policy type</li>
                            <li>Create policies with the specific retention periods required for EU data</li>
                            <li>Name these policies descriptively (e.g., <span style="color: #1565C0; font-weight: bold;">GDPR Compliant Retention</span>)</li>
                            <li>Save the new policies</li>
                        </ol>
                        """,
                        "icon": "✏️"
                    },
                    {
                        "title": "Create a Policy Group for EU Compliance",
                        "content": """
                        <ol>
                            <li>Go to the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Create New Policy Group</span></li>
                            <li>Name it <span style="color: #1565C0; font-weight: bold;">EU GDPR Compliance</span></li>
                            <li>Add a description explaining the regional requirements</li>
                            <li>Set the version and mark it as active</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Group</span></li>
                        </ol>
                        """,
                        "icon": "📋"
                    },
                    {
                        "title": "Add Policies to the EU Group",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Manage Policy Groups</span> section, find your EU GDPR group</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Add Policies to this Group</span></li>
                            <li>Select all the GDPR-compliant policies you created</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Add Policies</span></li>
                        </ol>
                        """,
                        "icon": "➕"
                    },
                    {
                        "title": "Create a Region-Based Context Override",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab, find the <span style="color: #1565C0; font-weight: bold;">Create New Override</span> expander</li>
                            <li>Select your EU GDPR policy group</li>
                            <li>Select the appropriate purposes (or leave empty to apply to all purposes)</li>
                            <li>Select <span style="color: #1565C0; font-weight: bold;">European Union</span> from the region dropdown</li>
                            <li>Set a high priority to ensure it overrides default policies</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Override</span></li>
                        </ol>
                        """,
                        "icon": "🔄"
                    }
                ],
                "result": """
                <div style="background-color: #FFF8E1; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 5px solid #FF8F00;">
                    <p style="margin-top: 0; font-weight: bold; color: #FF8F00;">How It Works:</p>
                    <p>When data is processed:</p>
                    <ol>
                        <li>The system identifies the geographic region of the data subject</li>
                        <li>For EU data subjects, it applies the stricter GDPR-compliant retention policies</li>
                        <li>For data subjects in other regions, it applies the standard retention policies</li>
                        <li>This ensures compliance with regional regulations without over-restricting data in regions with different requirements</li>
                    </ol>
                    <p>This region-based approach allows you to maintain regulatory compliance across different jurisdictions while optimizing data usage where permitted.</p>
                </div>
                """,
                "color": "#E0F7FA"
            },
            {
                "title": "Implementing Time-Based Policy Changes",
                "question": "How do I schedule policy changes to take effect at a specific time?",
                "description": """
                <p>This scenario demonstrates how to schedule policy changes to automatically take effect at a specific date and time, such as for a new regulatory requirement or seasonal business change.</p>
                
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p style="margin-top: 0; font-weight: bold; color: #2E7D32;">Use Case Example:</p>
                    <p>A new data protection regulation will come into effect on January 1, 2026, requiring stricter retention policies. You want to prepare these policies in advance and have them automatically activate on the effective date.</p>
                </div>
                """,
                "steps": [
                    {
                        "title": "Create the New Compliant Policies",
                        "content": """
                        <ol>
                            <li>Navigate to the <span style="color: #1565C0; font-weight: bold;">Define Policies</span> tab</li>
                            <li>Select <span style="color: #1565C0; font-weight: bold;">Retention</span> as the policy type</li>
                            <li>Create policies that comply with the new regulation</li>
                            <li>Name these policies to indicate they're for the new regulation</li>
                            <li>Save the new policies</li>
                        </ol>
                        """,
                        "icon": "✏️"
                    },
                    {
                        "title": "Create a Policy Group for the New Regulation",
                        "content": """
                        <ol>
                            <li>Go to the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Create New Policy Group</span></li>
                            <li>Name it after the new regulation</li>
                            <li>Add a description explaining the regulatory requirement</li>
                            <li>Set the version and mark it as active</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Group</span></li>
                        </ol>
                        """,
                        "icon": "📋"
                    },
                    {
                        "title": "Add the New Policies to the Group",
                        "content": """
                        <ol>
                            <li>Find your newly created regulation policy group</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Add Policies to this Group</span></li>
                            <li>Select all the new compliant policies</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Add Policies</span></li>
                        </ol>
                        """,
                        "icon": "➕"
                    },
                    {
                        "title": "Create a Time-Based Context Override",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Create New Override</span> expander, select your new regulation policy group</li>
                            <li>Select the appropriate purposes (or leave empty to apply to all purposes)</li>
                            <li>Set a high priority to ensure it overrides existing policies</li>
                            <li>Set the <span style="color: #1565C0; font-weight: bold;">Effective From</span> date to January 1, 2026</li>
                            <li>Leave the <span style="color: #1565C0; font-weight: bold;">Effective To</span> date empty for indefinite application</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Override</span></li>
                        </ol>
                        """,
                        "icon": "🔄"
                    }
                ],
                "result": """
                <div style="background-color: #FFF8E1; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 5px solid #FF8F00;">
                    <p style="margin-top: 0; font-weight: bold; color: #FF8F00;">How It Works:</p>
                    <p>The system will automatically manage the policy transition:</p>
                    <ol>
                        <li>Before January 1, 2026, the current policies remain in effect</li>
                        <li>Starting January 1, 2026, the system will automatically begin applying the new regulation policies</li>
                        <li>The transition happens without any manual intervention on the effective date</li>
                        <li>You can prepare and test the policies well in advance of the regulatory deadline</li>
                    </ol>
                    <p>This approach allows you to prepare for regulatory changes proactively while ensuring compliance exactly when required.</p>
                </div>
                """,
                "color": "#FFEBEE"
            },
            {
                "title": "Combining Multiple Policy Types",
                "question": "How do I create a comprehensive data governance strategy using different policy types together?",
                "description": """
                <p>This scenario demonstrates how to combine different policy types (Access Control, Security, and Retention) to create a comprehensive data governance strategy for sensitive data.</p>
                
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <p style="margin-top: 0; font-weight: bold; color: #2E7D32;">Use Case Example:</p>
                    <p>You need to implement a complete governance strategy for financial data that controls who can access it, ensures proper masking of sensitive fields, and enforces appropriate retention periods - all aligned with purpose-based access control.</p>
                </div>
                """,
                "steps": [
                    {
                        "title": "Create Policies of Each Type",
                        "content": """
                        <ol>
                            <li>Navigate to the <span style="color: #1565C0; font-weight: bold;">Define Policies</span> tab</li>
                            <li>Create <span style="color: #1565C0; font-weight: bold;">Access Control</span> policies that define who can access financial data and under what conditions</li>
                            <li>Create <span style="color: #1565C0; font-weight: bold;">Security</span> policies that specify appropriate masking for sensitive financial fields</li>
                            <li>Create <span style="color: #1565C0; font-weight: bold;">Retention</span> policies that define how long financial data should be kept</li>
                            <li>Name each policy descriptively to indicate its purpose and target</li>
                        </ol>
                        """,
                        "icon": "✏️"
                    },
                    {
                        "title": "Create a Comprehensive Policy Group",
                        "content": """
                        <ol>
                            <li>Go to the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Create New Policy Group</span></li>
                            <li>Name it <span style="color: #1565C0; font-weight: bold;">Financial Data Governance</span></li>
                            <li>Add a detailed description explaining the comprehensive approach</li>
                            <li>Set the version and mark it as active</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Group</span></li>
                        </ol>
                        """,
                        "icon": "📋"
                    },
                    {
                        "title": "Add All Policy Types to the Group",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Manage Policy Groups</span> section, find your Financial Data Governance group</li>
                            <li>Click on <span style="color: #1565C0; font-weight: bold;">Add Policies to this Group</span></li>
                            <li>Use the multi-select to choose policies of all three types (Access Control, Security, and Retention)</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Add Policies</span></li>
                        </ol>
                        """,
                        "icon": "➕"
                    },
                    {
                        "title": "Create Purpose-Based Context Overrides",
                        "content": """
                        <ol>
                            <li>In the <span style="color: #1565C0; font-weight: bold;">Policy Groups & Overrides</span> tab, find the <span style="color: #1565C0; font-weight: bold;">Create New Override</span> expander</li>
                            <li>Select your Financial Data Governance policy group</li>
                            <li>Select the appropriate business purpose (e.g., <span style="color: #1565C0; font-weight: bold;">Financial Reporting</span>)</li>
                            <li>Set appropriate priority levels</li>
                            <li>Click <span style="color: #1565C0; font-weight: bold;">Create Override</span></li>
                            <li>Repeat for other relevant business purposes with appropriate variations</li>
                        </ol>
                        """,
                        "icon": "🔄"
                    }
                ],
                "result": """
                <div style="background-color: #FFF8E1; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 5px solid #FF8F00;">
                    <p style="margin-top: 0; font-weight: bold; color: #FF8F00;">How It Works:</p>
                    <p>When financial data is accessed:</p>
                    <ol>
                        <li>The system first checks the <span style="font-weight: bold;">purpose</span> of the access request</li>
                        <li>It applies the <span style="font-weight: bold;">Access Control</span> policies to determine if access is permitted</li>
                        <li>If access is granted, it applies the <span style="font-weight: bold;">Security</span> policies to mask sensitive fields as appropriate</li>
                        <li>In parallel, it enforces the <span style="font-weight: bold;">Retention</span> policies to ensure data isn't kept longer than necessary</li>
                        <li>All of this is done based on the legitimate business purpose, ensuring purpose-based access control</li>
                    </ol>
                    <p>This layered approach provides comprehensive protection while ensuring data remains available for legitimate business purposes.</p>
                </div>
                """,
                "color": "#EDE7F6"
            }
        ]
        
        # Display scenarios in expandable sections with colored headers
        for i, scenario in enumerate(scenarios):
            # Add colored header above each expander
            st.markdown(f"""
            <div style="background-color: {scenario['color']}; padding: 10px; border-radius: 10px 10px 0 0; border-left: 5px solid #1565C0; margin-bottom: 0;">
                <h3 style="margin: 0; color: #1565C0;">{i+1}. {scenario['title']}</h3>
                <p style="margin: 5px 0 0 0; font-style: italic;">{scenario['question']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Solution", expanded=i==0):
                # Scenario description
                st.markdown(scenario['description'], unsafe_allow_html=True)
                
                # Steps with visual timeline
                st.markdown(f"""
                <div style="margin: 20px 0; text-align: center;">
                    <h4 style="color: #1565C0;">Step-by-Step Implementation</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Display steps in a visually appealing way
                for j, step in enumerate(scenario['steps']):
                    col1, col2 = st.columns([1, 5])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background-color: #1565C0; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                            <span style="font-size: 20px;">{step['icon']}</span>
                        </div>
                        <div style="text-align: center; margin-top: 5px;">
                            <span style="font-weight: bold;">Step {j+1}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="background-color: {scenario['color']}; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #1565C0;">
                            <h4 style="margin-top: 0; color: #1565C0;">{step['title']}</h4>
                            {step['content']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Result explanation
                st.markdown(scenario['result'], unsafe_allow_html=True)
        
        # Additional help section
        st.markdown("""
        <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin-top: 30px; text-align: center; border: 1px solid #1565C0;">
            <h4 style="color: #1565C0; margin: 0;">Need More Help?</h4>
            <p style="margin: 10px 0 0 0;">If you have questions about other scenarios or need assistance implementing a specific policy management approach, please contact the Data Governance team.</p>
        </div>
        """, unsafe_allow_html=True)

    def _render_policy_groups(self):
        """Render the policy groups and overrides section."""
        st.markdown("""
        <h3 style="color: #1565C0;">Policy Groups & Overrides</h3>
        <p>Organize related policies into groups and define context-specific overrides.</p>
        """, unsafe_allow_html=True)
        
        # Two columns layout
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Policy Groups
            st.subheader("Policy Groups")
            
            # Create new policy group form
            with st.expander("Create New Policy Group"):
                group_name = st.text_input("Group Name", key="group_name_input")
                group_description = st.text_area("Description", key="group_desc_input")
                group_version = st.text_input("Version", value="1.0", key="group_version_input")
                is_active = st.checkbox("Active", value=True, key="group_active_checkbox")
                
                if st.button("Create Group", key="create_group_btn"):
                    if self.policy_definition_repository and group_name:
                        self.policy_definition_repository.create_policy_group(group_name, group_description, group_version, is_active)
                        st.success("Policy group created successfully!")
                        # Rerun the app to refresh the UI
                        st.experimental_rerun()
                    elif not group_name:
                        st.warning("Please enter a group name.")
            
            # View Policy Group Contents
            st.markdown("---")
            st.subheader("View Policy Group Contents")
            
            # Get all policy groups for the dropdown
            policy_groups = self.policy_definition_repository.get_all_policy_groups() if self.policy_definition_repository else []
            
            if not policy_groups:
                st.info("No policy groups defined yet.")
            else:
                # Create a dropdown to select a policy group
                group_options = {g["id"]: f"{g['name']} (v{g['version']})" for g in policy_groups}
                selected_group_id = st.selectbox(
                    "Select Policy Group",
                    options=list(group_options.keys()),
                    format_func=lambda x: group_options.get(x, "Unknown"),
                    key="view_policy_group_select"
                )
                
                # Display the policies in the selected group
                if selected_group_id:
                    # Get the selected group details
                    selected_group = next((g for g in policy_groups if g["id"] == selected_group_id), None)
                    
                    if selected_group:
                        st.write(f"**Description:** {selected_group['description']}")
                        st.write(f"**Status:** {'Active' if selected_group['is_active'] else 'Inactive'}")
                        
                        # Get policies in the group
                        group_policies = self.policy_definition_repository.get_policies_in_group(selected_group_id) if self.policy_definition_repository else []
                        
                        if not group_policies:
                            st.info(f"No policies in group '{selected_group['name']}' yet.")
                        else:
                            # Display policies in a table
                            st.write(f"**Policies in {selected_group['name']}:**")
                            
                            # Create a DataFrame for the policies
                            policy_data = []
                            for p in group_policies:
                                target_name = p.get("data_element_name") or p.get("data_category_name") or p.get("sensitivity_name") or "Global"
                                policy_data.append({
                                    "Policy Type": p.get("policy_type_name", "Unknown"),
                                    "Target": target_name,
                                    "Target System": p.get("target_system", ""),
                                })
                            
                            if policy_data:
                                policy_df = pd.DataFrame(policy_data)
                                st.dataframe(policy_df, use_container_width=True)
            
            # Manage Policy Groups
            st.markdown("---")
            st.subheader("Manage Policy Groups")
            
            if not policy_groups:
                st.info("No policy groups defined yet.")
            else:
                for group in policy_groups:
                    with st.container():
                        st.markdown(f"### {group['name']} (v{group['version']})")
                        
                        # Group details
                        st.write(f"**Description:** {group['description']}")
                        st.write(f"**Status:** {'Active' if group['is_active'] else 'Inactive'}")
                        
                        # Add policy to group
                        with st.expander("Add Policies to this Group"):
                            # Get all policies
                            all_policies = self.policy_definition_repository.get_all_policies() if self.policy_definition_repository else []
                            
                            if not all_policies:
                                st.warning("No policies available. Please create policies first.")
                            else:
                                policy_options = {p["id"]: f"{p.get('policy_type_name', 'Unknown')} - {p.get('data_element_name') or p.get('data_category_name') or p.get('sensitivity_name') or 'Global'}" for p in all_policies}
                                
                                selected_policy_ids = st.multiselect(
                                    "Select Policies to Add",
                                    options=list(policy_options.keys()),
                                    format_func=lambda x: policy_options.get(x, "Unknown"),
                                    key=f"group_{group['id']}_policy_select"
                                )
                                
                                target_system = st.text_input("Target System (Optional)", key=f"group_{group['id']}_target_input")
                                
                                add_button = st.button("Add Policies", key=f"group_{group['id']}_add_policy_btn")
                                if add_button and selected_policy_ids:
                                    # Add each selected policy to the group
                                    for policy_id in selected_policy_ids:
                                        if self.policy_definition_repository:
                                            self.policy_definition_repository.add_policy_to_group(group['id'], policy_id, target_system)
                                    
                                    st.success(f"{len(selected_policy_ids)} policies added to group {group['name']}")
                                    # Rerun the app to refresh the UI
                                    st.experimental_rerun()
                                elif add_button and not selected_policy_ids:
                                    st.warning("Please select at least one policy to add to the group.")
                        
                        # Delete group button
                        if st.button("Delete Group", key=f"delete_group_{group['id']}_btn"):
                            if self.policy_definition_repository:
                                self.policy_definition_repository.delete_policy_group(group['id'])
                                st.success("Policy group deleted successfully!")
                                # Rerun the app to refresh the UI
                                st.experimental_rerun()
                            else:
                                st.error("Failed to delete policy group.")
            
            # Create new context override form
            with st.expander("Create New Override"):
                # Get policy groups
                policy_groups = self.policy_definition_repository.get_all_policy_groups() if self.policy_definition_repository else []
                
                if not policy_groups:
                    st.warning("No policy groups available. Please create a policy group first.")
                else:
                    policy_group_options = {pg["id"]: pg["name"] for pg in policy_groups}
                    
                    selected_policy_group_id = st.selectbox(
                        "Select Policy Group",
                        options=list(policy_group_options.keys()),
                        format_func=lambda x: policy_group_options.get(x, "Unknown"),
                        key="override_group_select"
                    )
                    
                    # Context selectors
                    st.markdown("### Context Criteria")
                    
                    # Purpose selector
                    purposes = self.glossary_repository.get_purposes() if self.glossary_repository else []
                    
                    if purposes:
                        purpose_options = {p["id"]: p["name"] for p in purposes}
                        selected_purpose_id = st.selectbox(
                            "Select Purpose (Optional)",
                            options=[None] + list(purpose_options.keys()),
                            format_func=lambda x: purpose_options.get(x, "Any") if x else "Any",
                            key="override_purpose_select"
                        )
                    else:
                        st.info("No purposes available.")
                        selected_purpose_id = None
                    
                    # Role selector
                    roles = self.glossary_repository.get_external_roles() if self.glossary_repository else []
                    
                    if roles:
                        # Handle roles as tuples (id, name, description, source_system, source_role_name, asset_id)
                        role_options = {r[0]: r[1] for r in roles}  # Use index 0 for id, index 1 for name
                        selected_role_id = st.selectbox(
                            "Select Role (Optional)",
                            options=[None] + list(role_options.keys()),
                            format_func=lambda x: role_options.get(x, "Any") if x else "Any",
                            key="override_role_select"
                        )
                    else:
                        st.info("No roles available.")
                        selected_role_id = None
                    
                    # Region selector
                    regions = self.policy_definition_repository.get_all_regions() if self.policy_definition_repository else []
                    
                    if regions:
                        region_options = {r["id"]: r["name"] for r in regions}
                        selected_region_id = st.selectbox(
                            "Select Region (Optional)",
                            options=[None] + list(region_options.keys()),
                            format_func=lambda x: region_options.get(x, "Any") if x else "Any",
                            key="override_region_select"
                        )
                    else:
                        st.info("No regions available.")
                        selected_region_id = None
                    
                    # Context tags
                    context_tags = st.text_area("Context Tags (JSON format)", key="context_tags_textarea")
                    
                    # Priority and dates
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        manual_priority = st.number_input("Priority", min_value=0, max_value=100, value=10, key="priority_input")
                        effective_from = st.date_input("Effective From", value=datetime.now().date(), key="override_from_date")
                    
                    with col2:
                        is_active = st.checkbox("Active", value=True, key="override_active_checkbox")
                        effective_to = st.date_input("Effective To (Optional)", value=None, key="override_to_date")
                    
                    if st.button("Create Override", key="create_override_btn"):
                        if not selected_group_id:
                            st.error("Please select a policy group.")
                        else:
                            # Format dates properly for database
                            from_date = effective_from.strftime('%Y-%m-%d') if effective_from else None
                            to_date = effective_to.strftime('%Y-%m-%d') if effective_to else None
                            
                            # Validate and parse context tags if provided
                            tags_json = None
                            if context_tags:
                                try:
                                    tags_json = json.dumps(json.loads(context_tags))
                                except json.JSONDecodeError:
                                    st.error("Context tags must be valid JSON. Please check the format.")
                                    return
                            
                            # Create the context policy group
                            if self.policy_definition_repository:
                                result = self.policy_definition_repository.create_context_policy_group(
                                    purpose_id=selected_purpose_id,
                                    external_role_id=selected_role_id,
                                    region_id=selected_region_id,
                                    policy_group_id=selected_group_id,
                                    manual_priority=manual_priority,
                                    context_tags=tags_json,
                                    effective_from=from_date,
                                    effective_to=to_date
                                )
                                
                                if result:
                                    st.success("Context override created successfully!")
                                    # Rerun the app to refresh the UI
                                    st.rerun()
                                else:
                                    st.error("Failed to create context override. Please check the logs for details.")
                            else:
                                st.error("Repository not available. Cannot create context override.")
            
            # Existing context overrides
            st.markdown("---")
            st.subheader("Existing Overrides")
            
            context_policy_groups = self.policy_definition_repository.get_all_context_policy_groups() if self.policy_definition_repository else []
            
            if not context_policy_groups:
                st.info("No context overrides defined yet.")
            else:
                for cpg in context_policy_groups:
                    with st.container():
                        st.markdown(f"### Override for {cpg.get('policy_group_name', 'Unknown Group')}")
                        
                        # Context criteria
                        criteria = []
                        if cpg.get('purpose_name'):
                            criteria.append(f"Purpose: {cpg.get('purpose_name')}")
                        if cpg.get('external_role_name'):
                            criteria.append(f"Role: {cpg.get('external_role_name')}")
                        if cpg.get('region_name'):
                            criteria.append(f"Region: {cpg.get('region_name')}")
                        
                        if criteria:
                            st.markdown(", ".join(criteria))
                        else:
                            st.markdown("Global override (no specific context)")
                        
                        # Details
                        cols = st.columns([2, 2, 1])
                        with cols[0]:
                            st.markdown(f"Priority: {cpg.get('manual_priority', 0)}")
                        with cols[1]:
                            st.markdown(f"Effective: {cpg.get('effective_from', 'Always')} to {cpg.get('effective_to', 'Indefinite')}")
                        with cols[2]:
                            if st.button("Delete", key=f"delete_override_{cpg['id']}_btn"):
                                st.warning("Override deleted")
