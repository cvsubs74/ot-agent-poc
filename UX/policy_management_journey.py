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
        # Add minimal custom CSS for better styling
        st.markdown("""
        <style>
        .policy-header {
            color: #1565C0;
            margin-bottom: 10px;
        }
        .policy-step {
            background-color: #F5F5F5;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .step-number {
            background-color: #1565C0;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-weight: bold;
        }
        .step-title {
            font-weight: 600;
            color: #1565C0;
            display: inline;
            vertical-align: middle;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Improved header with description
        st.markdown("""
        <h3 class="policy-header">Define Policies</h3>
        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0;">Create and manage policies to protect your data assets. Policies define how data should be accessed, secured, and retained.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for policy creation, viewing, and management
        policy_tabs = st.tabs(["Create New Policy", "View Policies", "Manage Policies"])
        
        # Create New Policy tab
        with policy_tabs[0]:
            # Step 1: Basic Information
            st.markdown("""
            <div class="policy-step">
                <span class="step-number">1</span>
                <span class="step-title">Basic Information</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                policy_name = st.text_input("Policy Name", placeholder="Enter a descriptive name")
                effective_from = st.date_input("Effective From", value=datetime.now().date())
            
            with col2:
                policy_description = st.text_area("Description", placeholder="Describe the purpose of this policy")
                effective_to = st.date_input("Effective To (Optional)", value=None)
            
            # Step 2: Policy Type Selection
            st.markdown("""
            <div class="policy-step">
                <span class="step-number">2</span>
                <span class="step-title">Select Policy Type</span>
                <p style="margin: 10px 0 0 38px; color: #616161;">Choose the type of policy you want to create. Each type serves a different purpose in protecting your data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get policy types
            policy_types = self.policy_definition_repository.get_all_policy_types() if self.policy_definition_repository else []
            
            if not policy_types:
                st.warning("No policy types available. Please define policy types first.")
                return
            
            # Create policy type options with descriptions and icons
            policy_type_info = {
                "Access Control": {
                    "icon": "🔒",
                    "description": "Define who can access data and what operations they can perform (read, write, share)."
                },
                "Security": {
                    "icon": "🛡️",
                    "description": "Specify encryption and masking requirements to protect sensitive data."
                },
                "Retention": {
                    "icon": "⏱️",
                    "description": "Set how long data should be kept before archival or deletion."
                }
            }
            
            # Create a dictionary mapping policy type IDs to names
            policy_type_options = {pt["id"]: pt["name"] for pt in policy_types}
            
            # Add CSS for policy type cards
            st.markdown("""
            <style>
            .policy-type-card {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                border: 1px solid #E0E0E0;
                transition: all 0.2s ease;
            }
            .policy-type-card:hover {
                border-color: #1565C0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .policy-type-card.selected {
                border-color: #1565C0;
                border-width: 2px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .policy-type-icon {
                font-size: 24px;
                margin-right: 10px;
                color: #1565C0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Use radio buttons for a more visual selection
            selected_policy_type_id = st.radio(
                "Select Policy Type",
                options=list(policy_type_options.keys()),
                format_func=lambda x: policy_type_options.get(x, "Unknown"),
                horizontal=True,
                label_visibility="collapsed"
            )
            
            policy_type_name = policy_type_options.get(selected_policy_type_id)
            
            # Display information about the selected policy type
            if policy_type_name in policy_type_info:
                info = policy_type_info[policy_type_name]
                st.markdown(f"""
                <div style="background-color: #F5F5F5; border-radius: 8px; padding: 15px; margin: 10px 0;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 24px; margin-right: 10px;">{info['icon']}</span>
                        <span style="font-weight: 600; font-size: 18px;">{policy_type_name}</span>
                    </div>
                    <p style="margin: 10px 0 0 0;">{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Update policy name based on policy type if not already set
            if not policy_name and policy_type_name:
                policy_name = f"{policy_type_name} Policy"
            
            # Step 3: Target Selection
            st.markdown("""
            <div class="policy-step">
                <span class="step-number">3</span>
                <span class="step-title">Select Policy Targets</span>
                <p style="margin: 10px 0 0 38px; color: #616161;">Choose what data elements, categories, or sensitivity levels this policy will apply to.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add CSS for target badges
            st.markdown("""
            <style>
            .target-badge {
                display: inline-block;
                background-color: #E3F2FD;
                color: #1565C0;
                padding: 5px 10px;
                border-radius: 16px;
                margin: 5px;
                font-size: 12px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Create a more visual target type selector
            target_options = ["Data Element", "Data Category", "Sensitivity Level"]
            target_descriptions = {
                "Data Element": "Individual data fields like 'Email Address' or 'Credit Card Number'",
                "Data Category": "Groups of related data elements like 'Personal Information' or 'Financial Data'",
                "Sensitivity Level": "Classification levels like 'Public', 'Internal', 'Confidential', or 'Restricted'"
            }
            
            # Use tabs for target selection
            target_tabs = st.tabs(target_options)
            
            # Target selection based on tab
            selected_targets = []
            selected_target_names = []
            
            # Data Element tab
            with target_tabs[0]:
                st.markdown(f"<p style='color: #616161;'>{target_descriptions['Data Element']}</p>", unsafe_allow_html=True)
                
                data_elements = self.glossary_repository.get_data_elements() if self.glossary_repository else []
                
                if not data_elements:
                    st.warning("No data elements available. Please define data elements first.")
                else:
                    data_element_options = {de["id"]: de["name"] for de in data_elements}
                    
                    # Add search box for data elements
                    search_term = st.text_input("Search Data Elements", placeholder="Type to filter data elements", key="search_data_elements")
                    
                    # Filter data elements based on search term
                    filtered_elements = {k: v for k, v in data_element_options.items() 
                                        if not search_term or search_term.lower() in v.lower()}
                    
                    # Show count of filtered elements
                    st.markdown(f"<p style='color: #616161;'>{len(filtered_elements)} data elements found</p>", unsafe_allow_html=True)
                    
                    # Multi-select for data elements with improved styling
                    selected_target_ids = st.multiselect(
                        "Select Data Elements",
                        options=list(filtered_elements.keys()),
                        format_func=lambda x: filtered_elements.get(x, "Unknown"),
                        key="data_element_multiselect"
                    )
                    
                    # Display selected targets as badges
                    if selected_target_ids:
                        st.markdown("<p style='margin-top: 15px;'>Selected Data Elements:</p>", unsafe_allow_html=True)
                        badges_html = ""
                        for target_id in selected_target_ids:
                            target_name = filtered_elements.get(target_id, "Unknown")
                            badges_html += f"<span class='target-badge'>{target_name}</span>"
                        st.markdown(f"<div style='margin-top: 5px;'>{badges_html}</div>", unsafe_allow_html=True)
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "data_element",
                            "id": target_id,
                            "name": data_element_options.get(target_id)
                        })
                        selected_target_names.append(data_element_options.get(target_id))
            
            # Data Category tab
            with target_tabs[1]:
                st.markdown(f"<p style='color: #616161;'>{target_descriptions['Data Category']}</p>", unsafe_allow_html=True)
                
                data_categories = self.glossary_repository.get_data_categories() if self.glossary_repository else []
                
                if not data_categories:
                    st.warning("No data categories available. Please define data categories first.")
                else:
                    data_category_options = {dc["id"]: dc["name"] for dc in data_categories}
                    
                    # Add search box for data categories
                    search_term = st.text_input("Search Data Categories", placeholder="Type to filter categories", key="search_data_categories")
                    
                    # Filter data categories based on search term
                    filtered_categories = {k: v for k, v in data_category_options.items() 
                                        if not search_term or search_term.lower() in v.lower()}
                    
                    # Show count of filtered categories
                    st.markdown(f"<p style='color: #616161;'>{len(filtered_categories)} data categories found</p>", unsafe_allow_html=True)
                    
                    # Multi-select for data categories with improved styling
                    selected_target_ids = st.multiselect(
                        "Select Data Categories",
                        options=list(filtered_categories.keys()),
                        format_func=lambda x: filtered_categories.get(x, "Unknown"),
                        key="data_category_multiselect"
                    )
                    
                    # Display selected targets as badges
                    if selected_target_ids:
                        st.markdown("<p style='margin-top: 15px;'>Selected Data Categories:</p>", unsafe_allow_html=True)
                        badges_html = ""
                        for target_id in selected_target_ids:
                            target_name = filtered_categories.get(target_id, "Unknown")
                            badges_html += f"<span class='target-badge'>{target_name}</span>"
                        st.markdown(f"<div style='margin-top: 5px;'>{badges_html}</div>", unsafe_allow_html=True)
                    
                    # Store selected targets
                    for target_id in selected_target_ids:
                        selected_targets.append({
                            "type": "data_category",
                            "id": target_id,
                            "name": data_category_options.get(target_id)
                        })
                        selected_target_names.append(data_category_options.get(target_id))
            
            # Sensitivity Level tab
            with target_tabs[2]:
                st.markdown(f"<p style='color: #616161;'>{target_descriptions['Sensitivity Level']}</p>", unsafe_allow_html=True)
                
                sensitivity_levels = self.glossary_repository.get_sensitivities() if self.glossary_repository else []
                
                if not sensitivity_levels:
                    st.warning("No sensitivity levels available. Please define sensitivity levels first.")
                else:
                    sensitivity_options = {sl["id"]: sl["name"] for sl in sensitivity_levels}
                    
                    # Multi-select for sensitivity levels with improved styling
                    selected_target_ids = st.multiselect(
                        "Select Sensitivity Levels",
                        options=list(sensitivity_options.keys()),
                        format_func=lambda x: sensitivity_options.get(x, "Unknown"),
                        key="sensitivity_multiselect"
                    )
                    
                    # Display selected targets as badges
                    if selected_target_ids:
                        st.markdown("<p style='margin-top: 15px;'>Selected Sensitivity Levels:</p>", unsafe_allow_html=True)
                        badges_html = ""
                        for target_id in selected_target_ids:
                            target_name = sensitivity_options.get(target_id, "Unknown")
                            badges_html += f"<span class='target-badge'>{target_name}</span>"
                        st.markdown(f"<div style='margin-top: 5px;'>{badges_html}</div>", unsafe_allow_html=True)
                    
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
                    policy_name = f"{policy_type_name} Policy for {len(selected_target_names)} targets"
            
            # Step 4: Preview and Submit
            st.markdown("""
            <div class="policy-step">
                <span class="step-number">4</span>
                <span class="step-title">Preview and Submit</span>
                <p style="margin: 10px 0 0 38px; color: #616161;">Review your policy before creating it.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add CSS for policy preview
            st.markdown("""
            <style>
            .policy-preview {
                background-color: #F9FAFC;
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
                border: 1px solid #E0E0E0;
            }
            </style>
            """, unsafe_allow_html=True)
            
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
                with st.container():
                    st.markdown("<div class='policy-preview'>", unsafe_allow_html=True)
                    st.markdown(f"<h4 style='margin-top: 0; color: #1565C0;'>{policy_name}</h4>", unsafe_allow_html=True)
                    
                    # Policy metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"<p><strong>Type:</strong> {policy_type_name}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Target Type:</strong> {selected_targets[0]['type'].replace('_', ' ').title()}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Targets:</strong> {len(selected_targets)} selected</p>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p><strong>Effective From:</strong> {effective_from}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p><strong>Effective To:</strong> {effective_to if effective_to else 'Indefinite'}</p>", unsafe_allow_html=True)
                        if policy_description:
                            st.markdown(f"<p><strong>Description:</strong> {policy_description}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Create a more concise policy representation for JSON preview
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
            
            # Step 5: Submit
            st.markdown("""
            <div class="policy-step">
                <span class="step-number">5</span>
                <span class="step-title">Submit Policy</span>
                <p style="margin: 10px 0 0 38px; color: #616161;">Create your policy to enforce data governance rules.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Submit button with enhanced styling
            submit_col1, submit_col2 = st.columns([3, 1])
            with submit_col2:
                submit_button = st.button("Create Policy", type="primary", use_container_width=True)
            
            if submit_button:
                # Validate inputs
                validation_errors = []
                
                if not policy_name or policy_name.strip() == "":
                    validation_errors.append("Policy name is required.")
                
                if not selected_targets:
                    validation_errors.append("At least one data element, category, or sensitivity level must be selected.")
                
                if validation_errors:
                    st.markdown("<div style='background-color: #FFEBEE; padding: 15px; border-radius: 8px; margin: 15px 0;'>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color: #C62828; margin-top: 0;'>Please fix the following issues:</h4>", unsafe_allow_html=True)
                    for error in validation_errors:
                        st.markdown(f"<p style='margin: 5px 0; color: #C62828;'>• {error}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # Show a spinner while creating the policy
                    with st.spinner("Creating policy..."):
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
                    
                    # Show results with enhanced visual feedback
                    if created_policies:
                        st.markdown("""
                        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <h4 style="color: #2E7D32; margin-top: 0;">Success!</h4>
                            <p style="margin: 5px 0;">The following policies were successfully created:</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show details of created policies in a more visual way
                        for policy in created_policies:
                            target_type = policy['target_type'].replace('_', ' ').title()
                            st.markdown(f"""
                            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px 0; border-left: 3px solid #2E7D32;">
                                <p style="margin: 0;"><strong>{policy['target_name']}</strong> <span style="color: #757575; font-size: 12px;">({target_type})</span></p>
                                <p style="margin: 5px 0 0 0; color: #757575; font-size: 12px;">Policy ID: {policy['id']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Add a button to view all policies
                        st.button("View All Policies", on_click=lambda: st.session_state.update({"active_tab": "Manage Existing Policies"}))
                    
                    if failed_policies:
                        st.markdown("""
                        <div style="background-color: #FFEBEE; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <h4 style="color: #C62828; margin-top: 0;">Some policies could not be created</h4>
                            <p style="margin: 5px 0;">The following policies failed to create:</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show details of failed policies with better formatting
                        for policy in failed_policies:
                            target_type = policy['target_type'].replace('_', ' ').title()
                            error_msg = policy.get('error', 'Unknown error')
                            st.markdown(f"""
                            <div style="background-color: white; border-radius: 8px; padding: 15px; margin: 10px 0; border-left: 3px solid #C62828;">
                                <p style="margin: 0;"><strong>{policy['target_name']}</strong> <span style="color: #757575; font-size: 12px;">({target_type})</span></p>
                                <p style="margin: 5px 0 0 0; color: #C62828; font-size: 12px;">Error: {error_msg}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Refresh the policy list
                    st.rerun()
        
        # View Policies tab
        with policy_tabs[1]:
            st.markdown("""
            <div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: #1565C0; margin-top: 0;">View Policies</h4>
                <p style="margin: 0;">Browse and explore all defined policies in the system.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add CSS for policy cards
            st.markdown("""
            <style>
            .policy-list-card {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
                border-left: 3px solid #1565C0;
                transition: all 0.2s ease;
            }
            .policy-list-card:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .policy-status {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
            }
            .status-active {
                background-color: #E8F5E9;
                color: #2E7D32;
            }
            .status-inactive {
                background-color: #FFEBEE;
                color: #C62828;
            }
            .policy-tag {
                display: inline-block;
                background-color: #EDE7F6;
                color: #5E35B1;
                padding: 3px 8px;
                border-radius: 12px;
                margin-right: 5px;
                font-size: 12px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Get policies
            policies = self.policy_definition_repository.get_all_policies() if self.policy_definition_repository else []
            
            if not policies:
                st.info("No policies defined yet.")
            else:
                # Create a dropdown to select a policy to view
                policy_options = {}
                for policy in policies:
                    policy_id = policy.get("id")
                    policy_name = policy.get("name", "Unnamed Policy")
                    policy_type = policy.get("policy_type_name", "Unknown")
                    target_name = policy.get("data_element_name") or policy.get("data_category_name") or policy.get("sensitivity_name") or "Global"
                    
                    # Create a descriptive label for the dropdown
                    label = f"{policy_name} - {policy_type} - {target_name} (ID: {policy_id})"
                    policy_options[policy_id] = label
                
                # Policy selection dropdown
                selected_policy_id = st.selectbox(
                    "Select a policy to view",
                    options=list(policy_options.keys()),
                    format_func=lambda x: policy_options.get(x, "Unknown")
                )
                
                if selected_policy_id:
                    # Get the selected policy
                    selected_policy = None
                    for policy in policies:
                        if policy.get("id") == selected_policy_id:
                            selected_policy = policy
                            break
                    
                    if selected_policy:
                        # Get policy details
                        policy_name = selected_policy.get("name", "Unnamed Policy")
                        policy_id = selected_policy.get("id")
                        policy_type = selected_policy.get("policy_type_name", "Unknown")
                        
                        # Determine target name and type
                        target_name = selected_policy.get("data_element_name") or selected_policy.get("data_category_name") or selected_policy.get("sensitivity_name") or "Global"
                        target_type = "Data Element" if selected_policy.get("data_element_name") else \
                                    "Data Category" if selected_policy.get("data_category_name") else \
                                    "Sensitivity Level" if selected_policy.get("sensitivity_name") else "Global"
                        
                        # Format dates
                        effective_from = selected_policy.get("effective_from")
                        effective_to = selected_policy.get("effective_to")
                        
                        if effective_from and isinstance(effective_from, str):
                            try:
                                effective_from = datetime.strptime(effective_from, "%Y-%m-%d").date()
                            except:
                                pass
                        elif effective_from and isinstance(effective_from, datetime):
                            effective_from = effective_from.date()
                        
                        if effective_to and isinstance(effective_to, str):
                            try:
                                effective_to = datetime.strptime(effective_to, "%Y-%m-%d").date()
                            except:
                                pass
                        elif effective_to and isinstance(effective_to, datetime):
                            effective_to = effective_to.date()
                        
                        # Check if policy is active
                        is_active = True
                        current_date = datetime.now().date()
                        
                        # Ensure effective_from is a date object
                        if effective_from:
                            if isinstance(effective_from, datetime):
                                effective_from = effective_from.date()
                            if effective_from > current_date:
                                is_active = False
                        
                        # Ensure effective_to is a date object
                        if effective_to:
                            if isinstance(effective_to, datetime):
                                effective_to = effective_to.date()
                            if effective_to < current_date:
                                is_active = False
                        
                        # Display policy details in a card
                        st.markdown(f"""
                        <div style="background-color: white; border-radius: 8px; padding: 20px; margin-top: 20px; border-left: 5px solid #1565C0; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <h3 style="margin: 0;">{policy_name}</h3>
                                <span class="policy-status {'status-active' if is_active else 'status-inactive'}">
                                    {'Active' if is_active else 'Inactive'}
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")                        
                        # Policy metadata
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"<p><strong>ID:</strong> {policy_id}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p><strong>Type:</strong> <span class='policy-tag'>{policy_type}</span></p>", unsafe_allow_html=True)
                            st.markdown(f"<p><strong>Target:</strong> {target_name} <span style='color: #757575; font-size: 12px;'>({target_type})</span></p>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"<p><strong>Effective From:</strong> {effective_from}</p>", unsafe_allow_html=True)
                            st.markdown(f"<p><strong>Effective To:</strong> {effective_to if effective_to else 'Indefinite'}</p>", unsafe_allow_html=True)
                            created_at = selected_policy.get("created_at")
                            if created_at:
                                st.markdown(f"<p><strong>Created:</strong> {created_at}</p>", unsafe_allow_html=True)
                            updated_at = selected_policy.get("updated_at")
                            if updated_at:
                                st.markdown(f"<p><strong>Last Updated:</strong> {updated_at}</p>", unsafe_allow_html=True)
                        
                        # Parse and display policy config
                        policy_config = selected_policy.get("policy_config")
                        if policy_config:
                            if isinstance(policy_config, str):
                                try:
                                    policy_config = json.loads(policy_config)
                                except:
                                    pass
                            
                            st.markdown("<h4 style='margin-top: 20px;'>Policy Configuration</h4>", unsafe_allow_html=True)
                            
                            # Display configuration based on policy type
                            if policy_type == "Access Control":
                                # Extract permissions for the specific target
                                target_id = selected_policy.get("data_element_id") or selected_policy.get("data_category_id") or selected_policy.get("sensitivity_id")
                                if target_id and isinstance(policy_config, dict) and policy_config.get("target_permissions"):
                                    target_permissions = policy_config.get("target_permissions", {})
                                    target_perms = target_permissions.get(str(target_id), {})
                                    
                                    # Display permissions in a more user-friendly format
                                    st.markdown("<p><strong>Permissions:</strong></p>", unsafe_allow_html=True)
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.markdown(f"<p>Read: <span style='color: {'green' if target_perms.get('read', False) else 'red'};'>{'✓' if target_perms.get('read', False) else '✗'}</span></p>", unsafe_allow_html=True)
                                    with col2:
                                        st.markdown(f"<p>Write: <span style='color: {'green' if target_perms.get('write', False) else 'red'};'>{'✓' if target_perms.get('write', False) else '✗'}</span></p>", unsafe_allow_html=True)
                                    with col3:
                                        st.markdown(f"<p>Share: <span style='color: {'green' if target_perms.get('share', False) else 'red'};'>{'✓' if target_perms.get('share', False) else '✗'}</span></p>", unsafe_allow_html=True)
                                else:
                                    # Display the full config if target permissions not found
                                    st.json(policy_config)
                            elif policy_type == "Security":
                                # Extract security settings for the specific target
                                target_id = selected_policy.get("data_element_id") or selected_policy.get("data_category_id") or selected_policy.get("sensitivity_id")
                                if target_id and isinstance(policy_config, dict) and policy_config.get("target_security"):
                                    target_security = policy_config.get("target_security", {})
                                    target_sec = target_security.get(str(target_id), {})
                                    
                                    # Display security settings in a more user-friendly format
                                    st.markdown("<p><strong>Security Settings:</strong></p>", unsafe_allow_html=True)
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown(f"<p>Encryption: <span style='color: {'green' if target_sec.get('encryption_required', False) else 'red'};'>{'Required' if target_sec.get('encryption_required', False) else 'Not Required'}</span></p>", unsafe_allow_html=True)
                                        if target_sec.get("encryption_required", False):
                                            st.markdown(f"<p>Algorithm: {target_sec.get('encryption_algorithm', 'Not Specified')}</p>", unsafe_allow_html=True)
                                    with col2:
                                        st.markdown(f"<p>Masking: <span style='color: {'green' if target_sec.get('masking_required', False) else 'red'};'>{'Required' if target_sec.get('masking_required', False) else 'Not Required'}</span></p>", unsafe_allow_html=True)
                                        if target_sec.get("masking_required", False):
                                            st.markdown(f"<p>Format: {target_sec.get('masking_format', 'Not Specified')}</p>", unsafe_allow_html=True)
                                else:
                                    # Display the full config if target security not found
                                    st.json(policy_config)
                            elif policy_type == "Retention":
                                # Extract retention settings for the specific target
                                target_id = selected_policy.get("data_element_id") or selected_policy.get("data_category_id") or selected_policy.get("sensitivity_id")
                                if target_id and isinstance(policy_config, dict) and policy_config.get("target_retention"):
                                    target_retention = policy_config.get("target_retention", {})
                                    target_ret = target_retention.get(str(target_id), {})
                                    
                                    # Display retention settings in a more user-friendly format
                                    st.markdown("<p><strong>Retention Settings:</strong></p>", unsafe_allow_html=True)
                                    st.markdown(f"<p>Period: {target_ret.get('retention_period', policy_config.get('retention_period', 'Not Specified'))}</p>", unsafe_allow_html=True)
                                    st.markdown(f"<p>Basis: {target_ret.get('retention_basis', policy_config.get('retention_basis', 'Not Specified'))}</p>", unsafe_allow_html=True)
                                    st.markdown(f"<p>Trigger: {target_ret.get('retention_trigger', policy_config.get('retention_trigger', 'Not Specified'))}</p>", unsafe_allow_html=True)
                                    
                                    exceptions = target_ret.get("exceptions", policy_config.get("exceptions", ""))
                                    if exceptions:
                                        st.markdown(f"<p>Exceptions: {exceptions}</p>", unsafe_allow_html=True)
                                else:
                                    # Display the full config if target retention not found
                                    st.json(policy_config)
                            else:
                                # For other policy types, display the full config
                                st.json(policy_config)
        
        # Manage Policies tab
        with policy_tabs[2]:
            st.markdown("""
            <div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: #1565C0; margin-top: 0;">Manage Policies</h4>
                <p style="margin: 0;">Update or modify existing policies in the system.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get all policies
            policies = self.policy_definition_repository.get_all_policies() if self.policy_definition_repository else []
            
            if not policies:
                st.info("No policies available to manage. Create a policy first.")
            else:
                # Create a dropdown to select a policy to update
                policy_options = {}
                for policy in policies:
                    policy_id = policy.get("id")
                    policy_name = policy.get("name", "Unnamed Policy")
                    policy_type = policy.get("policy_type_name", "Unknown")
                    target_name = policy.get("data_element_name") or policy.get("data_category_name") or policy.get("sensitivity_name") or "Global"
                    
                    # Create a descriptive label for the dropdown
                    label = f"{policy_name} - {policy_type} - {target_name} (ID: {policy_id})"
                    policy_options[policy_id] = label
                
                # Policy selection dropdown
                selected_policy_id = st.selectbox(
                    "Select a policy to manage",
                    options=list(policy_options.keys()),
                    format_func=lambda x: policy_options.get(x, "Unknown")
                )
                
                if selected_policy_id:
                    # Get the selected policy
                    selected_policy = None
                    for policy in policies:
                        if policy.get("id") == selected_policy_id:
                            selected_policy = policy
                            break
                    
                    if selected_policy:
                        st.markdown("<h4 style='margin-top: 20px;'>Update Policy</h4>", unsafe_allow_html=True)
                        
                        # Display current policy details
                        with st.expander("Current Policy Details", expanded=True):
                            # Policy metadata
                            policy_name = selected_policy.get("name", "Unnamed Policy")
                            policy_type = selected_policy.get("policy_type_name", "Unknown")
                            policy_type_id = selected_policy.get("policy_type_id")
                            
                            # Determine target details
                            data_element_id = selected_policy.get("data_element_id")
                            data_element_name = selected_policy.get("data_element_name")
                            data_category_id = selected_policy.get("data_category_id")
                            data_category_name = selected_policy.get("data_category_name")
                            sensitivity_id = selected_policy.get("sensitivity_id")
                            sensitivity_name = selected_policy.get("sensitivity_name")
                            
                            # Format dates
                            effective_from = selected_policy.get("effective_from")
                            effective_to = selected_policy.get("effective_to")
                            
                            if effective_from and isinstance(effective_from, str):
                                try:
                                    effective_from = datetime.strptime(effective_from, "%Y-%m-%d").date()
                                except:
                                    pass
                            elif effective_from and isinstance(effective_from, datetime):
                                effective_from = effective_from.date()
                            
                            if effective_to and isinstance(effective_to, str):
                                try:
                                    effective_to = datetime.strptime(effective_to, "%Y-%m-%d").date()
                                except:
                                    pass
                            elif effective_to and isinstance(effective_to, datetime):
                                effective_to = effective_to.date()
                            
                            # Parse policy config
                            policy_config = selected_policy.get("policy_config")
                            if policy_config and isinstance(policy_config, str):
                                try:
                                    policy_config = json.loads(policy_config)
                                except:
                                    pass
                            
                            # Display current values
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"<p><strong>ID:</strong> {selected_policy_id}</p>", unsafe_allow_html=True)
                                st.markdown(f"<p><strong>Name:</strong> {policy_name}</p>", unsafe_allow_html=True)
                                st.markdown(f"<p><strong>Type:</strong> {policy_type}</p>", unsafe_allow_html=True)
                                
                                if data_element_name:
                                    st.markdown(f"<p><strong>Data Element:</strong> {data_element_name}</p>", unsafe_allow_html=True)
                                if data_category_name:
                                    st.markdown(f"<p><strong>Data Category:</strong> {data_category_name}</p>", unsafe_allow_html=True)
                                if sensitivity_name:
                                    st.markdown(f"<p><strong>Sensitivity Level:</strong> {sensitivity_name}</p>", unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f"<p><strong>Effective From:</strong> {effective_from}</p>", unsafe_allow_html=True)
                                st.markdown(f"<p><strong>Effective To:</strong> {effective_to if effective_to else 'Indefinite'}</p>", unsafe_allow_html=True)
                                created_at = selected_policy.get("created_at")
                                if created_at:
                                    st.markdown(f"<p><strong>Created:</strong> {created_at}</p>", unsafe_allow_html=True)
                                updated_at = selected_policy.get("updated_at")
                                if updated_at:
                                    st.markdown(f"<p><strong>Last Updated:</strong> {updated_at}</p>", unsafe_allow_html=True)
                        
                        # Update form
                        with st.form("update_policy_form"):
                            st.markdown("<h5>Update Policy Details</h5>", unsafe_allow_html=True)
                            
                            # Policy name
                            updated_name = st.text_input("Policy Name", value=policy_name)
                            
                            # Effective dates
                            col1, col2 = st.columns(2)
                            with col1:
                                updated_effective_from = st.date_input("Effective From", value=effective_from if effective_from else datetime.now().date())
                            with col2:
                                updated_effective_to = st.date_input("Effective To (Optional)", value=effective_to if effective_to else None)
                            
                            # Policy configuration
                            st.markdown("<h5>Policy Configuration</h5>", unsafe_allow_html=True)
                            
                            # Different configuration options based on policy type
                            if policy_type == "Access Control" and policy_config:
                                # Get target permissions
                                target_permissions = policy_config.get("target_permissions", {})
                                target_id = data_element_id or data_category_id or sensitivity_id
                                target_perms = target_permissions.get(str(target_id), {})
                                
                                # Create toggles for permissions
                                st.markdown(f"<p>Set permissions for target:</p>", unsafe_allow_html=True)
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    updated_read = st.toggle("Read", value=target_perms.get("read", False))
                                with col2:
                                    updated_write = st.toggle("Write", value=target_perms.get("write", False))
                                with col3:
                                    updated_share = st.toggle("Share", value=target_perms.get("share", False))
                                
                                # Update policy config
                                if target_id:
                                    if not target_permissions:
                                        target_permissions = {}
                                    target_permissions[str(target_id)] = {
                                        "read": updated_read,
                                        "write": updated_write,
                                        "share": updated_share
                                    }
                                    updated_policy_config = {
                                        "type": "Access Control",
                                        "target_permissions": target_permissions
                                    }
                            elif policy_type == "Security" and policy_config:
                                # Security settings
                                target_security = policy_config.get("target_security", {})
                                target_id = data_element_id or data_category_id or sensitivity_id
                                target_sec = target_security.get(str(target_id), {})
                                
                                # Create form fields for security settings
                                st.markdown(f"<p>Security settings for target:</p>", unsafe_allow_html=True)
                                col1, col2 = st.columns(2)
                                with col1:
                                    updated_encryption = st.toggle("Encryption Required", value=target_sec.get("encryption_required", False))
                                    if updated_encryption:
                                        updated_encryption_algo = st.selectbox(
                                            "Encryption Algorithm",
                                            options=["AES-256", "RSA-2048", "ChaCha20-Poly1305", "Blowfish"],
                                            index=0 if target_sec.get("encryption_algorithm") == "AES-256" else \
                                                  1 if target_sec.get("encryption_algorithm") == "RSA-2048" else \
                                                  2 if target_sec.get("encryption_algorithm") == "ChaCha20-Poly1305" else \
                                                  3 if target_sec.get("encryption_algorithm") == "Blowfish" else 0
                                        )
                                    else:
                                        updated_encryption_algo = None
                                
                                with col2:
                                    updated_masking = st.toggle("Masking Required", value=target_sec.get("masking_required", False))
                                    if updated_masking:
                                        updated_masking_format = st.text_input(
                                            "Masking Format",
                                            value=target_sec.get("masking_format", "XXXX-XXXX-XXXX-####")
                                        )
                                    else:
                                        updated_masking_format = None
                                
                                # Update policy config
                                if target_id:
                                    if not target_security:
                                        target_security = {}
                                    target_security[str(target_id)] = {
                                        "encryption_required": updated_encryption,
                                        "encryption_algorithm": updated_encryption_algo,
                                        "masking_required": updated_masking,
                                        "masking_format": updated_masking_format
                                    }
                                    updated_policy_config = {
                                        "encryption_required": updated_encryption,
                                        "masking_required": updated_masking,
                                        "target_security": target_security
                                    }
                            elif policy_type == "Retention" and policy_config:
                                # Retention settings
                                target_retention = policy_config.get("target_retention", {})
                                target_id = data_element_id or data_category_id or sensitivity_id
                                target_ret = target_retention.get(str(target_id), {})
                                
                                # Create form fields for retention settings
                                st.markdown(f"<p>Retention settings for target:</p>", unsafe_allow_html=True)
                                
                                # Retention period
                                retention_period_options = ["30 days", "90 days", "1 year", "3 years", "5 years", "7 years", "10 years", "Indefinite", "Custom"]
                                current_period = target_ret.get("retention_period", policy_config.get("retention_period", "7 years"))
                                period_index = next((i for i, p in enumerate(retention_period_options) if p == current_period), 5)  # Default to 7 years
                                
                                updated_retention_period = st.selectbox(
                                    "Retention Period",
                                    options=retention_period_options,
                                    index=period_index
                                )
                                
                                if updated_retention_period == "Custom":
                                    updated_retention_period = st.text_input("Custom Retention Period", value=current_period)
                                
                                # Retention basis
                                basis_options = ["Legal Requirement", "Regulatory Compliance", "Business Need", "Industry Standard", "Custom"]
                                current_basis = target_ret.get("retention_basis", policy_config.get("retention_basis", "Legal Requirement"))
                                basis_index = next((i for i, b in enumerate(basis_options) if b == current_basis), 0)  # Default to Legal Requirement
                                
                                updated_retention_basis = st.selectbox(
                                    "Retention Basis",
                                    options=basis_options,
                                    index=basis_index
                                )
                                
                                if updated_retention_basis == "Custom":
                                    updated_retention_basis = st.text_input("Custom Retention Basis", value=current_basis)
                                
                                # Retention trigger
                                trigger_options = ["creation_date", "last_modified", "last_accessed", "custom_event"]
                                current_trigger = target_ret.get("retention_trigger", policy_config.get("retention_trigger", "creation_date"))
                                trigger_index = next((i for i, t in enumerate(trigger_options) if t == current_trigger), 0)  # Default to creation_date
                                
                                updated_retention_trigger = st.selectbox(
                                    "Retention Trigger",
                                    options=trigger_options,
                                    index=trigger_index
                                )
                                
                                # Exceptions
                                current_exceptions = target_ret.get("exceptions", policy_config.get("exceptions", ""))
                                updated_exceptions = st.text_area("Exceptions (Optional)", value=current_exceptions)
                                
                                # Update policy config
                                if target_id:
                                    if not target_retention:
                                        target_retention = {}
                                    target_retention[str(target_id)] = {
                                        "retention_period": updated_retention_period,
                                        "retention_basis": updated_retention_basis,
                                        "retention_trigger": updated_retention_trigger,
                                        "exceptions": updated_exceptions
                                    }
                                    updated_policy_config = {
                                        "retention_period": updated_retention_period,
                                        "retention_basis": updated_retention_basis,
                                        "retention_trigger": updated_retention_trigger,
                                        "exceptions": updated_exceptions,
                                        "target_retention": target_retention
                                    }
                            else:
                                # For other policy types or if no config, provide a JSON editor
                                policy_config_str = json.dumps(policy_config, indent=2) if policy_config else "{}"
                                updated_policy_config_str = st.text_area("Policy Configuration (JSON)", value=policy_config_str, height=300)
                                try:
                                    updated_policy_config = json.loads(updated_policy_config_str)
                                except json.JSONDecodeError:
                                    st.error("Invalid JSON configuration. Please check the format.")
                                    updated_policy_config = policy_config
                            
                            # Submit button with prominent styling
                            st.markdown("""
                            <style>
                            div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
                                background-color: #1565C0;
                                color: white;
                                border-radius: 4px;
                                padding: 8px 16px;
                                font-weight: bold;
                                border: none;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                transition: all 0.2s ease;
                            }
                            div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
                                background-color: #0D47A1;
                                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            submit_button = st.form_submit_button("Update Policy", type="primary")
                        
                        if submit_button:
                            # Convert dates to string format
                            effective_from_str = updated_effective_from.strftime('%Y-%m-%d') if updated_effective_from else None
                            effective_to_str = updated_effective_to.strftime('%Y-%m-%d') if updated_effective_to else None
                            
                            # Update the policy
                            success = self.policy_definition_repository.update_policy(
                                policy_id=selected_policy_id,
                                policy_type_id=policy_type_id,  # Keep the same policy type
                                data_element_id=data_element_id,  # Keep the same target
                                data_category_id=data_category_id,
                                sensitivity_id=sensitivity_id,
                                policy_config=updated_policy_config,
                                effective_from=effective_from_str,
                                effective_to=effective_to_str
                            )
                            
                            if success:
                                st.markdown("""
                                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; margin: 15px 0;">
                                    <h4 style="color: #2E7D32; margin-top: 0;">Success!</h4>
                                    <p style="margin: 5px 0;">The policy has been updated successfully.</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Add a button to view the updated policy
                                st.button("View Updated Policy", on_click=lambda: st.session_state.update({"active_tab": "View Policies"}))
                                
                                # Refresh the page
                                st.rerun()
                            else:
                                st.markdown("""
                                <div style="background-color: #FFEBEE; padding: 15px; border-radius: 8px; margin: 15px 0;">
                                    <h4 style="color: #C62828; margin-top: 0;">Error</h4>
                                    <p style="margin: 5px 0;">Failed to update the policy. Please try again.</p>
                                </div>
                                """, unsafe_allow_html=True)
                                st.markdown("<h5 style='margin-top: 15px;'>Configuration</h5>", unsafe_allow_html=True)
                                st.json(policy_config)
    
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
        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #1565C0; margin-top: 0;">Policy Groups & Overrides</h3>
            <p style="margin: 0;">Organize related policies into groups and define context-specific overrides.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add CSS for policy groups cards - without affecting main menu buttons
        st.markdown("""
        <style>
        /* Custom styling for policy group buttons */
        .policy-group-btn {
            background-color: #5E35B1;
            color: white;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
            display: inline-block;
        }
        .policy-group-btn:hover {
            background-color: #4527A0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .group-card {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            border-left: 5px solid #5E35B1;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .policy-group-card {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 3px solid #5E35B1;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        .policy-group-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .group-tag {
            background-color: #E8EAF6;
            color: #3949AB;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-right: 5px;
            display: inline-block;
        }
        .status-active {
            background-color: #E8F5E9;
            color: #2E7D32;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        .status-inactive {
            background-color: #FFEBEE;
            color: #C62828;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create tabs for Policy Groups and Overrides
        group_tabs = st.tabs(["Define Policy Groups", "View Policy Groups", "Create Policy Overrides", "View Policy Overrides"])
        
        # Define Policy Groups tab
        with group_tabs[0]:
            st.markdown("""
            <div style="background-color: #EDE7F6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: #5E35B1; margin-top: 0;">Define Policy Groups</h4>
                <p style="margin: 0;">Create and manage policy groups to organize related policies.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create new policy group form
            with st.container():
                st.markdown("<h5 style='margin-bottom: 15px;'>Create New Policy Group</h5>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    group_name = st.text_input("Group Name", key="group_name_input")
                    group_version = st.text_input("Version", value="1.0", key="group_version_input")
                with col2:
                    is_active = st.checkbox("Active", value=True, key="group_active_checkbox")
                
                group_description = st.text_area("Description", key="group_desc_input", height=100)
                
                # Add CSS for the create button
                # Add CSS for policy group buttons with specific key selector to avoid affecting main menu
                st.markdown("""
                <style>
                /* Target only the specific button by its key */
                [data-testid="baseButton-secondary"][kind="secondary"][data-testid*="create_group_btn"] {
                    background-color: #5E35B1 !important;
                    color: white !important;
                    border-radius: 4px !important;
                    padding: 8px 16px !important;
                    font-weight: bold !important;
                    border: none !important;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                }
                [data-testid="baseButton-secondary"][kind="secondary"][data-testid*="create_group_btn"]:hover {
                    background-color: #4527A0 !important;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                if st.button("Create Policy Group", key="create_group_btn"):
                    if self.policy_definition_repository and group_name:
                        self.policy_definition_repository.create_policy_group(group_name, group_description, group_version, is_active)
                        st.markdown("""
                        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <h4 style="color: #2E7D32; margin-top: 0;">Success!</h4>
                            <p style="margin: 5px 0;">Policy group created successfully.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        # Rerun the app to refresh the UI
                        st.rerun()
                    elif not group_name:
                        st.markdown("""
                        <div style="background-color: #FFF3E0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <h4 style="color: #E65100; margin-top: 0;">Warning</h4>
                            <p style="margin: 5px 0;">Please enter a group name.</p>
                        </div>
                        """, unsafe_allow_html=True)
            
        # View Policy Groups tab
        with group_tabs[1]:
            st.markdown("""
            <div style="background-color: #EDE7F6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: #5E35B1; margin-top: 0;">View Policy Groups</h4>
                <p style="margin: 0;">Browse and explore policy groups and their associated policies.</p>
            </div>
            """, unsafe_allow_html=True)
            
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
                        # Display group details in a card
                        st.markdown(f"""
                        <div style="background-color: white; border-radius: 8px; padding: 20px; margin-top: 20px; border-left: 5px solid #5E35B1; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <h3 style="margin: 0;">{selected_group['name']} <span style="font-size: 14px; color: #757575;">v{selected_group['version']}</span></h3>
                                <span class="group-status {'status-active' if selected_group['is_active'] else 'status-inactive'}">
                                    {'Active' if selected_group['is_active'] else 'Inactive'}
                                </span>
                            </div>
                            <p style="margin-bottom: 15px;">{selected_group['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")
                        
                        # Get policies in the group
                        group_policies = self.policy_definition_repository.get_policies_in_group(selected_group_id) if self.policy_definition_repository else []
                        
                        if not group_policies:
                            st.markdown("""
                            <div style="background-color: #F5F5F5; padding: 15px; border-radius: 8px; margin-top: 15px;">
                                <p style="margin: 0; color: #616161;"><i>No policies in this group yet.</i></p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Display policies header
                            st.markdown("<h4 style='margin-top: 20px;'>Policies in this Group</h4>", unsafe_allow_html=True)
                            
                            # Display policies in a modern way
                            for i, p in enumerate(group_policies):
                                target_name = p.get("data_element_name") or p.get("data_category_name") or p.get("sensitivity_name") or "Global"
                                policy_type = p.get("policy_type_name", "Unknown")
                                target_system = p.get("target_system", "")
                                
                                # Create a card for each policy in the group with more details
                                # Extract policy configuration if available
                                policy_config = {}
                                if p.get("policy_config"):
                                    try:
                                        if isinstance(p["policy_config"], str):
                                            full_config = json.loads(p["policy_config"])
                                        else:
                                            full_config = p["policy_config"]
                                            
                                        # Print for debugging
                                        print(f"Full policy config for {target_name}: {full_config}")
                                        print(f"Policy config type: {type(full_config)}")
                                        
                                        # Check if we have a target_security section with data element specific configs
                                        if isinstance(full_config, dict) and "target_security" in full_config and p.get("data_element_id"):
                                            data_element_id = str(p["data_element_id"])
                                            print(f"Looking for data element ID: {data_element_id} in target_security")
                                            
                                            # Extract only the config for this specific data element
                                            if data_element_id in full_config["target_security"]:
                                                policy_config = full_config["target_security"][data_element_id]
                                                print(f"Found specific config for data element {data_element_id}: {policy_config}")
                                            else:
                                                # Fallback to root config if data element specific one not found
                                                policy_config = {k: v for k, v in full_config.items() if k != "target_security"}
                                                print(f"Using root config (no specific config for element {data_element_id}): {policy_config}")
                                        else:
                                            # No target_security section, use the whole config
                                            policy_config = full_config
                                            print(f"Using full config (no target_security section): {policy_config}")
                                    except Exception as e:
                                        print(f"Error parsing policy config: {e}")
                                        policy_config = {}
                                
                                # Format effective dates if available
                                effective_from = p.get("effective_from")
                                effective_to = p.get("effective_to")
                                
                                if effective_from and isinstance(effective_from, str):
                                    try:
                                        effective_from = datetime.strptime(effective_from, "%Y-%m-%d").date()
                                    except:
                                        pass
                                elif effective_from and isinstance(effective_from, datetime):
                                    effective_from = effective_from.date()
                                
                                if effective_to and isinstance(effective_to, str):
                                    try:
                                        effective_to = datetime.strptime(effective_to, "%Y-%m-%d").date()
                                    except:
                                        pass
                                elif effective_to and isinstance(effective_to, datetime):
                                    effective_to = effective_to.date()
                                
                                # Instead of building HTML with multi-line strings, create a simpler approach
                                # Start with an empty list to build the HTML parts
                                html_parts = []
                                
                                # Add the card header - without ID
                                html_parts.append(f'<div class="policy-group-card">')
                                html_parts.append(f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">')
                                html_parts.append(f'<div><span class="group-tag">{policy_type}</span> <strong style="font-size: 16px;">{target_name}</strong></div>')
                                html_parts.append(f'</div>')
                                
                                # Add the details section container
                                html_parts.append(f'<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">')
                                html_parts.append(f'<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 5px;">')
                                
                                # Build policy details directly into HTML parts list
                                if policy_config:
                                    # For Access Control policies
                                    if policy_type == "Access Control":
                                        # Check for read/write/share permissions
                                        read_permission = policy_config.get("read", False)
                                        write_permission = policy_config.get("write", False)
                                        share_permission = policy_config.get("share", False)
                                        
                                        # Also check for actions array for backward compatibility
                                        actions = policy_config.get("actions", [])
                                        if "read" in actions:
                                            read_permission = True
                                        if "write" in actions:
                                            write_permission = True
                                        if "share" in actions:
                                            share_permission = True
                                        
                                        # Create permissions display with check/cross icons
                                        html_parts.append(f'<div style="flex: 1;">')
                                        html_parts.append(f'<span style="font-size: 12px; color: #616161;">Permissions:</span>')
                                        html_parts.append(f'<div style="margin-top: 8px;">')
                                        
                                        # Read permission
                                        html_parts.append(f'<div style="display: flex; align-items: center; margin-bottom: 5px;">')
                                        if read_permission:
                                            html_parts.append(f'<span style="color: #4CAF50; margin-right: 8px;">✓</span>')
                                        else:
                                            html_parts.append(f'<span style="color: #F44336; margin-right: 8px;">✗</span>')
                                        html_parts.append(f'<span style="font-size: 13px;">Read</span>')
                                        html_parts.append(f'</div>')
                                        
                                        # Write permission
                                        html_parts.append(f'<div style="display: flex; align-items: center; margin-bottom: 5px;">')
                                        if write_permission:
                                            html_parts.append(f'<span style="color: #4CAF50; margin-right: 8px;">✓</span>')
                                        else:
                                            html_parts.append(f'<span style="color: #F44336; margin-right: 8px;">✗</span>')
                                        html_parts.append(f'<span style="font-size: 13px;">Write</span>')
                                        html_parts.append(f'</div>')
                                        
                                        # Share permission
                                        html_parts.append(f'<div style="display: flex; align-items: center;">')
                                        if share_permission:
                                            html_parts.append(f'<span style="color: #4CAF50; margin-right: 8px;">✓</span>')
                                        else:
                                            html_parts.append(f'<span style="color: #F44336; margin-right: 8px;">✗</span>')
                                        html_parts.append(f'<span style="font-size: 13px;">Share</span>')
                                        html_parts.append(f'</div>')
                                        
                                        html_parts.append(f'</div></div>')
                                    
                                    # For Security policies
                                    elif policy_type == "Security":
                                        # Initialize security policy attributes with defaults
                                        encryption_required = False
                                        encryption_algorithm = "Not specified"
                                        masking_required = False
                                        masking_format = "Not specified"
                                        access_logging = False
                                        
                                        # First check for properties at the root level
                                        if isinstance(policy_config, dict):
                                            # Encryption settings
                                            if "encryption_required" in policy_config:
                                                encryption_required = bool(policy_config["encryption_required"])
                                            if "encryption_algorithm" in policy_config:
                                                encryption_algorithm = policy_config["encryption_algorithm"]
                                                
                                            # Masking settings
                                            if "masking_required" in policy_config:
                                                masking_required = bool(policy_config["masking_required"])
                                            if "masking_format" in policy_config:
                                                masking_format = policy_config["masking_format"]
                                                # If format is specified, masking is implicitly required
                                                if masking_format and masking_format != "Not specified":
                                                    masking_required = True
                                                    
                                            # Access logging
                                            if "access_logging" in policy_config:
                                                access_logging = bool(policy_config["access_logging"])
                                        
                                        # Then check in settings if properties weren't found at root level
                                        if isinstance(policy_config, dict) and "settings" in policy_config and isinstance(policy_config["settings"], dict):
                                            settings = policy_config["settings"]
                                            
                                            # Encryption settings in nested settings object
                                            if not encryption_required and "encryption_required" in settings:
                                                encryption_required = bool(settings["encryption_required"])
                                            if encryption_algorithm == "Not specified" and "encryption_algorithm" in settings:
                                                encryption_algorithm = settings["encryption_algorithm"]
                                                
                                            # Masking settings in nested settings object
                                            if not masking_required and "masking_required" in settings:
                                                masking_required = bool(settings["masking_required"])
                                            if masking_format == "Not specified" and "masking_format" in settings:
                                                masking_format = settings["masking_format"]
                                                # If format is specified, masking is implicitly required
                                                if masking_format and masking_format != "Not specified":
                                                    masking_required = True
                                                    
                                            # Access logging in nested settings object
                                            if not access_logging and "access_logging" in settings:
                                                access_logging = bool(settings["access_logging"])
                                        # Print for debugging
                                        print(f"Final security settings for {target_name}:")
                                        print(f"  encryption_required: {encryption_required}")
                                        print(f"  encryption_algorithm: {encryption_algorithm}")
                                        print(f"  masking_required: {masking_required}")
                                        print(f"  masking_format: {masking_format}")
                                        print(f"  access_logging: {access_logging}")
                                        
                                        # Create security requirements display with compact format using check/cross icons
                                        html_parts.append(f'<div style="flex: 1;">')
                                        html_parts.append(f'<div style="margin-top: 8px;">')
                                        
                                        # Encryption with inline algorithm - only show algorithm if encryption is required
                                        html_parts.append(f'<div style="display: flex; align-items: center; margin-bottom: 8px;">')
                                        if encryption_required:
                                            html_parts.append(f'<span style="color: #4CAF50; margin-right: 8px;">✓</span>')
                                            # Only show algorithm if encryption is required
                                            if encryption_algorithm and encryption_algorithm != "Not specified":
                                                html_parts.append(f'<span style="font-size: 13px;">Encryption: <span style="color: #1565C0;">{encryption_algorithm}</span></span>')
                                            else:
                                                html_parts.append(f'<span style="font-size: 13px;">Encryption</span>')
                                        else:
                                            html_parts.append(f'<span style="color: #F44336; margin-right: 8px;">✗</span>')
                                            html_parts.append(f'<span style="font-size: 13px;">Encryption</span>')
                                        html_parts.append(f'</div>')
                                        
                                        # Masking with inline format
                                        # If we have a masking format, always show masking as required
                                        if masking_format and masking_format != "Not specified":
                                            masking_required = True
                                        
                                        html_parts.append(f'<div style="display: flex; align-items: center; margin-bottom: 8px;">')
                                        if masking_required:
                                            html_parts.append(f'<span style="color: #4CAF50; margin-right: 8px;">✓</span>')
                                            # Only show format if masking is required
                                            if masking_format and masking_format != "Not specified":
                                                html_parts.append(f'<span style="font-size: 13px;">Masking: <span style="color: #1565C0;">{masking_format}</span></span>')
                                            else:
                                                html_parts.append(f'<span style="font-size: 13px;">Masking</span>')
                                        else:
                                            html_parts.append(f'<span style="color: #F44336; margin-right: 8px;">✗</span>')
                                            html_parts.append(f'<span style="font-size: 13px;">Masking</span>')
                                        html_parts.append(f'</div>')
                                        
                                        # Access logging
                                        html_parts.append(f'<div style="display: flex; align-items: center;">')
                                        if access_logging:
                                            html_parts.append(f'<span style="color: #4CAF50; margin-right: 8px;">✓</span>')
                                        else:
                                            html_parts.append(f'<span style="color: #F44336; margin-right: 8px;">✗</span>')
                                        html_parts.append(f'<span style="font-size: 13px;">Access Logging</span>')
                                        html_parts.append(f'</div>')
                                        
                                        html_parts.append(f'</div></div>')
                                    
                                    # For Retention policies
                                    elif policy_type == "Retention":
                                        retention_period = policy_config.get("retention_period", "Not specified")
                                        html_parts.append(f'<div style="flex: 1;">')
                                        html_parts.append(f'<span style="font-size: 12px; color: #616161;">Retention Period:</span>')
                                        html_parts.append(f'<div style="margin-top: 3px; font-size: 13px;">{retention_period}</div>')
                                        html_parts.append(f'</div>')
                                
                                # Add target system if available
                                if target_system:
                                    html_parts.append(f'<div style="flex: 1;">')
                                    html_parts.append(f'<span style="font-size: 12px; color: #616161;">Target System:</span>')
                                    html_parts.append(f'<div style="margin-top: 3px; font-size: 13px;">{target_system}</div>')
                                    html_parts.append(f'</div>')
                                
                                # Add effective dates
                                effective_period = f"{effective_from if effective_from else 'Always'} - {effective_to if effective_to else 'Indefinite'}"
                                html_parts.append(f'<div style="flex: 1;">')
                                html_parts.append(f'<span style="font-size: 12px; color: #616161;">Effective Period:</span>')
                                html_parts.append(f'<div style="margin-top: 3px; font-size: 13px;">{effective_period}</div>')
                                html_parts.append(f'</div>')
                                
                                # Close the HTML structure
                                html_parts.append(f'</div></div></div>')
                                
                                # Join all HTML parts and render the complete card
                                card_html = ''.join(html_parts)
                                st.markdown(card_html, unsafe_allow_html=True)
            
        # Create Policy Overrides tab
        with group_tabs[2]:
            st.markdown("""
            <div style="background-color: #EDE7F6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: #5E35B1; margin-top: 0;">Create Policy Overrides</h4>
                <p style="margin: 0;">Create context-specific overrides to customize policy behavior based on purpose, role, region, or other criteria.</p>
            </div>
            """, unsafe_allow_html=True)
            # Get policy groups
            policy_groups = self.policy_definition_repository.get_all_policy_groups() if self.policy_definition_repository else []
            
            if not policy_groups:
                st.markdown("""
                <div style="background-color: #FFF3E0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4 style="color: #E65100; margin-top: 0;">Warning</h4>
                    <p style="margin: 5px 0;">No policy groups available. Please create a policy group first.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<h5 style='margin-bottom: 15px;'>Create New Policy Override</h5>", unsafe_allow_html=True)
                    
                # Policy Group selector with enhanced styling
                policy_group_options = {pg["id"]: pg["name"] for pg in policy_groups}
                
                selected_policy_group_id = st.selectbox(
                    "Select Policy Group",
                    options=list(policy_group_options.keys()),
                    format_func=lambda x: policy_group_options.get(x, "Unknown"),
                    key="override_group_select"
                )
                
                # Context criteria section with modern styling
                st.markdown("""
                <div style="background-color: #F5F5F5; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h5 style="margin-top: 0; color: #5E35B1;">Context Criteria</h5>
                    <p style="margin: 0; font-size: 14px; color: #616161;">Define when this override should apply based on context.</p>
                </div>
                """, unsafe_allow_html=True)
                    
                # Purpose selector
                purposes = self.glossary_repository.get_purposes() if self.glossary_repository else []
                
                col1, col2 = st.columns(2)
                with col1:
                    if purposes:
                        purpose_options = {p["id"]: p["name"] for p in purposes}
                        selected_purpose_id = st.selectbox(
                            "Purpose",
                            options=[None] + list(purpose_options.keys()),
                            format_func=lambda x: purpose_options.get(x, "Any") if x else "Any",
                            key="override_purpose_select"
                        )
                    else:
                        st.info("No purposes available.")
                        selected_purpose_id = None
                        
                    # Region selector
                    regions = self.policy_definition_repository.get_all_regions() if self.policy_definition_repository else []
                    
                    if regions:
                        region_options = {r["id"]: r["name"] for r in regions}
                        selected_region_id = st.selectbox(
                            "Region",
                            options=[None] + list(region_options.keys()),
                            format_func=lambda x: region_options.get(x, "Any") if x else "Any",
                            key="override_region_select"
                        )
                    else:
                        st.info("No regions available.")
                        selected_region_id = None
                    
                with col2:
                    # Role selector
                    roles = self.glossary_repository.get_external_roles() if self.glossary_repository else []
                    
                    if roles:
                        # Handle roles as tuples (id, name, description, source_system, source_role_name, asset_id)
                        role_options = {r[0]: r[1] for r in roles}  # Use index 0 for id, index 1 for name
                        selected_role_id = st.selectbox(
                            "Role",
                            options=[None] + list(role_options.keys()),
                            format_func=lambda x: role_options.get(x, "Any") if x else "Any",
                            key="override_role_select"
                        )
                    else:
                        st.info("No roles available.")
                        selected_role_id = None
                    
                    # Priority input
                    manual_priority = st.number_input("Priority", min_value=0, max_value=100, value=10, key="priority_input", 
                                                   help="Higher priority overrides take precedence when multiple overrides match")
                    
                # Context tags with improved styling
                st.markdown("<p><strong>Context Tags</strong> <span style='color: #757575; font-size: 12px;'>(JSON format)</span></p>", unsafe_allow_html=True)
                context_tags = st.text_area("Context Tags", key="context_tags_textarea", height=100, label_visibility="collapsed", 
                                          placeholder='{"department": "finance", "environment": "production"}')
                
                # Effective dates section
                st.markdown("<h5 style='margin-top: 20px;'>Effective Period</h5>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    effective_from = st.date_input("Effective From", value=datetime.now().date(), key="override_from_date")
                    is_active = st.checkbox("Active", value=True, key="override_active_checkbox")
                with col2:
                    effective_to = st.date_input("Effective To (Optional)", value=None, key="override_to_date")
                    
                # Add CSS for the create override button with specific key selector
                st.markdown("""
                <style>
                /* Target only the specific button by its key */
                [data-testid="baseButton-secondary"][kind="secondary"][data-testid*="create_override_btn"] {
                    background-color: #5E35B1 !important;
                    color: white !important;
                    border-radius: 4px !important;
                    padding: 8px 16px !important;
                    font-weight: bold !important;
                    border: none !important;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                    margin-top: 15px !important;
                }
                [data-testid="baseButton-secondary"][kind="secondary"][data-testid*="create_override_btn"]:hover {
                    background-color: #4527A0 !important;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
                }
                </style>
                """, unsafe_allow_html=True)
                    
                # Using regular st.button without the custom HTML
                create_btn_clicked = st.button("Create Override", key="create_override_btn")
                
                if create_btn_clicked:
                    if not selected_policy_group_id:
                        st.markdown("""
                        <div style="background-color: #FFEBEE; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <h4 style="color: #C62828; margin-top: 0;">Error</h4>
                            <p style="margin: 5px 0;">Please select a policy group.</p>
                        </div>
                        """, unsafe_allow_html=True)
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
                                st.markdown("""
                                <div style="background-color: #FFEBEE; padding: 15px; border-radius: 8px; margin: 15px 0;">
                                    <h4 style="color: #C62828; margin-top: 0;">Error</h4>
                                    <p style="margin: 5px 0;">Context tags must be valid JSON. Please check the format.</p>
                                </div>
                                """, unsafe_allow_html=True)
                                return
                            
                            # Create the context policy group
                        if self.policy_definition_repository:
                            try:
                                # Create context policy group
                                context_policy_group_id = self.policy_definition_repository.create_context_policy_group(
                                    policy_group_id=selected_policy_group_id,
                                    purpose_id=selected_purpose_id,
                                    role_id=selected_role_id,
                                    region_id=selected_region_id,
                                    context_tags=tags_json,
                                    priority=manual_priority,
                                    is_active=is_active,
                                    effective_from=from_date,
                                    effective_to=to_date
                                )
                                
                                if context_policy_group_id:
                                    st.markdown("""
                                    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; margin: 15px 0;">
                                        <h4 style="color: #2E7D32; margin-top: 0;">Success</h4>
                                        <p style="margin: 5px 0;">Policy override created successfully!</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown("""
                                    <div style="background-color: #FFEBEE; padding: 15px; border-radius: 8px; margin: 15px 0;">
                                        <h4 style="color: #C62828; margin-top: 0;">Error</h4>
                                        <p style="margin: 5px 0;">Failed to create policy override. Please try again.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            except Exception as e:
                                st.markdown(f"""
                                <div style="background-color: #FFEBEE; padding: 15px; border-radius: 8px; margin: 15px 0;">
                                    <h4 style="color: #C62828; margin-top: 0;">Error</h4>
                                    <p style="margin: 5px 0;">An error occurred: {str(e)}</p>
                                </div>
                                """, unsafe_allow_html=True)
            
        # View Policy Overrides tab
        with group_tabs[3]:
            # Add explanatory section at the top
            st.markdown("""
            <div style="background-color: #F3E5F5; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: #6A1B9A; margin-top: 0;">View Policy Overrides</h4>
                <p style="margin-bottom: 10px;">Policy overrides allow you to customize how policies are applied in specific contexts:</p>
                <ul style="margin-bottom: 0;">
                    <li><strong>Purpose-based:</strong> Apply different policies based on business purpose (e.g., Customer Support vs Marketing)</li>
                    <li><strong>Role-based:</strong> Customize policies for specific user roles (e.g., Data Analyst vs Administrator)</li>
                    <li><strong>Region-based:</strong> Adapt policies to meet regional regulatory requirements</li>
                    <li><strong>Priority:</strong> Higher priority overrides take precedence when multiple contexts match</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Get existing context overrides
            context_overrides = self.policy_definition_repository.get_all_context_policy_groups() if self.policy_definition_repository else []
            
            # Add filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.selectbox("Filter by Status", ["All", "Active", "Inactive"], key="override_status_filter")
            with col2:
                # Get all purposes for filtering
                purposes = self.glossary_repository.get_purposes() if self.glossary_repository else []
                purpose_options = {p["id"]: p["name"] for p in purposes} if purposes else {}
                purpose_options[0] = "All Purposes"
                filter_purpose = st.selectbox("Filter by Purpose", 
                                           options=list(purpose_options.keys()),
                                           format_func=lambda x: purpose_options.get(x, "All"),
                                           key="override_purpose_filter")
            with col3:
                sort_by = st.selectbox("Sort by", ["Priority (High to Low)", "Priority (Low to High)", "Newest First", "Oldest First"], key="override_sort")
                
            # Apply filters and sorting
            filtered_overrides = []
            for override in context_overrides:
                # Check status filter
                is_active = override.get("is_active", False)
                current_date = datetime.now().date()
                
                if override.get("effective_from") and isinstance(override["effective_from"], str):
                    try:
                        effective_from = datetime.strptime(override["effective_from"], "%Y-%m-%d").date()
                        if effective_from > current_date:
                            is_active = False
                    except:
                        pass
                
                if override.get("effective_to") and isinstance(override["effective_to"], str):
                    try:
                        effective_to = datetime.strptime(override["effective_to"], "%Y-%m-%d").date()
                        if effective_to < current_date:
                            is_active = False
                    except:
                        pass
                
                if filter_status == "Active" and not is_active:
                    continue
                if filter_status == "Inactive" and is_active:
                    continue
                
                # Check purpose filter
                if filter_purpose != 0 and override.get("purpose_id") != filter_purpose:
                    continue
                
                filtered_overrides.append(override)
                
            # Apply sorting
            if sort_by == "Priority (High to Low)":
                filtered_overrides.sort(key=lambda x: x.get("manual_priority", 0), reverse=True)
            elif sort_by == "Priority (Low to High)":
                filtered_overrides.sort(key=lambda x: x.get("manual_priority", 0))
            elif sort_by == "Newest First":
                filtered_overrides.sort(key=lambda x: x.get("created_at", "2000-01-01"), reverse=True)
            elif sort_by == "Oldest First":
                filtered_overrides.sort(key=lambda x: x.get("created_at", "2000-01-01"))
            
            if not filtered_overrides:
                st.markdown("""
                <div style="background-color: #F5F5F5; padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <p style="margin: 0; color: #616161;"><i>No policy overrides match your filter criteria.</i></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display count of overrides
                st.markdown(f"<h5 style='margin-bottom: 15px;'>Showing {len(filtered_overrides)} Policy Override{'' if len(filtered_overrides) == 1 else 's'}</h5>", unsafe_allow_html=True)
                
                # Add legend for status indicators
                st.markdown("""
                <div style="display: flex; gap: 15px; margin-bottom: 15px; font-size: 12px;">
                    <div style="display: flex; align-items: center;">
                        <span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #4CAF50; margin-right: 5px;"></span>
                        <span>Active</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background-color: #F44336; margin-right: 5px;"></span>
                        <span>Inactive</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                    
                for override in filtered_overrides:
                    # Get policy group details
                    policy_group_name = "Unknown Group"
                    policy_groups = self.policy_definition_repository.get_all_policy_groups() if self.policy_definition_repository else []
                    for group in policy_groups:
                        if group["id"] == override.get("policy_group_id"):
                            policy_group_name = group["name"]
                            break
                        
                    # Format context criteria
                    context_criteria = []
                    
                    # Purpose
                    if override.get("purpose_id"):
                        purposes = self.glossary_repository.get_purposes() if self.glossary_repository else []
                        for purpose in purposes:
                            if purpose["id"] == override.get("purpose_id"):
                                context_criteria.append(f"Purpose: {purpose['name']}")
                                break
                        
                    # Role
                    if override.get("external_role_id"):
                        roles = self.glossary_repository.get_external_roles() if self.glossary_repository else []
                        for role in roles:
                            if role[0] == override.get("external_role_id"):  # role[0] is the ID
                                context_criteria.append(f"Role: {role[1]}")  # role[1] is the name
                                break
                    
                    # Region
                    if override.get("region_id"):
                        regions = self.policy_definition_repository.get_all_regions() if self.policy_definition_repository else []
                        for region in regions:
                            if region["id"] == override.get("region_id"):
                                context_criteria.append(f"Region: {region['name']}")
                                break
                        
                    # Format dates
                    effective_from = override.get("effective_from")
                    effective_to = override.get("effective_to")
                    
                    if effective_from and isinstance(effective_from, str):
                        try:
                            effective_from = datetime.strptime(effective_from, "%Y-%m-%d").date()
                        except:
                            pass
                    elif effective_from and isinstance(effective_from, datetime):
                        effective_from = effective_from.date()
                    
                    if effective_to and isinstance(effective_to, str):
                        try:
                            effective_to = datetime.strptime(effective_to, "%Y-%m-%d").date()
                        except:
                            pass
                    elif effective_to and isinstance(effective_to, datetime):
                        effective_to = effective_to.date()
                        
                    # Check if override is active
                    is_active = override.get("is_active", False)
                    current_date = datetime.now().date()
                    
                    if effective_from and effective_from > current_date:
                        is_active = False
                    if effective_to and effective_to < current_date:
                        is_active = False
                    # Create a container for each override
                    with st.container():
                        # Use columns for layout
                        col1, col2 = st.columns([3, 1])
                            
                        with col1:
                            # Display override header
                            st.markdown(f"""
                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                <h4 style="margin: 0;">{policy_group_name} Override</h4>
                                <span style="margin-left: 10px;" class="group-status {'status-active' if is_active else 'status-inactive'}">
                                    {'Active' if is_active else 'Inactive'}
                                </span>
                                <span style="margin-left: 10px; background-color: #E8EAF6; color: #3949AB; padding: 3px 8px; border-radius: 12px; font-size: 12px;">
                                    Priority: {override.get('manual_priority', 0)}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display context criteria
                            criteria_html = ''
                            if context_criteria:
                                criteria_html = ''.join([f'<span class="group-tag">{criteria}</span>' for criteria in context_criteria])
                            if override.get('context_tags'):
                                criteria_html += f'<span class="group-tag">Custom Tags</span>'
                            
                            st.markdown(f"""
                            <div style="margin-bottom: 15px;">
                                <p style="margin-bottom: 5px;"><strong>Context Criteria:</strong></p>
                                <div style="display: flex; flex-wrap: wrap; gap: 5px;">
                                    {criteria_html}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display effective dates
                            st.markdown(f"""
                            <div>
                                <p style="margin: 0; font-size: 14px;"><strong>Effective From:</strong> {effective_from}</p>
                                <p style="margin: 0; font-size: 14px;"><strong>Effective To:</strong> {effective_to if effective_to else 'Indefinite'}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Add delete button in the second column
                            with col2:
                                # Create a unique key for each delete button
                                delete_button_key = f"delete_override_{override.get('id')}"
                                if st.button("Delete", key=delete_button_key, type="primary", help="Delete this policy override"):
                                    # Confirm deletion
                                    if st.session_state.get(f"confirm_{delete_button_key}", False):
                                        # Delete the override
                                        if self.policy_definition_repository.delete_context_policy_group(override.get('id')):
                                            st.success("Override deleted successfully!")
                                            # Clear confirmation state and rerun to refresh the UI
                                            st.session_state[f"confirm_{delete_button_key}"] = False
                                            st.rerun()
                                        else:
                                            st.error("Failed to delete override. Please try again.")
                                    else:
                                        # Set confirmation state and show confirmation message
                                        st.session_state[f"confirm_{delete_button_key}"] = True
                                        st.warning("Click 'Delete' again to confirm deletion. This action cannot be undone.")
                        
                            # Add a separator between overrides
                            st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
            
            
            
