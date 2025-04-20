import streamlit as st
import datetime
import re
from core.breach_notification_inference import BreachNotificationInference
from UX.decision_tree_renderer import DecisionTreeRenderer

class BreachNotificationPage:
    """Class to handle the breach notification page UI and logic."""
    
    def __init__(self, glossary_repository, regulatory_metadata_repository):
        """Initialize the breach notification page with required repositories and inference engines.
        
        Args:
            glossary_repository: Repository for glossary data
            regulatory_metadata_repository: Repository for regulatory metadata
            breach_notification_inference: Inference engine for breach notification guidance
        """
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.breach_notification_inference = BreachNotificationInference(
            self.regulatory_metadata_repository,
            self.glossary_repository
        )

    
    def render(self):
        """Render the breach notification page UI."""
        st.markdown("<div class='page-header'><i class='fas fa-exclamation-triangle'></i> &nbsp;Breach Notification</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            This API helps determine the notification requirements for data breaches based on regulatory metadata.<br><br>
            <ul>
                <li>Provides guidance on notification requirements and timelines</li>
                <li>Identifies authorities that must be notified</li>
                <li>Calculates risk scores to determine notification necessity</li>
                <li>Offers documentation templates and remediation guidance</li>
            </ul>
            <strong>How the Algorithm Works:</strong><br><br>
            <ul>
                <li><strong>Law-Specific Guidance:</strong> Retrieves notification requirements for the selected law</li>
                <li><strong>Risk Assessment:</strong> Calculates risk score based on breach type and impact</li>
                <li><strong>Jurisdiction Analysis:</strong> Considers jurisdiction-specific requirements</li>
                <li><strong>Timeline Calculation:</strong> Determines precise notification deadlines</li>
                <li><strong>Documentation Guidance:</strong> Provides internal documentation templates</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        st.subheader("Breach Incident Details")
        
        # Get laws for dropdown selection
        laws = self.glossary_repository.get_laws()
        if not laws:
            st.warning("No laws available in the database.")
            return
            
        law_options = [law["name"] for law in laws]
        selected_law = st.selectbox("Select Applicable Law", options=law_options)
        
        # Get jurisdictions
        jurisdictions = self.glossary_repository.get_jurisdictions()
        if jurisdictions:
            jurisdiction_options = [j["name"] for j in jurisdictions]
            selected_jurisdiction = st.selectbox("Select Jurisdiction", options=jurisdiction_options)
        else:
            selected_jurisdiction = None
            
        # Breach details
        breach_type = st.selectbox(
            "Type of Breach", 
            options=[
                "Unauthorized Access", 
                "Data Disclosure", 
                "Data Alteration", 
                "Data Loss", 
                "Ransomware Attack", 
                "Phishing Attack", 
                "Insider Threat", 
                "Physical Breach", 
                "Other"
            ]
        )
            
        # Get data categories
        data_categories = self.glossary_repository.get_data_categories()
        if data_categories:
            dc_options = [dc["name"] for dc in data_categories]
            affected_data_categories = st.multiselect("Affected Data Categories", options=dc_options, key="breach_data_categories")
        else:
            st.warning("No data categories available.")
            return
            
        # Get data subject types
        data_subject_types = self.glossary_repository.get_data_subject_types()
        if data_subject_types:
            dst_options = [dst["name"] for dst in data_subject_types]
            affected_data_subjects = st.multiselect("Affected Data Subject Types", options=dst_options, key="breach_data_subject_types")
        else:
            st.warning("No data subject types available.")
            return
            
        # Number of affected individuals
        num_affected = st.number_input("Number of Affected Individuals", min_value=0, value=100)
            
        # Risk assessment
        risk_level = st.select_slider(
            "Risk Level to Individuals",
            options=["Minimal", "Low", "Medium", "High", "Severe"],
            value="Medium"
        )
            
        # Containment status
        containment_status = st.radio(
            "Breach Containment Status",
            options=["Contained", "Partially Contained", "Not Contained"],
            horizontal=True
        )
            
        # Discovery date
        col_dates1, col_dates2 = st.columns(2)
        with col_dates1:
            discovery_date = st.date_input("Date Breach Discovered", value=None)
        with col_dates2:
            occurrence_date = st.date_input("Date Breach Occurred (if known)", value=None)
            
        analyze_button = st.button("Analyze Notification Requirements")
        
        if analyze_button:
            # Display a spinner while "processing"
            with st.spinner("Analyzing breach notification requirements..."):
                # Get breach notification guidance based on the selected law
                guidance = self.breach_notification_inference.get_breach_notification_guidance(selected_law)
                
                if guidance:
                    # Display the notification requirements with appropriate styling
                    st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #e74c3c25; border: 2px solid #e74c3c; margin-top: 20px;">
                        <h3 style="color: #e74c3c;">Notification Required</h3>
                        <p><strong>Authority to Notify:</strong> {guidance['authority']}</p>
                        <p><strong>Notification Deadline:</strong> {guidance['timeframe']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display the notification threshold
                    st.markdown("### Notification Threshold")
                    st.markdown(f"**{guidance['threshold']}**")
                    
                    # Display detailed guidance
                    st.markdown("### Detailed Guidance")
                    st.markdown(guidance['content'])
                    
                    # Display breach assessment
                    st.markdown("### Breach Assessment")
                    
                    # Calculate days since discovery
                    days_remaining = None
                    if discovery_date:
                        today = datetime.date.today()
                        days_since_discovery = (today - discovery_date).days
                        
                        # Extract the timeframe in hours if possible
                        hours_match = re.search(r'(\d+)\s*hours', guidance['timeframe'])
                        if hours_match:
                            hours = int(hours_match.group(1))
                            days_allowed = hours / 24
                            days_remaining = days_allowed - days_since_discovery
                    
                    # Notification urgency based on days remaining
                    if days_remaining is not None:
                        if days_remaining < 0:
                            st.markdown(f"""
                            <div style="padding: 15px; border-radius: 5px; background-color: #e74c3c25; margin: 10px 0;">
                                <strong style="color: #e74c3c;">⚠️ URGENT: Notification deadline has passed!</strong><br>
                                The breach was discovered {days_since_discovery} days ago, which exceeds the notification timeframe.
                                Notify the relevant authority immediately to minimize potential penalties.
                            </div>
                            """, unsafe_allow_html=True)
                        elif days_remaining < 1:
                            st.markdown(f"""
                            <div style="padding: 15px; border-radius: 5px; background-color: #f39c1225; margin: 10px 0;">
                                <strong style="color: #f39c12;">⚠️ URGENT: Notification deadline approaching!</strong><br>
                                The breach was discovered {days_since_discovery} days ago. You have less than 24 hours remaining to notify.
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="padding: 15px; border-radius: 5px; background-color: #3498db25; margin: 10px 0;">
                                <strong style="color: #3498db;">Notification timeline:</strong><br>
                                The breach was discovered {days_since_discovery} days ago. You have approximately {days_remaining:.1f} days remaining to notify.
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Risk assessment
                    risk_color = "#e74c3c" if risk_level in ["High", "Severe"] else \
                                "#f39c12" if risk_level == "Medium" else \
                                "#2ecc71"
                    
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 5px; background-color: {risk_color}25; margin: 10px 0;">
                        <strong style="color: {risk_color};">Risk assessment:</strong><br>
                        Based on your input, this breach poses a <strong>{risk_level}</strong> risk to affected individuals.
                        {"This likely requires notification based on the threshold criteria." if risk_level in ["Medium", "High", "Severe"] else "This may fall below the notification threshold, but consider notifying as a precaution."}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Scope assessment
                    if num_affected > 500:
                        scope_severity = "large-scale"
                        scope_color = "#e74c3c"
                    elif num_affected > 100:
                        scope_severity = "significant"
                        scope_color = "#f39c12"
                    else:
                        scope_severity = "limited"
                        scope_color = "#2ecc71"
                    
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 5px; background-color: {scope_color}25; margin: 10px 0;">
                        <strong style="color: {scope_color};">Scope assessment:</strong><br>
                        This breach affects <strong>{num_affected}</strong> individuals, which is considered a <strong>{scope_severity}</strong> incident.
                        {"This scale of breach typically requires notification to authorities and possibly affected individuals." if scope_severity in ["significant", "large-scale"] else "Even with a limited scope, notification may still be required depending on the nature of the data affected."}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add notification checklist
                    st.markdown("### Notification Checklist")
                    st.markdown("""
                    ✅ **Information to include in your notification:**
                    
                    1. **Nature of the breach**
                       - Type of breach: {}
                       - How it occurred (if known)
                       - When it occurred and when it was discovered
                    
                    2. **Scope of the breach**
                       - Categories of personal data affected
                       - Number of data records concerned
                       - Number of data subjects affected
                    
                    3. **Likely consequences**
                       - Potential impact on individuals
                       - Risk assessment
                    
                    4. **Measures taken or proposed**
                       - Steps taken to contain the breach
                       - Steps taken to mitigate possible adverse effects
                       - Future preventative measures
                    
                    5. **Contact information**
                       - Details of your Data Protection Officer or other contact point
                    """.format(breach_type))
                    
                    # Add notification to individuals section if high risk
                    if risk_level in ["High", "Severe"]:
                        st.markdown("### Notification to Affected Individuals")
                        st.markdown(f"""
                        <div style="padding: 15px; border-radius: 5px; background-color: #e74c3c25; margin: 10px 0;">
                            <strong style="color: #e74c3c;">Individual notification required</strong><br>
                            Based on the {risk_level} risk level, you likely need to notify affected individuals without undue delay.
                        </div>
                        
                        **Information to include in individual notifications:**
                        
                        1. Clear description of the breach in plain language
                        2. Name and contact details of your data protection officer or other contact point
                        3. Description of the likely consequences of the breach
                        4. Description of measures taken or proposed to address the breach
                        5. Specific recommendations for individuals to protect themselves
                        """, unsafe_allow_html=True)
                        
                    # Define nodes for the decision tree
                    nodes = [
                        {"id": "breach", "label": "Data Breach", "color": "#e74c3c", "shape": "ellipse", "size": 30},
                        {"id": "jurisdiction", "label": "Affected Jurisdiction", "color": "#3498db", "shape": "box", "size": 25},
                        {"id": "law", "label": "Applicable Law", "color": "#9b59b6", "shape": "box", "size": 25},
                        {"id": "data_types", "label": "Data Types Affected", "color": "#f39c12", "shape": "box", "size": 25},
                        {"id": "severity", "label": "Breach Severity", "color": "#e74c3c", "shape": "box", "size": 25},
                        {"id": "lookup", "label": "Notification Requirements Lookup", "color": "#2ecc71", "shape": "box", "size": 25,
                         "title": {"html": """
                            <div style='max-width: 400px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; border-left: 5px solid #2ecc71;'>
                                <h3>Breach Notification Lookup Process</h3>
                                <p>This lookup process determines notification requirements by:</p>
                                <ol>
                                    <li>Querying the <b>Law Incident Breach Notification</b> table for the applicable law</li>
                                    <li>Evaluating breach severity based on data types affected and number of individuals</li>
                                    <li>Determining authority notification requirements and deadlines</li>
                                    <li>Assessing individual notification thresholds and exemptions</li>
                                    <li>Calculating notification timeframes based on discovery date</li>
                                </ol>
                                <p>The algorithm considers risk level, containment status, and jurisdiction-specific requirements to provide comprehensive notification guidance.</p>
                            </div>
                        """}},
                        {"id": "authority", "label": "Authority Notification", "color": "#3498db", "shape": "box", "size": 25},
                        {"id": "individual", "label": "Individual Notification", "color": "#f39c12", "shape": "box", "size": 25},
                        {"id": "timeframe", "label": "Notification Timeframe", "color": "#9b59b6", "shape": "box", "size": 25}
                    ]
                    
                    # Define edges for the decision tree
                    edges = [
                        {"source": "breach", "target": "jurisdiction", "label": "Occurs in"},
                        {"source": "jurisdiction", "target": "law", "label": "Governed by"},
                        {"source": "breach", "target": "data_types", "label": "Involves"},
                        {"source": "breach", "target": "severity", "label": "Has"},
                        {"source": "law", "target": "lookup", "label": ""},
                        {"source": "data_types", "target": "lookup", "label": ""},
                        {"source": "severity", "target": "lookup", "label": ""},
                        {"source": "lookup", "target": "authority", "label": "Requires"},
                        {"source": "lookup", "target": "individual", "label": "May require"},
                        {"source": "lookup", "target": "timeframe", "label": "Specifies"}
                    ]
                    
                    # Render the decision tree
                    DecisionTreeRenderer.render(nodes, edges, "Breach Notification Process", 700)
                else:
                    st.warning(f"No breach notification guidance found for {selected_law}.")
                    st.markdown("""
                    This could be because:
                    1. The selected law does not have specific breach notification requirements in our database
                    2. The regulatory metadata for this law needs to be updated
                    
                    Consider consulting with a privacy professional for guidance specific to this law.
                    """)
                    
                    # Provide general breach notification guidance
                    st.markdown("### General Breach Notification Guidance")
                    st.markdown("""
                    While specific guidance for the selected law is not available, here are general principles for breach notification:
                    
                    1. **Assess the risk** to individuals resulting from the breach
                    2. **Notify relevant authorities** as soon as possible, typically within 72 hours of discovery
                    3. **Notify affected individuals** if the breach is likely to result in high risk to their rights and freedoms
                    4. **Document the breach** including facts, effects, and remedial actions taken
                    5. **Implement measures** to contain the breach and prevent future incidents
                    
                    Many jurisdictions have mandatory breach notification requirements with specific timeframes and thresholds.
                    """)
