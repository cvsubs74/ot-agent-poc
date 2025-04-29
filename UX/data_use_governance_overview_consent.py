import streamlit as st

def render_consent_row_filtering_section():
    """Render a detailed section about consent management and row filtering."""
    st.markdown("""
    <h2 class="section-header">Advanced Consent Management & Row-Level Security</h2>
    """, unsafe_allow_html=True)
    
    # Consent Management
    st.markdown("""
    <div class="solution-container">
        <h3 class="subsection-header">Consent Management System</h3>
        <p>
            The consent management system tracks user consents with the following key components:
        </p>
        <ul>
            <li><strong>Consent Profiles</strong>: Store user identifiers (user_id, email) and associated metadata</li>
            <li><strong>Consent Records</strong>: Track individual consent grants/revocations by purpose</li>
            <li><strong>Purpose Mapping</strong>: Link business purposes to specific data processing activities</li>
            <li><strong>Consent Status</strong>: Track whether consent is granted, denied, or expired</li>
            <li><strong>Expiry Management</strong>: Support time-limited consents with automatic expiration</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-Step Security Architecture
    st.markdown("""
    <div class="architecture-container">
        <h3 class="subsection-header">Two-Step Security Architecture</h3>
        <p>
            Due to Snowflake's limitation where columns with masking policies cannot have row access policies, 
            we implement a two-step security approach:
        </p>
        <ol>
            <li><strong>Step 1: Row-Level Security on Base Tables</strong></li>
            <ul>
                <li>Create a secure view of consent records that tracks user consents by purpose</li>
                <li>Generate row access policies (RAPs) for tables with consent-based filtering</li>
                <li>Apply these RAPs to the base tables using ALTER TABLE statements</li>
                <li>This filters data based on user consents for specific purposes</li>
            </ul>
            <li><strong>Step 2: Column-Level Security via Secure Views</strong></li>
            <ul>
                <li>Create secure views on top of the row-filtered base tables</li>
                <li>Implement column masking directly in the view's SELECT statement using CASE expressions</li>
                <li>The views inherit the row-level filtering from the base tables</li>
                <li>Grant access to these secure views instead of the base tables</li>
            </ul>
        </ol>
        <p>
            This approach ensures both row-level and column-level security while working within Snowflake's constraints.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="challenge-container">
        <h3 class="subsection-header">Data Element-Based Identifier Matching</h3>
        <p>
            The system uses a direct data element matching approach to identify user identifier columns:
        </p>
        <ol>
            <li><strong>Problem</strong>: Different tables may use different column names for the same user identifiers</li>
            <li><strong>Solution</strong>: Leverage existing data element classifications to identify the right columns</li>
            <li><strong>Benefits</strong>: Reliable and consistent matching based on established data catalog</li>
        </ol>
        <p>
            The SimpleIdentifierMatcher class uses the following approach:
        </p>
        <ol>
            <li>Map consent profile identifiers to standard data elements:</li>
            <ul>
                <li>user_id → "Customer ID" data element</li>
                <li>email → "Email Address" data element</li>
            </ul>
            <li>For each table, find columns classified with these data elements</li>
            <li>Create a direct mapping between consent identifiers and table columns</li>
            <li>This ensures consistent and accurate identification without complex algorithms</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Row Filtering JSON Structure
    st.markdown("""
    <div class="solution-container">
        <h3 class="subsection-header">Row Filtering JSON Structure</h3>
        <p>
            The system generates a structured JSON representation that includes row filtering information:
        </p>
        <pre style="background-color: #f1f1f1; padding: 15px; border-radius: 5px; font-size: 0.8rem; overflow: auto;">
{
  "tables": {
    "Customer.profiles": {
      "columns": { ... },
      "row_filtering": {
        "identifier_columns": {
          "user_id": "user_id",
          "email": "email_address"
        },
        "purposes": ["Marketing", "Analytics"]
      }
    }
  }
}
        </pre>
        <p>
            This structure specifies:
        </p>
        <ul>
            <li><strong>identifier_columns</strong>: Maps consent profile identifiers to table columns</li>
            <li><strong>purposes</strong>: Lists purposes that require consent checks for this table</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Snowflake DDL Generation
    st.markdown("""
    <div class="architecture-container">
        <h3 class="subsection-header">Snowflake DDL Generation</h3>
        <p>
            The system generates Snowflake DDL that implements our two-step security approach:
        </p>
        <pre style="background-color: #f1f1f1; padding: 15px; border-radius: 5px; font-size: 0.8rem; overflow: auto;">
            
            -- STEP 1: Row-Level Security
            CREATE OR REPLACE ROW ACCESS POLICY consent_rap AS 
            ( email_address VARCHAR ) 
            RETURNS BOOLEAN → 
            CASE 
                WHEN IS_ROLE_IN_SESSION('ACCOUNTADMIN') THEN TRUE
                WHEN IS_ROLE_IN_SESSION('PURPOSE_MARKETING') THEN
                    EXISTS (
                        SELECT 1 FROM consent_view
                        WHERE email = email_address
                        AND purpose_name = 'MARKETING'
                    )
                ELSE FALSE
            END;

            -- STEP 2: Column-Level Security
            CREATE OR REPLACE SECURE VIEW profiles_secure AS
            SELECT 
                CASE 
                    WHEN IS_ROLE_IN_SESSION('ACCOUNTADMIN') THEN email_address
                    WHEN IS_ROLE_IN_SESSION('PURPOSE_MARKETING') THEN email_address
                    ELSE NULL 
                END AS email_address,

                CASE 
                    WHEN IS_ROLE_IN_SESSION('ACCOUNTADMIN') THEN customer_id
                    WHEN IS_ROLE_IN_SESSION('PURPOSE_CUSTOMER_SUPPORT') THEN customer_id
                    ELSE CONCAT('****', RIGHT(customer_id, 4)) 
                END AS customer_id,
                first_name,
                last_name 
            FROM profiles;
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits and Use Cases
    st.markdown("""
    <div class="challenge-container">
        <h3 class="subsection-header">Benefits & Use Cases</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px;">
            <div style="flex: 1; min-width: 200px; background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #1565C0; margin-top: 0;">GDPR Compliance</h4>
                <p>Enforce purpose-specific consent requirements and demonstrate compliance with data subject rights</p>
            </div>
            <div style="flex: 1; min-width: 200px; background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #1565C0; margin-top: 0;">Multi-tenant Systems</h4>
                <p>Ensure data isolation between different customers or organizational units</p>
            </div>
            <div style="flex: 1; min-width: 200px; background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="color: #1565C0; margin-top: 0;">Personalized Marketing</h4>
                <p>Only target users who have explicitly consented to marketing communications</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
