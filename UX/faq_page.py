import streamlit as st
import pandas as pd

class FAQPage:
    """Page for displaying and searching the knowledge base FAQ."""
    
    def __init__(self, knowledge_repository):
        """Initialize the FAQ page with the knowledge repository."""
        self.knowledge_repository = knowledge_repository
    
    def render(self):
        """Render the FAQ page."""
        st.title("Knowledge Base")
        
        st.markdown('''
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>This comprehensive knowledge base contains information about all aspects of the Data Use Governance platform, 
            from core constructs to regulatory metadata, decision trees, inference APIs, and more.</p>
            <p>Use the search and filtering options below to find answers to your questions.</p>
        </div>''', unsafe_allow_html=True)
        
        # Create main tabs for AI Chatbot and Knowledge Base browsing
        chatbot_tab, browse_tab = st.tabs(["AI Chatbot", "Browse Knowledge Base"])
        
        # Tab 1: AI Chatbot
        with chatbot_tab:
            st.markdown("### 🤖 Knowledge Base Chatbot")
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>Ask questions in natural language and get instant answers from our knowledge base.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize chat history in session state if not already present
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                        <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; max-width: 80%;">
                            <p style="margin: 0;"><strong>You:</strong> {message["content"]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # assistant
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                        <div style="background-color: #f1f8e9; padding: 10px; border-radius: 10px; max-width: 80%;">
                            <p style="margin: 0;"><strong>Assistant:</strong> {message["content"]}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Simple form for chat input
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_area(
                    "Ask a question about the platform",
                    height=100,
                    placeholder="Examples:\n- How do decision trees work?\n- What is purpose-based access control?\n- How do I implement data use governance?\n- What are the key components of a policy?",
                    label_visibility="collapsed"
                )
                # Use columns for the buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    submit_button = st.form_submit_button(
                        "Send", 
                        use_container_width=True,
                        type="primary",  # Use primary button type
                        help="Send your question to the chatbot"
                    )
                with col3:
                    if st.form_submit_button(
                        "Clear Chat", 
                        use_container_width=True,
                        type="primary",  # Use primary button type
                        help="Clear the chat history"
                    ):
                        st.session_state.chat_history = []
                        st.rerun()
            
            # Process user input when form is submitted
            if submit_button and user_input:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                try:
                    # Import VertexAI here to avoid loading it unless needed
                    import os
                    import vertexai
                    from vertexai.generative_models import GenerativeModel
                    
                    # Initialize Vertex AI
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]
                    vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
                    model = GenerativeModel(os.environ["MODEL"])
                    
                    # Get all knowledge base items
                    all_items = self.knowledge_repository.get_all_knowledge_items()
                    
                    # Format context for the prompt - simply include all knowledge base items
                    context_text = "Complete Knowledge Base Content:\n\n"
                    
                    # Add all knowledge base items to the context
                    for i, item in enumerate(all_items):
                        context_text += f"Entry {i+1}:\n"
                        context_text += f"Category: {item['category']}\n"
                        context_text += f"Subcategory: {item['subcategory'] or 'General'}\n"
                        context_text += f"Question: {item['question']}\n"
                        context_text += f"Answer: {item['answer']}\n\n"
                    
                    # Generate prompt
                    prompt = f"""
                    You are a helpful assistant for a Data Use Governance platform. Your task is to answer questions about data governance, 
                    privacy, compliance, and related topics based ONLY on the provided knowledge base information.
                    
                    {context_text}
                    
                    User Question: {user_input}
                    
                    IMPORTANT INSTRUCTIONS:
                    1. ONLY answer based on the knowledge base context provided above. Do not make up or hallucinate information.
                    2. If the knowledge base doesn't contain information directly relevant to the question, say "I don't have specific information about that in my knowledge base" rather than making up an answer.
                    3. Do not reference external sources, websites, or documentation that isn't mentioned in the knowledge base context.
                    4. If you're unsure about any details, acknowledge the limitations of your knowledge rather than guessing.
                    5. Focus on the specific implementation details of this application as described in the knowledge base.
                    
                    Your answer should:
                    1. Be direct and to the point
                    2. Use bullet points or numbered lists for complex explanations
                    3. Include examples from the knowledge base where appropriate
                    4. Avoid technical jargon unless necessary
                    5. Not include any references to the "knowledge base entries" or the format of the context
                    6. Be formatted in a way that's easy to read
                    
                    Answer:
                    """
                    
                    # Get response from Vertex AI
                    response = model.generate_content(prompt)
                    
                    if response and hasattr(response, 'text'):
                        answer = response.text.strip()
                        
                        # Clean up the response if it contains markdown code blocks
                        if answer.startswith("```"):
                            answer = answer.replace("```", "", 1)
                        if answer.endswith("```"):
                            answer = answer.replace("```", "", 1)
                        
                        # Add assistant response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    else:
                        st.session_state.chat_history.append({"role": "assistant", "content": "I'm sorry, I couldn't generate a response. Please try asking a different question."})
                
                except Exception as e:
                    st.session_state.chat_history.append({"role": "assistant", "content": f"I'm sorry, an error occurred: {str(e)}. Please try again later."})
                
                # Rerun to update the chat display
                st.rerun()
        
        # Tab 2: Browse Knowledge Base
        with browse_tab:
            # Get all knowledge items
            knowledge_items = self.knowledge_repository.get_all_knowledge_items()
            
            if not knowledge_items:
                st.warning("No knowledge base items found. Please ensure the database is properly seeded.")
                return
            
            # Extract unique categories for filtering
            categories = sorted(list(set([item['category'] for item in knowledge_items])))
            
            # Modern interface with category and question dropdowns
            st.markdown("### Browse Knowledge Base")
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
                <p>Select a category and question to view the answer directly.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Category selection
            selected_category = st.selectbox(
                "Select a category",
                options=["All Categories"] + categories,
                key="category_dropdown"
            )
            
            # Filter items by selected category
            if selected_category == "All Categories":
                filtered_items = knowledge_items
            else:
                filtered_items = [item for item in knowledge_items if item['category'] == selected_category]
            
            # Create a list of questions for the dropdown
            questions = [(item['question'], item) for item in filtered_items]
            
            if questions:
                # Question selection
                selected_question_text = st.selectbox(
                    "Select a question",
                    options=[q[0] for q in questions],
                    key="question_dropdown"
                )
                
                # Find the selected item
                selected_item = next((item[1] for item in questions if item[0] == selected_question_text), None)
                
                if selected_item:
                    # Display the answer in a nice card
                    st.markdown("### Answer")
                    st.markdown(f"""
                    <div style="background-color: #f1f8e9; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #4caf50;">
                        <p>{selected_item['answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Category:** {selected_item['category']}")
                    with col2:
                        if selected_item['subcategory']:
                            st.markdown(f"**Subcategory:** {selected_item['subcategory']}")
                    
                    # Display tags if available
                    if selected_item['tags']:
                        st.markdown("**Tags:**")
                        tags = selected_item['tags'].split(',')
                        tag_html = ' '.join([f'<span style="background-color: #f0f0f0; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{tag.strip()}</span>' for tag in tags])
                        st.markdown(tag_html, unsafe_allow_html=True)
            else:
                st.info("No questions available for the selected category.")
    
    def _render_faq_items(self, faq_items):
        """Render a list of FAQ items grouped by subcategory."""
        if not faq_items:
            st.info("No items found. Try adjusting your search or filters.")
            return
            
        # Group by subcategory
        subcategories = sorted(list(set([item['subcategory'] for item in faq_items if item['subcategory']])))        
        
        # Display items by subcategory
        for subcategory in subcategories:
            st.markdown(f"### {subcategory}")
            subcategory_items = [item for item in faq_items if item['subcategory'] == subcategory]
            
            for item in subcategory_items:
                with st.expander(f"**{item['question']}**"):
                    st.markdown(item['answer'])
                    
                    # Display tags if available
                    if item['tags']:
                        tags = item['tags'].split(',')
                        tag_html = ' '.join([f'<span style="background-color: #f0f0f0; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{tag.strip()}</span>' for tag in tags])
                        st.markdown(f"**Tags:** {tag_html}", unsafe_allow_html=True)
        
        # Display items without subcategory
        general_items = [item for item in faq_items if not item['subcategory']]
        if general_items:
            st.markdown("### General")
            for item in general_items:
                with st.expander(f"**{item['question']}**"):
                    st.markdown(item['answer'])
                    
                    # Display tags if available
                    if item['tags']:
                        tags = item['tags'].split(',')
                        tag_html = ' '.join([f'<span style="background-color: #f0f0f0; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em;">{tag.strip()}</span>' for tag in tags])
                        st.markdown(f"**Tags:** {tag_html}", unsafe_allow_html=True)
