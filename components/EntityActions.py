import streamlit as st

from components.UX import UX
from repositories.ContextGraphRepository import ContextGraphRepository


class EntityActions:
    def __init__(self, context_graph_repo: ContextGraphRepository):
        self.context_graph_repo = context_graph_repo

    def actions(self):
        """Handles the logic for listing, enabling/disabling, and adding entity actions."""
        st.markdown("""
            <div style='font-size: 1em; margin-bottom: 15px;'>
                Manage and tailor actions specific to each entity type to enhance OT Explorer's recommendation engine. This section allows you to:
                <ul>
                    <li>Define custom actions for various entity types to align with your business processes.</li>
                    <li>Enable or disable existing actions to control their availability and relevance.</li>
                    <li>Add new actions to expand the platform's capabilities and address evolving business needs.</li>
                </ul>
                Utilize these tools to refine action recommendations from OT Explorer.
            </div>
            """, unsafe_allow_html=True)
        UX.divider()

        # Step 1: Select Entity Type
        entity_types = self.context_graph_repo.list_entity_types()
        if not entity_types:
            st.info("No entity types found. Please add entity types before managing actions.")
            return

        entity_type_labels = [et['label'] for et in entity_types]
        selected_entity_type = st.selectbox("Select Entity Type", entity_type_labels, key="selected_entity_type")

        # Fetch actions for the selected entity type
        actions = self.context_graph_repo.list_entity_actions_by_entity_type(selected_entity_type)

        if actions:
            # Create a form to batch update action statuses
            with st.form("update_entity_actions_form"):
                for action in actions:
                    # Display each action with a toggle to enable/disable
                    action_enabled = st.toggle(
                        f"**{action['action_name']}**: {action['description']}",
                        value=action.get('active', True),  # Default to True if 'active' not present
                        key=f"action_toggle_{action['id']}"
                    )
                    # Update the action's active status in the actions list
                    action['active'] = action_enabled

                # Submit button to update action statuses
                update_submit = st.form_submit_button("Update Actions")

                if update_submit:
                    # Save the updated enabled/disabled states to the database
                    for action in actions:
                        self.context_graph_repo.update_entity_action_status(action['id'], action['active'])
                    st.success("Entity actions updated successfully!")
                    st.rerun()  # Refresh the page to reflect changes

        else:
            st.info(f"No actions found for entity type '{selected_entity_type}'.")

        # Step 3: Add a New Action for the Selected Entity Type
        with st.form("add_entity_action_form", clear_on_submit=True):
            new_action_name = st.text_input("Action Name")
            new_api_endpoint = st.text_input("API Endpoint")
            new_description = st.text_area("Action Description")
            new_action_active = st.checkbox("Active", value=True)
            submit = st.form_submit_button("Add Entity Action")

            if submit:
                # Input Validation
                if not new_action_name:
                    st.error("Please provide an Action Name.")
                elif not new_api_endpoint:
                    st.error("Please provide an API Endpoint.")
                elif not new_description:
                    st.error("Please provide an Action Description.")
                else:
                    # Add the new action using the repository method
                    self.context_graph_repo.add_entity_action(
                        entity_type_label=selected_entity_type,
                        action_name=new_action_name,
                        api_endpoint=new_api_endpoint,
                        description=new_description,
                        active=new_action_active
                    )
                    st.success(f"Entity action '{new_action_name}' added successfully!")
                    st.rerun()

