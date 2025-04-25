import os
import json
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

class DDLGenerator:
    """
    A class for generating Snowflake security policy DDL from JSON policy specifications using VertexAI.
    """
    
    def __init__(self):
        """
        Initialize the DDL Generator with VertexAI configuration.
        """
        # Initialize Vertex AI with the provided project ID
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]
        vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
        self.model = GenerativeModel(os.environ["MODEL"])
    
    def generate_snowflake_ddl(self, policy_json):
        """
        Generate Snowflake security policy DDL based on the provided policy JSON specification.
        
        Args:
            policy_json: Dictionary containing the policy specification with tables, columns, and data types
            
        Returns:
            String containing the Snowflake DDL statements for implementing security policies
        """
        # Convert the policy JSON to a string if it's a dictionary
        if isinstance(policy_json, dict):
            json_str = json.dumps(policy_json, indent=2)
        else:
            json_str = policy_json
        
        # Create a prompt for the VertexAI model to generate security policies
        prompt = f"""
        Generate Snowflake security policy DDL statements based on the following JSON policy specification:
        
        {json_str}
        
        Focus on creating the following types of statements:
        
        1. CREATE ROLE statements for each purpose found in the JSON (e.g., PURPOSE_DEFAULT_ROLE_ASSIGNMENT, PURPOSE_CUSTOMER_SUPPORT, etc.)
           - The role name should be prefixed with 'PURPOSE_' followed by the purpose name in uppercase with spaces replaced by underscores
           - For example, for the purpose 'Customer Support', create a role named 'PURPOSE_CUSTOMER_SUPPORT'
        
        2. GRANT purpose-based roles to the original Snowflake roles:
           - For each purpose in the JSON, look for the "role" object within that purpose
           - The "role" object contains "id" and "name" fields that identify the external Snowflake role
           - Create a GRANT statement that grants the purpose-based role to this external role
           - For example, if a purpose 'Customer Support' has a role with name "Data Analyst", include a statement like:
             GRANT ROLE PURPOSE_CUSTOMER_SUPPORT TO ROLE DATA_ANALYST;
           - Make sure to convert the external role name to uppercase with spaces replaced by underscores
        
        3. CREATE OR REPLACE MASKING POLICY statements for each column and purpose combination where masking is required:
           - The masking policy name should be "<Purpose>_<column_name>" with spaces replaced by underscores
           - If masking_required is 0 or not specified, the policy should return the original value
           - If masking_required is 1, implement the masking based on the masking_format:
             * For emails: implement appropriate email masking based on formats like "xxxx@####.com", "user****@domain.com", etc.
             * For numbers: implement appropriate number masking based on formats like "######"
             * For addresses: implement appropriate address masking based on formats like "#### ***** St, City, ST #####"
             * For phone numbers: implement appropriate phone masking based on formats like "###-###-####"
           - The masking policy should be applied only to users with the specific purpose-based role
           - For other roles, the policy should return the original value
        
        4. Apply the masking policies to the appropriate tables and columns:
           - For each masking policy created, include an ALTER TABLE statement to apply the policy
           - The format should be: ALTER TABLE <schema>.<table> MODIFY COLUMN <column> SET MASKING POLICY <policy_name>;
        
        5. Group the statements logically and add comments to make the DDL easy to understand:
           - First, create all purpose-based roles
           - Then, grant these roles to the external Snowflake roles
           - Next, create all masking policies grouped by table and column
           - Finally, apply the masking policies to the appropriate tables and columns
        
        Do not include CREATE TABLE statements or other DDL not related to security policies and roles.
        Format the DDL with proper indentation and SQL best practices.
        """
        
        try:
            # Call the AI model to generate the DDL
            with st.spinner("Generating Snowflake Security Policy DDL..."):
                response = self.model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                # Extract the SQL content from the response
                ddl_text = response.text.strip()
                
                # Clean up the response if it contains markdown code blocks
                if ddl_text.startswith("```sql"):
                    ddl_text = ddl_text.replace("```sql", "", 1)
                if ddl_text.endswith("```"):
                    ddl_text = ddl_text.replace("```", "", 1)
                
                return ddl_text.strip()
            else:
                st.error("Failed to generate security policy DDL. No valid response from the AI model.")
                return None
        except Exception as e:
            st.error(f"An error occurred while generating security policy DDL: {str(e)}")
            return None
