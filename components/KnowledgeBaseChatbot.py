import os
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

class KnowledgeBaseChatbot:
    """
    A class for implementing a knowledge base chatbot using Vertex AI.
    This chatbot answers questions based on the knowledge base content.
    """
    
    def __init__(self, knowledge_repository):
        """
        Initialize the Knowledge Base Chatbot with Vertex AI configuration.
        
        Args:
            knowledge_repository: Repository object for accessing knowledge base items
        """
        # Store the knowledge repository for accessing knowledge base content
        self.knowledge_repository = knowledge_repository
        
        # Initialize Vertex AI with the provided project ID
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]
        vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
        self.model = GenerativeModel(os.environ["MODEL"])
        
        # Initialize chat history if not already in session state
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
    
    def get_knowledge_context(self, query):
        """
        Retrieve relevant knowledge base items for the given query.
        
        Args:
            query: User's question or query string
            
        Returns:
            String containing relevant knowledge base items formatted for the prompt
        """
        # Use the repository's search function to find relevant items
        relevant_items = self.knowledge_repository.search_knowledge_base(query)
        
        # Format the relevant items for inclusion in the prompt
        context_text = ""
        if relevant_items:
            context_text = "Here are some relevant knowledge base entries:\n\n"
            for i, item in enumerate(relevant_items[:5]):  # Limit to top 5 most relevant items
                context_text += f"Entry {i+1}:\n"
                context_text += f"Category: {item['category']}\n"
                context_text += f"Subcategory: {item['subcategory']}\n"
                context_text += f"Question: {item['question']}\n"
                context_text += f"Answer: {item['answer']}\n\n"
        
        return context_text
    
    def generate_prompt(self, query, context_text):
        """
        Generate the prompt for the Vertex AI model to answer the user's question.
        
        Args:
            query: User's question or query string
            context_text: Relevant knowledge base context
            
        Returns:
            String containing the complete prompt for the model
        """
        return f"""
        You are a helpful assistant for a Data Use Governance platform. Your task is to answer questions about data governance, 
        privacy, compliance, and related topics based on the provided knowledge base information.
        
        {context_text}
        
        User Question: {query}
        
        Please provide a clear, concise, and accurate answer based on the knowledge base information provided above. 
        If the knowledge base doesn't contain information directly relevant to the question, provide a general answer 
        based on your understanding of data governance and privacy best practices, but clearly indicate that this is 
        general information rather than specific to the platform.
        
        Your answer should:
        1. Be direct and to the point
        2. Use bullet points or numbered lists for complex explanations
        3. Include examples where appropriate
        4. Avoid technical jargon unless necessary
        5. Not include any references to the "knowledge base entries" or the format of the context
        6. Be formatted in a way that's easy to read
        
        Answer:
        """
    
    def process_query(self, query):
        """
        Process a user query and get an answer from the Vertex AI model.
        
        Args:
            query: User's question or query string
            
        Returns:
            String containing the model's answer
        """
        try:
            # Get relevant knowledge base context
            context_text = self.get_knowledge_context(query)
            
            # Generate the prompt with the context and query
            prompt = self.generate_prompt(query, context_text)
            
            # Get response from Vertex AI
            response = self.model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                answer = response.text.strip()
                
                # Clean up the response if it contains markdown code blocks
                if answer.startswith("```"):
                    answer = answer.replace("```", "", 1)
                if answer.endswith("```"):
                    answer = answer.replace("```", "", 1)
                
                return answer
            else:
                return "I'm sorry, I couldn't generate a response. Please try asking a different question."
                
        except Exception as e:
            return f"I'm sorry, an error occurred: {str(e)}. Please try again later."
    
    def render_chat_interface(self):
        """
        Render the chat interface in the Streamlit app.
        """
        st.markdown("### 🤖 Knowledge Base Chatbot")
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #3498db;">
            <p>Ask questions in natural language and get instant answers from our knowledge base.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.chat_messages:
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
        
        # Chat form
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Ask a question about the platform",
                height=50,
                placeholder="e.g., How do decision trees work?",
                label_visibility="collapsed"
            )
            submit_button = st.form_submit_button("Send", use_container_width=True)
            
            if submit_button and user_input:
                # Add user message to chat
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                
                # Get AI response
                answer = self.process_query(user_input)
                
                # Add AI response to chat
                st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                
                # Rerun to update the chat display
                st.experimental_rerun()
    
    def clear_chat_history(self):
        """
        Clear the chat history.
        """
        st.session_state.chat_messages = []
