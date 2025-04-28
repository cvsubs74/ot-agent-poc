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
        
        # Architecture
        st.markdown("<h2 class='section-header'>Architecture</h2>", unsafe_allow_html=True)
        self._render_architecture()
        
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
        # Create two columns for the overview
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            <div class="card">
                <h3 class="subsection-header">The Challenge</h3>
                <p>Organizations today face increasing complexity in managing how data is used across their enterprise:</p>
                <ul>
                    <li><strong>Regulatory Compliance</strong>: Meeting requirements from GDPR, CCPA, and other regulations</li>
                    <li><strong>Purpose Limitation</strong>: Ensuring data is only used for specified, legitimate purposes</li>
                    <li><strong>Role-Based Access</strong>: Implementing proper access controls based on user roles</li>
                    <li><strong>Data Masking</strong>: Protecting sensitive information while enabling business functions</li>
                </ul>
                
                <h3 class="subsection-header">Our Solution</h3>
                <p>The Data Use Governance module provides a comprehensive framework for:</p>
                <ol>
                    <li><strong>Purpose Definition</strong>: Define clear business purposes for data use</li>
                    <li><strong>Policy Creation</strong>: Create policies that govern how data can be used</li>
                    <li><strong>Role Management</strong>: Define and manage roles with appropriate access levels</li>
                    <li><strong>Asset-Purpose-Role Mapping</strong>: Create relationships between data assets, purposes, and roles</li>
                    <li><strong>Security Policy Generation</strong>: Automatically generate Snowflake DDL for implementing security policies</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Create a modern relationship diagram
            fig = go.Figure()
            
            # Nodes
            nodes = {
                "Assets": {"x": 0, "y": 0, "color": "#1E88E5"},
                "Purposes": {"x": 1, "y": 1, "color": "#43A047"},
                "Roles": {"x": 2, "y": 0, "color": "#E53935"},
                "Policies": {"x": 1, "y": -1, "color": "#8E24AA"}
            }
            
            # Add nodes
            for name, attrs in nodes.items():
                fig.add_trace(go.Scatter(
                    x=[attrs["x"]], 
                    y=[attrs["y"]],
                    mode="markers+text",
                    marker=dict(size=40, color=attrs["color"]),
                    text=[name],
                    textposition="middle center",
                    name=name,
                    textfont=dict(color="white", size=12)
                ))
            
            # Add edges
            edges = [
                ("Assets", "Purposes", "used for"),
                ("Purposes", "Roles", "accessed by"),
                ("Assets", "Policies", "governed by"),
                ("Policies", "Roles", "enforced on")
            ]
            
            for source, target, label in edges:
                source_x, source_y = nodes[source]["x"], nodes[source]["y"]
                target_x, target_y = nodes[target]["x"], nodes[target]["y"]
                
                # Add line
                fig.add_trace(go.Scatter(
                    x=[source_x, target_x],
                    y=[source_y, target_y],
                    mode="lines",
                    line=dict(width=2, color="#9E9E9E"),
                    showlegend=False
                ))
                
                # Add label
                fig.add_trace(go.Scatter(
                    x=[(source_x + target_x) / 2],
                    y=[(source_y + target_y) / 2],
                    mode="text",
                    text=[label],
                    textposition="middle center",
                    textfont=dict(size=10, color="#616161"),
                    showlegend=False
                ))
            
            fig.update_layout(
                title="Data Use Governance Relationships",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                showlegend=False,
                height=400,
                margin=dict(l=0, r=0, t=40, b=0),
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Create a simple diagram showing the relationships
        fig = go.Figure()
        
        # Nodes
        nodes = {
            "Assets": {"x": 0, "y": 0, "color": "blue"},
            "Purposes": {"x": 1, "y": 1, "color": "green"},
            "Roles": {"x": 2, "y": 0, "color": "red"},
            "Policies": {"x": 1, "y": -1, "color": "purple"}
        }
        
        # Add nodes
        for name, attrs in nodes.items():
            fig.add_trace(go.Scatter(
                x=[attrs["x"]], 
                y=[attrs["y"]],
                mode="markers+text",
                marker=dict(size=30, color=attrs["color"]),
                text=[name],
                textposition="middle center",
                name=name
            ))
        
        # Add edges
        edges = [
            ("Assets", "Purposes", "used for"),
            ("Purposes", "Roles", "accessed by"),
            ("Assets", "Policies", "governed by"),
            ("Policies", "Roles", "enforced on")
        ]
        
        for source, target, label in edges:
            source_x, source_y = nodes[source]["x"], nodes[source]["y"]
            target_x, target_y = nodes[target]["x"], nodes[target]["y"]
            
            # Add line
            fig.add_trace(go.Scatter(
                x=[source_x, target_x],
                y=[source_y, target_y],
                mode="lines",
                line=dict(width=2, color="gray"),
                showlegend=False
            ))
            
            # Add label
            fig.add_trace(go.Scatter(
                x=[(source_x + target_x) / 2],
                y=[(source_y + target_y) / 2],
                mode="text",
                text=[label],
                textposition="middle center",
                textfont=dict(size=10, color="black"),
                showlegend=False
            ))
        
        fig.update_layout(
            title="Data Use Governance Relationships",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            showlegend=True,
            width=700,
            height=500
        )
        
        st.plotly_chart(fig)
    
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
    
    def _render_architecture(self):
        """Render the Architecture section with a modern design."""
        st.markdown("""
        <p style="font-size: 1.1rem; margin-bottom: 20px;">The Data Use Governance module is built on a layered architecture that separates concerns and provides flexibility:</p>
        """, unsafe_allow_html=True)
        
        # Create a modern architecture diagram
        architecture_layers = [
            {
                "name": "User Interface Layer",
                "components": ["Purposes Page", "Policies Page", "Roles Page", "Policy Compliance Page"],
                "color": "#1E88E5",  # Blue
                "icon": "🖥️"
            },
            {
                "name": "Business Logic Layer",
                "components": ["Purpose Management", "Policy Management", "Role Management", "DDL Generator"],
                "color": "#43A047",  # Green
                "icon": "⚙️"
            },
            {
                "name": "Data Access Layer",
                "components": ["GlossaryRepository", "PolicyRepository", "RegulatoryMetadataRepository"],
                "color": "#FB8C00",  # Orange
                "icon": "🔄"
            },
            {
                "name": "Database Layer",
                "components": ["Purposes Table", "Policies Table", "Roles Table", "Asset-Purpose-Role Mappings"],
                "color": "#8E24AA",  # Purple
                "icon": "💾"
            }
        ]
        
        # Render the architecture diagram with modern styling
        for layer in architecture_layers:
            st.markdown(f"""
            <div class="architecture-layer" style="border-left: 4px solid {layer['color']}">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 24px; margin-right: 10px;">{layer['icon']}</div>
                    <h3 class="layer-title" style="color: {layer['color']}; margin: 0;">{layer['name']}</h3>
                </div>
                <div style="margin-top: 15px;">
            """, unsafe_allow_html=True)
            
            # Display components as pills
            for component in layer['components']:
                st.markdown(f"""
                <span class="component-pill" style="background-color: {layer['color']}20; color: {layer['color']}; border: 1px solid {layer['color']}40;">{component}</span>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Add connector arrows between layers
            if layer != architecture_layers[-1]:
                st.markdown(f"<div style='text-align: center; margin: 10px 0;'><i class='fas fa-arrow-down' style='color: {layer['color']}; font-size: 20px;'></i></div>", unsafe_allow_html=True)
    
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
        
        # Key implementation details with modern styling
        st.markdown("<h3 class='subsection-header' style='margin-top: 30px;'>Key Implementation Details</h3>", unsafe_allow_html=True)
        
        # Create three columns for the key implementation details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 40px;">🔄</div>
                    <h4 style="color: #1565C0; margin: 10px 0;">Purpose-Role-Asset Relationship</h4>
                </div>
                <p>The system maintains a three-way relationship between:</p>
                <ul>
                    <li><strong>Assets</strong> (data tables and columns)</li>
                    <li><strong>Purposes</strong> (business justifications)</li>
                    <li><strong>Roles</strong> (user roles with varying access)</li>
                </ul>
                <p>This ensures data access is:</p>
                <ul>
                    <li><strong>Purpose-bound</strong>: Only for legitimate business purposes</li>
                    <li><strong>Role-appropriate</strong>: Based on user responsibilities</li>
                    <li><strong>Minimized</strong>: Limited to necessary data</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 40px;">🛡️</div>
                    <h4 style="color: #1565C0; margin: 10px 0;">Masking Policy Generation</h4>
                </div>
                <p>The DDL Generator automatically creates Snowflake masking policies based on:</p>
                <ul>
                    <li><strong>Data element sensitivity</strong></li>
                    <li><strong>Purpose-role mappings</strong></li>
                    <li><strong>Masking requirements for each role</strong></li>
                </ul>
                <div class="highlight-text">
                    For roles with <code>masking_required=false</code>, full access is granted to the data.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="card">
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 40px;">🔌</div>
                    <h4 style="color: #1565C0; margin: 10px 0;">External Role Integration</h4>
                </div>
                <p>The system allows:</p>
                <ul>
                    <li><strong>Adding external roles</strong> from systems like Snowflake</li>
                    <li><strong>Linking roles to specific assets</strong></li>
                    <li><strong>Including these roles</strong> in purpose-role mappings</li>
                </ul>
                <p>This ensures consistent security policy application across systems.</p>
            </div>
            """, unsafe_allow_html=True)
