import streamlit as st

def render_consent_row_filtering_section():
    """Render a detailed section about consent management and row filtering."""
    st.markdown("""
    <h2 class="section-header">Advanced Consent Management & Row-Level Security</h2>
    """, unsafe_allow_html=True)
    
    # Overview
    st.markdown("""
    <div class="overview-container">
        <h3 class="subsection-header">Overview</h3>
        <p>
            The advanced consent management and row-level security features enable organizations to implement
            fine-grained access control at the individual record level, ensuring that users only see data
            for which explicit consent has been granted for their specific purpose.
        </p>
    </div>
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
    
    # Row Filtering Architecture
    st.markdown("""
    <div class="architecture-container">
        <h3 class="subsection-header">Row Filtering Architecture</h3>
        <p>
            The row-level security implementation follows a sophisticated multi-layered approach:
        </p>
        <ol>
            <li><strong>Policy Generation</strong>: JSON policies are generated that include row filtering specifications</li>
            <li><strong>Identifier Matching</strong>: AI-powered matching of user identifiers to table columns</li>
            <li><strong>DDL Generation</strong>: Snowflake DDL with row access policies based on the matched identifiers</li>
            <li><strong>Runtime Enforcement</strong>: Row-level filtering applied at query time based on user's role and purpose</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Intelligent Column Matching
    cols = st.columns([2, 1])
    with cols[0]:
        st.markdown("""
        <div class="challenge-container">
            <h3 class="subsection-header">AI-Powered Identifier Matching</h3>
            <p>
                The system uses a sophisticated AI approach to match user identifiers with table columns:
            </p>
            <ol>
                <li><strong>Problem</strong>: Different tables may use different column names for the same user identifiers</li>
                <li><strong>Solution</strong>: AI-powered semantic matching to identify the right columns</li>
                <li><strong>Benefits</strong>: More accurate row filtering without manual configuration</li>
            </ol>
            <p>
                The IdentifierMatcher class uses the following algorithm:
            </p>
            <ol>
                <li>Analyze table column names, data element names, and data types</li>
                <li>Compare against known identifier types (user_id, email)</li>
                <li>Generate a semantic matching score based on multiple factors</li>
                <li>Select the best matches with high confidence scores</li>
                <li>Return a mapping of identifier types to column names</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 15px; margin-top: 20px;">
            <h4 style="color: #1565C0;">Example Prompt</h4>
            <pre style="background-color: #f1f1f1; padding: 10px; border-radius: 5px; font-size: 0.8rem; overflow: auto;">
You are an expert in data mapping and identity resolution. 
Your task is to find the best matching columns 
in a database table that correspond to user 
identifiers needed for consent-based row filtering.

Here are the available columns in the table, 
with their data element names and types:
{
  "user_id": {
    "data_element_name": "User Identifier",
    "data_type": "VARCHAR"
  },
  "email_address": {
    "data_element_name": "Email",
    "data_type": "VARCHAR"
  }
}

Here are the consent identifiers we need to match:
{
  "user_id": {
    "description": "Unique identifier for a user",
    "examples": ["user_id", "userid", "uid"]
  },
  "email": {
    "description": "Email address of a user",
    "examples": ["email", "email_address"]
  }
}
            </pre>
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
            The system generates sophisticated Snowflake DDL that implements row-level security:
        </p>
        <pre style="background-color: #f1f1f1; padding: 15px; border-radius: 5px; font-size: 0.8rem; overflow: auto;">
-- Create a secure view of consent records
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

-- Create row access policy for Customer.profiles
CREATE OR REPLACE ROW ACCESS POLICY consent_rap_Customer_profiles AS (
    email_address VARCHAR, 
    user_id VARCHAR
) RETURNS BOOLEAN ->
  CASE
    -- System roles bypass consent checks
    WHEN IS_ROLE_IN_SESSION('ACCOUNTADMIN') THEN TRUE
    WHEN IS_ROLE_IN_SESSION('SECURITYADMIN') THEN TRUE
    
    -- Purpose-specific consent checks
    WHEN IS_ROLE_IN_SESSION('PURPOSE_MARKETING') THEN
      EXISTS (
        SELECT 1 FROM consent_view
        WHERE (
          (email_address IS NOT NULL AND email = email_address)
          OR 
          (user_id IS NOT NULL AND user_id = user_id)
        )
        AND purpose_name = 'MARKETING'
      )
    
    -- Default deny
    ELSE FALSE
  END;

-- Apply row access policy to the table
ALTER TABLE Customer.profiles ADD ROW ACCESS POLICY consent_rap_Customer_profiles ON (
    email_address, user_id
);
        </pre>
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
