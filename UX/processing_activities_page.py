import streamlit as st
import pandas as pd
from UX.policy_compliance_page import PolicyCompliancePage

class ProcessingActivitiesPage:
    def __init__(self, inventory_repository, glossary_repository, regulatory_metadata_repository):
        self.inventory_repository = inventory_repository
        self.glossary_repository = glossary_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.policy_compliance_page = PolicyCompliancePage(
            self.glossary_repository,
            self.regulatory_metadata_repository
        )

    def render(self):
        st.markdown("<div class='page-header'><i class='fas fa-cogs'></i> &nbsp;Processing Activities</div>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This section provides an overview of data processing activities within the organization, including their purposes and the data elements they process.</p>
            <ul>
                <li>Processing activities represent business operations that process personal data</li>
                <li>Each processing activity has a specific business purpose</li>
                <li>Processing activities use data from one or more assets</li>
                <li>Data elements processed are tracked for compliance and transparency</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        
        processing_activities = self.inventory_repository.get_processing_activities()
        if not processing_activities:
            st.warning("No processing activities available in the database.")
            return
        
        processing_activity_purposes = self.inventory_repository.get_processing_activity_purposes()
        processing_activity_asset_data_elements = self.inventory_repository.get_processing_activity_asset_data_elements()
        
        # Group purposes by processing activity
        activity_to_purposes = {}
        for pap in processing_activity_purposes:
            activity_id = pap['processing_activity_id']
            if activity_id not in activity_to_purposes:
                activity_to_purposes[activity_id] = []
            activity_to_purposes[activity_id].append({
                'name': pap['purpose_name'],
                'category': pap['purpose_category'],
                'risk_level': pap['purpose_risk_level'],
                'description': pap['purpose_description']
            })
        
        # Group asset data elements by processing activity and then by asset
        activity_to_assets = {}
        for paade in processing_activity_asset_data_elements:
            activity_id = paade['processing_activity_id']
            asset_id = paade['asset_id']
            if activity_id not in activity_to_assets:
                activity_to_assets[activity_id] = {}
            if asset_id not in activity_to_assets[activity_id]:
                activity_to_assets[activity_id][asset_id] = {
                    'name': paade['asset_name'],
                    'description': paade['asset_description'],
                    'data_elements': []
                }
            activity_to_assets[activity_id][asset_id]['data_elements'].append({
                'name': paade['data_element_name'],
                'description': paade['data_element_description']
            })
        
        col1, col2 = st.columns(2)
        with col1:
            all_purposes = set()
            for purposes in activity_to_purposes.values():
                all_purposes.update([p['name'] for p in purposes])
            selected_purpose = st.selectbox("Filter by Purpose", ["All"] + sorted(list(all_purposes)))
        with col2:
            all_assets = set()
            for assets in activity_to_assets.values():
                all_assets.update([a['name'] for _, a in assets.items()])
            selected_asset = st.selectbox("Filter by Asset", ["All"] + sorted(list(all_assets)))
        
        filtered_activities = processing_activities
        if selected_purpose != "All" or selected_asset != "All":
            filtered_activities = []
            for activity in processing_activities:
                include = True
                if selected_purpose != "All":
                    purposes = activity_to_purposes.get(activity['id'], [])
                    purpose_names = [p['name'] for p in purposes]
                    if selected_purpose not in purpose_names:
                        include = False
                if selected_asset != "All" and include:
                    assets = activity_to_assets.get(activity['id'], {})
                    asset_names = [a['name'] for _, a in assets.items()]
                    if selected_asset not in asset_names:
                        include = False
                if include:
                    filtered_activities.append(activity)
        pa_data = {
            "Processing Activity": [],
            "Description": [],
            "Status": [],
            "Start Date": [],
            "End Date": [],
            "Purpose(s)": [],
            "Asset(s)": [],
            "Data Element Count": []
        }
        if not filtered_activities:
            st.warning("No processing activities match the selected filters.")
        else:
            for activity in filtered_activities:
                purposes = activity_to_purposes.get(activity['id'], [])
                purpose_names = ", ".join([p['name'] for p in purposes]) if purposes else "None"
                assets = activity_to_assets.get(activity['id'], {})
                asset_names = ", ".join([a['name'] for _, a in assets.items()]) if assets else "None"
                data_element_count = sum(len(a['data_elements']) for _, a in assets.items()) if assets else 0
                pa_data["Processing Activity"].append(activity['name'])
                pa_data["Description"].append(activity['description'])
                pa_data["Status"].append(activity['status'])
                pa_data["Start Date"].append(activity['start_date'])
                pa_data["End Date"].append(activity['end_date'] if activity['end_date'] else "N/A")
                pa_data["Purpose(s)"].append(purpose_names)
                pa_data["Asset(s)"].append(asset_names)
                pa_data["Data Element Count"].append(data_element_count)
            df = pd.DataFrame(pa_data)
            df = df.dropna(how='all')
            st.dataframe(df, use_container_width=True, height=min(400, len(df) * 35 + 38))
            activity_names = [activity['name'] for activity in filtered_activities]
            if activity_names:
                selected_activity_name = st.selectbox("Select a processing activity to view details", activity_names)
                selected_activity = next((activity for activity in filtered_activities if activity['name'] == selected_activity_name), None)
                with st.container():
                    card_header = f'''
                    <div style="background-color: white; border-radius: 10px 10px 0 0; padding: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">
                        <h3 style="color: #2c3e50; margin-top: 0;">{selected_activity['name']}</h3>
                        <p style="color: #7f8c8d;">{selected_activity['description']}</p>
                        <p><span style="background-color: #e8f4f8; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">{selected_activity['status']}</span></p>
                    </div>
                    '''
                    st.markdown(card_header, unsafe_allow_html=True)
                    card_body = '<div style="background-color: white; border-radius: 0 0 10px 10px; padding: 0 15px 15px 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid #3498db;">'
                    st.markdown(card_body, unsafe_allow_html=True)
                    purposes = activity_to_purposes.get(selected_activity['id'], [])
                    if purposes:
                        with st.expander(f"Purpose{'s' if len(purposes) > 1 else ''} ({len(purposes)})"):
                            for purpose in purposes:
                                risk_color = {
                                    'Low': '#2ecc71',
                                    'Medium': '#f39c12',
                                    'High': '#e74c3c'
                                }.get(purpose['risk_level'], '#7f8c8d')
                                st.markdown(f'''
                                <div style="background-color: white; border-radius: 5px; padding: 10px; margin-bottom: 10px; border-left: 3px solid {risk_color};">
                                    <h4 style="margin-top: 0;">{purpose['name']}</h4>
                                    <p style="font-size: 0.9em; margin-bottom: 5px;"><strong>Category:</strong> {purpose['category'] or 'N/A'}</p>
                                    <p style="font-size: 0.9em; margin-bottom: 5px;"><strong>Risk Level:</strong> <span style="color: {risk_color};">{purpose['risk_level'] or 'N/A'}</span></p>
                                    <p style="font-size: 0.9em;">{purpose['description'] or 'No description available'}</p>
                                </div>
                                ''', unsafe_allow_html=True)
                    else:
                        st.info(f"No purposes associated with {selected_activity['name']}")
                    assets = activity_to_assets.get(selected_activity['id'], {})
                    if assets:
                        with st.expander(f"Assets and Data Elements ({len(assets)})"):
                            for asset_id, asset in assets.items():
                                st.markdown(f"#### {asset['name']}")
                                st.markdown(f"*{asset['description']}*")
                                de_data = {
                                    "Data Element": [],
                                    "Description": []
                                }
                                for de in asset['data_elements']:
                                    de_data["Data Element"].append(de['name'])
                                    de_data["Description"].append(de['description'])
                                st.dataframe(pd.DataFrame(de_data), use_container_width=True)
                    else:
                        st.info(f"No assets associated with {selected_activity['name']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    if purposes and assets:
                        
                        st.markdown("Check if this processing activity complies with organizational policies.")
                        purpose = purposes[0]['name'] if purposes else None
                        all_data_elements = []
                        for _, asset in assets.items():
                            for de in asset['data_elements']:
                                all_data_elements.append(de['name'])
                        all_data_elements = list(set(all_data_elements))
                        operation = st.selectbox(
                            "Select Operation",
                            options=["read", "write", "share"],
                            index=0,
                            key=f"operation_select_{selected_activity['id']}"
                        )
                        analyze_button = st.button(
                            "Analyze Policy Compliance", 
                            key=f"analyze_btn_{selected_activity['id']}"
                        )

                        st.markdown("""
                        <div style="background-color: #eaf7ea; padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 5px solid #27ae60;">
                            <h4 style="margin-top: 0;">How Policy Compliance Analysis Works</h4>
                            <p>The Policy Compliance Analysis uses these mapping tables to determine if a processing activity complies with organizational policies:</p>
                            <ol>
                                <li><strong>Policy Purpose Data Elements</strong>: Maps which data elements are allowed for specific purposes under each policy.</li>
                                <li><strong>Policy Purpose Data Usage</strong>: Defines permitted operations (read, write, share) for each data element-purpose combination.</li>
                                <li><strong>Purpose Risk Levels</strong>: Categorizes purposes by risk level, which influences the strictness of compliance requirements.</li>
                            </ol>
                            <p>When analyzing policy compliance, the system considers:</p>
                            <ul>
                                <li>The business purpose of the processing activity</li>
                                <li>All data elements involved in the processing</li>
                                <li>The specific operation being performed (read, write, share)</li>
                                <li>Any usage restrictions defined in the policy</li>
                            </ul>
                            <p>The system then evaluates each data element against policy rules and provides a detailed compliance assessment with recommendations for addressing any violations.</p>
                        </div>
                        """, unsafe_allow_html=True)

                        if purpose and all_data_elements:
                            if analyze_button:
                                st.markdown(f"### Policy Compliance Analysis for {purpose}")
                                st.markdown(f"**Operation:** {operation.upper()}")
                                self._analyze_policy_compliance_for_activity(purpose, all_data_elements, operation)
                        else:
                            st.info("Insufficient data for policy compliance analysis.")

    def _analyze_policy_compliance_for_activity(self, purpose, data_elements, operation):
        self.policy_compliance_page.analyze_policy_compliance(purpose, data_elements, operation)