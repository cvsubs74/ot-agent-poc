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
            position: relative;
            z-index: 1;
        }
        
        .step-card:hover {
            transform: translateY(-8px) translateX(5px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
            z-index: 2;
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
        
        # User Journey
        st.markdown("<h2 class='section-header'>User Journey</h2>", unsafe_allow_html=True)
        self._render_user_journey()
        
        # Integration Workflow
        st.markdown("<h2 class='section-header'>Integration Workflow</h2>", unsafe_allow_html=True)
        self._render_workflow_example()
        
        # Render the new consent management and row filtering section
        render_consent_row_filtering_section()
        
        # Regulatory Policy Gap Analysis
        st.markdown("<h2 class='section-header'>Policy Gap Analysis</h2>", unsafe_allow_html=True)
        
        # Add dual policy inference engines section
        st.markdown("""
        <div class="overview-container">
            <h3 class="subsection-header">Dual Policy Inference Engines</h3>
            <p>The system leverages two complementary policy inference engines to provide comprehensive data governance:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for the policy engines
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="challenge-container">
                <h4 class="blue-header">Purpose Driven Policy Inference Engine</h4>
                <p>Infers policies based on customer-defined purpose-driven policy definitions for different roles and data elements.</p>
                <ul>
                    <li>Based on data steward inputs</li>
                    <li>Reflects organizational policy preferences</li>
                    <li>Considers business-specific requirements</li>
                </ul>
                <div class="highlight-text">
                    <strong>Example:</strong> Marketing team requires email masking for customer outreach
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="solution-container">
                <h4 class="green-header">Regulatory Rules Driven Policy Inference Engine</h4>
                <p>Infers policies based on regulatory intelligence built from core regulatory constructs and requirements.</p>
                <ul>
                    <li>Built on regulatory frameworks (GDPR, CCPA, etc.)</li>
                    <li>Based on data element sensitivity</li>
                    <li>Considers industry best practices</li>
                </ul>
                <div class="highlight-text">
                    <strong>Example:</strong> Financial transaction data requires encryption at rest and in transit
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add risk alert section
        st.markdown("""
        <div style="background-color: #FFEBEE; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h4 style="color: #E53935; margin-top: 0;">Risk Alert: Stricter Regulatory Requirements</h4>
            <p>When regulatory intelligence suggests stricter policies than those defined by data stewards, the system generates alerts highlighting potential compliance risks.</p>
            <div class="highlight-text">
                <strong>Example:</strong> Email masking required by GDPR for marketing purposes, but not implemented in current policies
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add confidence validation section
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h4 style="color: #2E7D32; margin-top: 0;">Confidence Validation: Stricter Organizational Controls</h4>
            <p>When data steward policies are stricter than regulatory requirements, the system confirms that the organization is exceeding compliance requirements.</p>
            <div class="highlight-text">
                <strong>Example:</strong> Organization implements end-to-end encryption for financial data, exceeding basic regulatory requirements
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add regulatory intelligence policy flow section
        st.markdown("""
        <div class="overview-container">
            <h3 class="subsection-header">Policy Inference and Gap Analysis Flows</h3>
            <p>Visual representation of how business policies and regulatory requirements flow through both engines:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a visualization of the regulatory intelligence policy flow
        fig = go.Figure()
        
        # Define node positions
        nodes = {
            'Data Elements': {'x': 0, 'y': 5},
            'Regulatory Requirements': {'x': -2, 'y': 3},
            'Purpose Definitions': {'x': 2, 'y': 3},
            'Reg Intel Policies': {'x': -2, 'y': 1},
            'Data Steward Policies': {'x': 2, 'y': 1},
            'Gap Analysis': {'x': 0, 'y': -1},
            'Recommendations': {'x': 0, 'y': -3},
            'Implemented Policies': {'x': 0, 'y': -5}
        }
        
        # Add nodes
        for node, pos in nodes.items():
            fig.add_trace(go.Scatter(
                x=[pos['x']], 
                y=[pos['y']],
                mode='markers+text',
                marker=dict(size=25, color=['#1565C0', '#7B1FA2', '#43A047', '#7B1FA2', '#43A047', '#E53935', '#FB8C00', '#5E35B1'][list(nodes.keys()).index(node)]),
                text=[node],
                textposition='bottom center',
                hoverinfo='text',
                name=node
            ))
        
        # Add edges (connections between nodes)
        edges = [
            ('Data Elements', 'Regulatory Requirements'),
            ('Data Elements', 'Purpose Definitions'),
            ('Regulatory Requirements', 'Reg Intel Policies'),
            ('Purpose Definitions', 'Data Steward Policies'),
            ('Reg Intel Policies', 'Gap Analysis'),
            ('Data Steward Policies', 'Gap Analysis'),
            ('Gap Analysis', 'Recommendations'),
            ('Recommendations', 'Implemented Policies')
        ]
        
        for edge in edges:
            start, end = edge
            fig.add_trace(go.Scatter(
                x=[nodes[start]['x'], nodes[end]['x']],
                y=[nodes[start]['y'], nodes[end]['y']],
                mode='lines',
                line=dict(width=2, color='rgba(100, 100, 100, 0.5)'),
                hoverinfo='none',
                showlegend=False
            ))
        
        # Update layout
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
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
        
    # _render_use_case_overview method has been removed as it's no longer needed
    
    def _render_user_journey(self):
        """Render the User Journey section with a modern design."""
        # Create a timeline of the user journey with modern styling
        journey_steps = [
            {
                "step": "Build or Import Catalog",
                "description": "Import metadata about external systems with sensitive data, classify key tables/columns as data elements within assets",
                "icon": "📊",
                "color": "#1E88E5"
            },
            {
                "step": "Define Purposes",
                "description": "Create business purposes that justify data access, including a default purpose for enforcing baseline policies",
                "icon": "🎯",
                "color": "#43A047"
            },
            {
                "step": "Create Policies",
                "description": "Define policies for all identified purposes, including the default purpose, to govern how data can be used",
                "icon": "📋",
                "color": "#8E24AA"
            },
            {
                "step": "Manage External Roles",
                "description": "Import external roles into the system and manage them via purposes, with policies enforced directly on these roles",
                "icon": "👥",
                "color": "#E53935"
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
                <li><strong>Purpose, Data Element Level</strong>: Purpose-specific policies for individual data elements</li>
                <li><strong>Purpose, Data Category Level</strong>: Purpose-specific policies for groups of data elements</li>
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
                <li><strong>Purpose Based Policy Inference Agent</strong>: This agent infers policies based on business-driven purposes attached to data sets or assets. Given a data set or asset, the policies will be inferred based on the purposes attached to those data sets or processing activities</li>
                <li><strong>Regulatory Rules Driven Policy Inference Agent</strong>: This agent is primarily driven by regulatory requirements derived from the sensitivity of the information contained in a data set or asset and the processing activities that process this data</li>
                <li><strong>Gap Analysis Agent</strong>: Based on the policies inferred by the two policy inference engines, this agent determines gaps and provides contextual feedback on where an organization stands regarding both compliance and security standards</li>
                <li><strong>Gap Resolution Agent</strong>: This agent resolves the identified gaps by recommending exact policies that would need to be implemented to close the gap</li>
                <li><strong>Control Implementation Agent</strong>: Maps policies to frameworks/controls, so when policies are implemented, several frameworks/controls are automatically implemented. This connects the dots between policy-based data governance and GRC controls</li>
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
                "icon": "📊",
                "title": "Catalog Management",
                "description": "Build or import metadata about external systems with sensitive data assets"
            },
            {
                "icon": "🎯",
                "title": "Purpose Management",
                "description": "Define business purposes including default purpose for baseline policies"
            },
            {
                "icon": "📋",
                "title": "Policy Creation",
                "description": "Create policies for all purposes including default purpose for baseline security"
            },
            {
                "icon": "👥",
                "title": "External Role Management",
                "description": "Import and manage external roles via purpose-based policies"
            },
            {
                "icon": "🔗",
                "title": "Purpose-Role Mapping",
                "description": "Determine which roles can access data for specific purposes"
            },
            {
                "icon": "🛡️",
                "title": "Security Policies",
                "description": "Automatically generate security policies for external systems"
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
                "title": "Identifier Matching",
                "description": "Match consent profile identifiers to table columns for row filtering"
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
