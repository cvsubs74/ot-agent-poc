import os
from decimal import Decimal

import streamlit as st
import json
from datetime import datetime

import vertexai
from vertexai.generative_models import GenerativeModel

from enums.EntityType import EntityType
from enums.RelationshipType import RelationshipType
from repositories.ContextGraphRepository import ALLOWED_RELATIONSHIPS


# Custom JSON encoder to handle datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()  # Handle datetime serialization
        return super(CustomJSONEncoder, self).default(obj)


class GraphChatbot:
    def __init__(self, graph_repo, context_graph_generator, graph_visualizer):
        self.graph_repo = graph_repo
        self.context_graph_generator = context_graph_generator
        self.graph_visualizer = graph_visualizer
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]

        # Initialize Vertex AI with the provided project ID
        vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
        self.model = GenerativeModel(os.environ["MODEL"])

    def context_graph_analyzer_chatbot(self, graph_id, entity=None):
        # Fetch the graph details by ID
        if entity:
            graph_details = self.graph_repo.get_subgraph_for_entity(
                graph_id, entity)
        else:
            graph_details = self.graph_repo.get_graph_details_by_id(graph_id)

        if not graph_details:
            st.error(f"Graph with ID {graph_id} not found.")
            return

        # Convert the graph details to JSON using custom encoder
        graph_details_json = json.dumps(graph_details, indent=4, cls=CustomJSONEncoder)

        # Define categories of questions related to the graph
        categories = {
            "Data Transfer": [
                "What data is being transferred between entities?",
                "Which assets are involved in data transfer?",
                "How is data transfer managed between vendors and assets?",
                "What are the security protocols for data transfer?",
                "Are there any data transfer relationships between entities and vendors?"
            ],
            "Policies": [
                "What policies govern data transfer in this graph?",
                "How do policies impact vendor relationships?",
                "Are there any policies related to asset management?",
                "Which policies are connected to specific data flows?",
                "How are compliance and risk management policies enforced in the graph?"
            ],
            "Assets": [
                "What assets are part of this graph?",
                "Which assets are critical to data transfer?",
                "How are the assets related to the vendors in the graph?",
                "Are there any security measures linked to specific assets?",
                "What is the relationship between assets and policies in this graph?"
            ],
            "Vendors": [
                "Which vendors are involved in data transfer?",
                "What are the relationships between vendors and assets?",
                "Which vendors are responsible for managing data transfer?",
                "Are any vendors subject to specific policies?",
                "How do vendor relationships impact the risk profile of the graph?"
            ],
            "Risks and Controls": [
                "What are the identified risks in this graph?",
                "How are risks mitigated through controls?",
                "Which assets or entities are linked to specific risks?",
                "What controls are in place to manage vendor-related risks?",
                "How are risks related to data transfers being managed?",
                "What policies are associated with risk management in this graph?",
                "Are there any high-risk vendors or assets involved?",
                "What is the process for monitoring and updating risk controls?",
                "How are risk assessments conducted and reviewed in the graph?",
                "What are the critical controls in place for data security?"
            ]
        }

        # Initialize session state variables
        if 'selected_category' not in st.session_state:
            st.session_state.selected_category = None
        if 'selected_question' not in st.session_state:
            st.session_state.selected_question = None

        # Display categories as buttons
        category_keys = list(categories.keys())
        for i in range(0, len(category_keys), 5):
            cols = st.columns(5)
            for j in range(5):
                if i + j < len(category_keys):
                    category = category_keys[i + j]
                    if cols[j].button(category):
                        st.session_state.selected_category = category
                        st.session_state.selected_question = None

        # Display questions within the selected category
        if st.session_state.selected_category:
            self.divider()
            selected_category = st.session_state.selected_category
            questions = categories[selected_category]
            for i in range(0, len(questions), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(questions):
                        question = questions[i + j]
                        if cols[j].button(question):
                            st.session_state.selected_question = question

        # Retrieve previously asked questions for the graph and display them in a dropdown
        questions = self.graph_repo.get_graph_questions(graph_id)
        question_options = []
        if questions:
            question_options = ["--Select a question--"] + [q['question'] for q in questions]
            selected_question = st.selectbox("Select a question:", options=question_options)

            # Ensure that only valid selections are processed
            if selected_question and selected_question != "--Select a question--":
                st.session_state.selected_question = selected_question

        # Define a form for asking custom questions with clear_on_submit=True
        with st.form("question_form", clear_on_submit=True):
            # Provide a text input for custom questions
            user_question = st.text_input("Ask a question:", key="user_question")

            # Detect when the form is submitted (e.g., pressing Enter in the text input)
            submitted = st.form_submit_button("Submit")

            if submitted and user_question:  # Check if the form is submitted and the input is not empty
                # Check if the question already exists in the list of questions
                if user_question not in question_options:
                    self.graph_repo.add_graph_question(graph_id, user_question)
                st.session_state.selected_question = user_question

        # Handle the selected question
        if st.session_state.selected_question:
            self.handle_question(st.session_state.selected_question, graph_details_json)
            st.session_state.selected_question = None

    def handle_question(self, question, graph_details_json):
        """
        Handles the logic of answering a graph-related question by injecting the graph details into the response.
        If 'show_json' is true, display the graph JSON to the user.
        """
        # Parse the graph details back into a Python dictionary
        graph_data = json.loads(graph_details_json)

        # Extract specific data from graph_data
        relationships = json.dumps(graph_data.get('relationships', []), indent=2, cls=CustomJSONEncoder)

        # Prepare hyperlinked actions based on entities in the graph
        actions = self.get_actions_from_graph(graph_data)

        # If no actions are available, adjust the prompt accordingly
        if not actions.strip():
            actions = "No specific actions are available for these entities."

        # Construct the prompt for the AI model based on the graph details and the user's question
        prompt = f"""
            The user has asked the following question: "{question}"

            Here is the relevant information:

            **Entities and Relationships:**
            {relationships}

            **Available Actions** (if needed): 
            {actions}

            Provide a direct, detailed, and insightful response to the user's question. Ensure the response:

            - Directly answers the question using only the information present in the graph data.
            - Avoids any assumptions or speculative statements, such as "likely," "possibly," or "could."
            - Focuses solely on the relationships, entities, and connections as defined in the graph data, ensuring that the analysis is strictly factual and data-driven.
            - Highlights important information by **bolding** them.
            - Uses bullet points for clarity and emphasis wherever applicable.
            - Recommends actions **only if absolutely necessary**, and only if they are directly supported by the graph data, using hyperlinks for **Available Actions** when applicable.
            """

        try:
            # Generate content using Google Vertex AI Generative Model
            with st.spinner("Please wait..."):
                response = self.model.generate_content(prompt)

            # Return the response content
            if response and hasattr(response, 'text'):
                # Show the response from the model as Markdown
                st.markdown(response.text, unsafe_allow_html=True)
            else:
                st.warning("Please try again later.")
        except Exception as e:
            # Log the exception for debugging purposes
            st.error(f"An error occurred: {str(e)}")
            st.warning("Please try again later.")

    @staticmethod
    def get_actions_from_graph(graph_data):
        """
        Get the actions for all entities present in the graph based on their type and generate clickable hyperlinks.
        """
        entities = graph_data.get('relationships', [])
        actions_html = []

        for entity in entities:
            # Get the entity types
            try:
                source_type = EntityType.from_value(entity['source_entity_type'])
                target_type = EntityType.from_value(entity['target_entity_type'])
            except ValueError:
                continue  # Skip if the entity type is not recognized

            # Extract actions for the source and target entity types
            source_actions = source_type.value.get('actions', [])
            target_actions = target_type.value.get('actions', [])

            # Generate clickable links for actions for the source entity
            for action in source_actions:
                action_name = action['action_name']
                action_url = action['api_endpoint']
                # Creating proper clickable link using triggerAction
                actions_html.append(
                    f"<a href='#' onclick='triggerAction(\"{action_url}\")'>{action_name}</a>: {action['description']}"
                )

            # Generate clickable links for actions for the target entity
            for action in target_actions:
                action_name = action['action_name']
                action_url = action['api_endpoint']
                # Creating proper clickable link using triggerAction
                actions_html.append(
                    f"<a href='#' onclick='triggerAction(\"{action_url}\")'>{action_name}</a>: {action['description']}"
                )

        # Convert actions list to a string for the prompt
        return "<br>".join(actions_html)

    def context_graph_generation_chatbot(self):
        # Pre-seeded graph categories and subcategories with 10 different categories
        st.markdown(
            """
            <div style='font-size: 1em; margin-bottom: 15px;'>
                Build custom context graphs that represent relationships between various entities 
                such as vendors, assets, policies, risks, and more. You can start by selecting one of the pre-defined categories or subcategories, or provide 
                detailed custom instructions to generate your own graph tailored to your specific business needs. Each graph can help you visualize data flow, 
                assess risk exposure, and ensure compliance with regulations. 
                <br><br>
                Use this feature to:
                <ul>
                    <li>Create context graphs for data transfers, risk assessments, and vendor management.</li>
                    <li>Explore complex relationships between policies, assets, vendors, and controls.</li>
                    <li>Identify compliance gaps and take corrective actions based on visualized data.</li>
                    <li>Generate customized graphs by providing specific instructions related to your data ecosystem.</li>
                </ul>
                Once the graph is generated, you can visualize it and interact with it through our chatbot interface to further explore the insights.
            </div>
            """, unsafe_allow_html=True)
        self.divider()

        privacy_graphs = {
            # Your privacy_graphs categories
        }

        # Step 1: Allow user to select a category using buttons
        selected_category = None
        graph_id = None

        # Display category buttons (5 per row)
        category_keys = list(privacy_graphs.keys())
        for i in range(0, len(category_keys), 5):
            cols = st.columns(5)
            for j in range(5):
                if i + j < len(category_keys):
                    category = category_keys[i + j]
                    if cols[j].button(category):
                        selected_category = category
                        st.session_state.graph_creation_selected_category = category

        self.divider()

        # Step 2: If a category is selected, show subcategory buttons
        if 'graph_creation_selected_category' in st.session_state and st.session_state.graph_creation_selected_category:
            selected_category = st.session_state.graph_creation_selected_category
            subcategories = privacy_graphs[selected_category]
            subcategory_keys = list(subcategories.keys())
            for i in range(0, len(subcategory_keys), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(subcategory_keys):
                        subcategory = subcategory_keys[i + j]
                        if cols[j].button(subcategory):
                            st.session_state.graph_creation_selected_subcategory = subcategory

        # Show description for the selected subcategory
        if 'graph_creation_selected_subcategory' in st.session_state:
            selected_subcategory = st.session_state.graph_creation_selected_subcategory
            title = privacy_graphs[selected_category][selected_subcategory]
        else:
            title = "Custom Graph"

        # Step 3: Create graph based on selection or instructions
        instruction = st.text_input("Enter custom instructions to generate a context graph:")

        # Only generate JSON if the user clicks the "Create Graph" button
        if st.button("Create Graph"):
            generated_json = None
            if 'graph_creation_selected_category' in st.session_state and 'graph_creation_selected_subcategory' in st.session_state:
                # Automatically generate instruction based on selection
                generated_json = self.generate_graph_generation_json(
                    f"{st.session_state.graph_creation_selected_category}: {st.session_state.graph_creation_selected_subcategory}"
                )
            elif instruction:
                # Use custom instruction
                generated_json = self.generate_graph_generation_json(instruction)

            if generated_json:
                try:
                    graph_data = json.loads(generated_json)
                    graph_id, graph_name, success = self.context_graph_generator.create_graph_from_json(graph_data)
                    if success:
                        summary = self.summarize_graph(generated_json)
                        st.success(f"Graph '{graph_name}' created successfully!")

                        # Displaying the title and summary with a line space using markdown
                        st.markdown(f"""
                            <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
                                <strong>{title}</strong>
                                <br><br>
                                {summary}
                            </div>
                        """, unsafe_allow_html=True)

                        # Clear session state variables related to graph creation
                        for key in ['graph_creation_selected_category', 'graph_creation_selected_subcategory']:
                            if key in st.session_state:
                                del st.session_state[key]
                        self.graph_visualizer.visualize_graph(graph_id)
                    else:
                        st.error(f"Failed to create graph '{graph_name}'.")
                except json.JSONDecodeError:
                    st.error("Invalid JSON format. Please check your input.")
            else:
                st.warning("Please select a category, subcategory, or provide custom instructions to create a graph.")

        return graph_id

    def generate_graph_generation_json(self, instruction):
        """
        Use Vertex AI to generate a valid JSON for graph creation based on the given instruction,
        utilizing the entity types, relationship types, and allowed relationships. Ensure the graph has at least 50 nodes.
        """

        # Dynamically build the entity types and relationship types from the enums
        entity_types = [et.value["label"] for et in EntityType]  # Accessing the 'label' field correctly
        relationship_types = [rt.value for rt in RelationshipType]

        # Convert allowed relationships into a string format
        allowed_relationships_str = ""
        for relationship_type, pairs in ALLOWED_RELATIONSHIPS.items():
            allowed_relationships_str += f"\n- {relationship_type.value}:\n"
            for source, target in pairs:
                allowed_relationships_str += f"    ({source.value['label']} -> {target.value['label']})\n"  # Correctly accessing 'label'

        prompt = f"""
        The user has provided the following instruction: "{instruction}"

        Based on this instruction, generate a valid JSON for a graph creation. If the instruction specifies a particular number of nodes or entities, ensure that the graph adheres to that specification. Otherwise, generate a graph with **at most 50 nodes**. The format should be:

        {{
            "graph_name": "<Name of the graph>",
            "description": "<Description of the graph>",
            "entities": [
                {{ "type": "EntityType", "name": "EntityName" }},
                ...
            ],
            "relationships": [
                {{ "source": "EntityName1", "target": "EntityName2", "relationship": "RelationshipType" }},
                ...
            ]
        }}

        Ensure that the graph adheres to the specified or default number of entities. Here are the possible entity types:
        {', '.join(entity_types)}

        Here are the possible relationship types:
        {', '.join(relationship_types)}

        These are the allowed relationships:
        {allowed_relationships_str}

        Ensure that the response **only** contains a valid JSON object with no other explanation, commentary, or natural language text. Return only the JSON.
        """

        try:
            # Call the AI model to generate the JSON based on instruction
            with st.spinner("Generating the graph.."):
                response = self.model.generate_content(prompt)

            # Ensure that we strip the response and only extract the JSON part
            if response and hasattr(response, 'text'):
                response_text = response.text.strip()

                # Find the first occurrence of '{' and the last occurrence of '}'
                start_index = response_text.find('{')
                end_index = response_text.rfind('}')

                if start_index != -1 and end_index != -1:
                    # Extract the valid JSON part
                    json_content = response_text[start_index:end_index + 1]
                    return json_content
                else:
                    st.error("The generated response does not contain a valid JSON object.")
                    return None
            else:
                st.error("No valid response from the AI model.")
                return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    def summarize_graph(self, generated_json):
        """
        Generates a concise, business-oriented summary of the graph using the LLM without describing the entities.

        :param generated_json: Dictionary containing the graph details (entities, relationships).
        :return: A formatted summary of the graph generated by the LLM.
        """

        # Count the number of entities and relationships
        graph_data = json.loads(generated_json)
        entity_count = len(graph_data.get("entities", []))
        relationship_count = len(graph_data.get("relationships", []))

        # Prepare the concise, high-level business-oriented prompt
        prompt = f"""
        Provide a brief summary of the purpose and key insights of the graph. The graph contains {entity_count} entities and {relationship_count} relationships. Explain the overall purpose of the graph in business terms, without describing individual entities.
        """

        try:
            # Call the LLM to generate the summary based on the prompt
            with st.spinner("Generating the graph summary..."):
                response = self.model.generate_content(prompt)

            if response and hasattr(response, 'text'):
                # Return the LLM-generated summary
                return response.text
            else:
                st.warning("Failed to generate the summary. Please try again later.")
                return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    @staticmethod
    def divider(height=1):
        """Utility function to create a divider with specified height."""
        st.markdown(f"<hr style='height:{height}px; "
                    f"margin-top: 0;  margin-bottom: 0; border-width:0; background: lightblue;'>",
                    unsafe_allow_html=True)
