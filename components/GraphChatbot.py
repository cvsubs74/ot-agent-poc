import os
from decimal import Decimal

import streamlit as st
import json
from datetime import datetime

import vertexai
from vertexai.generative_models import GenerativeModel

from components.UX import UX
from enums.EntityType import EntityType
from enums.RelationshipType import RelationshipType
from repositories.ContextGraphRepository import ENTITY_TYPE_ATTRIBUTES, ALLOWED_RELATIONSHIPS


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
        # Fetch the graph details by ID, including entities with their attributes
        if entity:
            graph_details = self.graph_repo.get_subgraph_for_entity(graph_id, entity)
        else:
            graph_details = self.graph_repo.get_graph_details_by_id(graph_id)

        if not graph_details:
            st.error(f"Graph with ID {graph_id} not found.")
            return

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
            UX.divider()
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
            response = self.handle_question(st.session_state.selected_question, graph_details)
            st.markdown(response, unsafe_allow_html=True)
            st.session_state.selected_question = None

    def ai_insights_context_graph_analyzer_chatbot(self):
        if 'ai_insights_selected_question' not in st.session_state:
            st.session_state.ai_insights_selected_question = None

        if 'ai_insights_question_responses' not in st.session_state:
            st.session_state.ai_insights_question_responses = {}  # Dictionary to store question-response pairs

        # Retrieve previously asked questions (no filtering by graph_id, as it's across all graphs)
        questions = self.graph_repo.get_graph_questions()
        question_options = []
        selected_question = None
        if questions:
            question_options = ["--Select a question--"] + [q['question'] for q in questions]

            # Display the dropdown to select a question from previous questions
            selected_question = st.selectbox("Select a question:", options=question_options,
                                             key="ai_insights_select_question")

        # Process selected question from dropdown
        if selected_question and selected_question != "--Select a question--":
            st.session_state.ai_insights_selected_question = selected_question

        # Define a form for asking custom questions with clear_on_submit=True
        with st.form("ai_insights_question_form", clear_on_submit=True):
            # Provide a text input for custom questions
            user_question = st.text_input("Ask a new question:", key="ai_insights_user_question")

            # Detect when the form is submitted (e.g., pressing Enter in the text input)
            submitted = st.form_submit_button("Submit")

            if submitted and user_question:
                # Add the new question if it's not already in the list of previous questions
                if user_question not in question_options:
                    self.graph_repo.add_graph_question(None,
                                                       user_question)  # Add the question with no specific graph_id
                st.session_state.ai_insights_selected_question = user_question

        # Handle the selected or newly submitted question
        if st.session_state.ai_insights_selected_question:
            question = st.session_state.ai_insights_selected_question

            # Check if the response for the selected question is already stored
            if question in st.session_state.ai_insights_question_responses:
                # Retrieve the stored response
                response = st.session_state.ai_insights_question_responses[question]
            else:
                # Fetch all graph details, including entities with their attributes
                with st.spinner("Please wait.."):
                    graph_details = self.graph_repo.get_all_graph_details()

                # Call handle_question and store the response in session state
                response = self.handle_question(question, graph_details)
                st.session_state.ai_insights_question_responses[question] = response

            # Display the response
            st.markdown(response, unsafe_allow_html=True)

        UX.divider()
        st.write("")
        entities = self.graph_repo.get_entities()
        entity_names = ["--Select an entity--"] + [entity['name'] for entity in entities]
        selected_entity_name = st.selectbox("Select an Entity to Explore", entity_names,
                                            key="ai_insights_selected_entity_name")
        if selected_entity_name != "--Select an entity--":
            entity = self.graph_repo.get_entity_by_name(selected_entity_name)
            subgraph_data = self.graph_repo.get_subgraph_for_entity(entity["graph_id"], selected_entity_name)

            if subgraph_data:
                sub_entities = subgraph_data['entities']
                sub_relationships = subgraph_data['relationships']

                # Visualize the subgraph
                self.graph_visualizer.visualize(sub_entities, sub_relationships)

    def handle_question(self, question, graph_details):
        """
        Handles the logic of answering a graph-related question by injecting the graph details into the response.
        If 'show_json' is true, display the graph JSON to the user.
        """
        # Fetch the context grammar rules from the database
        context_grammar_rules = self.graph_repo.get_enabled_rules()

        # Format the context grammar rules into a string for the prompt
        context_grammar = "\n".join(
            [f"- **{rule['rule_name']}**: {rule['description']}" for rule in context_grammar_rules])

        # Convert relationships from the graph details to JSON
        relationships_json = json.dumps(graph_details.get('relationships', []), indent=4, cls=CustomJSONEncoder)

        # Extract entities and their attributes from the graph details
        entities = graph_details.get('entities', [])
        entities_with_attributes = "\n".join(
            [f"- **{entity['name']}** ({entity['type']}): {json.dumps(entity['attributes'], indent=2)}" for entity in
             entities])

        # Prepare hyperlinked actions based on entities in the graph
        actions = self.get_actions_from_graph(graph_details)

        # Construct the prompt for the AI model based on the graph details and the user's question
        prompt = f"""
            The user has asked the following question: "{question}"

            Here is the relevant information:

            **Entities and their Attributes:**
            {entities_with_attributes}

            **Relationships:**
            {relationships_json}
            
            **Available Actions** (if needed): 
            {actions}

            **Context Grammar:**
            {context_grammar}

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
                response = response.text
            else:
                st.warning("Please try again later.")
        except Exception as e:
            # Log the exception for debugging purposes
            st.error(f"An error occurred: {str(e)}")
            st.warning("Please try again later.")

        return response

    def get_actions_from_graph(self, graph_data):
        """
        Get the actions for all entities present in the graph based on their type and generate clickable hyperlinks.

        Parameters:
        - graph_data (dict): The graph data containing entities and their attributes.

        Returns:
        - str: A string containing HTML-formatted clickable action links separated by line breaks.
        """
        entities = graph_data.get('entities', [])  # Get entities from the graph data
        actions_html = []

        for entity in entities:
            # Get the entity type
            entity_type_str = entity.get('type')
            if not entity_type_str:
                continue  # Skip if entity type is missing

            try:
                # Convert the entity type string to its enum value
                entity_type = EntityType.from_value(entity_type_str)
            except ValueError:
                continue  # Skip if the entity type is not recognized

            # Fetch actions from the repository for the entity type
            actions = self.graph_repo.list_entity_actions_by_entity_type(entity_type.value)

            # Generate clickable links for actions associated with the entity
            for action in actions:
                action_name = action['action_name']
                action_url = action['api_endpoint']
                description = action['description']
                # Creating clickable link using triggerAction JavaScript function
                actions_html.append(
                    f"<a href='#' onclick='triggerAction(\"{action_url}\")'>{action_name}</a>: {description}"
                )

        # Convert the list of action links into a single HTML string separated by line breaks
        return "<br>".join(actions_html)

    def context_graph_generation_chatbot(self):
        # Pre-seeded graph categories and subcategories with 10 different categories
        st.markdown(
            """
            <div style='font-size: 1em; margin-bottom: 15px;'>
                Build scenarios that represent relationships between various entities 
                such as vendors, assets, policies, risks, and more. You can start by selecting one of the pre-defined categories or subcategories, or provide 
                detailed custom instructions to generate your own scenario tailored to your specific business needs. Each scenario can help you visualize data flow, 
                assess risk exposure, and ensure compliance with regulations. 
                <br><br>
                Use this feature to:
                <ul>
                    <li>Create scenarios for data transfers, risk assessments, and vendor management.</li>
                    <li>Explore complex relationships between policies, assets, vendors, and controls.</li>
                    <li>Identify compliance gaps and take corrective actions based on visualized data.</li>
                    <li>Generate customized scenarios by providing specific instructions related to your data ecosystem.</li>
                </ul>
                Choose a category and subcategory below to construct your scenario.
            </div>
            """, unsafe_allow_html=True)
        UX.divider()

        # Pre-seeded graph categories and subcategories
        privacy_scenarios = {
            "Data Transfers": {
                "Cross-Border Transfers": "International data transfers involving multiple jurisdictions, vendors, and compliance checks.",
                "Sensitive Data Transfers": "Transfers of sensitive personal data with encryption, access controls, and risk assessments.",
                "Third-Party Data Sharing": "Sharing personal data with third-party vendors, covering contracts and data processing agreements."
            },
            "Policies and Compliance": {
                "GDPR Compliance": "Ensuring GDPR compliance, covering data protection policies and lawful processing.",
                "Privacy Impact Assessment": "Evaluating data processing activities and mitigating privacy risks under regulations.",
                "Data Retention and Deletion": "Managing data retention policies and deletion processes for compliance."
            },
            "Vendor and Third-Party Management": {
                "Third-Party Risk Management": "Assessing third-party risks and ensuring vendor compliance with regulations.",
                "Vendor Data Processing Agreements": "Managing vendor relationships and ensuring data processing agreements are in place.",
                "Supply Chain Security": "Securing data flows in the supply chain and managing vendor agreements."
            },
            "Risk Management": {
                "Privacy Risk Assessments": "Evaluating privacy-related risks and mitigation strategies.",
                "Compliance Risk Monitoring": "Monitoring compliance risks with frameworks like GDPR and CCPA.",
                "Incident Response and Mitigation": "Responding to data breaches and mitigating associated risks."
            },
            "Security Management": {
                "Asset Security": "Implementing security measures like encryption and access control for assets.",
                "Threat Detection": "Real-time detection of security threats involving assets and vulnerabilities.",
                "Breach Response": "Responding to security breaches and addressing asset-related risks."
            },
            "Compliance Audits": {
                "Internal Audits": "Conducting internal compliance audits across departments and assets.",
                "Third-Party Audits": "Auditing third-party vendors for compliance with contracts and regulations.",
                "GDPR Audits": "Ensuring compliance with GDPR through regular audits."
            },
            "Data Management": {
                "Data Classification": "Categorizing sensitive, personal, and internal data for proper management.",
                "Data Lifecycle": "Managing data from collection to deletion, including retention policies.",
                "Data Minimization": "Ensuring only necessary data is collected and stored."
            },
            "Incident Management": {
                "Incident Tracking": "Tracking security incidents and linking them to assets and vendors.",
                "Incident Mitigation": "Mitigating the impact of incidents through effective response measures.",
                "Incident Reporting": "Reporting incidents across departments with clear communication."
            },
            "Access Management": {
                "Role-Based Access": "Managing role-based access controls for systems, vendors, and assets.",
                "Access Control Policies": "Implementing access control policies for managing data and assets.",
                "Third-Party Access": "Controlling third-party access to sensitive data and assets."
            },
            "AI Governance": {
                "Model Accountability": "Ensuring that AI models adhere to ethical standards and accountability frameworks.",
                "Model Transparency": "Tracking the transparency of AI models, including data sources and decision-making processes.",
                "Governance Compliance": "Ensuring AI governance policies comply with regulations, ethical standards, and industry best practices."
            }
        }

        # Step 1: Allow user to select a category using buttons
        graph_id = None

        # Display category buttons (5 per row)
        category_keys = list(privacy_scenarios.keys())
        for i in range(0, len(category_keys), 5):
            cols = st.columns(5)
            for j in range(5):
                if i + j < len(category_keys):
                    category = category_keys[i + j]
                    if cols[j].button(category):
                        st.session_state.graph_creation_selected_category = category

        UX.divider()

        # Step 2: If a category is selected, show subcategory buttons
        if 'graph_creation_selected_category' in st.session_state and st.session_state.graph_creation_selected_category:
            selected_category = st.session_state.graph_creation_selected_category
            subcategories = privacy_scenarios[selected_category]
            subcategory_keys = list(subcategories.keys())
            for i in range(0, len(subcategory_keys), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(subcategory_keys):
                        subcategory = subcategory_keys[i + j]
                        if cols[j].button(subcategory):
                            st.session_state.graph_creation_selected_subcategory = subcategory

        # Step 3: Automatically generate the graph if both category and subcategory are selected
        if 'graph_creation_selected_category' in st.session_state and 'graph_creation_selected_subcategory' in st.session_state:
            selected_category = st.session_state.graph_creation_selected_category
            selected_subcategory = st.session_state.graph_creation_selected_subcategory
            title = privacy_scenarios[selected_category][selected_subcategory]

            # Automatically generate the graph based on category and subcategory
            generated_json = self.generate_graph_generation_json(
                f"{st.session_state.graph_creation_selected_category}: {st.session_state.graph_creation_selected_subcategory}"
            )

            if generated_json:
                try:
                    graph_data = json.loads(generated_json)
                    graph_id, graph_name, success = self.context_graph_generator.create_graph_from_json(graph_data)
                    if success:
                        summary = self.summarize_graph(generated_json)
                        st.success(f"Scenario '{graph_name}' created successfully!")

                        # Display the title and summary with a line space using markdown
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
                        with st.spinner("Generating visuals.."):
                            self.graph_visualizer.visualize_graph(graph_id)
                    else:
                        st.error(f"Failed to create scenario '{graph_name}'.")
                except json.JSONDecodeError:
                    st.error("Invalid JSON format. Please check your input.")

        # Step 4: If you prefer to generate a custom scenario, enter your instructions and click "Create"
        instruction = st.text_input("Want to build a custom scenario? Enter your instructions below:")
        if st.button("Create"):
            if not instruction:
                st.warning("Please enter custom instructions to proceed.")
                return

            generated_json = self.generate_graph_generation_json(instruction)

            if generated_json:
                try:
                    graph_data = json.loads(generated_json)
                    with st.spinner("Creating scenario.."):
                        graph_id, graph_name, success = self.context_graph_generator.create_graph_from_json(graph_data)
                    if success:
                        summary = self.summarize_graph(generated_json)
                        st.success(f"Scenario '{graph_name}' created successfully!")

                        # Display the title and summary with a line space using markdown
                        st.markdown(f"""
                            <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
                                <strong>Custom Graph</strong>
                                <br><br>
                                {summary}
                            </div>
                        """, unsafe_allow_html=True)

                        with st.spinner("Generating visuals.."):
                            self.graph_visualizer.visualize_graph(graph_id)
                    else:
                        st.error(f"Failed to create scenario '{graph_name}'.")
                except json.JSONDecodeError:
                    st.error("Invalid JSON format. Please check your input.")

        return graph_id

    def generate_graph_generation_json(self, instruction):
        """
        Use Vertex AI to generate a valid JSON for graph creation based on the given instruction,
        utilizing the entity types, relationship types, and allowed relationships. Ensure the graph has at most 50 nodes.
        The generated JSON should include entities with realistic attribute values based on the predefined attributes.
        The relationships should correctly reference the 'name' attributes of the entities.
        """
        # Dynamically build the entity types and relationship types from the enums
        entity_types = [et.value for et in EntityType]
        relationship_types = [rt.value for rt in RelationshipType]

        # Convert allowed relationships into a string format
        allowed_relationships_str = ""
        for relationship_type, pairs in ALLOWED_RELATIONSHIPS.items():
            allowed_relationships_str += f"\n- {relationship_type.value}:\n"
            for source, target in pairs:
                allowed_relationships_str += f"    ({source.value} -> {target.value})\n"

        # Predefined attributes for each entity type as provided earlier
        predefined_attributes_str = json.dumps(ENTITY_TYPE_ATTRIBUTES, indent=4)

        prompt = f"""
        The user has provided the following instruction: "{instruction}"

        Based on this instruction, generate a valid JSON for a graph creation. 
        If the instruction specifies a **particular number of nodes or entities**, ensure that the graph **adheres** to that **specification**. 
        Otherwise, generate a graph with **at most 50 nodes**. The format should be:

        {{
            "graph_name": "<Name of the graph>",
            "description": "<Description of the graph>",
            "entities": [
                {{ 
                    "type": "EntityType", 
                    "name": "EntityName", 
                    "attributes": {{
                        "attribute_name1": "realistic_value1",
                        "attribute_name2": "realistic_value2",
                        ...
                    }} 
                }},
                ...
            ],
            "relationships": [
                {{ 
                    "source": "EntityName1",  // Must match the value in the name attribute of an entity in the 'entities' list
                    "target": "EntityName2",  // Must match the value in the name attribute of another entity in the 'entities' list
                    "relationship": "RelationshipType" 
                }},
                ...
            ]
        }}

        Here are the possible entity types:
        {', '.join(entity_types)}

        Here are the possible relationship types:
        {', '.join(relationship_types)}

        These are the allowed relationships:
        {allowed_relationships_str}

        Ensure that each entity includes realistic attribute values according to its type. Here are the predefined attributes for each entity type:

        {predefined_attributes_str}

        For example, for a 'Vendor' entity:
        - 'name' should be a realistic company name (e.g., 'Acme Corp').
        - 'country' should be a valid country (e.g., 'USA', 'Germany', 'India').
        - 'status' should reflect a realistic status like 'Active' or 'Inactive'.

        When defining relationships, ensure that the 'source' and 'target' fields match the 'name' attribute of the entities in the 'entities' list. For example, if you have an entity named 'Acme Corp' and another entity named 'ServerXYZ', a valid relationship could look like:

        {{
            "source": "Acme Corp",
            "target": "ServerXYZ",
            "relationship": "DATA_TRANSFER"
        }}

        Generate realistic values for entity attributes and ensure that relationships properly link the entities by their names. Return only the JSON object.
        """

        try:
            # Call the AI model to generate the JSON based on instruction
            with st.spinner("Generating the scenario..."):
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
        Generates a concise, business-oriented summary of the graph using the LLM, incorporating context grammar and summarizing entities and relationships.

        :param generated_json: Dictionary containing the graph details (entities, relationships).
        :return: A formatted summary of the graph generated by the LLM.
        """

        # Parse the graph data
        graph_data = json.loads(generated_json)
        entity_count = len(graph_data.get("entities", []))
        relationship_count = len(graph_data.get("relationships", []))

        # Fetch the context grammar rules from the database
        context_grammar_rules = self.graph_repo.get_enabled_rules()

        # Format the context grammar rules into a string for the prompt
        context_grammar = "\n".join(
            [f"- **{rule['rule_name']}**: {rule['description']}" for rule in context_grammar_rules]
        )

        # Prepare the high-level business-oriented prompt with context grammar
        prompt = f"""
                Provide a detailed explanation of the graph based on the following context grammar rules:

                {context_grammar}

                The graph contains {entity_count} entities and {relationship_count} relationships. Explain the purpose of the graph and the insights it offers, focusing on the relationships between the entities in business terms. Summarize the overall structure and meaning of the relationships while incorporating the context rules, without describing individual entities by name. Avoid providing any recommendations or action steps.
                """

        try:
            # Call the LLM to generate the summary based on the prompt
            with st.spinner("Generating the scenario summary..."):
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


