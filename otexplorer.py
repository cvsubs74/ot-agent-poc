import streamlit as st
from components.GraphVisualizer import GraphVisualizer
from components.ContextGraphGenerator import ContextGraphGenerator
from components.GraphChatbot import GraphChatbot
from repositories.ContextGraphRepository import ContextGraphRepository
from repositories.DatabaseManager import DatabaseManager
import pymysql


class OTExplorer:
    def __init__(self):
        """Initialize the core components of the app."""
        self.database_manager = DatabaseManager()
        self.context_graph_repo = ContextGraphRepository(self.database_manager.connection)
        self.context_graph_generator = ContextGraphGenerator(self.context_graph_repo)
        self.graph_visualizer = GraphVisualizer(self.context_graph_generator)
        self.graph_chatbot = GraphChatbot(
            self.context_graph_repo, self.context_graph_generator, self.graph_visualizer)

    def configure_page(self):
        """Configure the Streamlit page settings."""
        st.set_page_config(page_title="OT Explorer - Contextual Graph Generator and Explorer", layout="wide")

        # Inject custom CSS for styling tabs
        st.markdown("""
        <style>
        .stTabs [role="tablist"] {
            background-color: #f4f4f4; /* Tab background color */
            padding: 5px;
            border-radius: 10px;
        }
        .stTabs [role="tab"] {
            background-color: #0e76a8; /* Individual tab background color */
            color: white;
            font-size: 18px;
            margin-right: 0px;
            padding: 20px;
            border-radius: 5px;
        }
        .stTabs [role="tab"]:hover {
            background-color: #005682; /* Hover color for tabs */
            color: #f4f4f4;
        }
        .stTabs [role="tab"]:active {
            background-color: #003f5c; /* Active tab background color */
        }
        .intro-text {
            font-size: 18px; 
            color: #318283; 
            margin-bottom: 15px;
        }
        </style>
        """, unsafe_allow_html=True)

    def create_graph(self):
        """Handle the Create Graph functionality."""
        graph_id = self.graph_chatbot.context_graph_generation_chatbot()
        if graph_id:
            st.session_state['graph_id'] = graph_id  # Store in session state for access across tabs
        return graph_id

    def explore_graph(self, graph_id=None):
        """Handle the Explore Graph functionality."""
        st.markdown("""
        <div style='font-size: 1em; margin-bottom: 15px;'>
            Dive deep into existing scenarios, which represent the complex relationships between various entities such as vendors, assets, policies, risks, and more. 
            <br><br>
            Each scenario is a visual representation of how entities are interconnected, and it allows you to:
            <ul>
                <li>Visualize and explore the entire network of entities and relationships in a clear, interactive graph.</li>
                <li>Select specific entities to drill down into their relationships, revealing all their direct and indirect connections.</li>
                <li>Leverage the built-in chatbot to query the graph and receive context-driven answers, helping you analyze relationships and take context-sensitive actions.</li>
            </ul>
            Use this powerful tool to gain insights, identify potential risks, and monitor compliance across your organizational data in real time.
        </div>
        """, unsafe_allow_html=True)

        # Get graph list
        graphs = self.context_graph_generator.list_graphs()

        if not graphs:
            st.info("No scenarios found. Please create a new scenario in the 'Create Scenario' tab.")
        else:
            graph_options = {f"{graph['name']}": graph for graph in graphs}
            graph_names = ["--Select a Scenario--"] + list(graph_options.keys())  # Add default option

            # Retrieve the graph_id from session state or passed value
            if graph_id is None:
                graph_id = st.session_state.get('graph_id')  # Get from session state if not passed

            # Callback to update session state when graph selection changes
            def update_selected_graph():
                selected_graph_name = st.session_state['selected_graph_name']
                selected_graph = graph_options.get(selected_graph_name)
                if selected_graph:
                    st.session_state['graph_id'] = selected_graph['id']

            # Set default selected graph
            selected_graph_name = next(
                (name for name, graph in graph_options.items() if graph['id'] == graph_id),
                "--Select a Scenario--"
            )

            # Dropdown to select a graph, with an on_change callback
            st.selectbox("Select a Scenario", graph_names, index=graph_names.index(selected_graph_name),
                         key="selected_graph_name", on_change=update_selected_graph)

            # Continue only if a valid graph is selected
            if selected_graph_name != "--Select a Scenario--":
                selected_graph = graph_options[selected_graph_name]
                graph_id = selected_graph['id']
                st.session_state['graph_id'] = graph_id  # Update session state with selected graph_id

                # Visualize the full graph
                entities = []
                relationships = self.context_graph_generator.context_graph_repo.get_relationships_for_graph(graph_id)
                if relationships:
                    entity_set = set()
                    for rel in relationships:
                        entity_set.add((rel['source_entity_type'], rel['source_entity_name']))
                        entity_set.add((rel['target_entity_type'], rel['target_entity_name']))
                    entities = [{'name': name, 'type': etype} for etype, name in entity_set]
                    self.graph_visualizer.visualize(entities, relationships)
                else:
                    st.warning("No relationships found in this graph.")

                # Display dropdown for entity selection below the graph
                entity_names = ["--Select an entity--"] + [entity['name'] for entity in entities]
                selected_entity_name = st.selectbox("Select an Entity to Explore", entity_names)

                if selected_entity_name != "--Select an entity--":
                    subgraph_data = self.context_graph_repo.get_subgraph_for_entity(graph_id, selected_entity_name)

                    if subgraph_data:
                        sub_entities = subgraph_data['entities']
                        sub_relationships = subgraph_data['relationships']

                        # Visualize the subgraph
                        self.graph_visualizer.visualize(sub_entities, sub_relationships)
                    else:
                        st.warning(f"No relationships found for entity: {selected_entity_name}")

                # Display chatbot functionality below the graph
                st.markdown("<h3 style='text-align: center; font-size: 24px;'>Query Explorer</h3>",
                            unsafe_allow_html=True)
                self.graph_chatbot.context_graph_analyzer_chatbot(
                    graph_id, None if selected_entity_name == "--Select an entity--" else selected_entity_name)

    def display_business_rules(self):
        """Handles the logic for listing, enabling/disabling, and adding business rules."""
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

    def run(self):
        """Main function to run the Streamlit app."""
        # Step 1: Configure the page
        self.configure_page()

        # Step 2: Application Title
        st.markdown("<h3 style='text-align: center;'>OT Explorer - A New Paradigm in Contextual Intelligence</h3>", unsafe_allow_html=True)

        # Step 3: Introduction Section
        st.write(f"""
            #### **Welcome to OT Explorer**

            **Unlock the Power of Context-Driven Insights and Actionable Intelligence**

            OT Explorer revolutionizes how organizations explore and manage their data by offering an interactive, context-driven graph platform. Whether you're looking to understand risks, manage vendor relationships, or ensure compliance, OT Explorer brings clarity to your complex data landscape:

            - **Visualize & Analyze**: Create dynamic scenarios that represent the relationships between vendors, assets, policies, risks, and more, allowing you to see the full context of your data.
            - **Interact & Act**: Explore your scenario through a chatbot interface that allows you to ask complex business questions and receive detailed, contextually relevant answers. Take action directly within the interface by triggering risk assessments, audits, and more.
            - **Monitor & Mitigate**: OT Explorer ensures you stay ahead of risks with real-time insights and actions. Visualize how entities are connected, spot potential issues, and take proactive measures.

            Ready to explore and take action? **Create a scenario**, **explore existing scenarios**, or manage **business rules** to see how OT Explorer can transform your decision-making process.
        """)

        # Step 4: Create tabs for "Create Scenarios", "Explore Scenarios", and "Business Rules"
        tab1, tab2, tab3 = st.tabs(["Create Scenarios", "Explore Scenarios", "Business Rules"])

        with tab1:
            graph_id = self.create_graph()

        with tab2:
            self.explore_graph(graph_id)

        with tab3:
            self.display_business_rules()


if __name__ == "__main__":
    app = OTExplorer()
    app.run()
