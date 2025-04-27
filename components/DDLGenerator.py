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
            # Check if this is the new column-based structure
            if 'tables' in policy_json:
                # We have the new column-based structure
                json_str = json.dumps(policy_json, indent=2)
            else:
                # Handle legacy format - convert to new format for backward compatibility
                st.warning("Using legacy JSON format. Consider updating to the new column-based format.")
                json_str = json.dumps(policy_json, indent=2)
        else:
            json_str = policy_json
        
        # Create a prompt for the VertexAI model to generate security policies
        prompt = f"""
        Generate Snowflake security policy DDL statements based on the following JSON policy specification, which is organized by table/column:
        
        {json_str}
        
        Note that the JSON is structured with tables at the top level, where each table contains columns. Each column contains roles, and each role contains purposes with their associated policies.
        
        Focus on creating the following types of statements in this exact order:
        
        1. CREATE ROLE statements for each purpose found in the JSON (e.g., PURPOSE_CUSTOMER_SUPPORT, PURPOSE_FRAUD_DETECTION, etc.)
           - The role name should be prefixed with 'PURPOSE_' followed by the purpose name in uppercase with spaces replaced by underscores
           - For example, for the purpose 'Customer Support', create a role named 'PURPOSE_CUSTOMER_SUPPORT'
           - Add a comment: "-- 1) Create Purpose Roles" before this section
        
        2. GRANT purpose-based roles to the original Snowflake roles:
           - The JSON is now organized by table/column at the top level
           - Each column contains roles, and each role contains purposes with their associated policies
           - Create a GRANT statement that grants each purpose-based role to the appropriate external role
           - For example, if a column has a role 'Customer Data Analyst' with a purpose 'Customer Support', include a statement like:
             GRANT ROLE PURPOSE_CUSTOMER_SUPPORT TO ROLE "Customer Data Analyst";
           - Add a comment: "-- 2) Grant Purpose Roles to Imported Roles" before this section
           - Add a comment before each grant to explain the mapping, like: "--    (Customer Data Analyst → Customer Support)"
        
        3. CREATE OR REPLACE MASKING POLICY statements based on data types and masking formats:
           - Instead of creating a policy for each column and purpose, create consolidated masking policies by data type
           - For example, create a single "mask_email" policy for all email columns and a "mask_customer_id" policy for all customer ID columns
           - In each policy, use CASE statements with IS_ROLE_IN_SESSION checks to apply different masking based on the role
           - Add a comment: "-- 3) Define Masking Policies" before this section
           - Add numbered comments for each policy like "-- 3.1 Email Masking Policy"
        
        4. Apply the masking policies to the appropriate tables and columns:
           - For each table and column combination, include an ALTER TABLE statement to apply the policy
           - The format should be: ALTER TABLE <schema>.<table> MODIFY COLUMN <column> SET MASKING POLICY <policy_name>;
           - Group these by table with a comment before each table's section
           - Add a comment: "-- 4) Attach Masking Policies to Columns" before this section
        
        Follow this exact format for the output:
        -- 1) Create Purpose Roles
        CREATE ROLE IF NOT EXISTS PURPOSE_CUSTOMER_SUPPORT;
        CREATE ROLE IF NOT EXISTS PURPOSE_FRAUD_DETECTION;
        CREATE ROLE IF NOT EXISTS PURPOSE_MARKETING_CAMPAIGNS;
        
        -- 2) Grant Purpose Roles to Imported Roles
        --    (Customer Data Analyst → Customer Support)
        GRANT ROLE PURPOSE_CUSTOMER_SUPPORT    TO ROLE "Customer Data Analyst";
        --    (Financial Analyst → Fraud Detection)
        GRANT ROLE PURPOSE_FRAUD_DETECTION     TO ROLE "Financial Analyst";
        --    (Marketing Analyst → Marketing Campaigns)
        GRANT ROLE PURPOSE_MARKETING_CAMPAIGNS TO ROLE "Marketing Analyst";
        
        -- 3) Define Masking Policies
        -- 3.1 Email Masking Policy
        CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING)
          RETURNS STRING ->
            CASE
              WHEN IS_ROLE_IN_SESSION('Financial Analyst')      THEN val
              WHEN IS_ROLE_IN_SESSION('Customer Data Analyst')  THEN CONCAT(LEFT(val,4),'****@domain.com')
              WHEN IS_ROLE_IN_SESSION('Marketing Analyst')      THEN CONCAT('xxxx@', SPLIT_PART(val,'@',2))
              ELSE NULL
            END;
        
        -- 4) Attach Masking Policies to Columns
        -- Customer.profiles
        ALTER TABLE Customer.profiles         
          MODIFY COLUMN email       SET MASKING POLICY mask_email;
        
        Do not include CREATE TABLE statements or other DDL not related to security policies and roles.
        Format the DDL with proper indentation and SQL best practices.
        """
        
        try:
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
