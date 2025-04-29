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
        
        # Example of enhanced row filtering JSON structure with supported identifier columns
        row_filtering_example = '''
        {
          "tables": {
            "Customer.profiles": {
              "columns": { "..." },
              "row_filtering": {
                "identifier_columns": {
                  "user_id": "user_id",
                  "email": "email_address"
                },
                "purposes": ["Marketing Campaigns", "Customer Support"]
              }
            }
          }
        }
        '''
        
        # Create a prompt for the VertexAI model to generate security policies
        prompt = f"""
        Generate Snowflake security policy DDL statements based on the following JSON policy specification, which is organized by table/column:
        
        {json_str}
        
        Note that the JSON is structured with tables at the top level, where each table contains columns. Each column contains roles, and each role contains purposes with their associated policies. Each table may also contain row_filtering information that specifies which purposes require row-level access control based on user consents.
        
        Here's an example of the enhanced row_filtering structure in the JSON:
        
        {row_filtering_example}
        
        The row_filtering object now specifies:
        1. identifier_columns: A mapping of consent profile identifiers to table columns that can be used for joining with the consent_view
           - user_id: Maps to the user_id column in the consent_profile table
           - email: Maps to the email column in the consent_profile table
        2. purposes: A list of purposes that require consent checks for this table
        
        Create a Snowflake DDL script that implements these security policies following this exact structure and format:
        
        1. START with a header section that explains the purpose of the script:
        ```
        -- =====================================================================
        -- SNOWFLAKE SECURITY POLICY IMPLEMENTATION
        -- =====================================================================
        -- This DDL script implements security policies based on the provided JSON
        -- specification, using role inheritance, column-level masking policies,
        -- and row-level security based on user consents.
        -- =====================================================================
        ```
        
        2. ROLE CREATION section:
        ```
        -- ---------------------------------------------------------------------
        -- Create roles for each purpose
        
        -- Create purpose-based roles
        CREATE ROLE IF NOT EXISTS PURPOSE_[PURPOSE_NAME];
        ```
        
        IMPORTANT: Due to Snowflake's limitation where columns with masking policies cannot have row access policies, implement a two-step approach:
        1. First apply row access policies to the base tables
        2. Then create secure views with column masking policies on top of the row-filtered tables
        
        3. GRANT PURPOSE ROLES TO IMPORTED ROLES section:
        ```
        -- ---------------------------------------------------------------------
        -- 2. GRANT PURPOSE ROLES TO IMPORTED ROLES
        -- ---------------------------------------------------------------------
        -- Grant purpose-based roles to imported Snowflake roles
        GRANT ROLE PURPOSE_MARKETING_CAMPAIGNS TO ROLE "Marketing Analyst";
        ```
        Establish the role hierarchy by granting purpose-based roles to imported Snowflake roles as appropriate based on the JSON.
        
        4. TWO-STEP SECURITY APPROACH section:
        ```
        -- ---------------------------------------------------------------------
        -- 5. IMPLEMENT TWO-STEP SECURITY APPROACH
        -- ---------------------------------------------------------------------
        -- Step 1: Apply row access policies to base tables
        
        -- Create a secure view of consent records
        
        -- Customer.profiles table
        ALTER TABLE Customer.profiles MODIFY COLUMN email SET MASKING POLICY mask_email;
        ```
        Group the ALTER TABLE statements by table, with a comment indicating the table name before each group.
        Use the data element name to match columns to their appropriate masking policies.
        
        6. CREATE ROW ACCESS POLICIES section:
        ```
        -- ---------------------------------------------------------------------
        -- 6. CREATE ROW ACCESS POLICIES
        -- ---------------------------------------------------------------------
        -- Create row access policies based on user consents
        
        -- Create a secure view of consent records with user_id and email lookups
        CREATE OR REPLACE SECURE VIEW consent_view AS
        SELECT 
            cp.user_id, 
            cp.email,
            p.name as purpose_name, 
            cr.status
        FROM consent_record cr
        JOIN consent_profile cp ON cr.consent_profile_id = cp.id
        JOIN purpose p ON cr.purpose_id = p.id
        WHERE cr.status = 'granted'
          AND (cr.expiry_date IS NULL OR cr.expiry_date > CURRENT_TIMESTAMP());
        
        -- Create row access policy for [TABLE_NAME]
        CREATE OR REPLACE ROW ACCESS POLICY consent_rap_[TABLE_NAME] AS (
            [EMAIL_COLUMN] VARCHAR, 
            [USER_ID_COLUMN] VARCHAR
        ) RETURNS BOOLEAN ->
          CASE
            -- For each purpose in the row_filtering list for this table
            WHEN IS_ROLE_IN_SESSION('PURPOSE_[PURPOSE_NAME]') THEN
              EXISTS (
                SELECT 1 FROM consent_view
                WHERE (
                  -- Match on any available identifier, prioritizing more specific matches
                  ([EMAIL_COLUMN] IS NOT NULL AND email = [EMAIL_COLUMN])
                  OR 
                  ([USER_ID_COLUMN] IS NOT NULL AND user_id = [USER_ID_COLUMN])
                )
                AND purpose_name = '[PURPOSE_NAME]'
              )
            
            -- Add additional WHEN clauses for each purpose in the row_filtering
        
            -- Default deny
            ELSE FALSE
          END;
        
        -- Apply row access policy to the table
        -- Apply row access policy to the table with all potential identifier columns
        ALTER TABLE [TABLE_NAME] ADD ROW ACCESS POLICY consent_rap_[TABLE_NAME] ON (
            [EMAIL_COLUMN], [USER_ID_COLUMN]
        );
        ```
        
        The row_filtering in the JSON should specify:
        1. identifier_columns: A mapping of consent profile identifiers to table columns
           - This allows for flexible matching between tables and the consent_view
           - Can include user_id, email, customer_id, or any other identifiers that can be linked to consent records
        2. The list of purposes that require consent checks
        
        Generate a separate row access policy for each table that has row_filtering specified, with appropriate WHEN clauses for each purpose. The policy should attempt to match on any available identifier column, prioritizing the most reliable matches (typically email or user_id).
        
        7. ENCRYPTION POLICY NOTES section:
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
        
        7. CRITICAL IMPLEMENTATION ORDER - YOU MUST FOLLOW THIS EXACT SEQUENCE:
           
           STEP 1: Create Roles and Grants
           - Create purpose-based roles
           - Grant purpose roles to imported roles
           
           STEP 2: Row-Level Security on Base Tables
           - Create a secure view called 'consent_view' that exposes only valid consents
           - Create row access policies (RAPs) for tables with row_filtering
           - Apply these RAPs to the base tables using ALTER TABLE statements
           - This MUST be done BEFORE any column masking
           
           STEP 3: Column-Level Security via Secure Views ONLY
           - Create secure views on top of the row-filtered base tables
           - NEVER apply masking policies directly to base tables
           - NEVER use ALTER TABLE ... MODIFY COLUMN ... SET MASKING POLICY
           - Instead, implement masking directly in the view's SELECT using CASE expressions:
             ```
             CREATE OR REPLACE SECURE VIEW schema.table_secure_view AS
             SELECT 
               CASE
                 WHEN IS_ROLE_IN_SESSION('PURPOSE_X') THEN original_column
                 WHEN IS_ROLE_IN_SESSION('[SPECIFIC_ROLE]') THEN original_column
                 ELSE 'masked_value'
               END AS column_name,
               ...
             FROM schema.original_table;
             ```
           - Grant access to these secure views instead of the base tables
               
           ABSOLUTELY FORBIDDEN:
           - DO NOT create any masking policies with CREATE MASKING POLICY
           - DO NOT apply masking policies to base tables with ALTER TABLE ... SET MASKING POLICY
           - DO NOT mix the order - row filtering MUST come before column masking
           - DO NOT use built-in administrative roles like ACCOUNTADMIN or SECURITYADMIN in any part of the script
        
        CRITICAL SNOWFLAKE SYNTAX REQUIREMENTS:
        1. Do not include CREATE TABLE statements or other DDL not related to security policies and roles
        2. Ensure all object names are properly quoted when they contain special characters or case sensitivity is required
        3. For row access policies, ensure parameter names don't conflict with column names in the table
        4. Use semicolons to terminate each SQL statement
        5. Include appropriate error handling with CREATE OR REPLACE for all objects
        6. Ensure proper dependencies - objects must be created before they are referenced
        7. For secure views, ensure all columns from the base table are properly handled
        8. When applying row access policies, ensure the columns specified exist in the table
        9. For CASE expressions, ensure the data types in all branches are compatible
        10. Avoid using reserved keywords as identifiers, or properly quote them if necessary
        11. DO NOT use built-in administrative roles like ACCOUNTADMIN or SECURITYADMIN in any part of the script
        
        Format the DDL with proper indentation and SQL best practices. Test each statement for syntax correctness.
        
        You have flexibility to determine the best approach for implementing the security policies based on Snowflake best practices. The structure above is a guide, but you may adapt the implementation details as needed to create an optimal, maintainable solution.
        
        The final DDL script MUST be complete, executable, and ready to be run in a Snowflake environment without any modifications or errors.
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
