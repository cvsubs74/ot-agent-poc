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
        
        Create a Snowflake DDL script that implements these security policies following this exact structure and format:
        
        1. START with a header section that explains the purpose of the script:
        ```
        -- =====================================================================
        -- SNOWFLAKE SECURITY POLICY IMPLEMENTATION
        -- =====================================================================
        -- This DDL script implements security policies based on the provided JSON
        -- specification, using role inheritance and column-level masking policies.
        -- =====================================================================
        ```
        
        2. CREATE PURPOSE-BASED ROLES section:
        ```
        -- ---------------------------------------------------------------------
        -- 1. CREATE PURPOSE-BASED ROLES
        -- ---------------------------------------------------------------------
        -- Create roles for each business purpose mentioned in the policies
        CREATE ROLE IF NOT EXISTS PURPOSE_[PURPOSE_NAME];
        ```
        Create a purpose-based role for each unique purpose found in the JSON. Use the format PURPOSE_[PURPOSE_NAME] for all purpose roles.
        
        3. GRANT PURPOSE ROLES TO IMPORTED ROLES section:
        ```
        -- ---------------------------------------------------------------------
        -- 2. GRANT PURPOSE ROLES TO IMPORTED ROLES
        -- ---------------------------------------------------------------------
        -- Grant purpose-based roles to imported Snowflake roles
        GRANT ROLE PURPOSE_MARKETING_CAMPAIGNS TO ROLE "Marketing Analyst";
        ```
        Establish the role hierarchy by granting purpose-based roles to imported Snowflake roles as appropriate based on the JSON.
        
        4. DEFINE MASKING POLICIES section:
        ```
        -- ---------------------------------------------------------------------
        -- 3. DEFINE MASKING POLICIES
        -- ---------------------------------------------------------------------
        -- Define masking policies for sensitive data elements
        
        -- Email Masking Policy
        CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING)
          RETURNS STRING ->
            CASE
              -- Roles with masking_required=0 get full access (original value)
              WHEN IS_ROLE_IN_SESSION('[ROLE_WITH_MASKING_NOT_REQUIRED]') THEN val
              
              -- Roles with specific purpose get partial visibility
              WHEN IS_ROLE_IN_SESSION('[ROLE]') 
                   AND IS_ROLE_IN_SESSION('PURPOSE_[PURPOSE]') THEN 
                REGEXP_REPLACE(val, '(^[^@]{1,4})(.*)(@.*$)', 'xxxx@####.com')
              
              -- No access for others
              ELSE NULL
            END;
        ```
        Create masking policies based on data element names from the JSON. Name policies as mask_[data_element_name] in lowercase with underscores (e.g., mask_email, mask_address, mask_customer_id).
        
        5. APPLY MASKING POLICIES TO COLUMNS section:
        ```
        -- ---------------------------------------------------------------------
        -- 4. APPLY MASKING POLICIES TO COLUMNS
        -- ---------------------------------------------------------------------
        
        -- Customer.profiles table
        ALTER TABLE Customer.profiles MODIFY COLUMN email SET MASKING POLICY mask_email;
        ```
        Group the ALTER TABLE statements by table, with a comment indicating the table name before each group.
        Use the data element name to match columns to their appropriate masking policies.
        
        6. ENCRYPTION POLICY NOTES section:
        ```
        -- ---------------------------------------------------------------------
        -- 5. ENCRYPTION POLICY NOTES
        -- ---------------------------------------------------------------------
        -- Note: The JSON specifies AES-256 encryption for many fields.
        -- Snowflake handles encryption at rest automatically, so no explicit
        -- encryption DDL is needed. All data in Snowflake is encrypted using
        -- AES-256 by default.
        ```
        
        IMPORTANT IMPLEMENTATION DETAILS:
        
        1. Use IS_ROLE_IN_SESSION() for all role-based conditions in masking policies
        
        2. Create masking policies based on data element names from the JSON, not data types or column names
           - This approach is more standardized and allows for consistent policy application across tables
           - When the same data element appears in multiple tables, it should use the same masking policy
        
        3. Use purpose-based roles in masking policy conditions rather than listing individual roles
           - For example, use IS_ROLE_IN_SESSION('PURPOSE_DEFAULT_ROLE_ASSIGNMENT') instead of listing all roles
           - This leverages the role hierarchy and makes policies more maintainable
        
        4. DO NOT create any data access roles (like DATA_PII_FULL_ACCESS or DATA_PII_PARTIAL_ACCESS)
           - Instead, use purpose-based roles directly in the role hierarchy
           - The masking policies should check for specific Snowflake roles and purpose roles
        
        5. For masking policies, determine the appropriate masking format based on the data element type and sensitivity:
           - Choose appropriate masking formats for each data type (emails, addresses, IDs, dates, phone numbers, etc.)
           - Consider the purpose and role when determining the level of masking
           - For some roles/purposes, partial visibility may be appropriate
           - For other roles/purposes, complete masking or NULL values may be required
        
        6. Skip masking for columns where masking_required=0 in the JSON
            - Columns with masking_required=0 should have FULL ACCESS for the specified roles, not NO ACCESS
            - Do not apply any masking policies to these columns
            - In masking policies for other columns, ensure roles with masking_required=0 get the original value (val) not NULL
            
            Do not include CREATE TABLE statements or other DDL not related to security policies and roles.
            Format the DDL with proper indentation and SQL best practices.
            
            Follow the structure and formatting shown above exactly. The section headers, comments, and overall organization should match the template precisely. The specific roles, purposes, and masking policies should be derived from the JSON input, but the format and approach should be consistent with the example.
            
            The final DDL script should be complete, executable, and ready to be run in a Snowflake environment without any modifications.
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
