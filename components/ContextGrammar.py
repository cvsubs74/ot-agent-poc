import streamlit as st

from components.UX import UX
from repositories.ContextGraphRepository import ContextGraphRepository


class ContextGrammar:
    def __init__(self, context_graph_repo: ContextGraphRepository):
        self.context_graph_repo = context_graph_repo

    def rules(self):
        """Handles the logic for listing, enabling/disabling, modifying rule details, and adding new business rules."""
        st.markdown("""
                <div style='font-size: 1em; margin-bottom: 15px;'>
                    Customize OT Explorer's recommendation engine by:
                    <ul>
                        <li>Defining your own context rules to tailor recommendations to your business needs.</li>
                        <li>Enabling, disabling, or editing rules to refine the system's insights based on your unique requirements.</li>
                    </ul>
                    Utilize these tools to refine the analysis and recommendations from OT Explorer.
                </div>
            """, unsafe_allow_html=True)
        UX.divider()

        # Fetch and display existing rules for enabling/disabling
        rules = self.context_graph_repo.list_context_grammar_rules()
        if rules:
            st.subheader("Enable/Disable Rules")
            for rule in rules:
                rule_enabled = st.toggle(
                    f"**{rule['rule_name']}**: {rule['description']}", value=rule['active'], key=f"active_{rule['id']}"
                )

                # Check if the toggle state changed, and update the database if needed
                if rule_enabled != rule['active']:
                    self.context_graph_repo.enable_disable_rule(rule['id'], rule_enabled)
                    st.success(f"Rule '{rule['rule_name']}' status updated to {'enabled' if rule_enabled else 'disabled'}.")

        else:
            st.info("No business rules found.")

        UX.divider()

        # Dropdown to select a rule and modify it
        if rules:
            st.subheader("Modify Existing Rule")
            rule_options = {rule['rule_name']: rule for rule in rules}
            selected_rule_name = st.selectbox("Select a rule to modify", list(rule_options.keys()))

            if selected_rule_name:
                selected_rule = rule_options[selected_rule_name]

                # Modify rule name and description
                with st.form("modify_rule_form"):
                    new_rule_name = st.text_input("Rule Name", value=selected_rule['rule_name'])
                    new_rule_description = st.text_area("Rule Description", value=selected_rule['description'])
                    modify_submit = st.form_submit_button("Update Rule")

                    if modify_submit and new_rule_name and new_rule_description:
                        self.context_graph_repo.update_context_grammar_rule(
                            selected_rule['id'], selected_rule['active'], new_rule_name, new_rule_description
                        )
                        st.success(f"Rule '{new_rule_name}' updated successfully!")
                        st.rerun()

        UX.divider()

        # Form to add a new rule
        st.subheader("Add New Rule")
        with st.form("add_rule_form", clear_on_submit=True):
            new_rule_name = st.text_input("Rule Name")
            new_rule_description = st.text_area("Rule Description")
            add_rule_submit = st.form_submit_button("Add Rule")

            if add_rule_submit and new_rule_name and new_rule_description:
                self.context_graph_repo.add_context_grammar_rule(new_rule_name, new_rule_description)
                st.success(f"Rule '{new_rule_name}' added successfully!")
                st.rerun()
