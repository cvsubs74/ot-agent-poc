import streamlit as st

class LawInferencePage:
    def __init__(self, law_inference):
        self.law_inference = law_inference

    def render(self, render_decision_tree_callback):
        """Implement a law inference API based on regulatory metadata."""
        st.markdown("<div class='page-header'><i class='fas fa-gavel'></i> &nbsp;Law Inference</div>", unsafe_allow_html=True)
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #27ae60;">
            <p>This API helps determine which data protection laws apply to specific jurisdictions based on regulatory metadata.</p>
            <p>The Law Inference API uses the Law Jurisdiction mapping table to identify applicable laws for a given jurisdiction, helping organizations understand their compliance obligations.</p>
        </div>
        ''', unsafe_allow_html=True)
        jurisdictions = self.law_inference.get_jurisdictions()
        selected_jurisdiction = st.selectbox(
            "Select Jurisdiction",
            jurisdictions,
            index=0 if jurisdictions else None
        )
        analyze_button = st.button("Determine Applicable Laws")
        nodes = self.law_inference.get_decision_tree_nodes()
        edges = self.law_inference.get_decision_tree_edges()
        if analyze_button and selected_jurisdiction:
            applicable_laws = self.law_inference.get_applicable_laws(selected_jurisdiction)
            if applicable_laws:
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: #3498db25; border: 2px solid #3498db; margin-top: 20px;">
                    <h3 style="color: #3498db;">Laws Applicable to {selected_jurisdiction}</h3>
                    <p>The following laws apply to activities in this jurisdiction:</p>
                </div>
                """, unsafe_allow_html=True)
                for i, law in enumerate(applicable_laws):
                    with st.expander(f"{i+1}. {law['name']}", expanded=True):
                        st.markdown(f"**Full Name:** {law['full_name']}")
                        st.markdown(f"**Description:** {law['description']}")
                        st.markdown(f"**Effective Date:** {law['effective_date']}")
            render_decision_tree_callback(nodes, edges, "Decision Tree", 700)
        else:
            st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-top: 20px;">
                <h3 style="color: #7F8C8D;">No Applicable Laws Found</h3>
                <p>No specific data protection laws were found for the selected jurisdiction in our database.</p>
                <p>This may be due to:</p>
                <ul>
                    <li>The jurisdiction may not have comprehensive data protection legislation</li>
                    <li>The jurisdiction may be covered by regional laws not specifically mapped in the database</li>
                    <li>The database may need to be updated with the latest regulatory information</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
