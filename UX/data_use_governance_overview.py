import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
import io
import numpy as np

class DataUseGovernanceOverview:
    """Class to render the Data Use Governance Overview page."""
    
    def __init__(self, glossary_repository, regulatory_metadata_repository, policy_repository):
        """Initialize with required repositories."""
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.policy_repository = policy_repository
    
    def render(self):
        """Render the Data Use Governance Overview page with a modern, single-page design."""
        # Custom CSS for modern look and feel
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E88E5;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .section-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #0D47A1;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #E3F2FD;
        }
        
        .subsection-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1565C0;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }
        
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        
        .highlight-text {
            background-color: #E3F2FD;
            padding: 10px;
            border-radius: 5px;
            font-weight: 500;
        }
        
        .step-card {
            background-color: white;
            border-left: 4px solid #1E88E5;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .step-number {
            background-color: #1E88E5;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .feature-card {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-top: 4px solid #1E88E5;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        .feature-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1565C0;
            margin-bottom: 10px;
        }
        
        .feature-description {
            color: #424242;
            margin-bottom: 10px;
        }
        
        .feature-implementation {
            font-size: 0.9rem;
            color: #616161;
            font-style: italic;
        }
        
        .status-complete {
            background-color: #E8F5E9;
            color: #2E7D32;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .architecture-layer {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .layer-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .component-pill {
            background-color: #E3F2FD;
            border-radius: 20px;
            padding: 8px 15px;
            margin: 5px;
            display: inline-block;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Page header
        st.markdown("<h1 class='main-header'>Data Use Governance</h1>", unsafe_allow_html=True)
        
        # Introduction section with hero image/diagram
        self._render_hero_section()
        
        # Use Case Overview
        st.markdown("<h2 class='section-header'>Use Case Overview</h2>", unsafe_allow_html=True)
        self._render_use_case_overview()
        
        # User Journey
        st.markdown("<h2 class='section-header'>User Journey</h2>", unsafe_allow_html=True)
        self._render_user_journey()
        
        # Integration Workflow
        st.markdown("<h2 class='section-header'>Integration Workflow</h2>", unsafe_allow_html=True)
        self._render_workflow_example()
        
        # Features & Implementation
        st.markdown("<h2 class='section-header'>Features & Implementation</h2>", unsafe_allow_html=True)
        self._render_features_implementation()
    
    def _render_hero_section(self):
        """Render the hero section with an overview diagram."""
        # Create two columns for the hero section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style="padding: 20px 0;">
                <h3 style="color: #1565C0; font-weight: 600; margin-bottom: 15px;">Secure, Compliant Data Access</h3>
                <p style="font-size: 1.1rem; line-height: 1.6; color: #424242;">
                    Our Data Use Governance solution empowers organizations to implement purpose-based access controls, 
                    ensuring data is only accessed for legitimate business purposes by authorized roles.
                </p>
                <div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin-top: 20px;">
                    <p style="font-size: 1rem; margin: 0; color: #0D47A1;">
                        <strong>Key Benefits:</strong><br>
                        ✓ Regulatory compliance<br>
                        ✓ Purpose-based access control<br>
                        ✓ Automated security policy generation<br>
                        ✓ Simplified role management
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Create a modern diagram showing the relationships between components
            fig = px.sunburst(
                names=['Data Governance', 'Assets', 'Purposes', 'Roles', 'Policies', 
                       'Tables', 'Columns', 'Business', 'Technical', 'Internal', 'External', 
                       'Data Use', 'Security'],
                parents=['', 'Data Governance', 'Data Governance', 'Data Governance', 'Data Governance',
                         'Assets', 'Assets', 'Purposes', 'Purposes', 'Roles', 'Roles',
                         'Policies', 'Policies'],
                values=[100, 25, 25, 25, 25, 12, 13, 12, 13, 12, 13, 12, 13],
                color_discrete_sequence=px.colors.qualitative.Bold,
                branchvalues='total'
            )
            
            fig.update_layout(
                margin=dict(t=0, l=0, r=0, b=0),
                height=350,
                font=dict(size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Divider
        st.markdown("<hr style='height:1px; margin-top: 20px; margin-bottom: 30px; border:none; background-color:#E0E0E0;'>", unsafe_allow_html=True)
    
    def _render_use_case_overview(self):
        """Render the Use Case Overview section with a modern design."""
        # The Challenge section
        st.markdown("### The Challenge")
        st.write("Organizations today face increasing complexity in managing how data is used across their enterprise:")
        
        challenges = [
            "**Regulatory Compliance**: Meeting requirements from GDPR, CCPA, and other regulations",
            "**Purpose Limitation**: Ensuring data is only used for specified, legitimate purposes",
            "**Role-Based Access**: Implementing proper access controls based on user roles",
            "**Data Masking**: Protecting sensitive information while enabling business functions"
        ]
        
        for challenge in challenges:
            st.markdown(f"- {challenge}")
            
        # Our Solution section
        st.markdown("### Our Solution")
        st.write("The Data Use Governance module provides a comprehensive framework for:")
        
        solutions = [
            "**Purpose Definition**: Define clear business purposes for data use",
            "**Policy Creation**: Create policies that govern how data can be used",
            "**Role Management**: Define and manage roles with appropriate access levels",
            "**Purpose Determination**: Automatically determine purposes through processing activities or user requests",
            "**Security Policy Generation**: Automatically generate security policies for any target system"
        ]
        
        for i, solution in enumerate(solutions):
            st.markdown(f"{i+1}. {solution}")
        
        # Control Plane Architecture section
        st.markdown("### Control Plane Architecture")
        st.write("This architecture serves as the control plane that governs data access across multiple external systems:")
        
        architecture_features = [
            "Centralized policy management with distributed enforcement",
            "Real-time role detection and policy application",
            "Hierarchical policy resolution and dynamic DDL generation",
            "Automated governance workflows with human oversight"
        ]
        
        for feature in architecture_features:
            st.markdown(f"- {feature}")
    
    def _render_user_journey(self):
        """Render the User Journey section with a modern design."""
        st.markdown("""
        <p style="font-size: 1.1rem; margin-bottom: 20px;">The Data Use Governance module provides a streamlined workflow for implementing data use controls:</p>
        """, unsafe_allow_html=True)
        
        # Create a timeline of the user journey with modern styling
        journey_steps = [
            {
                "step": "Define Assets",
                "description": "Catalog data assets including tables, columns, and sensitivity",
                "icon": "📊",
                "color": "#1E88E5"
            },
            {
                "step": "Define Purposes",
                "description": "Create business purposes that justify data access",
                "icon": "🎯",
                "color": "#43A047"
            },
            {
                "step": "Create Policies",
                "description": "Define policies for data usage and protection",
                "icon": "📋",
                "color": "#8E24AA"
            },
            {
                "step": "Manage Roles",
                "description": "Define internal and external roles with appropriate access levels",
                "icon": "👥",
                "color": "#E53935"
            },
            {
                "step": "Map Assets to Purposes",
                "description": "Associate data assets with legitimate business purposes",
                "icon": "🔄",
                "color": "#FB8C00"
            },
            {
                "step": "Map Purposes to Roles",
                "description": "Determine which roles can access data for specific purposes",
                "icon": "🔗",
                "color": "#00ACC1"
            },
            {
                "step": "Generate Security Policies",
                "description": "Automatically create Snowflake DDL for implementing security",
                "icon": "🛡️",
                "color": "#5E35B1"
            }
        ]
        
        # Display the journey as a modern timeline with cards
        for i, step in enumerate(journey_steps):
            st.markdown(f"""
            <div class="step-card" style="border-left-color: {step['color']}">
                <div style="display: flex; align-items: center;">
                    <div style="background-color: {step['color']}; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px;">{i+1}</div>
                    <div>
                        <h3 style="margin: 0; font-size: 1.2rem; color: {step['color']}">{step['step']}</h3>
                        <p style="margin: 5px 0 0 0; color: #616161;">{step['description']}</p>
                    </div>
                    <div style="margin-left: auto; font-size: 24px;">{step['icon']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add connector line between steps
            if i < len(journey_steps) - 1:
                st.markdown(f"<div style='border-left: 2px dashed #E0E0E0; height: 20px; margin-left: 15px;'></div>", unsafe_allow_html=True)
    
    def _render_workflow_example(self):
        """Render a detailed workflow example with external system integration."""
        st.markdown("""
        <h3 class="subsection-header">Integration Workflow</h3>
        <p style="font-size: 1.1rem; margin-bottom: 20px;">This example illustrates how the Data Use Governance control plane manages data access across external systems:</p>
        """, unsafe_allow_html=True)
        
        # Create a workflow example with modern styling
        workflow_steps = [
            {
                "title": "Role Detection",
                "description": "When a role is created in an external system, a role detection agent intercepts it and pushes the event to the control plane.",
                "icon": "🔍",
                "color": "#1E88E5"
            },
            {
                "title": "Default Purpose Assignment",
                "description": "In the control plane, there is a default purpose with baseline policies defined to govern the use of sensitive data - such as masking, encryption, etc.",
                "icon": "🎯",
                "color": "#43A047"
            },
            {
                "title": "Baseline Policy Enforcement",
                "description": "The baseline policy enforcement agent associates the newly discovered role to the default purpose and enforces the baseline policies in the target system, ensuring continuous data use governance.",
                "icon": "🛡️",
                "color": "#FB8C00"
            },
            {
                "title": "Data Steward Notification",
                "description": "The system immediately notifies the data steward about this external role that is now persisted and tracked in the system.",
                "icon": "💬",
                "color": "#8E24AA"
            },
            {
                "title": "Purpose Determination",
                "description": "The system determines the appropriate purpose either through attached processing activities or explicitly from the user requesting access, not through manual mapping.",
                "icon": "📝",
                "color": "#E53935"
            },
            {
                "title": "Policy Implementation",
                "description": "The policy enforcement agent implements these policies on the source system.",
                "icon": "⚙️",
                "color": "#00ACC1"
            },
            {
                "title": "Dynamic Policy Resolution",
                "description": "The target policy is dynamically derived from the hierarchical policy definitions, and appropriate security configurations are generated dynamically for the target system.",
                "icon": "🔄",
                "color": "#5E35B1"
            }
        ]
        
        # Display the workflow as a modern timeline with cards
        for i, step in enumerate(workflow_steps):
            st.markdown(f"""
            <div class="step-card" style="border-left-color: {step['color']}">
                <div style="display: flex; align-items: center;">
                    <div style="background-color: {step['color']}; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px;">{i+1}</div>
                    <div style="flex-grow: 1;">
                        <h3 style="margin: 0; font-size: 1.2rem; color: {step['color']}">{step['title']}</h3>
                        <p style="margin: 5px 0 0 0; color: #616161;">{step['description']}</p>
                    </div>
                    <div style="margin-left: 15px; font-size: 24px;">{step['icon']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add connector line between steps
            if i < len(workflow_steps) - 1:
                st.markdown(f"<div style='border-left: 2px dashed #E0E0E0; height: 20px; margin-left: 15px;'></div>", unsafe_allow_html=True)
        
        # Add hierarchical policy section
        st.markdown("""
        <div class="card" style="margin-top: 30px;">
            <h3 class="subsection-header">Hierarchical Policy Management</h3>
            <p>Policies are created and maintained at multiple levels:</p>
            <ul>
                <li><strong>Data Element Level</strong>: Policies specific to individual data elements</li>
                <li><strong>Data Category Level</strong>: Policies applied to entire categories of data</li>
                <li><strong>Purpose and Data Element</strong>: Policies for specific data elements when used for particular purposes</li>
                <li><strong>Purpose and Data Category</strong>: Policies for data categories when used for particular purposes</li>
                <li><strong>Role, Purpose, and Data Category</strong>: Role-specific policies for data categories used for particular purposes</li>
                <li><strong>Role, Purpose, and Data Element</strong>: The most granular level of policy definition</li>
            </ul>
            <p>The system dynamically resolves these hierarchical policies to determine the most appropriate access controls and security requirements for each specific context, regardless of the target system.</p>
        </div>
        
        <div class="card" style="margin-top: 30px;">
            <h3 class="subsection-header">Intelligent Agents</h3>
            <p>The Data Use Governance control plane employs several intelligent agents to automate governance tasks:</p>
            <ul>
                <li><strong>Role Detection Agent</strong>: Detects the creation or modification of roles in external systems and sends these events to the control plane, which persists them as external roles</li>
                <li><strong>Policy Enforcement Agent</strong>: When a new external role is detected, this agent assigns it to the default purpose with baseline policies and implements them in source systems like Snowflake, Databricks, etc.</li>
                <li><strong>Policy Inference Agent</strong>: Monitors changes in organizational data (assets, processing activities) and dynamically recommends policies for effective data governance</li>
                <li><strong>Evidence Task Generation Agent</strong>: Verifies that enforced policies are effective in source systems by automatically testing them (e.g., confirming masking policies work as expected)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_features_implementation(self):
        """Render the Features & Implementation section with a modern design."""
        st.markdown("""
        <p style="font-size: 1.1rem; margin-bottom: 20px;">The Data Use Governance module includes the following key features:</p>
        """, unsafe_allow_html=True)
        
        features = [
            {
                "name": "Purpose Management",
                "description": "Create and manage business purposes that justify data access",
                "implementation": "Implemented in the Purposes page with CRUD operations and purpose categories",
                "status": "Complete",
                "icon": "🎯",
                "color": "#43A047"  # Green
            },
            {
                "name": "Policy Management",
                "description": "Define policies that govern how data can be used",
                "implementation": "Implemented in the Policies page with policy-purpose mappings",
                "status": "Complete",
                "icon": "📋",
                "color": "#1E88E5"  # Blue
            },
            {
                "name": "Role Management",
                "description": "Define and manage roles with appropriate access levels",
                "implementation": "Implemented in the Roles page with internal and external role management",
                "status": "Complete",
                "icon": "👥",
                "color": "#E53935"  # Red
            },
            {
                "name": "Asset-Purpose Mapping",
                "description": "Associate data assets with legitimate business purposes",
                "implementation": "Implemented in the Purposes page with asset selection and mapping",
                "status": "Complete",
                "icon": "🔗",
                "color": "#FB8C00"  # Orange
            },
            {
                "name": "Purpose-Role Mapping",
                "description": "Determine which roles can access data for specific purposes",
                "implementation": "Implemented in the Roles page with purpose-role mapping and masking requirements",
                "status": "Complete",
                "icon": "🔄",
                "color": "#8E24AA"  # Purple
            },
            {
                "name": "External Role Integration",
                "description": "Import and manage external roles from systems like Snowflake",
                "implementation": "Implemented in the Roles page with external role creation and asset linking",
                "status": "Complete",
                "icon": "🔌",
                "color": "#00ACC1"  # Cyan
            },
            {
                "name": "Security Policy Generation",
                "description": "Automatically generate Snowflake DDL for implementing security policies",
                "implementation": "Implemented using the DDLGenerator component with masking policy creation",
                "status": "Complete",
                "icon": "🛡️",
                "color": "#5E35B1"  # Deep Purple
            }
        ]
        
        # Create a grid of feature cards
        cols = st.columns(3)
        for i, feature in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="feature-card" style="border-top-color: {feature['color']}">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <div style="background-color: {feature['color']}; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-size: 18px;">{feature['icon']}</div>
                        <h3 class="feature-title" style="color: {feature['color']}; margin: 0;">{feature['name']}</h3>
                    </div>
                    <p class="feature-description">{feature['description']}</p>
                    <p class="feature-implementation">{feature['implementation']}</p>
                    <div style="text-align: right; margin-top: 10px;">
                        <span class="status-complete">✓ {feature['status']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # No Key Implementation Details section
