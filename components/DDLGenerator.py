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
        Generate a complete, ready-to-execute Snowflake security policy DDL script based on the following JSON policy specification, which is organized by table/column:
        
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
        -- 1. CREATE ROLES AND GRANTS
        -- ---------------------------------------------------------------------
        -- Create roles for each purpose
        
        -- Create purpose-based roles
        CREATE ROLE IF NOT EXISTS PURPOSE_MARKETING_CAMPAIGNS;
        ```
        
        3. GRANT PURPOSE ROLES TO IMPORTED ROLES section:
        ```
        -- ---------------------------------------------------------------------
        -- 2. GRANT PURPOSE ROLES TO IMPORTED ROLES
        -- ---------------------------------------------------------------------
        -- Grant purpose-based roles to imported Snowflake roles
        GRANT ROLE PURPOSE_MARKETING_CAMPAIGNS TO ROLE "Marketing Analyst";
        ```
        
        4. TWO-STEP SECURITY APPROACH section:
        ```
        -- ---------------------------------------------------------------------
        -- 5. IMPLEMENT TWO-STEP SECURITY APPROACH
        -- ---------------------------------------------------------------------
        -- Step 1: Apply row access policies to base tables
        
        -- Customer.profiles table
        ```
        
        5. CREATE ROW ACCESS POLICIES section:
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
        ```
        
        6. CREATE SECURE VIEWS section:
        ```
        -- ---------------------------------------------------------------------
        -- STEP 3: Column-Level Security via Secure Views ONLY
        -- ---------------------------------------------------------------------
        -- Create secure views on top of the row-filtered base tables
        -- NEVER apply masking policies directly to base tables
        -- NEVER use ALTER TABLE ... MODIFY COLUMN ... SET MASKING POLICY
        -- Include ALL columns from the original table in the secure view
        -- Only apply masking to columns that have policies defined
        -- Non-classified columns should be returned as-is without any masking
        -- Implement masking directly in the view's SELECT using CASE expressions:
        ```
        CREATE OR REPLACE SECURE VIEW schema.table_secure_view AS
        SELECT 
          -- Masked column with policy
          CASE
            WHEN IS_ROLE_IN_SESSION('PURPOSE_X') THEN sensitive_column
            WHEN IS_ROLE_IN_SESSION('[SPECIFIC_ROLE]') THEN sensitive_column
            ELSE 'masked_value'
          END AS sensitive_column,
          
          -- Non-classified column passed through as-is
          regular_column,
          
          -- Other columns...
          *
        FROM schema.original_table;
        
        -- REVOKE access to the original table from the specific role only
        REVOKE ALL PRIVILEGES ON schema.original_table FROM ROLE "Marketing Analyst";
        
        -- GRANT access to the secure view to appropriate roles
        GRANT SELECT ON schema.table_secure_view TO ROLE "Marketing Analyst";
        
        -- Example row access policy format (will be generated with actual values from JSON)
        CREATE OR REPLACE ROW ACCESS POLICY consent_rap_table AS (
            identifier_column VARCHAR
        ) RETURNS BOOLEAN ->
          EXISTS (
            SELECT 1 FROM consent_view
            WHERE (
              -- Match on available identifier
              (identifier_column IS NOT NULL AND identifier_field = identifier_column)
            )
            AND purpose_name IN ('Purpose A', 'Purpose B')
            AND (
              -- Only allow roles with the appropriate purpose to access the data
              CASE
                WHEN purpose_name = 'Purpose A' THEN IS_ROLE_IN_SESSION('PURPOSE_A')
                WHEN purpose_name = 'Purpose B' THEN IS_ROLE_IN_SESSION('PURPOSE_B')
                ELSE FALSE
              END
            )
          );
        
        -- DO NOT use ACCOUNTADMIN or SECURITYADMIN in row access policies
        -- Row access should be based ONLY on the purposes and roles from the JSON
        
        The script should be complete and ready to execute in Snowflake without any modifications. Do not include placeholders like [TABLE_NAME] or [PURPOSE_NAME] - replace these with actual values from the JSON. Do not include comments instructing users to modify the script.
        
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
        
        For each table with row_filtering in the JSON, create a complete row access policy with all necessary WHEN clauses for each purpose. The policy should match on any available identifier column, prioritizing the most reliable matches (typically email or user_id).
        
        IMPLEMENTATION GUIDELINES:
        
        1. Use IS_ROLE_IN_SESSION() for all role-based conditions in masking policies
        
        2. For secure views, implement column masking directly in the SELECT using CASE expressions that check for specific roles and purposes
        
        3. Create purpose-based roles and grant them to the appropriate imported roles from the JSON
        
        4. For row access policies, create a policy for each table with row_filtering in the JSON, ensuring that policies include role checks using IS_ROLE_IN_SESSION() to verify that users have the appropriate role for the purpose
        
        5. For masking in secure views, use appropriate masking formats based on data type (emails, addresses, IDs, dates, phone numbers)
        
        6. Follow this implementation order:
           - First create all roles and grants
           - Then implement row-level security on base tables
           - Finally create secure views with column-level masking
        
        The final script must:
        1. Be complete and ready to execute without modifications
        2. Not contain any placeholders or template variables
        3. Not include any instructions to the user
        4. Not use any built-in administrative roles like ACCOUNTADMIN or SECURITYADMIN
        5. Implement all security policies specified in the JSON
        6. Use only the existing Snowflake roles mentioned in the JSON
        7. Include ALL columns from original tables in secure views (not just classified columns)
        8. Apply masking only to columns that have policies defined in the JSON
        9. Include proper REVOKE statements to remove access to original tables
        10. Include proper GRANT statements to give access to secure views
        
        CRITICAL REQUIREMENTS:
        - Do not create any masking policies with CREATE MASKING POLICY
        - Do not apply masking policies to base tables with ALTER TABLE ... SET MASKING POLICY
        - Apply row filtering before column masking
        - Do not use built-in administrative roles like ACCOUNTADMIN or SECURITYADMIN anywhere in the script
        - For row access policies, do NOT use CURRENT_ROLE() IN ('ACCOUNTADMIN', 'SECURITYADMIN')
        - Row access policies should be based ONLY on the purposes and roles from the JSON
        - Row access policies MUST include role checks using IS_ROLE_IN_SESSION() to verify that users have the appropriate role for the purpose
        - When revoking privileges, only revoke from the specific role mentioned, not from all roles (do not use FROM ROLE ALL)
        - Properly quote object names with special characters
        - Use semicolons to terminate each SQL statement
        - Ensure proper dependencies - objects must be created before they are referenced
        - Ensure data type compatibility in CASE expressions
        - Avoid using reserved keywords as identifiers
        
        The final DDL script MUST be complete, executable, and ready to be run in a Snowflake environment without any modifications or errors.
        
        Format the DDL with proper indentation and SQL best practices. Test each statement for syntax correctness.
        
        The final DDL script MUST be complete, executable, and ready to be run in a Snowflake environment without any modifications, placeholders, or instructions to the user.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                # Extract the SQL content from the response
                ddl_text = response.text.strip()
                
                # Clean up the response if it contains markdown code blocks
                if ddl_text.startswith("```sql"):
                    ddl_text = ddl_text.replace("```sql", "", 1)
                elif ddl_text.startswith("```"):
                    ddl_text = ddl_text.replace("```", "", 1)
                if ddl_text.endswith("```"):
                    ddl_text = ddl_text.replace("```", "", 1)
                
                # Remove any remaining template placeholders
                ddl_text = ddl_text.replace("[TABLE_NAME]", "")
                ddl_text = ddl_text.replace("[PURPOSE_NAME]", "")
                ddl_text = ddl_text.replace("[EMAIL_COLUMN]", "")
                ddl_text = ddl_text.replace("[USER_ID_COLUMN]", "")
                ddl_text = ddl_text.replace("[SPECIFIC_ROLE]", "")
                
                return ddl_text.strip()
            else:
                st.error("Failed to generate security policy DDL. No valid response from the AI model.")
                return None
        except Exception as e:
            st.error(f"An error occurred while generating security policy DDL: {str(e)}")
            return None

    def _generate_access_role_ddl_prompt(self, json_str, role_name):
        """Generate the prompt for the VertexAI model to create a data access role DDL."""
        return f"""
        Generate a Snowflake DDL script to create a data access role based on the following JSON policy specification:
        
        {json_str}
        
        The role name should be: {role_name}
        
        Create a DDL script that follows these requirements:
        
        1. Create a purpose-based role hierarchy:
           - Create the specified data access role if it doesn't exist
           - Create purpose-based roles for each purpose in the JSON (e.g., PURPOSE_MARKETING_CAMPAIGNS)
           - Grant purpose-based roles to the data access role
        
        2. Apply row-level security using row access policies:
           - Create row access policies for tables that have row_filtering in the JSON
           - Policies should filter rows based on user consents for the specified purposes
           - Apply these policies to the base tables
           - Row access policies MUST include role checks using IS_ROLE_IN_SESSION() with purpose-based roles
           - Even if users have consented to a purpose, they should only see data if they have the appropriate role
        
        3. Create secure views for each table in the JSON:
           - Include ALL columns from the original tables
           - Apply column-level masking in the secure views using CASE expressions with IS_ROLE_IN_SESSION checks
           - Only apply masking to columns that have policies defined in the JSON
           - Non-classified columns should be returned as-is without any masking
           - Name masking policies based on data element names (not data types or column names)
        
        4. Set up proper access controls:
           - Revoke access to the original tables from the specific role mentioned, not from all roles
           - Grant access to the secure views to the role
           - Do not use any built-in administrative roles like ACCOUNTADMIN or SECURITYADMIN
        
        The script should follow this structure:
        
        1. CREATE ROLES section
        ```
        -- Create the data access role
        CREATE ROLE IF NOT EXISTS {role_name};
        
        -- Create purpose-based roles
        CREATE ROLE IF NOT EXISTS PURPOSE_MARKETING_CAMPAIGNS;
        
        -- Grant purpose roles to the data access role
        GRANT ROLE PURPOSE_MARKETING_CAMPAIGNS TO ROLE {role_name};
        ```
        
        2. ROW ACCESS POLICIES section
        ```
        -- Create row access policy for a table
        CREATE OR REPLACE ROW ACCESS POLICY consent_rap_table AS (
            identifier_column VARCHAR
        ) RETURNS BOOLEAN ->
          EXISTS (
            SELECT 1 FROM consent_view
            WHERE (
              (identifier_column IS NOT NULL AND identifier_field = identifier_column)
            )
            AND purpose_name IN ('Purpose A', 'Purpose B')
            AND consent_status = 'granted'
            AND (expiry_date IS NULL OR expiry_date > CURRENT_TIMESTAMP())
            -- Only allow roles with the appropriate purpose to access the data
            AND CASE
              WHEN purpose_name = 'Purpose A' THEN IS_ROLE_IN_SESSION('PURPOSE_A')
              WHEN purpose_name = 'Purpose B' THEN IS_ROLE_IN_SESSION('PURPOSE_B')
              ELSE FALSE
            END
          );
          
        -- Apply row access policy
        ALTER TABLE schema.table ADD ROW ACCESS POLICY consent_rap_table(identifier_column);
        ```
        
        3. SECURE VIEWS section
        ```
        -- Create secure view for a table
        CREATE OR REPLACE SECURE VIEW schema.table_secure_view AS
        SELECT
          -- Masked column with policy
          CASE
            WHEN IS_ROLE_IN_SESSION('PURPOSE_A') THEN sensitive_column_1
            ELSE 'masked_value_1'
          END AS sensitive_column_1,
          
          -- Another masked column with policy
          CASE
            WHEN IS_ROLE_IN_SESSION('PURPOSE_B') THEN sensitive_column_2
            ELSE 'masked_value_2'
          END AS sensitive_column_2,
          
          -- Non-classified columns passed through as-is
          id,
          non_sensitive_column_1,
          non_sensitive_column_2,
          non_sensitive_column_3,
          created_at,
          updated_at
        FROM schema.table;
        ```
        
        4. REVOKE & GRANT section
        ```
        -- Revoke access to original tables from the specific role only
        REVOKE ALL PRIVILEGES ON TABLE schema.table FROM ROLE {role_name};
        
        -- Grant access to secure views
        GRANT SELECT ON VIEW schema.table_secure_view TO ROLE {role_name};
        ```
        
        The final script must:
        1. Be complete and ready to execute without modifications
        2. Not contain any placeholders or template variables
        3. Not include any instructions to the user
        4. Not use any built-in administrative roles like ACCOUNTADMIN or SECURITYADMIN
        5. Include ALL columns from original tables in secure views (both classified and non-classified columns)
        6. Apply masking only to columns that have policies defined in the JSON
        7. Non-classified columns must be passed through as-is without any masking
        8. Include row filtering policies based on the purposes in the JSON
        9. Ensure row filtering policies include role checks (using IS_ROLE_IN_SESSION) to verify that users have the appropriate role for the purpose
        10. Use purpose-based roles in the role hierarchy and in masking policy conditions
        11. Name masking policies based on data element names for standardization
        12. When revoking privileges, only revoke from the specific role mentioned, not from all roles
        
        Format the DDL with proper indentation and SQL best practices.
        """
        
    def generate_access_role_ddl(self, policy_json, role_name):
        """Generate Snowflake DDL for creating a data access role based on the provided policy JSON."""
        if policy_json is None:
            return "No policy JSON provided"
        
        # Convert policy_json to string if it's a dictionary
        if isinstance(policy_json, dict):
            import json
            json_str = json.dumps(policy_json, indent=2)
        else:
            json_str = policy_json
            
        # Generate the prompt
        prompt = self._generate_access_role_ddl_prompt(json_str, role_name)
        
        try:
            response = self.model.generate_content(prompt)
            
            if response and hasattr(response, 'text'):
                # Extract the SQL content from the response
                ddl_text = response.text.strip()
                
                # Clean up the response if it contains markdown code blocks
                if ddl_text.startswith("```sql"):
                    ddl_text = ddl_text.replace("```sql", "", 1)
                elif ddl_text.startswith("```"):
                    ddl_text = ddl_text.replace("```", "", 1)
                if ddl_text.endswith("```"):
                    ddl_text = ddl_text.replace("```", "", 1)
                
                return ddl_text.strip()
            else:
                st.error("Failed to generate access role DDL. No valid response from the AI model.")
                return ""
        except Exception as e:
            st.error(f"Error generating access role DDL: {e}")
            return ""
