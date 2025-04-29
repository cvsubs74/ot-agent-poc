import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
import io
import numpy as np
from UX.data_use_governance_overview_consent import render_consent_row_filtering_section

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
            font-weight: 500;
            color: #1E88E5;
            margin-bottom: 1.5rem;
            text-align: center;
            padding: 1rem 0;
        }
        
        .section-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #0D47A1;
            margin-top: 2.5rem;
            margin-bottom: 1.2rem;
            padding-bottom: 0.5rem;
        }
        
        .subsection-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1565C0;
            margin-top: 0rem;
            margin-bottom: 0rem;
            padding-bottom: 0.1rem;
        }
        
        .card {
            background-color: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 25px;
            transition: transform 0.2s ease;
        }
        
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        .overview-container {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .challenge-container, .solution-container, .architecture-container {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left-width: 6px;
            border-left-style: solid;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .challenge-container:hover, .solution-container:hover, .architecture-container:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        .challenge-container {
            background-color: #e3f2fd;
            border-left-color: #1565C0;
        }
        
        .solution-container {
            background-color: #e8f5e9;
            border-left-color: #43A047;
        }
        
        .architecture-container {
            background-color: #f3e5f5;
            border-left-color: #7B1FA2;
        }
        
        .blue-header, .green-header, .purple-header {
            color: #1565C0;
            margin-top: 0;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }
        
        .step-card {
            background-color: white;
            border-left: 4px solid #1E88E5;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .step-card:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .step-number {
            background-color: #1E88E5;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 12px;
        }
        
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 25px;
            margin: 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border-top: 4px solid #1E88E5;
            transition: all 0.3s ease;
            flex: 0 1 calc(33.333% - 20px);
            min-width: 300px;
            max-width: 350px;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        ul {
            padding-left: 20px;
            margin: 1rem 0;
        }
        
        li {
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }
        
        strong {
            color: #1565C0;
        }
        
        .highlight-text {
            background-color: #E3F2FD;
            padding: 12px;
            border-radius: 8px;
            font-weight: 500;
            margin: 1rem 0;
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
        
        .intelligent-agents-container {
            background-color: #e8f5e9;
            border-left: 6px solid #43A047;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .hierarchical-policy-container {
            background-color: #f3e5f5;
            border-left: 6px solid #7B1FA2;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .user-journey-container {
            background-color: #e3f2fd;
            border-left: 6px solid #1565C0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .integration-workflow-container {
            background-color: #f3e5f5;
            border-left: 6px solid #7B1FA2;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .intelligent-agents-container:hover, .hierarchical-policy-container:hover, .user-journey-container:hover, .integration-workflow-container:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Page header
        st.markdown("<h2 class='main-header'>Data Use Governance</h2>", unsafe_allow_html=True)
        
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
        
        # Render the new consent management and row filtering section
        render_consent_row_filtering_section()
        
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
                    The Data Use Governance solution empowers organizations to implement purpose-based access controls, 
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
        
    def _render_use_case_overview(self):
        """Render the Use Case Overview section with a modern design and nice background color."""
        
        # Add custom CSS for the containers
        st.markdown("""
        <style>
        .overview-container {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .challenge-container, .solution-container, .architecture-container {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left-width: 6px;
            border-left-style: solid;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .challenge-container:hover, .solution-container:hover, .architecture-container:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        
        .challenge-container {
            background-color: #e3f2fd;
            border-left-color: #1565C0;
        }
        
        .solution-container {
            background-color: #e8f5e9;
            border-left-color: #43A047;
        }
        
        .architecture-container {
            background-color: #f3e5f5;
            border-left-color: #7B1FA2;
        }
        
        .blue-header, .green-header, .purple-header {
            color: #1565C0;
            margin-top: 0;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # The Challenge Section
        challenge_html = '''
        <div class="challenge-container">
            <h4 class="blue-header">The Challenge</h4>
            <p>Organizations today face increasing complexity in managing how data is used across their enterprise:</p>
            <ul>
                <li><strong>Regulatory Compliance</strong>: Meeting requirements from GDPR, CCPA, and other regulations</li>
                <li><strong>Purpose Limitation</strong>: Ensuring data is only used for specified, legitimate purposes</li>
                <li><strong>Role-Based Access</strong>: Implementing proper access controls based on user roles</li>
                <li><strong>Data Masking</strong>: Protecting sensitive information while enabling business functions</li>
            </ul>
        </div>
        '''
        st.markdown(challenge_html, unsafe_allow_html=True)
        
        # Our Solution Section
        solution_html = '''
        <div class="solution-container">
            <h4 class="green-header">Solution</h4>
            <p>The Data Use Governance module provides a comprehensive framework for:</p>
            <ul>
                <li><strong>Purpose Definition</strong>: Define clear business purposes for data use</li>
                <li><strong>Policy Creation</strong>: Create policies that govern how data can be used</li>
                <li><strong>Role Management</strong>: Define and manage roles with appropriate access levels</li>
                <li><strong>Purpose Determination</strong>: Automatically determine purposes through processing activities or user requests</li>
                <li><strong>Security Policy Generation</strong>: Automatically generate security policies for any target system</li>
            </ul>
        </div>
        '''
        st.markdown(solution_html, unsafe_allow_html=True)
        
        # Control Plane Architecture section
        architecture_html = '''
        <div class="architecture-container">
            <h4 class="purple-header">Control Plane Architecture</h4>
            <p>This architecture serves as the control plane that governs data access across multiple external systems:</p>
            <ul>
                <li><strong>Centralized Policy Management</strong>: With distributed enforcement across systems</li>
                <li><strong>Real-time Role Detection</strong>: And immediate policy application</li>
                <li><strong>Hierarchical Policy Resolution</strong>: With dynamic security policy generation</li>
                <li><strong>Automated Governance Workflows</strong>: With human oversight when needed</li>
            </ul>
        </div>
        '''
        st.markdown(architecture_html, unsafe_allow_html=True)
    
    def _render_user_journey(self):
        """Render the User Journey section with a modern design."""
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
                "description": "Define policies that govern how data can be used",
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
                "description": "Automatically generate Snowflake DDL for implementing security",
                "icon": "🛡️",
                "color": "#5E35B1"
            }
        ]
        
        # Display the journey as a modern timeline with cards
        for i, step in enumerate(journey_steps):
            st.markdown(f"""
            <div class="step-card" style="border-left-color: {step['color']}">
                <div style="display: flex; align-items: center;">
                    <div style="background-color: {step['color']}; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{i+1}</div>
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
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_workflow_example(self):
        """Render a detailed workflow example with external system integration."""
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
                "description": "The system determines the appropriate purpose either through attached processing activities or explicitly from the user requesting access.",
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
                    <div style="margin-left: auto; font-size: 24px;">{step['icon']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add connector line between steps
            if i < len(workflow_steps) - 1:
                st.markdown(f"<div style='border-left: 2px dashed #E0E0E0; height: 20px; margin-left: 15px;'></div>", unsafe_allow_html=True)
        
        # Add hierarchical policy section
        st.markdown("<h2 class='section-header'>Hierarchical Policy Management</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="hierarchical-policy-container">
            <p>Policies are created and maintained at multiple levels:</p>
            <ul>
                <li><strong>Data Element Level</strong>: Policies specific to individual data elements</li>
                <li><strong>Data Category Level</strong>: Policies for groups of data elements</li>
                <li><strong>Role, Purpose, and Data Category</strong>: Role-specific policies for data categories used for particular purposes</li>
                <li><strong>Role, Purpose, and Data Element</strong>: The most granular level of policy definition</li>
            </ul>
            <p>The system dynamically resolves these hierarchical policies to determine the most appropriate access controls and security requirements for each specific context, regardless of the target system.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2 class='section-header'>Intelligent Agents</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="intelligent-agents-container">
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
        <style>
        .features-container {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border-top: 4px solid #1E88E5;
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            color: #1E88E5;
            margin-bottom: 15px;
        }
        
        .feature-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1565C0;
            margin-bottom: 10px;
        }
        
        .feature-description {
            color: #616161;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Define the features
        features = [
            {
                "icon": "🎯",
                "title": "Purpose Management",
                "description": "Define and manage business purposes for data use across the organization"
            },
            {
                "icon": "📋",
                "title": "Policy Creation",
                "description": "Create and maintain policies that govern data access and usage"
            },
            {
                "icon": "👥",
                "title": "Role Management",
                "description": "Define and manage roles with appropriate access levels"
            },
            {
                "icon": "🔄",
                "title": "Purpose Mapping",
                "description": "Map data assets to legitimate business purposes"
            },
            {
                "icon": "🔗",
                "title": "Role Mapping",
                "description": "Determine which roles can access data for specific purposes"
            },
            {
                "icon": "🛡️",
                "title": "Security Policies",
                "description": "Automatically generate security policies for any target system"
            },
            {
                "icon": "✅",
                "title": "Consent Management",
                "description": "Track and enforce user consents for specific data processing purposes"
            },
            {
                "icon": "🔍",
                "title": "Row-Level Security",
                "description": "Implement fine-grained access control at the row level based on user identifiers"
            },
            {
                "icon": "🧠",
                "title": "Intelligent Column Matching",
                "description": "Use AI to intelligently match user identifiers to table columns for row filtering"
            }
        ]
        
        # Create three columns
        col1, col2, col3 = st.columns(3)
        
        # Display features in columns
        with col1:
            for i in range(0, len(features), 3):
                if i < len(features):
                    feature = features[i]
                    st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{feature['icon']}</div>
                        <h3 class="feature-title">{feature['title']}</h3>
                        <p class="feature-description">{feature['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            for i in range(1, len(features), 3):
                if i < len(features):
                    feature = features[i]
                    st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{feature['icon']}</div>
                        <h3 class="feature-title">{feature['title']}</h3>
                        <p class="feature-description">{feature['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col3:
            for i in range(2, len(features), 3):
                if i < len(features):
                    feature = features[i]
                    st.markdown(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{feature['icon']}</div>
                        <h3 class="feature-title">{feature['title']}</h3>
                        <p class="feature-description">{feature['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
