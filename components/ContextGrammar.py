import streamlit as st

from components.UX import UX
from repositories.ContextGraphRepository import ContextGraphRepository


class ContextGrammar:
    def __init__(self, context_graph_repo: ContextGraphRepository):
        self.context_graph_repo = context_graph_repo

    def rules(self):
        """Handles the logic for listing, enabling/disabling, and adding business rules."""
        st.markdown("""
                <div style='font-size: 1em; margin-bottom: 15px;'>
                    Customize OT Explorer's recommendation engine by:
                    <ul>
                        <li>Defining your own context rules to tailor recommendations to your business needs.</li>
                        <li>Enabling or disabling rules to refine the system's insights based on your unique requirements.</li>
                    </ul>
                    Utilize these tools to refine the analysis and recommendations from OT Explorer.
                </div>
            """, unsafe_allow_html=True)
        UX.divider()

        # Fetch and display existing rules with enable/disable toggles
        rules = self.context_graph_repo.list_context_grammar_rules()
        if rules:
            # Create a form to batch update rule status
            with st.form("update_rules_form"):
                for rule in rules:
                    # Display each rule with a toggle to enable/disable
                    rule_enabled = st.toggle(
                        f"**{rule['rule_name']}**: {rule['description']}", value=rule['active'], key=rule['id']
                    )
                    # Store the enabled/disabled state for the rule
                    rule['active'] = rule_enabled

                # Add a submit button for saving changes to the rules
                update_submit = st.form_submit_button("Update Rules")

                if update_submit:
                    # Save the updated enabled/disabled states to the database
                    for rule in rules:
                        self.context_graph_repo.update_context_grammar_rule(rule['id'], rule['active'])
                    st.success("Rules updated successfully!")
        else:
            st.info("No business rules found.")

        # Form to add a new rule
        with st.form("add_rule_form", clear_on_submit=True):
            new_rule_name = st.text_input("Rule Name")
            new_rule_description = st.text_area("Rule Description")
            submit = st.form_submit_button("Add Rule")

            if submit and new_rule_name and new_rule_description:
                self.context_graph_repo.add_context_grammar_rule(new_rule_name, new_rule_description)
                st.success(f"Rule '{new_rule_name}' added successfully!")
                st.rerun()

