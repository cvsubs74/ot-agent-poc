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
        
        3. CREATE DATA ACCESS ROLES section:
        ```
        -- ---------------------------------------------------------------------
        -- 2. CREATE DATA ACCESS ROLES
        -- ---------------------------------------------------------------------
        -- These roles will be used to control access to specific data elements
        CREATE ROLE IF NOT EXISTS DATA_PII_FULL_ACCESS;      -- Full access to PII
        CREATE ROLE IF NOT EXISTS DATA_PII_PARTIAL_ACCESS;   -- Partial/masked access to PII
        CREATE ROLE IF NOT EXISTS DATA_FINANCIAL_ACCESS;     -- Access to financial data
        CREATE ROLE IF NOT EXISTS DATA_CUSTOMER_ACCESS;      -- Access to customer data
        ```
        Create data access roles based on the types of data in the JSON. Create only roles that will be used in the role hierarchy and masking policies.
        
        4. GRANT HIERARCHY FOR PURPOSE-BASED ROLES section:
        ```
        -- ---------------------------------------------------------------------
        -- 3. GRANT HIERARCHY FOR PURPOSE-BASED ROLES
        -- ---------------------------------------------------------------------
        -- Grant appropriate data access roles to purpose-based roles
        GRANT ROLE DATA_[DATA_TYPE]_[ACCESS_LEVEL] TO ROLE PURPOSE_[PURPOSE_NAME];
        ```
        Establish the role hierarchy by granting data access roles to purpose-based roles as appropriate based on the JSON.
        
        5. GRANT PURPOSE ROLES TO IMPORTED ROLES section:
        ```
        -- ---------------------------------------------------------------------
        -- 4. GRANT PURPOSE ROLES TO IMPORTED ROLES
        -- ---------------------------------------------------------------------
        -- Grant purpose roles to each role from the JSON
        GRANT ROLE PURPOSE_[PURPOSE_NAME] TO ROLE "[ROLE_NAME]";
        ```
        For each role in the JSON, grant the appropriate purpose-based roles based on the purposes associated with that role.
        Include a comment with the role name before each set of grants for that role.
        
        5. DEFINE MASKING POLICIES section:
        ```
        -- ---------------------------------------------------------------------
        -- 5. DEFINE MASKING POLICIES
        -- ---------------------------------------------------------------------
        
        -- 5.1 Email Masking Policy
        CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING)
          RETURNS STRING ->
            CASE
              -- Customer Data Analyst with Customer Support purpose gets partial visibility
              WHEN IS_ROLE_IN_SESSION('Customer Data Analyst') 
                   AND IS_ROLE_IN_SESSION('PURPOSE_CUSTOMER_SUPPORT') THEN 
                REGEXP_REPLACE(val, '(^[^@]{1,4})(.*)(@.*$)', '\\1****\\3')
              
              -- Default masking for all other roles with PURPOSE_DEFAULT_ROLE_ASSIGNMENT
              WHEN IS_ROLE_IN_SESSION('PURPOSE_DEFAULT_ROLE_ASSIGNMENT') THEN 
                REGEXP_REPLACE(val, '(^[^@]*)(@)(.*$)', 'xxxx@####.com')
              
              -- No access for others
              ELSE NULL
            END;
        ```
        Create masking policies based on data element names from the JSON, not data types. Name policies as mask_[data_element_name] in lowercase with underscores (e.g., mask_email, mask_address, mask_customer_id).
        
        IMPORTANT: Use purpose-based roles (like PURPOSE_DEFAULT_ROLE_ASSIGNMENT) in the masking policy conditions rather than listing all individual roles. This leverages the role hierarchy and makes policies more maintainable.
        
        7. APPLY MASKING POLICIES TO COLUMNS section:
        ```
        -- ---------------------------------------------------------------------
        -- 6. APPLY MASKING POLICIES TO COLUMNS
        -- ---------------------------------------------------------------------
        
        -- 6.1 Customer.profiles table
        ALTER TABLE Customer.profiles MODIFY COLUMN email SET MASKING POLICY mask_email;
        ALTER TABLE Customer.profiles MODIFY COLUMN address SET MASKING POLICY mask_address;
        ALTER TABLE Customer.profiles MODIFY COLUMN customer_id SET MASKING POLICY mask_customer_id;
        ```
        Apply the appropriate masking policy to each column that requires masking according to the JSON.
        Group the ALTER TABLE statements by table, with a comment indicating the table name before each group.
        Use the data element name to match columns to their appropriate masking policies.
        
        8. END with an ENCRYPTION POLICY NOTES section:
        ```
        -- ---------------------------------------------------------------------
        -- 7. ENCRYPTION POLICY NOTES
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
        
        4. Only create data access roles that will actually be used in the role hierarchy
           - These roles should grant specific access levels to the purpose-based roles
           - For example, DATA_FINANCIAL_ACCESS might be granted to Financial Analysts for special access
        
        5. For email masking:
           - For roles with Customer Support purpose: use a format that shows first few characters (e.g., 'user****@domain.com')
           - For default masking: use 'xxxx@####.com' format
        
        6. For address masking: use '#### ***** St, City, ST #####' format
        
        7. For customer_id masking: use '######' format
        
        8. For date_of_birth masking: return NULL instead of a masked date
        
        9. For phone masking: use '###-###-####' format
        
        10. For credit card masking:
            - Financial Analysts: show last 4 digits only ('****-****-****-1234')
            - Default masking: use '####-####-####-####' format
        
        11. Skip masking for columns where masking_required=0 in the JSON
            
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
