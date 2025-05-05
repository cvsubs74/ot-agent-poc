-- Privacy Regulation Database Seed Script
-- This script creates and populates all tables for the GlossaryRepository, RegulatoryMetadataRepository, and KnowledgeRepository

-- Drop existing tables if they exist (in reverse order of creation to handle foreign key constraints)
DROP TABLE IF EXISTS framework_control;
DROP TABLE IF EXISTS policy_control;
DROP TABLE IF EXISTS risk_control;
DROP TABLE IF EXISTS obligation_risk;
DROP TABLE IF EXISTS obligation_policy;
DROP TABLE IF EXISTS risk;
DROP TABLE IF EXISTS sensitivity_policy_mapping;
DROP TABLE IF EXISTS sensitivity_obligation;
DROP TABLE IF EXISTS obligation;
DROP TABLE IF EXISTS purpose_role;
DROP TABLE IF EXISTS policy_purpose_data_retention;
DROP TABLE IF EXISTS policy_purpose_data_usage;
DROP TABLE IF EXISTS policy_purpose_data_element;
DROP TABLE IF EXISTS policy_purpose;
DROP TABLE IF EXISTS data_subject_right_exemptions;
DROP TABLE IF EXISTS data_subject_right_implementation_steps;
DROP TABLE IF EXISTS legal_basis_requirements;
DROP TABLE IF EXISTS law_purpose_category_legal_basis;
DROP TABLE IF EXISTS law_data_subject_access_request_notification_requirements;
DROP TABLE IF EXISTS law_transfer;

DROP TABLE IF EXISTS data_subject_type_data_element_sensitivity;
DROP TABLE IF EXISTS data_subject_type_data_category_sensitivity;
DROP TABLE IF EXISTS law_data_subject_type_data_category_sensitivity;
DROP TABLE IF EXISTS law_data_subject_type_data_element_sensitivity;
DROP TABLE IF EXISTS data_category_data_element;
DROP TABLE IF EXISTS law_incident_breach_guidance;
DROP TABLE IF EXISTS knowledge_base;
DROP TABLE IF EXISTS law_legal_basis;
DROP TABLE IF EXISTS data_access_request;
DROP TABLE IF EXISTS law_jurisdiction;
DROP TABLE IF EXISTS obligation;
DROP TABLE IF EXISTS policy;
DROP TABLE IF EXISTS asset;

DROP TABLE IF EXISTS sensitivity;
DROP TABLE IF EXISTS data_category;
DROP TABLE IF EXISTS data_subject_type;
DROP TABLE IF EXISTS data_element;
DROP TABLE IF EXISTS breach_type;
DROP TABLE IF EXISTS purpose_category;
DROP TABLE IF EXISTS legal_basis;
DROP TABLE IF EXISTS jurisdiction;
DROP TABLE IF EXISTS law;
DROP TABLE IF EXISTS framework;
DROP TABLE IF EXISTS control;

-- =============================================
-- KNOWLEDGE BASE TABLES
-- =============================================

-- Create Knowledge Base table
CREATE TABLE IF NOT EXISTS `knowledge_base` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category` VARCHAR(100) NOT NULL,
    `subcategory` VARCHAR(100),
    `question` TEXT NOT NULL,
    `answer` TEXT NOT NULL,
    `tags` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_category` (`category`),
    INDEX `idx_subcategory` (`subcategory`),
    FULLTEXT INDEX `idx_question_answer` (`question`, `answer`)
);

-- Seed Knowledge Base with comprehensive FAQ data
INSERT INTO `knowledge_base` (`category`, `subcategory`, `question`, `answer`, `tags`) VALUES

-- Core Constructs
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Core Constructs', 'Data Elements', 'What are data elements?', 'Data elements are the fundamental building blocks of information in the Data Use Governance platform. They represent specific pieces of information that can be collected, stored, processed, or shared, such as names, email addresses, phone numbers, etc. Each data element has properties like sensitivity level and applicable regulations.', 'data elements,basics,glossary'),
('Core Constructs', 'Data Categories', 'What are data categories?', 'Data categories are groupings of related data elements that share similar characteristics, sensitivity levels, or regulatory requirements. Examples include Personal Identifiers, Contact Information, Financial Information, and Health Information. Categorizing data helps in applying consistent policies and controls across similar types of information.', 'data categories,classification,glossary'),
('Core Constructs', 'Sensitivity Levels', 'What are sensitivity levels?', 'Sensitivity levels indicate the potential risk or impact associated with data elements if they were to be compromised. The platform uses sensitivity levels like Public, Internal, Confidential, and Restricted to determine appropriate security controls, access restrictions, and handling requirements for different types of data.', 'sensitivity,classification,risk'),
('Core Constructs', 'Purposes', 'What are purposes in data governance?', 'Purposes define the specific business reasons for collecting, processing, or sharing data. Each purpose must be legitimate, specific, and documented. Examples include Service Provision, Marketing, Analytics, and Legal Compliance. Purposes are crucial for demonstrating lawful processing under regulations like GDPR.', 'purposes,legal basis,processing'),
('Core Constructs', 'Assets', 'What are assets in the platform?', 'Assets represent systems, applications, databases, or other repositories where data is stored or processed. Each asset contains specific data elements and is subject to policies and controls based on the sensitivity of the data it contains. Assets are mapped to data elements to enable comprehensive data governance.', 'assets,systems,inventory');

-- Regulatory Metadata
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Regulatory Metadata', 'Laws and Regulations', 'What regulatory frameworks does the platform support?', 'The platform includes metadata for major privacy regulations including GDPR (Europe), CCPA/CPRA (California), LGPD (Brazil), PIPEDA (Canada), and others. Each regulation is modeled with its specific requirements, obligations, and implementation guidance to enable compliance across multiple jurisdictions.', 'regulations,compliance,legal'),
('Regulatory Metadata', 'Legal Basis', 'What is a legal basis for processing?', 'A legal basis is the lawful ground for processing personal data under privacy regulations. The platform tracks legal bases such as Consent, Contract, Legal Obligation, Vital Interests, Public Task, and Legitimate Interests. Different purposes may require different legal bases depending on the regulation and data involved.', 'legal basis,lawful processing,GDPR'),
('Regulatory Metadata', 'Obligations', 'What are regulatory obligations?', 'Obligations are specific requirements imposed by privacy regulations that organizations must fulfill. These include transparency requirements, security measures, data subject rights handling, breach notification procedures, and more. The platform maps obligations to relevant regulations and provides implementation guidance.', 'obligations,requirements,compliance'),
('Regulatory Metadata', 'Data Subject Rights', 'What are data subject rights?', 'Data subject rights are entitlements individuals have regarding their personal data. These include the right to access, rectification, erasure (right to be forgotten), restriction of processing, data portability, and objection. The platform provides workflows to handle data subject rights requests in compliance with applicable regulations.', 'data subject rights,DSR,privacy rights'),
('Regulatory Metadata', 'Cross-Border Transfers', 'How does the platform handle cross-border data transfers?', 'The platform includes metadata about cross-border transfer requirements, including adequacy decisions, appropriate safeguards (SCCs, BCRs), and exceptions. It helps organizations identify when transfers are occurring and what mechanisms are needed to ensure compliance with regulations like GDPR Chapter V.', 'cross-border,international transfers,SCCs');

-- Decision Trees
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Decision Trees', 'Purpose Selection', 'How do purpose selection decision trees work?', 'Purpose selection decision trees guide users through a structured series of questions to identify the appropriate business purpose for data processing activities. The trees consider factors like the type of relationship with the individual, the nature of the processing, and the business context to recommend compliant purposes.', 'purpose selection,decision support,compliance'),
('Decision Trees', 'Legal Basis Determination', 'How do legal basis decision trees work?', 'Legal basis decision trees help determine the appropriate lawful basis for processing based on the selected purpose, data categories involved, and applicable regulations. The system evaluates factors like the relationship with the data subject, necessity of processing, and potential impacts to recommend the most appropriate legal basis.', 'legal basis,decision support,GDPR'),
('Decision Trees', 'Data Subject Rights Handling', 'How do data subject rights decision trees work?', 'Data subject rights decision trees guide users through the process of evaluating and responding to rights requests. They consider factors like the identity verification status, applicable exemptions, technical feasibility, and regulatory requirements to determine the appropriate response and implementation steps.', 'DSR,rights handling,compliance'),
('Decision Trees', 'Breach Notification', 'How do breach notification decision trees work?', 'Breach notification decision trees help assess security incidents to determine notification requirements. They evaluate factors like the nature of the breach, types of data affected, potential harm to individuals, and applicable regulatory thresholds to recommend notification timing, recipients, and content.', 'breach notification,incident response,security');

-- Inference APIs
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Inference APIs', 'Sensitivity Inference', 'What is sensitivity inference?', 'Sensitivity inference is an AI-powered capability that analyzes data elements to automatically determine their sensitivity level based on their characteristics, content, and context. It uses machine learning models trained on regulatory definitions and industry standards to classify data consistently and accurately.', 'sensitivity,AI,classification'),
('Inference APIs', 'Policy Inference', 'What is policy inference?', 'Policy inference automatically recommends appropriate security and privacy policies based on data sensitivity levels and business purposes. It analyzes the combination of data elements, their sensitivity, processing purposes, and regulatory requirements to generate tailored policy recommendations that ensure compliance.', 'policy inference,automation,compliance'),
('Inference APIs', 'Obligation Inference', 'What is obligation inference?', 'Obligation inference identifies regulatory requirements that apply to specific data processing activities. By analyzing the data elements, purposes, legal bases, and applicable regulations, it determines which obligations must be fulfilled and provides implementation guidance tailored to the specific context.', 'obligation inference,regulatory requirements,compliance'),
('Inference APIs', 'Risk Inference', 'What is risk inference?', 'Risk inference evaluates potential privacy and security risks associated with data processing activities. It considers factors like data sensitivity, processing volume, recipient categories, security controls, and historical incidents to quantify risks and recommend appropriate mitigation measures.', 'risk inference,risk assessment,DPIA'),
('Inference APIs', 'Control Inference', 'What is control inference?', 'Control inference recommends appropriate technical and organizational security controls based on data sensitivity, identified risks, and regulatory requirements. It maps controls to specific frameworks (like ISO 27001, NIST) and provides implementation guidance to ensure adequate protection of personal data.', 'control inference,security controls,safeguards');

-- Data Use Governance
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Data Use Governance', 'Overview', 'What is Data Use Governance?', 'Data Use Governance is a comprehensive approach to managing how data is collected, used, shared, and protected within an organization. It combines regulatory compliance, ethical considerations, and business needs to ensure that data is used appropriately, lawfully, and in line with individual expectations and rights.', 'data governance,overview,compliance'),
('Data Use Governance', 'User Journeys', 'What are User Journeys in the platform?', 'User Journeys are guided workflows that help users navigate complex data governance processes. The platform includes journeys for Data Access Requests (helping users request access to data based on legitimate purposes) and Policy Inference (guiding users through the process of determining appropriate policies for data assets).', 'user journeys,workflows,user experience'),
('Data Use Governance', 'Data Access Requests', 'How do Data Access Requests work?', 'The Data Access Request journey allows users to request access to data assets for specific business purposes. The system validates that the purpose is legitimate, that the user has appropriate roles, and that the requested access complies with applicable policies. It creates an auditable record of the request, approval process, and granted access.', 'data access,authorization,audit'),
('Data Use Governance', 'Policy Implementation', 'How are policies implemented in systems?', 'The platform generates implementation artifacts like Snowflake DDL scripts that enforce policies in target systems. These artifacts include role definitions, masking policies, row-level security, and other controls that ensure data is protected according to its sensitivity and only accessible for authorized purposes.', 'policy implementation,enforcement,technical controls'),
('Data Use Governance', 'Compliance Monitoring', 'How does the platform support compliance monitoring?', 'The platform provides dashboards and reports that show the status of compliance across the organization. It tracks metrics like policy coverage, data subject rights fulfillment, breach response times, and control implementation to give visibility into compliance posture and identify areas needing improvement.', 'compliance monitoring,reporting,metrics');

-- Purpose-Based Access Control
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Purpose-Based Access Control', 'Core Concept', 'What is Purpose-Based Access Control?', 'Purpose-Based Access Control (PBAC) is a governance model that restricts data access based on the business purpose for which the data will be used. It extends traditional Role-Based Access Control (RBAC) by adding an additional layer of control that considers not just who the user is, but why they need the data. This approach ensures data is only used for legitimate, documented purposes that comply with privacy regulations and organizational policies.', 'PBAC,access control,data governance'),
('Purpose-Based Access Control', 'Architecture', 'How is Purpose-Based Access Control implemented in the platform?', 'The platform implements PBAC through a multi-layered architecture: (1) Purpose Registry - centralized repository of all legitimate business purposes; (2) Purpose-Role Mapping - associates roles with specific purposes; (3) Policy Engine - defines data access and protection rules for each purpose; (4) Enforcement Layer - generates technical controls (Snowflake DDL) that implement the policies in target systems. This architecture ensures consistent enforcement across all data assets.', 'architecture,implementation,enforcement'),
('Purpose-Based Access Control', 'Purpose Registry', 'How does the Purpose Registry work?', 'The Purpose Registry is a centralized repository that defines all legitimate business purposes for data processing. Each purpose includes: (1) A clear definition and description; (2) Associated legal bases under relevant regulations; (3) Data categories required for the purpose; (4) Retention periods; (5) Security requirements. The registry serves as the foundation for purpose-based access control by providing a reference for all purpose-related decisions.', 'purpose registry,business purposes,data processing'),
('Purpose-Based Access Control', 'Role Hierarchy', 'How does the role hierarchy work in Purpose-Based Access Control?', 'The platform implements a two-tier role hierarchy: (1) Purpose-based roles (PURPOSE_X) that represent business purposes like Marketing or Analytics; (2) Data access roles (DATA_X_Y) that are granted to purpose-based roles and provide actual access to data assets. This hierarchy ensures that users only receive access to data needed for their legitimate purposes, following the principle of least privilege.', 'role hierarchy,RBAC,least privilege'),
('Purpose-Based Access Control', 'Snowflake Implementation', 'How is Purpose-Based Access Control implemented in Snowflake?', 'The platform generates Snowflake DDL that implements PBAC through: (1) Purpose-based roles (PURPOSE_X) that users are assigned to; (2) Data access roles (DATA_X_Y) that are granted to purpose-based roles; (3) Masking policies that use IS_ROLE_IN_SESSION() to check for purpose-based roles; (4) Row-level security policies for consent-based filtering. This approach provides both column-level and row-level protection based on purposes.', 'Snowflake,DDL,implementation');

-- Consent Management
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Consent Management', 'Overview', 'How does the platform handle consent management?', 'The platform includes a comprehensive consent management system that tracks user consents with key components: (1) Consent Profiles - store user identifiers and metadata; (2) Consent Records - track individual consent grants/revocations by purpose; (3) Purpose Mapping - link business purposes to processing activities; (4) Consent Status - track whether consent is granted, denied, or expired; (5) Expiry Management - support time-limited consents with automatic expiration.', 'consent management,GDPR,privacy'),
('Consent Management', 'Row-Level Security', 'How does the platform implement consent-based row filtering?', 'The platform implements consent-based row filtering through a two-step approach: (1) Row-Level Security on Base Tables - creates secure views of consent records and applies row access policies to base tables; (2) Column-Level Security via Secure Views - creates secure views on top of row-filtered tables with column masking. This approach ensures both row-level and column-level security while working within Snowflake\'s constraints.', 'row filtering,RLS,consent enforcement'),
('Consent Management', 'Identifier Matching', 'How does the platform match user identifiers for consent enforcement?', 'The platform uses a data element-based identifier matching approach to identify user identifier columns: (1) Maps consent profile identifiers to standard data elements (e.g., user_id → "Customer ID"); (2) For each table, finds columns classified with these data elements; (3) Creates a direct mapping between consent identifiers and table columns. This ensures consistent and accurate identification without complex algorithms.', 'identifier matching,consent enforcement,data elements');

-- DDL Generation
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('DDL Generation', 'Overview', 'How does the DDL Generator work?', 'The DDL Generator automatically creates Snowflake Data Definition Language (DDL) scripts that implement purpose-based access control and data protection policies. It analyzes the data assets, purposes, and policies to generate a comprehensive set of DDL statements that create roles, masking policies, row access policies, secure views, and appropriate grants. This automation ensures consistent implementation of security controls across all data assets.', 'DDL,Snowflake,automation'),
('DDL Generation', 'Role Structure', 'What role structure does the DDL Generator create?', 'The DDL Generator creates a purpose-based role hierarchy with: (1) Purpose-based roles (PURPOSE_X) that represent business purposes; (2) Data access roles (DATA_X_Y) that are granted to purpose-based roles and provide actual access to data assets. This structure ensures that users only receive access to data needed for their legitimate purposes, following the principle of least privilege.', 'roles,hierarchy,least privilege'),
('DDL Generation', 'Masking Policies', 'How does the DDL Generator create masking policies?', 'The DDL Generator creates masking policies that: (1) Are named based on data element names for standardization and maintainability; (2) Use IS_ROLE_IN_SESSION() with purpose-based roles rather than listing individual roles; (3) Implement appropriate masking formats based on data types (e.g., email masking, partial masking for identifiers); (4) Include comments explaining the policy purpose and application. This approach ensures consistent and maintainable masking across all data assets.', 'masking policies,data protection,Snowflake'),
('DDL Generation', 'Row Access Policies', 'How does the DDL Generator create row access policies?', 'For consent-based filtering, the DDL Generator creates row access policies that: (1) Check the consent status for specific purposes; (2) Filter rows based on user identifiers matched to consent records; (3) Include appropriate exceptions for administrative roles; (4) Optimize performance through appropriate indexing and query design. These policies ensure that users only see rows for which they have consent-based authorization.', 'row access policies,consent,filtering');

-- Platform Architecture
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Platform Architecture', 'Vision', 'What is the vision for the unified platform?', 'The vision is to create a seamless, purpose-driven platform that unifies data governance, privacy management, and regulatory compliance into a cohesive ecosystem. This platform will empower organizations to confidently manage their data with built-in compliance and purpose-based access control, providing a single source of truth for all data-related activities and ensuring consistent enforcement of policies across the organization.', 'vision,platform,unification'),
('Platform Architecture', 'Key Components', 'What are the key components of the platform architecture?', 'The platform architecture includes: (1) Unified Data Model - consistent representation across systems; (2) Purpose Registry - central registry of defined purposes; (3) Policy Engine - automated enforcement of governance policies; (4) Compliance Automation - built-in regulatory requirements; (5) User Experience Layer - intuitive workflows and dashboards. These components work together to provide a comprehensive solution for data governance, privacy, and compliance.', 'components,architecture,design'),
('Platform Architecture', 'Implementation Roadmap', 'What is the implementation roadmap for the platform?', 'The platform implementation roadmap includes three phases: (1) Foundation (Q3 2025) - Establish the data model, purpose registry, and basic governance capabilities; (2) Policy Engine & Compliance Automation (Q1 2026) - Implement the policy engine, automated DDL generation, and compliance verification; (3) Unified User Experience & Integration (Q3 2026) - Complete the platform with a cohesive user experience and comprehensive integration capabilities.', 'roadmap,implementation,timeline'),
('Platform Architecture', 'Integration Capabilities', 'What integration capabilities does the platform provide?', 'The platform provides comprehensive integration capabilities including: (1) API-first design for programmatic access to all platform functions; (2) Pre-built connectors for common data sources and systems; (3) Webhook support for event-driven integration; (4) ETL/ELT capabilities for data ingestion and synchronization; (5) Export capabilities for reporting and auditing. These capabilities ensure the platform can integrate seamlessly with existing systems and data sources.', 'integration,API,connectors');

-- Decision Trees (Advanced)
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Decision Trees', 'Overview', 'What are Decision Trees in the platform?', 'Decision Trees in the platform are structured, rule-based models that automate complex decision-making processes for data governance and compliance. They represent a series of conditional checks and logical operations that determine the appropriate policies, controls, and actions for data assets based on their characteristics, regulatory requirements, and business context. Decision Trees enable consistent, transparent, and auditable decision-making across the organization.', 'decision trees,automation,rules engine'),
('Decision Trees', 'Architecture', 'How are Decision Trees structured in the platform?', 'Decision Trees in the platform follow a hierarchical structure with: (1) Root Node - the starting point of the decision process; (2) Decision Nodes - points where the tree branches based on specific conditions; (3) Leaf Nodes - endpoints that represent final decisions or outcomes; (4) Edges - connections between nodes representing possible paths; (5) Conditions - logical expressions evaluated at decision nodes. This structure allows for complex, multi-factor decision-making while maintaining transparency and auditability.', 'tree structure,nodes,conditions'),
('Decision Trees', 'Policy Inference', 'How do Decision Trees support policy inference?', 'Decision Trees power the policy inference engine by: (1) Evaluating data asset characteristics (classification, sensitivity, etc.); (2) Checking regulatory requirements based on jurisdictions and data types; (3) Considering business context and purposes; (4) Applying organizational policies and standards; (5) Determining appropriate security controls, retention periods, and usage restrictions. This automated inference ensures consistent policy application and reduces manual effort in policy determination.', 'policy inference,automation,compliance'),
('Decision Trees', 'Implementation', 'How are Decision Trees implemented in the platform?', 'Decision Trees are implemented through a combination of: (1) JSON-based tree definitions that specify the structure, conditions, and outcomes; (2) A rules engine that evaluates conditions and traverses the tree; (3) Integration points with metadata repositories, regulatory databases, and policy stores; (4) Caching mechanisms for performance optimization; (5) Versioning support for tracking changes over time. This implementation ensures flexibility, performance, and maintainability of the decision logic.', 'implementation,rules engine,JSON'),
('Decision Trees', 'Customization', 'Can Decision Trees be customized for specific organizational needs?', 'Yes, Decision Trees in the platform are fully customizable. Organizations can: (1) Define custom conditions based on their specific metadata attributes; (2) Create organization-specific decision paths and outcomes; (3) Implement custom logic for specialized compliance requirements; (4) Integrate with proprietary systems and data sources; (5) Extend the tree structure with additional nodes and conditions. This customization ensures the platform can adapt to the unique governance needs of each organization.', 'customization,extensibility,organization-specific'),
('Decision Trees', 'Auditability', 'How do Decision Trees support auditability?', 'Decision Trees provide comprehensive auditability through: (1) Complete decision path logging for every evaluation; (2) Timestamps and user context for each decision; (3) Version tracking of tree definitions; (4) Visualization tools for decision paths; (5) Exportable audit trails for compliance reporting. This auditability ensures organizations can demonstrate how and why specific governance decisions were made, supporting regulatory compliance and internal governance requirements.', 'auditability,compliance,logging');

-- Inference APIs (Advanced)
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Inference APIs', 'Overview', 'What are the Inference APIs in the platform?', 'The Inference APIs are a set of programmatic interfaces that enable applications to leverage the platform\'s decision-making capabilities. They provide access to the policy inference engine, decision trees, and compliance automation features through standardized, well-documented REST endpoints. These APIs allow for real-time policy decisions, automated compliance checks, and integration with external systems, making the platform\'s intelligence available throughout the organization\'s technology ecosystem.', 'APIs,inference,integration'),
('Inference APIs', 'Policy Inference API', 'How does the Policy Inference API work?', 'The Policy Inference API allows applications to determine appropriate policies for data assets by: (1) Accepting input parameters about data assets, contexts, and purposes; (2) Running these inputs through the decision tree-based inference engine; (3) Applying relevant regulatory requirements and organizational policies; (4) Returning comprehensive policy recommendations including security controls, retention periods, and usage restrictions; (5) Providing explanations for each recommendation. This API enables consistent policy application across all integrated systems.', 'policy inference,API,recommendations'),
('Inference APIs', 'Compliance Verification API', 'What does the Compliance Verification API do?', 'The Compliance Verification API enables automated compliance checks by: (1) Accepting descriptions of data processing activities or system configurations; (2) Evaluating these against applicable regulatory requirements and organizational policies; (3) Identifying compliance gaps or potential issues; (4) Recommending remediation actions; (5) Generating compliance evidence and documentation. This API helps organizations proactively identify and address compliance risks before they become problems.', 'compliance verification,regulatory requirements,remediation'),
('Inference APIs', 'Access Control API', 'How does the Access Control API work?', 'The Access Control API enables purpose-based access control by: (1) Evaluating access requests against legitimate business purposes; (2) Checking user roles and permissions; (3) Verifying consent status for relevant data subjects; (4) Determining appropriate data masking and filtering requirements; (5) Generating access control artifacts like Snowflake DDL. This API ensures that access to sensitive data is consistently governed according to regulatory requirements and organizational policies.', 'access control,PBAC,authorization'),
('Inference APIs', 'Integration Patterns', 'How can applications integrate with the Inference APIs?', 'Applications can integrate with the Inference APIs through multiple patterns: (1) Direct REST API calls for real-time decisions; (2) Webhook subscriptions for event-driven integration; (3) Batch processing for high-volume operations; (4) SDK integration for simplified development; (5) Message queue integration for asynchronous processing. These flexible integration patterns ensure the platform can support various application architectures and performance requirements.', 'integration patterns,REST,webhooks'),
('Inference APIs', 'Performance and Scalability', 'How do the Inference APIs handle performance and scalability?', 'The Inference APIs are designed for enterprise-scale performance through: (1) Distributed architecture with horizontal scaling; (2) Caching of frequently used decisions and reference data; (3) Asynchronous processing options for batch operations; (4) Rate limiting and throttling controls; (5) Performance monitoring and optimization. This design ensures the APIs can support high-volume, mission-critical applications while maintaining consistent response times and reliability.', 'performance,scalability,enterprise'),
('Inference APIs', 'Security', 'How are the Inference APIs secured?', 'The Inference APIs implement comprehensive security measures including: (1) OAuth 2.0/OIDC authentication and authorization; (2) Fine-grained access controls for API operations; (3) TLS encryption for all communications; (4) API key management with rotation policies; (5) Audit logging of all API calls; (6) Rate limiting and abuse prevention; (7) Vulnerability scanning and penetration testing. These measures ensure that the APIs themselves don\'t become a security or compliance risk.', 'API security,authentication,encryption');

-- Decision Tree Implementation
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Decision Tree Implementation', 'JSON Structure', 'How are Decision Trees defined in JSON?', 'Decision Trees are defined using a structured JSON format that includes: (1) Tree metadata (id, name, version, description); (2) Node definitions with unique identifiers, types (decision/leaf), and conditions; (3) Edge definitions connecting nodes and specifying transition conditions; (4) Condition expressions using a standardized syntax for evaluating attributes; (5) Outcome definitions at leaf nodes. This JSON structure makes trees both machine-processable and human-readable, supporting both automated execution and manual review.', 'JSON,tree definition,structure'),
('Decision Tree Implementation', 'Condition Syntax', 'What syntax is used for conditions in Decision Trees?', 'Decision Tree conditions use a standardized expression syntax that supports: (1) Comparison operators (==, !=, >, <, >=, <=); (2) Logical operators (AND, OR, NOT); (3) Functions for string operations, date calculations, and list processing; (4) Variable references to input parameters and context data; (5) Regular expressions for pattern matching. This expressive syntax allows for complex conditions while maintaining readability and maintainability.', 'conditions,expressions,syntax'),
('Decision Tree Implementation', 'Execution Engine', 'How does the Decision Tree execution engine work?', 'The Decision Tree execution engine: (1) Parses the JSON tree definition; (2) Validates the tree structure and condition syntax; (3) Initializes the execution context with input parameters; (4) Traverses the tree from the root node, evaluating conditions at each decision node; (5) Follows the appropriate edges based on condition results; (6) Collects outcomes when reaching leaf nodes; (7) Returns the complete decision path and outcomes. This process ensures deterministic, reproducible decision-making based on the defined tree structure.', 'execution engine,traversal,evaluation'),
('Decision Tree Implementation', 'Versioning and Governance', 'How are Decision Trees versioned and governed?', 'Decision Trees include comprehensive versioning and governance features: (1) Each tree has a version number and change history; (2) Trees go through defined approval workflows before activation; (3) Changes are tracked with author information and timestamps; (4) Previous versions remain available for audit purposes; (5) Impact analysis tools help evaluate the effects of changes. These features ensure that changes to decision logic are controlled, transparent, and auditable.', 'versioning,governance,change management');

-- Data Use Governance Design
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Data Use Governance Design', 'Purpose-Driven Architecture', 'How does purpose-driven governance work in the platform?', 'Purpose-driven governance is the core architectural principle of the platform, where all data access and usage controls flow from legitimate business purposes. The implementation follows these key steps: (1) Define business purposes in the Purpose Registry (e.g., "Marketing Analytics", "Customer Support"); (2) Associate purposes with legal bases (e.g., consent, legitimate interest); (3) Link purposes to specific data elements and processing activities; (4) Define purpose-specific policies for security, retention, and usage; (5) Implement technical controls based on these purposes. For example, when a data analyst needs access to customer data for marketing analytics, they request access for that specific purpose, and all controls (masking, filtering, retention) are automatically determined based on the purpose definition.', 'purpose-driven,architecture,governance model'),
('Data Use Governance Design', 'Purpose Registry', 'What information is stored in the Purpose Registry?', 'The Purpose Registry is the central repository for all legitimate business purposes and contains: (1) Purpose definitions with unique identifiers and descriptions; (2) Legal basis mapping (e.g., "Marketing Analytics" → consent required); (3) Data category requirements (e.g., "Fraud Detection" → requires transaction data); (4) Jurisdictional variations (e.g., different requirements in EU vs. US); (5) Purpose hierarchies and relationships; (6) Approval workflows and stakeholders; (7) Audit history of purpose definitions. For example, the "Customer Support" purpose might specify that it requires customer contact information and recent order history, operates under the legal basis of contract fulfillment, and has a retention period of 90 days after ticket resolution.', 'purpose registry,business purposes,legal basis'),
('Data Use Governance Design', 'Baseline Policy Implementation', 'What are baseline policies and how are they implemented?', 'Baseline policies represent the minimum controls that must be applied to all data assets regardless of purpose, establishing a foundation for data governance. They are implemented through: (1) A special "Baseline" purpose that is automatically applied to all data assets; (2) Mandatory controls defined at the organization level (e.g., encryption at rest for all PII); (3) Default retention periods based on data categories; (4) Minimum access control requirements; (5) Logging and monitoring standards. For example, a baseline policy might specify that all email addresses must be encrypted at rest, accessible only to authorized roles, and automatically purged after 7 years unless overridden by a more specific purpose-based policy.', 'baseline policies,minimum controls,default governance'),
('Data Use Governance Design', 'Default Purpose', 'How does the default purpose work for baseline policies?', 'The platform implements a special "Baseline" purpose that serves as the default for all data assets and enforces baseline policies. This works through: (1) Automatic association of all data assets with the Baseline purpose; (2) Definition of minimum controls in the Baseline purpose policies; (3) Override mechanisms where specific purposes can enhance but not weaken baseline controls; (4) Inheritance of baseline controls when no purpose-specific control is defined. For example, if the Baseline purpose specifies that all PII must be masked for general users, this masking will be applied even when data is accessed for Marketing unless the Marketing purpose explicitly defines stronger masking requirements.', 'default purpose,baseline,inheritance'),
('Data Use Governance Design', 'Policy Hierarchy', 'How are policies defined at multiple levels in the platform?', 'The platform implements a hierarchical policy model with multiple levels: (1) Organization-level policies that apply across all data; (2) Data domain policies for specific business domains (e.g., Finance, HR); (3) Data category policies based on data types (e.g., PII, Payment data); (4) Purpose-specific policies tied to business purposes; (5) Asset-specific policies for individual data assets. Policies defined at higher levels cascade down unless explicitly overridden. For example, an organization might define a baseline policy that all PII must be retained for at least 1 year, while the Marketing purpose might extend this to 3 years for customer contact information, and a specific campaign dataset might further extend it to 5 years due to specific regulatory requirements.', 'policy hierarchy,multi-level,inheritance'),
('Data Use Governance Design', 'Policy Resolution', 'How does the platform resolve conflicts between policies at different levels?', 'The platform resolves policy conflicts through a well-defined resolution mechanism: (1) More specific policies override more general ones (asset > purpose > category > domain > organization); (2) For security controls, the most restrictive policy wins (e.g., if one policy requires masking and another doesn\'t, masking is applied); (3) For retention periods, the longest required retention wins to ensure compliance; (4) Explicit exceptions can be documented with justifications; (5) Resolution decisions are logged for audit purposes. For example, if the organization baseline requires 1-year retention for transaction data, but the Fraud Detection purpose requires 7 years, and applicable financial regulations require 10 years, the 10-year retention period will be applied and documented.', 'conflict resolution,policy precedence,most restrictive'),
('Data Use Governance Design', 'Policy Inheritance Example', 'Can you provide an example of policy inheritance across multiple levels?', 'Consider customer email addresses in an e-commerce database: (1) Organization baseline policy: All PII must be encrypted at rest and retained for at least 1 year; (2) Data category policy for contact information: Must be masked for general users and retained for 3 years; (3) Marketing purpose policy: Requires explicit consent and full masking except for marketing team roles; (4) Customer Support purpose policy: Partial masking for support agents, full access for support managers; (5) Specific asset policy for VIP customer database: Additional access restrictions and 7-year retention. When a support agent accesses the VIP customer database for a support ticket, they see partially masked emails due to the Customer Support purpose policy, while the data is retained for 7 years due to the specific asset policy, and all access is logged per the organization baseline.', 'inheritance example,multi-level policies,practical application'),
('Data Use Governance Design', 'Purpose-Based Access Control Implementation', 'How is purpose-based access control technically implemented?', 'Purpose-based access control is implemented through: (1) Purpose-role mappings in identity management systems; (2) Purpose-based roles in data platforms (e.g., PURPOSE_MARKETING in Snowflake); (3) Dynamic policy generation based on purpose definitions; (4) Context-aware access control checks at runtime; (5) Purpose-specific data views and filters. For example, when a data analyst is assigned the Marketing Analyst role, they automatically receive the PURPOSE_MARKETING role in Snowflake. When they query customer data, Snowflake\'s masking policies check for this purpose role and apply the appropriate masking and filtering based on the Marketing purpose definition, showing only data from customers who have consented to marketing.', 'PBAC implementation,technical controls,access management');

-- Policy Implementation Examples
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Policy Implementation Examples', 'Snowflake DDL Example', 'Can you provide an example of how policies are implemented in Snowflake DDL?', 'Here\'s an example of how a purpose-based masking policy for email addresses is implemented in Snowflake:\n\n```sql\n-- Create purpose-based role\nCREATE ROLE IF NOT EXISTS PURPOSE_MARKETING;\n\n-- Create data access role and grant to purpose role\nCREATE ROLE IF NOT EXISTS DATA_CUSTOMER_READ;\nGRANT ROLE DATA_CUSTOMER_READ TO ROLE PURPOSE_MARKETING;\n\n-- Create masking policy for email addresses\nCREATE OR REPLACE MASKING POLICY email_address_mask AS\n(val STRING) RETURNS STRING ->\n  CASE\n    WHEN IS_ROLE_IN_SESSION(\'ACCOUNTADMIN\') THEN val\n    WHEN IS_ROLE_IN_SESSION(\'PURPOSE_MARKETING\') AND\n         EXISTS (SELECT 1 FROM consent_view\n                 WHERE email = val AND purpose = \'MARKETING\')\n      THEN val\n    WHEN IS_ROLE_IN_SESSION(\'PURPOSE_CUSTOMER_SUPPORT\')\n      THEN REGEXP_REPLACE(val, \'(.)(.*)(@.*)\'\n                        , \'$1****$3\')\n    ELSE \'****@****.com\'\n  END;\n\n-- Apply the masking policy to the email column\nALTER TABLE customers MODIFY COLUMN email\n  SET MASKING POLICY email_address_mask;\n```\n\nThis example shows how the email masking varies by purpose: full access for marketing with consent, partial masking for customer support, and full masking for other purposes.', 'Snowflake example,DDL,masking policy'),
('Policy Implementation Examples', 'Row-Level Security Example', 'Can you provide an example of purpose-based row-level security?', 'Here\'s an example of how purpose-based row-level security is implemented for consent-based filtering:\n\n```sql\n-- Create a secure view of consent records\nCREATE OR REPLACE SECURE VIEW consent_view AS\nSELECT user_id, email, purpose_name AS purpose, status\nFROM consent_records\nWHERE status = \'GRANTED\';\n\n-- Create row access policy for customer data\nCREATE OR REPLACE ROW ACCESS POLICY consent_rap AS\n(email_address VARCHAR) RETURNS BOOLEAN ->\nCASE\n  WHEN IS_ROLE_IN_SESSION(\'ACCOUNTADMIN\') THEN TRUE\n  WHEN IS_ROLE_IN_SESSION(\'PURPOSE_MARKETING\') THEN\n    EXISTS (\n      SELECT 1 FROM consent_view\n      WHERE email = email_address\n      AND purpose = \'MARKETING\'\n    )\n  WHEN IS_ROLE_IN_SESSION(\'PURPOSE_ANALYTICS\') THEN\n    EXISTS (\n      SELECT 1 FROM consent_view\n      WHERE email = email_address\n      AND purpose = \'ANALYTICS\'\n    )\n  ELSE FALSE\nEND;\n\n-- Apply the row access policy to the customers table\nALTER TABLE customers ADD ROW ACCESS POLICY consent_rap ON (email);\n```\n\nThis example shows how different purposes (Marketing, Analytics) only see rows for customers who have granted consent for that specific purpose.', 'row-level security,consent filtering,RLS example'),
('Policy Implementation Examples', 'Multi-Level Policy Example', 'Can you provide an example of how multi-level policies are combined?', 'Here\'s an example showing how policies at different levels are combined for credit card data:\n\n```sql\n-- Organization baseline policy (applies to all PCI data)\nCREATE OR REPLACE MASKING POLICY baseline_pci_mask AS\n(val STRING) RETURNS STRING ->\n  CASE\n    WHEN IS_ROLE_IN_SESSION(\'ACCOUNTADMIN\') THEN val\n    ELSE \'XXXX-XXXX-XXXX-XXXX\'\n  END;\n\n-- Purpose-specific policy for Customer Support\nCREATE OR REPLACE MASKING POLICY support_cc_mask AS\n(val STRING) RETURNS STRING ->\n  CASE\n    WHEN IS_ROLE_IN_SESSION(\'ACCOUNTADMIN\') THEN val\n    WHEN IS_ROLE_IN_SESSION(\'PURPOSE_CUSTOMER_SUPPORT\') THEN\n      REGEXP_REPLACE(val, \'(\\d{4})-(\\d{4})-(\\d{4})-(\\d{4})\'\n                    , \'XXXX-XXXX-XXXX-$4\')\n    ELSE \'XXXX-XXXX-XXXX-XXXX\'\n  END;\n\n-- Asset-specific policy for premium customer data\nCREATE OR REPLACE MASKING POLICY premium_cc_mask AS\n(val STRING) RETURNS STRING ->\n  CASE\n    WHEN IS_ROLE_IN_SESSION(\'ACCOUNTADMIN\') THEN val\n    WHEN IS_ROLE_IN_SESSION(\'PURPOSE_FRAUD_DETECTION\') THEN val\n    WHEN IS_ROLE_IN_SESSION(\'PURPOSE_CUSTOMER_SUPPORT\') AND\n         IS_ROLE_IN_SESSION(\'PREMIUM_SUPPORT\') THEN\n      REGEXP_REPLACE(val, \'(\\d{4})-(\\d{4})-(\\d{4})-(\\d{4})\'\n                    , \'$1-XXXX-XXXX-$4\')\n    ELSE \'XXXX-XXXX-XXXX-XXXX\'\n  END;\n\n-- Apply policies to different tables based on context\nALTER TABLE payment_data MODIFY COLUMN cc_number\n  SET MASKING POLICY baseline_pci_mask;\n\nALTER TABLE customer_support.payment_data MODIFY COLUMN cc_number\n  SET MASKING POLICY support_cc_mask;\n\nALTER TABLE premium_customers.payment_data MODIFY COLUMN cc_number\n  SET MASKING POLICY premium_cc_mask;\n```\n\nThis example shows how the same data element (credit card number) has different masking based on the context: complete masking by default, last 4 digits for customer support, and first 4 + last 4 for premium support with additional role requirements.', 'multi-level example,policy combination,contextual policies');
-- Policy Governance
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Policy Governance', 'Policy Lifecycle Management', 'How does the platform manage the policy lifecycle?', 'The platform manages the complete policy lifecycle through: (1) Policy creation with templates and wizards; (2) Review and approval workflows with stakeholder sign-offs; (3) Version control and change tracking; (4) Policy testing in non-production environments; (5) Controlled deployment to production; (6) Monitoring and effectiveness measurement; (7) Periodic review and recertification; (8) Policy retirement and archiving. For example, when creating a new data retention policy for customer data, the policy goes through drafting by the data governance team, review by legal and privacy, approval by the data governance board, testing in a sandbox environment, controlled rollout to production, and scheduled annual reviews to ensure it remains appropriate and effective.', 'policy lifecycle,governance process,change management'),
('Policy Governance', 'Policy Exceptions', 'How are policy exceptions handled in the platform?', 'The platform provides a structured process for policy exceptions: (1) Exception request with business justification; (2) Risk assessment of the exception; (3) Approval workflow with appropriate authorities; (4) Time-bound exception with expiration date; (5) Compensating controls to mitigate risks; (6) Documentation and audit trail; (7) Periodic review of active exceptions. For example, if a specific marketing campaign requires retaining customer data beyond the standard retention period, the marketing team can request an exception, which must be approved by the privacy officer and data governance board, will be valid only for the campaign duration plus 30 days, requires additional access controls as compensation, and is documented for audit purposes.', 'exceptions,risk assessment,compensating controls'),
('Policy Governance', 'Policy Effectiveness Measurement', 'How does the platform measure policy effectiveness?', 'The platform measures policy effectiveness through: (1) Compliance metrics tracking policy violations and exceptions; (2) Technical control validation to ensure policies are correctly implemented; (3) User behavior analysis to identify potential circumvention; (4) Periodic control testing and validation; (5) Audit findings and remediation tracking; (6) Benchmarking against industry standards; (7) Feedback collection from stakeholders. For example, the platform might track that a data retention policy for customer information has 98% compliance, with 3 approved exceptions, 2 violations that were remediated within 24 hours, and feedback from the privacy team that the policy is effective but could be improved with more granular controls for international customers.', 'effectiveness,metrics,measurement'),
('Policy Governance', 'Policy Documentation', 'How are policies documented in the platform?', 'The platform maintains comprehensive policy documentation including: (1) Policy statements with clear objectives and scope; (2) Technical implementation details; (3) Mappings to regulatory requirements; (4) Responsible roles and stakeholders; (5) Exception processes; (6) Review and approval history; (7) Related procedures and guidelines; (8) Training materials for affected users. For example, a data classification policy would include the formal policy statement, classification levels and criteria, implementation details in various systems, mapping to regulations like GDPR and CCPA, the governance committee responsible for the policy, the exception process, approval history showing it was last updated 3 months ago, procedures for classifying new data assets, and training materials for data stewards.', 'documentation,policy statements,knowledge management');

-- Purpose Management
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Purpose Management', 'Purpose Creation Process', 'How are new business purposes created in the platform?', 'The platform supports a structured purpose creation process: (1) Purpose definition with clear description and scope; (2) Legal basis determination (consent, contract, legitimate interest, etc.); (3) Data category requirements specification; (4) Purpose-specific policy definition; (5) Stakeholder review and approval; (6) Purpose activation and communication; (7) Integration with access control systems. For example, when creating a new "Product Improvement" purpose, the product team would define the purpose scope, work with legal to determine it operates under legitimate interest, specify it requires usage data but not PII, define appropriate retention and access policies, get approval from the privacy office, and then the purpose would be activated in the system and made available for access requests.', 'purpose creation,process,governance'),
('Purpose Management', 'Purpose Hierarchy', 'How does the platform handle purpose hierarchies?', 'The platform supports hierarchical purpose structures: (1) Top-level purpose categories (e.g., Operations, Marketing, Analytics); (2) Sub-purposes for specific activities (e.g., Email Marketing, Social Media Marketing); (3) Inheritance of policies from parent to child purposes; (4) Override capabilities for specific sub-purposes; (5) Purpose relationship mapping and visualization. For example, "Marketing" might be a top-level purpose with sub-purposes for "Email Campaigns," "Social Media," and "Event Marketing." The Email Campaigns purpose inherits the base Marketing policies but adds specific controls for email frequency and opt-out management, while all Marketing sub-purposes inherit the requirement for marketing consent from the parent purpose.', 'purpose hierarchy,inheritance,parent-child'),
('Purpose Management', 'Purpose-Based Data Discovery', 'How does purpose-based data discovery work?', 'The platform enables purpose-based data discovery through: (1) Purpose-to-data-asset mappings in the catalog; (2) Purpose-based search and filtering; (3) Automatic identification of relevant datasets for a purpose; (4) Purpose compatibility checking for data usage; (5) Discovery of similar data assets used for the same purpose. For example, a data analyst working on a Customer Churn Analysis project can search for data assets compatible with the "Churn Analysis" purpose, and the platform will show all datasets that are pre-approved for this purpose, along with their access requirements and usage restrictions, enabling the analyst to quickly find appropriate data without risking compliance violations.', 'data discovery,purpose-based search,compatibility'),
('Purpose Management', 'Purpose Attestation', 'How does purpose attestation work in the platform?', 'The platform implements purpose attestation to ensure ongoing legitimacy: (1) Periodic review requirements for active purposes; (2) Attestation workflows for purpose owners; (3) Evidence collection for purpose legitimacy; (4) Impact assessment for high-risk purposes; (5) Automatic expiration of non-attested purposes; (6) Audit trail of attestation history. For example, every six months, the owner of the "Customer Analytics" purpose receives an attestation request requiring them to confirm the purpose is still needed, the legal basis remains valid, the data usage is minimized appropriately, and the controls are effective. This attestation is documented, and if not completed, access based on this purpose may be suspended until review is complete.', 'attestation,periodic review,legitimacy');

-- Regulatory Compliance
INSERT INTO knowledge_base (category, subcategory, question, answer, tags) VALUES
('Regulatory Compliance', 'Regulatory Mapping', 'How does the platform map policies to regulatory requirements?', 'The platform maintains comprehensive regulatory mappings: (1) Regulatory requirement library with structured metadata; (2) Policy-to-regulation mapping matrices; (3) Control-to-requirement traceability; (4) Jurisdictional variations and applicability rules; (5) Regulatory update monitoring and impact assessment; (6) Gap analysis and remediation tracking. For example, a data retention policy for customer information is mapped to GDPR Article 5(1)(e) (storage limitation), CCPA Section 1798.100(e), and internal data minimization standards. When a regulation changes, the platform identifies all affected policies and controls, enabling targeted updates rather than wholesale policy revisions.', 'regulatory mapping,compliance,traceability'),
('Regulatory Compliance', 'Evidence Collection', 'How does the platform support compliance evidence collection?', 'The platform automates evidence collection for compliance: (1) Control effectiveness monitoring with metrics; (2) Policy implementation verification; (3) Access request and approval documentation; (4) Purpose legitimacy evidence; (5) Consent records and preference management; (6) Data subject request fulfillment records; (7) Incident response documentation. For example, for GDPR compliance, the platform automatically collects evidence of consent validity, records of data subject access requests and their fulfillment, documentation of purpose limitation implementation, and logs of data minimization controls in action. This evidence is organized by regulatory requirement and can be quickly assembled for audits or regulatory inquiries.', 'evidence collection,audit support,documentation'),
('Regulatory Compliance', 'Compliance Reporting', 'What compliance reporting capabilities does the platform provide?', 'The platform offers comprehensive compliance reporting: (1) Compliance dashboards with key metrics; (2) Control effectiveness reports; (3) Exception and violation tracking; (4) Regulatory requirement coverage analysis; (5) Audit-ready evidence packages; (6) Risk assessment and remediation status; (7) Trend analysis and benchmarking. For example, a Chief Privacy Officer can generate a GDPR compliance report showing the status of all Article 30 requirements, with metrics on data inventory completeness, purpose documentation, control implementation, third-party transfers, and security measures. The report highlights areas of strong compliance and identifies gaps requiring attention, with drill-down capabilities to specific controls and evidence.', 'compliance reporting,dashboards,metrics'),
('Regulatory Compliance', 'Regulatory Change Management', 'How does the platform handle regulatory changes?', 'The platform manages regulatory changes through: (1) Regulatory intelligence monitoring; (2) Change impact assessment on existing policies and controls; (3) Gap analysis and remediation planning; (4) Policy update workflows; (5) Control modification and testing; (6) Communication and training on changes; (7) Implementation verification and documentation. For example, when the CPRA amended the CCPA with new requirements for sensitive personal information, the platform identified all affected policies and controls, initiated updates to data classification schemes and purpose definitions, modified consent management processes, updated retention policies, and tracked the implementation of these changes across all systems to ensure timely compliance with the new requirements.', 'regulatory change,impact assessment,adaptation');


;

-- =============================================
-- GLOSSARY TABLES
-- =============================================

-- Create Law table
CREATE TABLE IF NOT EXISTS `law` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `scope` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Jurisdiction table
CREATE TABLE IF NOT EXISTS `jurisdiction` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Legal Basis table
CREATE TABLE IF NOT EXISTS `legal_basis` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Data Element table
CREATE TABLE IF NOT EXISTS `data_element` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `default_masking_format` VARCHAR(100) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Update default masking formats for sensitive data elements
UPDATE data_element SET default_masking_format = 'XXXX-XXXX-XXXX-####' WHERE name = 'Credit Card Number';
UPDATE data_element SET default_masking_format = 'XXXXXXXXXXXX####' WHERE name = 'Bank Account Number';
UPDATE data_element SET default_masking_format = 'XXX-XX-XXXX' WHERE name = 'Social Security Number';
UPDATE data_element SET default_masking_format = '****####' WHERE name = 'Phone Number';
UPDATE data_element SET default_masking_format = '****@domain.com' WHERE name = 'Email Address';
UPDATE data_element SET default_masking_format = 'IP: XXX.XXX.XXX.XXX' WHERE name = 'IP Address';
UPDATE data_element SET default_masking_format = 'Device: XXXXXXXX' WHERE name = 'Device ID';

-- Create external_roles table for external system roles
CREATE TABLE IF NOT EXISTS `external_roles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `source_system` VARCHAR(255) NOT NULL,
    `source_role_name` VARCHAR(255) NOT NULL,
    `asset_id` INT,
    UNIQUE(`source_system`, `source_role_name`),
    FOREIGN KEY (`asset_id`) REFERENCES `asset`(`id`)
);

-- Insert sample external roles
INSERT INTO `external_roles` (`name`, `description`, `source_system`, `source_role_name`, `asset_id`) VALUES
('Marketing Analyst', 'Role for marketing data analysis', 'Snowflake', 'MKTG_ANALYST', (SELECT id FROM asset WHERE name = 'Marketing Database')),
('Customer Service Rep', 'Role for customer support', 'Snowflake', 'CUST_SERVICE', (SELECT id FROM asset WHERE name = 'CRM System')),
('Marketing Analyst', 'Role for marketing data analysis', 'Databricks', 'marketing_analyst', (SELECT id FROM asset WHERE name = 'Marketing Database')),
('Data Engineer', 'Role for data pipeline management', 'Databricks', 'data_engineer', (SELECT id FROM asset WHERE name = 'ERP System')),
('HR Admin', 'Role for HR data management', 'AWS', 'hr-admin', (SELECT id FROM asset WHERE name = 'HR Portal')),
('Finance Manager', 'Role for financial data access', 'AWS', 'finance-manager', (SELECT id FROM asset WHERE name = 'Financial System'));

-- Create purpose_role table to map purposes to external roles
CREATE TABLE IF NOT EXISTS `purpose_role` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `purpose_id` INT NOT NULL,
    `external_role_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(`purpose_id`, `external_role_id`),
    FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`),
    FOREIGN KEY (`external_role_id`) REFERENCES `external_roles`(`id`)
);

-- Insert sample purpose-role mappings (will be populated after purposes and external roles are created)
INSERT INTO `purpose_role` (`purpose_id`, `external_role_id`) VALUES
-- Will be populated after the purpose and external_roles tables are populated
(1, 1), -- Marketing Campaigns - Snowflake Marketing Analyst
(1, 3), -- Marketing Campaigns - Databricks Marketing Analyst
(2, 2), -- Customer Support - Snowflake Customer Service Rep
(3, 4), -- Research and Development - Databricks Data Engineer
(4, 5), -- Employee Management - AWS HR Admin
(5, 6); -- Payment Processing - AWS Finance Manager

-- Create Data Subject Type table
CREATE TABLE IF NOT EXISTS `data_subject_type` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Data Category table
CREATE TABLE IF NOT EXISTS `data_category` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Sensitivity table
CREATE TABLE IF NOT EXISTS `sensitivity` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Purpose Category table
CREATE TABLE IF NOT EXISTS `purpose_category` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Breach Type table
CREATE TABLE IF NOT EXISTS `breach_type` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `category` VARCHAR(100),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Risk table
CREATE TABLE IF NOT EXISTS `risk` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `category` VARCHAR(100),
    `likelihood` VARCHAR(50) DEFAULT 'Medium',
    `impact` VARCHAR(50) DEFAULT 'Medium',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =============================================
-- REGULATORY METADATA TABLES
-- =============================================

-- Override table for Data Usage rules based on Role + Purpose + Data Element
CREATE TABLE IF NOT EXISTS policy_override_role_purpose_data_usage (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    policy_purpose_data_element_id INTEGER NOT NULL,
    external_role_id INTEGER NOT NULL, -- Added for role-specific override
    operation VARCHAR(50) NOT NULL,            -- e.g., read, write, share, delete
    allowed BOOLEAN NOT NULL,
    restrictions TEXT,                  -- e.g., justification, conditions
    UNIQUE(policy_purpose_data_element_id, external_role_id, operation),
    FOREIGN KEY (policy_purpose_data_element_id) REFERENCES policy_purpose_data_element(id),
    FOREIGN KEY (external_role_id) REFERENCES external_roles(id)
);

-- Override table for Data Retention rules based on Role + Purpose + Data Element
CREATE TABLE IF NOT EXISTS policy_override_role_purpose_data_retention (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    policy_purpose_data_element_id INTEGER NOT NULL,
    external_role_id INTEGER NOT NULL, -- Added for role-specific override
    retention_period TEXT NOT NULL,     -- e.g., "3 years", "Indefinite", "End of Session"
    retention_basis TEXT,               -- e.g., "Legal requirement", "Business need", "Contractual obligation"
    UNIQUE(policy_purpose_data_element_id, external_role_id),
    FOREIGN KEY (policy_purpose_data_element_id) REFERENCES policy_purpose_data_element(id),
    FOREIGN KEY (external_role_id) REFERENCES external_roles(id)
);

-- Override table for Data Security rules based on Role + Purpose + Data Element
CREATE TABLE IF NOT EXISTS policy_override_role_purpose_data_security (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    policy_purpose_data_element_id INTEGER NOT NULL,
    external_role_id INTEGER NOT NULL, -- Added for role-specific override
    UNIQUE(policy_purpose_data_element_id, external_role_id),
    FOREIGN KEY (policy_purpose_data_element_id) REFERENCES policy_purpose_data_element(id),
    FOREIGN KEY (external_role_id) REFERENCES external_roles(id)
);

-- Create Law Jurisdiction table
CREATE TABLE IF NOT EXISTS `law_jurisdiction` (
    `law_id` INT NOT NULL,
    `jurisdiction_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`law_id`, `jurisdiction_id`),
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`jurisdiction_id`) REFERENCES `jurisdiction`(`id`) ON DELETE CASCADE
);

-- Create Law Legal Basis table
CREATE TABLE IF NOT EXISTS `law_legal_basis` (
    `law_id` INT NOT NULL,
    `legal_basis_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`law_id`, `legal_basis_id`),
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`legal_basis_id`) REFERENCES `legal_basis`(`id`) ON DELETE CASCADE
);

-- Create Law Incident Breach Guidance table
CREATE TABLE IF NOT EXISTS `law_incident_breach_guidance` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `law_id` INT NOT NULL,
    `threshold` TEXT,
    `timeframe` VARCHAR(255),
    `authority` VARCHAR(255),
    `content` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
);

-- Create Data Category Data Element table
CREATE TABLE IF NOT EXISTS `data_category_data_element` (
    `data_category_id` INT NOT NULL,
    `data_element_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`data_category_id`, `data_element_id`),
    FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE
);

-- Create Law Data Subject Type Data Element Sensitivity table
CREATE TABLE IF NOT EXISTS `law_data_subject_type_data_element_sensitivity` (
    `law_id` INT NOT NULL,
    `data_subject_type_id` INT NOT NULL,
    `data_element_id` INT NOT NULL,
    `sensitivity_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`law_id`, `data_subject_type_id`, `data_element_id`, `sensitivity_id`),
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
);

-- Create Law Data Subject Type Data Category Sensitivity table
CREATE TABLE IF NOT EXISTS `law_data_subject_type_data_category_sensitivity` (
    `law_id` INT NOT NULL,
    `data_subject_type_id` INT NOT NULL,
    `data_category_id` INT NOT NULL,
    `sensitivity_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`law_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`),
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
);

-- Create Data Subject Type Data Category Sensitivity table
CREATE TABLE IF NOT EXISTS `data_subject_type_data_category_sensitivity` (
    `data_subject_type_id` INT NOT NULL,
    `data_category_id` INT NOT NULL,
    `sensitivity_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`data_subject_type_id`, `data_category_id`, `sensitivity_id`),
    FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
);

-- Create Data Subject Type Data Element Sensitivity table
CREATE TABLE IF NOT EXISTS `data_subject_type_data_element_sensitivity` (
    `data_subject_type_id` INT NOT NULL,
    `data_element_id` INT NOT NULL,
    `sensitivity_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`data_subject_type_id`, `data_element_id`, `sensitivity_id`),
    FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
);





-- Create Law Transfer table
CREATE TABLE IF NOT EXISTS `law_transfer` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `law_id` INT NOT NULL,
    `adequacy_countries` TEXT,
    `transfer_mechanisms` TEXT,
    `additional_requirements` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
);

-- Create Law Data Subject Access Request Notification Requirements table
CREATE TABLE IF NOT EXISTS `law_data_subject_access_request_notification_requirements` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `law_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `conditions` TEXT,
    `timeframe` VARCHAR(255),
    `exemptions` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
);

-- Create Law Purpose Category Legal Basis table
CREATE TABLE IF NOT EXISTS `law_purpose_category_legal_basis` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `law_id` INT NOT NULL,
    `purpose_category_id` INT NOT NULL,
    `legal_basis_id` INT NOT NULL,
    `preference_order` INT DEFAULT 1,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`purpose_category_id`) REFERENCES `purpose_category`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`legal_basis_id`) REFERENCES `legal_basis`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_law_purpose_legal_basis` (`law_id`, `purpose_category_id`, `legal_basis_id`)
);

-- Create Legal Basis Requirements table
CREATE TABLE IF NOT EXISTS `legal_basis_requirements` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `legal_basis_id` INT NOT NULL,
    `requirement` TEXT NOT NULL,
    FOREIGN KEY (`legal_basis_id`) REFERENCES `legal_basis`(`id`) ON DELETE CASCADE
);

-- Create Data Subject Right Implementation Steps table
CREATE TABLE IF NOT EXISTS `data_subject_right_implementation_steps` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `law_id` INT NOT NULL,
    `right_type` VARCHAR(255) NOT NULL,
    `step_order` INT NOT NULL,
    `description` TEXT NOT NULL,
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_law_right_step` (`law_id`, `right_type`, `step_order`)
);

-- Create Data Subject Right Exemptions table
CREATE TABLE IF NOT EXISTS `data_subject_right_exemptions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `law_id` INT NOT NULL,
    `right_type` VARCHAR(255) NOT NULL,
    `exemption` TEXT NOT NULL,
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
);



-- =============================================
-- SEED GLOSSARY DATA
-- =============================================

-- Seed Law data
INSERT INTO `law` (`name`, `description`, `scope`) VALUES
('GDPR', 'General Data Protection Regulation - A comprehensive data protection law in the EU.', 'Applies to organizations processing personal data of individuals in the EU, regardless of the organization\'s location.'),
('CCPA', 'California Consumer Privacy Act - Enhances privacy rights and consumer protection for residents of California.', 'Applies to for-profit businesses that collect personal information from California residents and meet certain thresholds.'),
('CPRA', 'California Privacy Rights Act - Expands and amends the CCPA, introducing additional privacy protections.', 'Applies to for-profit businesses that collect personal information from California residents and meet certain thresholds.'),
('LGPD', 'Lei Geral de Proteção de Dados - Brazil\'s General Data Protection Law.', 'Applies to any business or organization that processes the personal data of individuals in Brazil, regardless of where the organization is based.'),
('PIPEDA', 'Personal Information Protection and Electronic Documents Act - Canada\'s federal privacy law for private-sector organizations.', 'Applies to private-sector organizations across Canada that collect, use or disclose personal information in the course of commercial activities.');

-- Seed Jurisdiction data
INSERT INTO `jurisdiction` (`name`) VALUES
('European Union'),
('California, USA'),
('Brazil'),
('Canada'),
('United Kingdom'),
('Australia'),
('Japan'),
('South Korea'),
('India'),
('China');

-- Seed Legal Basis data
INSERT INTO `legal_basis` (`name`, `description`) VALUES
('Consent', 'The data subject has given clear consent for processing their personal data for a specific purpose.'),
('Contract', 'Processing is necessary for the performance of a contract with the data subject or to take steps to enter into a contract.'),
('Legal Obligation', 'Processing is necessary for compliance with a legal obligation to which the controller is subject.'),
('Vital Interests', 'Processing is necessary to protect the vital interests of the data subject or another person.'),
('Public Task', 'Processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority.'),
('Legitimate Interests', 'Processing is necessary for the purposes of legitimate interests pursued by the controller or a third party, except where such interests are overridden by the interests or rights of the data subject.');

-- Seed Legal Basis Requirements data
INSERT INTO `legal_basis_requirements` (`legal_basis_id`, `requirement`) VALUES
-- Consent requirements
(1, 'Must be freely given, specific, informed, and unambiguous'),
(1, 'Clear affirmative action required (no pre-ticked boxes)'),
(1, 'Must be as easy to withdraw as to give consent'),
(1, 'Keep records of when and how consent was obtained'),
(1, 'For children, obtain parental/guardian consent where required'),
(1, 'Regular review and refresh of consent may be necessary'),
-- Contract requirements
(2, 'Processing must be necessary for the performance of a contract'),
(2, 'The data subject must be a party to the contract'),
(2, 'Only collect data that is necessary for the contract'),
(2, 'Document the necessity of each data element for the contract'),
-- Legal Obligation requirements
(3, 'Processing must be necessary to comply with a legal obligation'),
(3, 'The legal obligation must be clearly documented'),
(3, 'Only process data specifically required by the legal obligation'),
(3, 'Maintain records of the specific legal requirements'),
-- Vital Interests requirements
(4, 'Processing must be necessary to protect someone\'s life'),
(4, 'Generally only applies in emergency medical situations'),
(4, 'Document why no other legal basis was available'),
(4, 'Switch to another legal basis once the emergency is over'),
-- Public Task requirements
(5, 'Processing must be necessary for a task in the public interest'),
(5, 'Must have a clear basis in law'),
(5, 'Document the specific public interest being served'),
(5, 'Consider if a less intrusive approach is possible'),
-- Legitimate Interest requirements
(6, 'Conduct and document a legitimate interest assessment (LIA)'),
(6, 'Identify a specific legitimate interest'),
(6, 'Ensure processing is necessary for that interest'),
(6, 'Balance your interests against the individual\'s rights'),
(6, 'Provide clear information about the legitimate interest in privacy notices');

-- Seed Data Element data
INSERT INTO `data_element` (`name`, `description`) VALUES
('Full Name', 'An individual\'s complete name including first, middle, and last name.'),
('Name', 'An individual\'s first name, last name, or full name.'),
('Email Address', 'An individual\'s email address used for electronic communication.'),
('Phone Number', 'An individual\'s telephone number used for voice communication.'),
('Address', 'An individual\'s physical address including street, city, state, and postal code.'),
('IP Address', 'A unique identifier assigned to a device connected to a network.'),
('Device ID', 'A unique identifier assigned to a specific device.'),
('Social Security Number', 'A unique identifier assigned to an individual for tax and identification purposes in the United States.'),
('Credit Card Number', 'A unique number assigned to a credit card for payment processing.'),
('Date of Birth', 'An individual\'s date of birth.'),
('Biometric Data', 'Physical or behavioral characteristics that can be used to identify an individual, such as fingerprints or facial recognition data.'),
('Customer ID', 'A unique identifier assigned to a customer within an organization\'s systems.'),
('Purchase History', 'Records of past purchases made by a customer.'),
('Bank Account Number', 'A unique identifier for a customer\'s bank account.');

-- Seed Data Subject Type data
INSERT INTO `data_subject_type` (`name`, `description`) VALUES
('Customer', 'An individual who purchases goods or services from an organization.'),
('Employee', 'An individual who works for an organization under an employment contract.'),
('Contractor', 'An individual who provides services to an organization but is not an employee.'),
('Job Applicant', 'An individual who applies for a job at an organization.'),
('Website Visitor', 'An individual who visits an organization\'s website.'),
('Minor', 'An individual under the age of 18 or the age of majority in their jurisdiction.'),
('Patient', 'An individual receiving medical care or treatment.'),
('Student', 'An individual enrolled in an educational institution.');

-- Seed Data Category data
INSERT INTO `data_category` (`name`, `description`) VALUES
('Personal Identifiers', 'Information that can directly identify an individual, such as name, email address, or phone number.'),
('Financial Information', 'Information related to an individual\'s financial status, such as bank account details, credit card numbers, or income.'),
('Health Information', 'Information related to an individual\'s health status, medical history, or treatment.'),
('Biometric Information', 'Physical or behavioral characteristics that can be used to identify an individual, such as fingerprints or facial recognition data.'),
('Location Data', 'Information about an individual\'s physical location, such as GPS coordinates or IP address geolocation.'),
('Online Activity', 'Information about an individual\'s online behavior, such as browsing history or search queries.'),
('Employment Information', 'Information related to an individual\'s employment, such as job title, salary, or performance reviews.'),
('Education Information', 'Information related to an individual\'s education, such as degrees, grades, or academic records.');

-- Seed Sensitivity data
INSERT INTO `sensitivity` (`name`, `description`) VALUES
('Public', 'Information that is publicly available and poses minimal risk if disclosed.'),
('Internal', 'Information that is intended for internal use within an organization but poses minimal risk if disclosed.'),
('Confidential', 'Information that requires protection and poses moderate risk if disclosed.'),
('Restricted', 'Information that requires strict protection and poses significant risk if disclosed.'),
('Special Category', 'Information that is considered sensitive under data protection laws, such as health data, biometric data, or data revealing racial or ethnic origin.');

-- Seed Purpose Category data
INSERT INTO `purpose_category` (`name`, `description`) VALUES
('Contractual Necessity', 'Processing necessary for the performance of a contract with the data subject'),
('Legal Compliance', 'Processing necessary for compliance with a legal obligation'),
('Vital Interests', 'Processing necessary to protect vital interests of the data subject or another person'),
('Public Interest', 'Processing necessary for the performance of a task carried out in the public interest'),
('Legitimate Business Interests', 'Processing necessary for the legitimate interests pursued by the controller or a third party'),
('Marketing and Advertising', 'Processing for direct marketing, advertising, and promotional activities'),
('Research and Development', 'Processing for scientific, historical research, or statistical purposes'),
('Service Provision', 'Processing necessary to provide the requested service to the data subject'),
('Security and Fraud Prevention', 'Processing for security, fraud detection, prevention, and investigation'),
('Analytics and Improvement', 'Processing for analytics, measurement, and service improvement'),
('Employment Management', 'Processing related to employment, workforce management, and HR functions'),
('Healthcare Provision', 'Processing for healthcare services, treatment, and management');

-- Seed Breach Type data
INSERT INTO `breach_type` (`name`, `description`, `category`) VALUES
-- Cyber Attacks category
('Phishing Attack', 'Cybercriminals impersonate trusted entities to deceive individuals into providing sensitive information such as usernames, passwords, and credit card details.', 'Cyber Attack'),
('Malware Attack', 'Harmful programs such as viruses, spyware, and Trojans that infiltrate systems through infected email attachments, malicious websites, or removable media.', 'Cyber Attack'),
('Ransomware Attack', 'Malware that encrypts a victim''s files, making them inaccessible without a decryption key, followed by a ransom demand for the key.', 'Cyber Attack'),
('SQL Injection', 'Attackers insert malicious SQL code into a database query, allowing them to access, modify, or delete database contents.', 'Cyber Attack'),
('Man-in-the-Middle Attack', 'The attacker intercepts and manipulates communication between two parties without their knowledge.', 'Cyber Attack'),
('Denial of Service (DoS)', 'Attacks that aim to disrupt the normal functioning of a network, service, or website by overwhelming it with a flood of traffic.', 'Cyber Attack'),
('Distributed Denial of Service (DDoS)', 'Similar to DoS but using multiple compromised systems to launch the attack, making it more powerful and harder to mitigate.', 'Cyber Attack'),
('Advanced Persistent Threat (APT)', 'Highly sophisticated and persistent attacks, often conducted by well-funded cybercriminals or nation-states, aiming to infiltrate and control networks for prolonged periods.', 'Cyber Attack'),
('Zero-day Exploit', 'Attacks that exploit previously unknown vulnerabilities in software or hardware before developers have had a chance to create and release patches.', 'Cyber Attack'),
('Credential Stuffing', 'Attackers use stolen account credentials from one service to gain unauthorized access to other services where users have reused the same credentials.', 'Cyber Attack'),
('API Abuse', 'Exploiting vulnerabilities in application programming interfaces to gain unauthorized access to data or functionality.', 'Cyber Attack'),

-- Insider Threats category
('Malicious Insider', 'Data theft or sabotage by a disgruntled employee or contractor with legitimate access to systems and data.', 'Insider Threat'),
('Accidental Exposure', 'Unintentional disclosure of sensitive information by employees through mistakes or negligence.', 'Insider Threat'),
('Privilege Misuse', 'Authorized users accessing data or systems beyond what is necessary for their job functions.', 'Insider Threat'),
('Compromised Insider', 'An employee whose credentials have been stolen or who has been manipulated through social engineering.', 'Insider Threat'),

-- Physical Breaches category
('Device Theft', 'Theft of physical devices such as laptops, smartphones, or storage media containing sensitive data.', 'Physical Breach'),
('Unauthorized Physical Access', 'Gaining unauthorized entry to facilities where sensitive data is stored or processed.', 'Physical Breach'),
('Dumpster Diving', 'Retrieving discarded documents or media containing sensitive information from trash containers.', 'Physical Breach'),
('Tailgating', 'Following an authorized person into a secure area without proper authentication.', 'Physical Breach'),

-- Supply Chain Breaches category
('Third-Party Vendor Breach', 'Security incidents at third-party vendors that compromise data they process or store on behalf of their clients.', 'Supply Chain Breach'),
('Software Supply Chain Attack', 'Compromising software updates or components to distribute malware to target organizations, as seen in the SolarWinds attack.', 'Supply Chain Breach'),
('Hardware Supply Chain Attack', 'Tampering with hardware components during manufacturing or distribution to introduce vulnerabilities or backdoors.', 'Supply Chain Breach');



-- =============================================
-- INVENTORY TABLES
-- =============================================

-- Create Asset table
CREATE TABLE IF NOT EXISTS `asset` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Asset Data Element table
CREATE TABLE IF NOT EXISTS `asset_data_element` (
    `asset_id` INT NOT NULL,
    `data_element_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`asset_id`, `data_element_id`),
    FOREIGN KEY (`asset_id`) REFERENCES `asset`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE
);

-- Create Catalog table for database metadata
CREATE TABLE IF NOT EXISTS `catalog` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `asset_id` INT NOT NULL,
    `schema_name` VARCHAR(255) NOT NULL,
    `table_name` VARCHAR(255) NOT NULL,
    `column_name` VARCHAR(255) NOT NULL,
    `data_type` VARCHAR(100) NOT NULL,
    `data_element_id` INT,
    `sample_data` TEXT,
    `last_scanned` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`asset_id`) REFERENCES `asset`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE SET NULL,
    UNIQUE KEY `unique_column` (`asset_id`, `schema_name`, `table_name`, `column_name`)
);

-- Create Policy Implementation table to track implementation status
CREATE TABLE IF NOT EXISTS `policy_implementation` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `catalog_id` INT NOT NULL,
    `policy_id` INT NOT NULL,
    `is_masked` BOOLEAN DEFAULT FALSE,
    `masking_format` VARCHAR(255),
    `is_encrypted` BOOLEAN DEFAULT FALSE,
    `encryption_algorithm` VARCHAR(255),
    `has_access_control` BOOLEAN DEFAULT FALSE,
    `access_control_type` VARCHAR(255),
    `has_retention_policy` BOOLEAN DEFAULT FALSE,
    `retention_period` VARCHAR(100),
    `has_audit_logging` BOOLEAN DEFAULT FALSE,
    `audit_level` VARCHAR(50),
    `implementation_status` ENUM('Not Implemented', 'Partially Implemented', 'Fully Implemented') DEFAULT 'Not Implemented',
    `last_verified` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`catalog_id`) REFERENCES `catalog`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_policy_implementation` (`catalog_id`, `policy_id`)
);

-- Create Processing Activity table
CREATE TABLE IF NOT EXISTS `processing_activity` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `status` VARCHAR(50),
    `start_date` DATE,
    `end_date` DATE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Processing Activity Purpose table
CREATE TABLE IF NOT EXISTS `processing_activity_purpose` (
    `processing_activity_id` INT NOT NULL,
    `purpose_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`processing_activity_id`, `purpose_id`),
    FOREIGN KEY (`processing_activity_id`) REFERENCES `processing_activity`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`) ON DELETE CASCADE
);

-- Create Processing Activity Asset Data Element table
CREATE TABLE IF NOT EXISTS `processing_activity_asset_data_element` (
    `processing_activity_id` INT NOT NULL,
    `asset_id` INT NOT NULL,
    `data_element_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`processing_activity_id`, `asset_id`, `data_element_id`),
    FOREIGN KEY (`processing_activity_id`) REFERENCES `processing_activity`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`asset_id`) REFERENCES `asset`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE
);

-- Create Data Access Request table
CREATE TABLE IF NOT EXISTS `data_access_request` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `requester_name` VARCHAR(255) NOT NULL,
    `requester_email` VARCHAR(255) NOT NULL,
    `asset_id` INT NOT NULL,
    `asset_name` VARCHAR(255) NOT NULL,
    `tables` TEXT NOT NULL,
    `purposes` TEXT NOT NULL,
    `purpose_ids` TEXT NOT NULL,
    `role_name` VARCHAR(255) NOT NULL,
    `status` ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    `request_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `approval_date` TIMESTAMP NULL,
    `expiry_date` TIMESTAMP NULL,
    `ddl` TEXT NOT NULL,
    `policy_json` TEXT NOT NULL,
    `notes` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`asset_id`) REFERENCES `asset`(`id`) ON DELETE CASCADE
);

-- Seed Asset data
INSERT INTO `asset` (`name`, `description`) VALUES
('CRM System', 'Customer Relationship Management system containing customer data and interactions'),
('ERP System', 'Enterprise Resource Planning system for managing business processes'),
('HR Portal', 'Human Resources portal for employee data management'),
('Marketing Database', 'Database containing customer marketing data and campaign information'),
('Financial System', 'Financial management system containing transaction and payment data');

-- Seed Catalog data
INSERT INTO `catalog` (`asset_id`, `schema_name`, `table_name`, `column_name`, `data_type`, `data_element_id`, `sample_data`) VALUES
-- CRM System
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'customers', 'customer_id', 'INT', (SELECT id FROM data_element WHERE name = 'Customer ID'), '10001'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'customers', 'first_name', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Name'), 'John'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'customers', 'last_name', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Name'), 'Smith'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'customers', 'email', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Email Address'), 'john.smith@example.com'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'customers', 'phone', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Phone Number'), '555-123-4567'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'customers', 'address', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Address'), '123 Main St, Anytown, CA 94001'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'purchases', 'purchase_id', 'INT', NULL, '50001'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'purchases', 'customer_id', 'INT', (SELECT id FROM data_element WHERE name = 'Customer ID'), '10001'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'purchases', 'purchase_date', 'DATE', NULL, '2025-01-15'),
((SELECT id FROM asset WHERE name = 'CRM System'), 'crm', 'purchases', 'amount', 'DECIMAL', (SELECT id FROM data_element WHERE name = 'Purchase History'), '129.99'),

-- HR Portal
((SELECT id FROM asset WHERE name = 'HR Portal'), 'hr', 'employees', 'employee_id', 'INT', NULL, '5001'),
((SELECT id FROM asset WHERE name = 'HR Portal'), 'hr', 'employees', 'first_name', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Name'), 'Jane'),
((SELECT id FROM asset WHERE name = 'HR Portal'), 'hr', 'employees', 'last_name', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Name'), 'Doe'),
((SELECT id FROM asset WHERE name = 'HR Portal'), 'hr', 'employees', 'ssn', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Social Security Number'), 'XXX-XX-1234'),
((SELECT id FROM asset WHERE name = 'HR Portal'), 'hr', 'employees', 'dob', 'DATE', (SELECT id FROM data_element WHERE name = 'Date of Birth'), '1985-06-15'),
((SELECT id FROM asset WHERE name = 'HR Portal'), 'hr', 'employees', 'salary', 'DECIMAL', NULL, '85000.00'),
((SELECT id FROM asset WHERE name = 'HR Portal'), 'hr', 'employees', 'bank_account', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Bank Account Number'), 'XXXX1234'),

-- Financial System
((SELECT id FROM asset WHERE name = 'Financial System'), 'finance', 'transactions', 'transaction_id', 'INT', NULL, '75001'),
((SELECT id FROM asset WHERE name = 'Financial System'), 'finance', 'transactions', 'customer_id', 'INT', (SELECT id FROM data_element WHERE name = 'Customer ID'), '10001'),
((SELECT id FROM asset WHERE name = 'Financial System'), 'finance', 'transactions', 'amount', 'DECIMAL', NULL, '500.00'),
((SELECT id FROM asset WHERE name = 'Financial System'), 'finance', 'transactions', 'transaction_date', 'DATE', NULL, '2025-03-10'),
((SELECT id FROM asset WHERE name = 'Financial System'), 'finance', 'payments', 'payment_id', 'INT', NULL, '30001'),
((SELECT id FROM asset WHERE name = 'Financial System'), 'finance', 'payments', 'credit_card_number', 'VARCHAR', (SELECT id FROM data_element WHERE name = 'Credit Card Number'), 'XXXX-XXXX-XXXX-5678'),
((SELECT id FROM asset WHERE name = 'Financial System'), 'finance', 'payments', 'expiry_date', 'VARCHAR', NULL, '06/28');

-- Seed Asset_Data_Element relationships based on catalog classifications
INSERT IGNORE INTO `asset_data_element` (`asset_id`, `data_element_id`) 
SELECT DISTINCT c.asset_id, c.data_element_id 
FROM catalog c 
WHERE c.data_element_id IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM asset_data_element ade 
    WHERE ade.asset_id = c.asset_id 
    AND ade.data_element_id = c.data_element_id
);

-- Seed Policy Implementation data
INSERT INTO `policy_implementation` (`catalog_id`, `policy_id`, `is_masked`, `masking_format`, `is_encrypted`, `encryption_algorithm`, 
                                   `has_access_control`, `access_control_type`, `has_retention_policy`, `retention_period`, 
                                   `has_audit_logging`, `audit_level`, `implementation_status`) VALUES
-- CRM System - Email Address (Data Security Policy)
((SELECT id FROM catalog WHERE asset_id = (SELECT id FROM asset WHERE name = 'CRM System') AND column_name = 'email'), 
 (SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 TRUE, 'Partial - Show only domain', TRUE, 'AES-256', TRUE, 'Role-based', TRUE, '2 years', TRUE, 'Full', 'Fully Implemented'),

-- CRM System - Phone Number (Data Security Policy)
((SELECT id FROM catalog WHERE asset_id = (SELECT id FROM asset WHERE name = 'CRM System') AND column_name = 'phone'), 
 (SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 TRUE, 'Last 4 digits only', FALSE, NULL, TRUE, 'Role-based', TRUE, '2 years', TRUE, 'Full', 'Partially Implemented'),

-- HR Portal - SSN (Data Security Policy)
((SELECT id FROM catalog WHERE asset_id = (SELECT id FROM asset WHERE name = 'HR Portal') AND column_name = 'ssn'), 
 (SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 TRUE, 'Show only last 4 digits', TRUE, 'AES-256', TRUE, 'Role-based', TRUE, '7 years', TRUE, 'Full', 'Fully Implemented'),

-- HR Portal - Salary (Data Access Control Policy) - Note: salary no longer has a data_element_id
((SELECT id FROM catalog WHERE asset_id = (SELECT id FROM asset WHERE name = 'HR Portal') AND column_name = 'salary'), 
 (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 TRUE, 'Full masking for non-HR', FALSE, NULL, TRUE, 'Role-based', TRUE, '7 years', TRUE, 'Full', 'Partially Implemented'),

-- Financial System - Credit Card Number (Data Security Policy)
((SELECT id FROM catalog WHERE asset_id = (SELECT id FROM asset WHERE name = 'Financial System') AND column_name = 'credit_card_number'), 
 (SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 TRUE, 'Show only last 4 digits', TRUE, 'AES-256', TRUE, 'Role-based', TRUE, '2 years', TRUE, 'Full', 'Fully Implemented');

-- Seed Asset Data Element relationships
INSERT IGNORE INTO `asset_data_element` (`asset_id`, `data_element_id`)
SELECT a.id, de.id
FROM `asset` a, `data_element` de
WHERE 
    (a.name = 'CRM System' AND de.name IN ('Name', 'Email Address', 'Phone Number', 'Address', 'Customer ID', 'Purchase History')) OR
    (a.name = 'ERP System' AND de.name IN ('Name', 'Email Address', 'Customer ID', 'Purchase History')) OR
    (a.name = 'HR Portal' AND de.name IN ('Name', 'Email Address', 'Phone Number', 'Address', 'Date of Birth', 'Social Security Number', 'Bank Account Number')) OR
    (a.name = 'Marketing Platform' AND de.name IN ('Name', 'Email Address', 'Phone Number', 'Customer ID', 'IP Address', 'Device ID')) OR
    (a.name = 'Financial System' AND de.name IN ('Name', 'Customer ID', 'Credit Card Number', 'Bank Account Number'));

-- Seed Processing Activity data
INSERT INTO `processing_activity` (`name`, `description`, `status`, `start_date`, `end_date`) VALUES
('Customer Data Management', 'Managing customer data for account management and support', 'Active', '2025-01-01', NULL),
('Marketing Campaign Analysis', 'Analyzing customer data for targeted marketing campaigns', 'Active', '2025-01-15', NULL),
('Employee Onboarding', 'Processing employee data during the onboarding process', 'Active', '2025-02-01', NULL),
('Financial Transactions Processing', 'Processing financial transaction data for accounting purposes', 'Active', '2025-01-10', NULL),
('Website User Analytics', 'Collecting and analyzing website user behavior data', 'Active', '2025-01-05', NULL),
('Financial Score Prediction', 'Processing financial data to generate AI-based credit scoring models', 'Active', '2025-03-01', NULL);

-- Seed Processing Activity Purpose relationships (one purpose per activity)
INSERT INTO `processing_activity_purpose` (`processing_activity_id`, `purpose_id`)
SELECT pa.id, p.id
FROM `processing_activity` pa, `purpose` p
WHERE 
    (pa.name = 'Customer Data Management' AND p.name = 'Customer Support') OR
    (pa.name = 'Marketing Campaign Analysis' AND p.name = 'Marketing Campaigns') OR
    (pa.name = 'Employee Onboarding' AND p.name = 'Employee Management') OR
    (pa.name = 'Financial Transactions Processing' AND p.name = 'Payment Processing') OR
    (pa.name = 'Website User Analytics' AND p.name = 'Product Analytics') OR
    (pa.name = 'Financial Score Prediction' AND p.name = 'AI Model Generation');

-- Seed Processing Activity Asset Data Element relationships
INSERT INTO `processing_activity_asset_data_element` (`processing_activity_id`, `asset_id`, `data_element_id`)
SELECT pa.id, a.id, de.id
FROM `processing_activity` pa, `asset` a, `data_element` de
WHERE 
    -- Customer Data Management - CRM System - Customer data elements
    (pa.name = 'Customer Data Management' AND a.name = 'CRM System' AND de.name IN ('Full Name', 'Email Address', 'Phone Number', 'Address', 'Customer ID')) OR
    -- Customer Data Management - ERP System - Customer data elements
    (pa.name = 'Customer Data Management' AND a.name = 'ERP System' AND de.name IN ('Full Name', 'Email Address', 'Customer ID')) OR
    -- Marketing Campaign Analysis - Marketing Platform - Customer and behavior data elements
    (pa.name = 'Marketing Campaign Analysis' AND a.name = 'Marketing Platform' AND de.name IN ('Full Name', 'Email Address', 'Customer ID', 'IP Address', 'Device ID')) OR
    -- Employee Onboarding - HR Portal - Employee data elements
    (pa.name = 'Employee Onboarding' AND a.name = 'HR Portal' AND de.name IN ('Full Name', 'Email Address', 'Phone Number', 'Address', 'Date of Birth', 'Social Security Number')) OR
    -- Financial Transactions Processing - Financial Database - Financial data elements
    (pa.name = 'Financial Transactions Processing' AND a.name = 'Financial Database' AND de.name IN ('Full Name', 'Customer ID', 'Credit Card Number', 'Bank Account Number')) OR
    -- Website User Analytics - Marketing Platform - User behavior data elements
    (pa.name = 'Website User Analytics' AND a.name = 'Marketing Platform' AND de.name IN ('IP Address', 'Device ID')) OR
    -- Financial Score Prediction - Financial Database - Financial and personal data elements
    (pa.name = 'Financial Score Prediction' AND a.name = 'Financial Database' AND de.name IN ('Full Name', 'Customer ID', 'Credit Card Number', 'Bank Account Number', 'Date of Birth', 'Address', 'Income'));

-- =============================================
-- SEED REGULATORY METADATA
-- =============================================

-- Seed Law Jurisdiction data
INSERT INTO `law_jurisdiction` (`law_id`, `jurisdiction_id`)
SELECT l.id, j.id
FROM `law` l, `jurisdiction` j
WHERE (l.name = 'GDPR' AND j.name = 'European Union') OR
      (l.name = 'CCPA' AND j.name = 'California, USA') OR
      (l.name = 'CPRA' AND j.name = 'California, USA') OR
      (l.name = 'LGPD' AND j.name = 'Brazil') OR
      (l.name = 'PIPEDA' AND j.name = 'Canada') OR
      (l.name = 'GDPR' AND j.name = 'United Kingdom');

-- Seed Law Legal Basis data
INSERT INTO `law_legal_basis` (`law_id`, `legal_basis_id`)
SELECT l.id, lb.id
FROM `law` l, `legal_basis` lb
WHERE (l.name = 'GDPR' AND lb.name = 'Consent') OR
      (l.name = 'GDPR' AND lb.name = 'Contract') OR
      (l.name = 'GDPR' AND lb.name = 'Legal Obligation') OR
      (l.name = 'GDPR' AND lb.name = 'Vital Interests') OR
      (l.name = 'GDPR' AND lb.name = 'Public Task') OR
      (l.name = 'GDPR' AND lb.name = 'Legitimate Interests') OR
      (l.name = 'CCPA' AND lb.name = 'Consent') OR
      (l.name = 'CCPA' AND lb.name = 'Contract') OR
      (l.name = 'LGPD' AND lb.name = 'Consent') OR
      (l.name = 'LGPD' AND lb.name = 'Legal Obligation') OR
      (l.name = 'LGPD' AND lb.name = 'Legitimate Interests') OR
      (l.name = 'PIPEDA' AND lb.name = 'Consent') OR
      (l.name = 'PIPEDA' AND lb.name = 'Legal Obligation');

-- Seed Law Incident Breach Guidance data
INSERT INTO `law_incident_breach_guidance` (`law_id`, `threshold`, `timeframe`, `authority`, `content`)
SELECT l.id, 
       CASE 
           WHEN l.name = 'GDPR' THEN 'Any breach that poses a risk to the rights and freedoms of individuals'
           WHEN l.name = 'CCPA' THEN 'Unauthorized acquisition of unencrypted personal information'
           WHEN l.name = 'LGPD' THEN 'Security incidents that may result in risk or damage to data subjects'
           WHEN l.name = 'PIPEDA' THEN 'Breach of security safeguards involving personal information that poses a real risk of significant harm'
       END AS threshold,
       CASE 
           WHEN l.name = 'GDPR' THEN '72 hours'
           WHEN l.name = 'CCPA' THEN 'Most expedient time possible'
           WHEN l.name = 'LGPD' THEN 'Reasonable time period'
           WHEN l.name = 'PIPEDA' THEN 'As soon as feasible'
       END AS timeframe,
       CASE 
           WHEN l.name = 'GDPR' THEN 'Supervisory Authority'
           WHEN l.name = 'CCPA' THEN 'California Attorney General'
           WHEN l.name = 'LGPD' THEN 'National Data Protection Authority (ANPD)'
           WHEN l.name = 'PIPEDA' THEN 'Privacy Commissioner of Canada'
       END AS authority,
       CASE 
           WHEN l.name = 'GDPR' THEN 'Under GDPR, organizations must notify the relevant supervisory authority of a personal data breach within 72 hours of becoming aware of it, unless the breach is unlikely to result in a risk to the rights and freedoms of individuals. The notification must include the nature of the breach, categories of data, approximate number of data subjects affected, likely consequences, and measures taken to address the breach.'
           WHEN l.name = 'CCPA' THEN 'The CCPA does not explicitly include breach notification requirements, but California has a separate breach notification law (California Civil Code 1798.82) that requires businesses to notify California residents when their unencrypted personal information was acquired by an unauthorized person.'
           WHEN l.name = 'LGPD' THEN 'Under LGPD, data controllers must report data breaches that may result in risk or damage to data subjects to the ANPD within a reasonable time period. The notification must include a description of the affected data, information about the data subjects involved, security measures used, risks related to the incident, and measures taken to reverse or mitigate the effects of the damage.'
           WHEN l.name = 'PIPEDA' THEN 'Under PIPEDA, organizations must report to the Privacy Commissioner of Canada any breach of security safeguards involving personal information under their control if it is reasonable to believe that the breach creates a real risk of significant harm to an individual. Organizations must also notify affected individuals and keep records of all breaches.'
       END AS content
FROM `law` l
WHERE l.name IN ('GDPR', 'CCPA', 'LGPD', 'PIPEDA');

-- =============================================
-- SEED ADDITIONAL REGULATORY METADATA
-- =============================================

-- Seed Data Category Data Element relationships
INSERT INTO `data_category_data_element` (`data_category_id`, `data_element_id`)
SELECT dc.id, de.id
FROM `data_category` dc, `data_element` de
WHERE 
    (dc.name = 'Personal Identifiers' AND de.name IN ('Name', 'Email Address', 'Phone Number', 'Address', 'Social Security Number')) OR
    (dc.name = 'Financial Information' AND de.name IN ('Credit Card Number')) OR
    (dc.name = 'Biometric Information' AND de.name IN ('Biometric Data')) OR
    (dc.name = 'Location Data' AND de.name IN ('IP Address', 'Address')) OR
    (dc.name = 'Online Activity' AND de.name IN ('IP Address', 'Device ID'));

-- Seed Law Data Subject Type Data Element Sensitivity relationships
INSERT INTO `law_data_subject_type_data_element_sensitivity` (`law_id`, `data_subject_type_id`, `data_element_id`, `sensitivity_id`)
SELECT l.id, dst.id, de.id, s.id
FROM `law` l, `data_subject_type` dst, `data_element` de, `sensitivity` s
WHERE 
    (l.name = 'GDPR' AND dst.name = 'Customer' AND de.name = 'Name' AND s.name = 'Internal') OR
    (l.name = 'GDPR' AND dst.name = 'Customer' AND de.name = 'Email Address' AND s.name = 'Internal') OR
    (l.name = 'GDPR' AND dst.name = 'Customer' AND de.name = 'Credit Card Number' AND s.name = 'Restricted') OR
    (l.name = 'GDPR' AND dst.name = 'Customer' AND de.name = 'Biometric Data' AND s.name = 'Special Category') OR
    (l.name = 'CCPA' AND dst.name = 'Customer' AND de.name = 'Name' AND s.name = 'Internal') OR
    (l.name = 'CCPA' AND dst.name = 'Customer' AND de.name = 'Social Security Number' AND s.name = 'Restricted') OR
    (l.name = 'LGPD' AND dst.name = 'Customer' AND de.name = 'Name' AND s.name = 'Internal') OR
    (l.name = 'PIPEDA' AND dst.name = 'Customer' AND de.name = 'Name' AND s.name = 'Internal');

-- Seed Law Data Subject Type Data Category Sensitivity relationships
INSERT INTO `law_data_subject_type_data_category_sensitivity` (`law_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`)
SELECT l.id, dst.id, dc.id, s.id
FROM `law` l, `data_subject_type` dst, `data_category` dc, `sensitivity` s
WHERE 
    (l.name = 'GDPR' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'GDPR' AND dst.name = 'Customer' AND dc.name = 'Financial Information' AND s.name = 'Restricted') OR
    (l.name = 'GDPR' AND dst.name = 'Customer' AND dc.name = 'Health Information' AND s.name = 'Special Category') OR
    (l.name = 'GDPR' AND dst.name = 'Employee' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'GDPR' AND dst.name = 'Employee' AND dc.name = 'Employment Information' AND s.name = 'Confidential') OR
    (l.name = 'CCPA' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'CCPA' AND dst.name = 'Customer' AND dc.name = 'Financial Information' AND s.name = 'Restricted') OR
    (l.name = 'LGPD' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'PIPEDA' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal');

-- Seed Data Subject Type Data Category Sensitivity relationships
INSERT INTO `data_subject_type_data_category_sensitivity` (`data_subject_type_id`, `data_category_id`, `sensitivity_id`)
SELECT dst.id, dc.id, s.id
FROM `data_subject_type` dst, `data_category` dc, `sensitivity` s
WHERE 
    (dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (dst.name = 'Customer' AND dc.name = 'Financial Information' AND s.name = 'Restricted') OR
    (dst.name = 'Customer' AND dc.name = 'Health Information' AND s.name = 'Special Category') OR
    (dst.name = 'Employee' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (dst.name = 'Employee' AND dc.name = 'Employment Information' AND s.name = 'Confidential') OR
    (dst.name = 'Minor' AND dc.name = 'Personal Identifiers' AND s.name = 'Restricted') OR
    (dst.name = 'Patient' AND dc.name = 'Health Information' AND s.name = 'Special Category') OR
    (dst.name = 'Website Visitor' AND dc.name = 'Online Activity' AND s.name = 'Internal');

-- Seed Data Subject Type Data Element Sensitivity relationships
INSERT INTO `data_subject_type_data_element_sensitivity` (`data_subject_type_id`, `data_element_id`, `sensitivity_id`)
SELECT dst.id, de.id, s.id
FROM `data_subject_type` dst, `data_element` de, `sensitivity` s
WHERE 
    (dst.name = 'Customer' AND de.name = 'Name' AND s.name = 'Internal') OR
    (dst.name = 'Customer' AND de.name = 'Email Address' AND s.name = 'Internal') OR
    (dst.name = 'Customer' AND de.name = 'Credit Card Number' AND s.name = 'Restricted') OR
    (dst.name = 'Customer' AND de.name = 'Social Security Number' AND s.name = 'Restricted') OR
    (dst.name = 'Employee' AND de.name = 'Name' AND s.name = 'Internal') OR
    (dst.name = 'Employee' AND de.name = 'Social Security Number' AND s.name = 'Restricted') OR
    (dst.name = 'Patient' AND de.name = 'Name' AND s.name = 'Confidential') OR
    (dst.name = 'Patient' AND de.name = 'Biometric Data' AND s.name = 'Special Category') OR
    (dst.name = 'Website Visitor' AND de.name = 'IP Address' AND s.name = 'Internal');



-- Seed Law Transfer data
INSERT INTO `law_transfer` (`law_id`, `adequacy_countries`, `transfer_mechanisms`, `additional_requirements`)
SELECT l.id,
       CASE 
           WHEN l.name = 'GDPR' THEN 'Andorra, Argentina, Canada (commercial organizations), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, United Kingdom, Uruguay'
           WHEN l.name = 'LGPD' THEN 'Countries with adequate level of protection as determined by ANPD'
           WHEN l.name = 'PIPEDA' THEN 'Countries with substantially similar legislation'
           ELSE NULL
       END AS adequacy_countries,
       CASE 
           WHEN l.name = 'GDPR' THEN 'Standard Contractual Clauses (SCCs), Binding Corporate Rules (BCRs), Codes of Conduct, Certification Mechanisms'
           WHEN l.name = 'CCPA' THEN 'Service provider contracts'
           WHEN l.name = 'LGPD' THEN 'Standard Contractual Clauses, Binding Corporate Rules, Codes of Conduct, Certification, Specific Contractual Clauses'
           WHEN l.name = 'PIPEDA' THEN 'Contractual or other means'
           ELSE NULL
       END AS transfer_mechanisms,
       CASE 
           WHEN l.name = 'GDPR' THEN 'Transfer Impact Assessment (TIA), Supplementary Measures'
           WHEN l.name = 'LGPD' THEN 'Specific authorization from the ANPD may be required'
           ELSE NULL
       END AS additional_requirements
FROM `law` l
WHERE l.name IN ('GDPR', 'CCPA', 'LGPD', 'PIPEDA');

-- Seed Law Data Subject Access Request Notification Requirements data
INSERT INTO `law_data_subject_access_request_notification_requirements` (`law_id`, `name`, `description`, `conditions`, `timeframe`, `exemptions`)
VALUES
((SELECT id FROM law WHERE name = 'GDPR'), 'Right of Access', 'Data subjects have the right to obtain confirmation as to whether personal data concerning them is being processed, and if so, access to that data.', 'Valid identification may be required to verify the identity of the requestor.', '1 month (can be extended by 2 additional months where necessary)', 'Requests that are manifestly unfounded or excessive; legal prohibitions; adversely affecting rights of others'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Right to Rectification', 'Data subjects have the right to have inaccurate personal data rectified or completed if it is incomplete.', 'Requestor must specify what data is inaccurate and provide correct information.', '1 month (can be extended by 2 additional months where necessary)', 'Requests that are manifestly unfounded or excessive'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Right to Erasure', 'Data subjects have the right to have personal data erased in certain circumstances.', 'Applies when: data is no longer necessary, consent is withdrawn, subject objects, data unlawfully processed, legal obligation.', '1 month (can be extended by 2 additional months where necessary)', 'Legal obligation to keep data; public interest; legal claims'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Right to Know', 'Consumers have the right to request that a business disclose what personal information it collects, uses, shares, or sells.', 'Verifiable consumer request required.', '45 days (can be extended by additional 45 days where necessary)', 'Requests that are manifestly unfounded or excessive; cannot verify identity'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Right to Delete', 'Consumers have the right to request that a business delete personal information about them.', 'Verifiable consumer request required.', '45 days (can be extended by additional 45 days where necessary)', 'Certain business purposes; legal obligations; security purposes'),
((SELECT id FROM law WHERE name = 'LGPD'), 'Right of Access', 'Data subjects have the right to obtain confirmation of the existence of processing and access to their personal data.', 'Valid identification may be required.', 'Immediately (simplified format) or 15 days (complete declaration)', 'Commercial and industrial secrets'),
((SELECT id FROM law WHERE name = 'PIPEDA'), 'Right of Access', 'Individuals have the right to access their personal information held by an organization.', 'Request must be in writing; reasonable assistance must be provided.', '30 days (can be extended where necessary)', 'Legal privilege; confidential commercial information; would reveal third-party information');

-- Seed Law Purpose Category Legal Basis data
-- GDPR mappings
INSERT INTO `law_purpose_category_legal_basis` (`law_id`, `purpose_category_id`, `legal_basis_id`, `preference_order`, `description`)
VALUES
-- Contractual Necessity -> Contract (1), Legitimate Interests (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Contractual Necessity'), (SELECT id FROM legal_basis WHERE name = 'Contract'), 1, 'Primary legal basis for processing necessary for contract performance'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Contractual Necessity'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 2, 'Secondary legal basis if contract performance is not applicable'),

-- Legal Compliance -> Legal Obligation (1)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Legal Compliance'), (SELECT id FROM legal_basis WHERE name = 'Legal Obligation'), 1, 'Processing necessary for compliance with legal obligations'),

-- Vital Interests -> Vital Interests (1), Legitimate Interests (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Vital Interests'), (SELECT id FROM legal_basis WHERE name = 'Vital Interests'), 1, 'Processing necessary to protect vital interests'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Vital Interests'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 2, 'Secondary legal basis if vital interest is not applicable'),

-- Public Interest -> Public Task (1), Legal Obligation (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Public Interest'), (SELECT id FROM legal_basis WHERE name = 'Public Task'), 1, 'Processing necessary for the performance of a task in the public interest'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Public Interest'), (SELECT id FROM legal_basis WHERE name = 'Legal Obligation'), 2, 'Secondary legal basis if public task is not applicable'),

-- Legitimate Business Interests -> Legitimate Interests (1), Consent (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Legitimate Business Interests'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 1, 'Processing necessary for legitimate interests'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Legitimate Business Interests'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 2, 'Secondary legal basis if legitimate interest is not applicable'),

-- Marketing and Advertising -> Consent (1), Legitimate Interests (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Marketing and Advertising'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Primary legal basis for marketing activities'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Marketing and Advertising'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 2, 'Secondary legal basis for existing customers (soft opt-in)'),

-- Research and Development -> Legitimate Interests (1), Consent (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Research and Development'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 1, 'Primary legal basis for research activities'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Research and Development'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 2, 'Secondary legal basis for research involving special categories of data'),

-- Service Provision -> Contract (1), Legitimate Interests (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Service Provision'), (SELECT id FROM legal_basis WHERE name = 'Contract'), 1, 'Primary legal basis for service provision'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Service Provision'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 2, 'Secondary legal basis if contract is not applicable'),

-- Security and Fraud Prevention -> Legitimate Interests (1), Legal Obligation (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Security and Fraud Prevention'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 1, 'Primary legal basis for security and fraud prevention'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Security and Fraud Prevention'), (SELECT id FROM legal_basis WHERE name = 'Legal Obligation'), 2, 'Secondary legal basis if required by law'),

-- Analytics and Improvement -> Legitimate Interests (1), Consent (2)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Analytics and Improvement'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 1, 'Primary legal basis for analytics and improvement'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Analytics and Improvement'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 2, 'Secondary legal basis if legitimate interest is not applicable'),

-- Employment Management -> Contract (1), Legal Obligation (2), Legitimate Interests (3)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Employment Management'), (SELECT id FROM legal_basis WHERE name = 'Contract'), 1, 'Primary legal basis for employment management'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Employment Management'), (SELECT id FROM legal_basis WHERE name = 'Legal Obligation'), 2, 'Secondary legal basis for legal requirements'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Employment Management'), (SELECT id FROM legal_basis WHERE name = 'Legitimate Interests'), 3, 'Tertiary legal basis for legitimate employer interests'),

-- Healthcare Provision -> Vital Interests (1), Legal Obligation (2), Consent (3)
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Healthcare Provision'), (SELECT id FROM legal_basis WHERE name = 'Vital Interests'), 1, 'Primary legal basis for emergency healthcare'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Healthcare Provision'), (SELECT id FROM legal_basis WHERE name = 'Legal Obligation'), 2, 'Secondary legal basis for legal requirements'),
((SELECT id FROM law WHERE name = 'GDPR'), (SELECT id FROM purpose_category WHERE name = 'Healthcare Provision'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 3, 'Tertiary legal basis for non-emergency healthcare');

-- CCPA mappings
INSERT INTO `law_purpose_category_legal_basis` (`law_id`, `purpose_category_id`, `legal_basis_id`, `preference_order`, `description`)
VALUES
-- For CCPA, most processing is allowed with notice, but consent (opt-out) is required for certain activities
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Contractual Necessity'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Legal Compliance'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Vital Interests'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Public Interest'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Legitimate Business Interests'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Marketing and Advertising'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Research and Development'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Service Provision'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Security and Fraud Prevention'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Analytics and Improvement'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Employment Management'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance'),
((SELECT id FROM law WHERE name = 'CCPA'), (SELECT id FROM purpose_category WHERE name = 'Healthcare Provision'), (SELECT id FROM legal_basis WHERE name = 'Consent'), 1, 'Opt-out consent required for CCPA compliance');

-- =============================================
-- SEED DATA SUBJECT RIGHTS IMPLEMENTATION STEPS
-- =============================================

-- Insert implementation steps for GDPR Access right
INSERT INTO `data_subject_right_implementation_steps` (`law_id`, `right_type`, `step_order`, `description`) VALUES
-- GDPR Access right steps
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 1, 'Confirm receipt of the request within 3 business days'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 2, 'Verify the identity of the requestor'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 3, 'Search all relevant systems and databases for personal data'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 4, 'Compile the information in a clear, accessible format'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 5, 'Include information about processing purposes, categories of data, recipients, retention periods, and other rights'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 6, 'Review for third-party data or exemptions before disclosure'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 7, 'Provide the response securely to the data subject'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 8, 'Document the fulfillment of the request'),

-- GDPR Erasure right steps
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 1, 'Confirm receipt of the request within 3 business days'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 2, 'Verify the identity of the requestor'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 3, 'Determine if one of the grounds for erasure applies'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 4, 'Identify all systems and databases containing the data'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 5, 'Check for any legal basis to retain certain data'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 6, 'Implement technical erasure in all systems'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 7, 'Notify third parties of the erasure request where data has been shared'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 8, 'Provide confirmation of erasure to the data subject'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 9, 'Document the fulfillment of the request'),

-- CCPA Access right steps
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 1, 'Confirm receipt of the request within 10 business days'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 2, 'Verify the identity of the requestor'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 3, 'Search all relevant systems for personal information collected in the past 12 months'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 4, 'Compile the information in a readily usable format'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 5, 'Include categories of sources, business purpose, and third parties shared with'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 6, 'Provide two or more designated methods for submitting requests'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 7, 'Deliver the information free of charge'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 8, 'Document the fulfillment of the request'),

-- CCPA Deletion right steps
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 1, 'Confirm receipt of the request within 10 business days'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 2, 'Verify the identity of the requestor'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 3, 'Identify all systems and databases containing the consumer\'s personal information'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 4, 'Check for any exceptions that allow retention'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 5, 'Delete the personal information from your records'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 6, 'Direct service providers to delete the consumer\'s personal information'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 7, 'Notify the consumer that their request has been fulfilled'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 8, 'Document the deletion process and maintain records');

-- =============================================
-- CONSENT MANAGEMENT TABLES
-- =============================================

-- Drop existing consent tables if they exist
DROP TABLE IF EXISTS consent_record;
DROP TABLE IF EXISTS consent_profile;

-- Create consent_profile table to store user profiles
CREATE TABLE IF NOT EXISTS `consent_profile` (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `user_id` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(`email`),
    UNIQUE(`user_id`)
);

-- Create consent_record table to map users to purposes with their consent status
CREATE TABLE IF NOT EXISTS `consent_record` (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `consent_profile_id` INTEGER NOT NULL,
    `purpose_id` INTEGER NOT NULL,
    `status` ENUM('granted', 'denied', 'withdrawn', 'expired') NOT NULL,
    `consent_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `expiry_date` TIMESTAMP NULL,
    `proof_of_consent` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(`consent_profile_id`, `purpose_id`),
    FOREIGN KEY (`consent_profile_id`) REFERENCES `consent_profile`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`) ON DELETE CASCADE
);

-- =============================================
-- SEED DATA SUBJECT RIGHTS EXEMPTIONS
-- =============================================

INSERT INTO `data_subject_right_exemptions` (`law_id`, `right_type`, `exemption`) VALUES
-- GDPR Access right exemptions
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 'Information protected by legal professional privilege'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 'Confidential references'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 'Management forecasting or planning if disclosure would prejudice the business'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 'Negotiations with the data subject if disclosure would prejudice those negotiations'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Access', 'Third-party data where disclosure would breach confidentiality'),

-- GDPR Erasure right exemptions
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 'Legal obligation to retain the data'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 'Public interest in public health'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 'Archiving purposes in the public interest'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 'Establishment, exercise, or defense of legal claims'),
((SELECT id FROM law WHERE name = 'GDPR'), 'Erasure', 'Freedom of expression and information'),

-- CCPA Access right exemptions
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 'Cannot provide specific pieces of information if disclosure creates substantial security risk'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 'Not required to provide access more than twice in a 12-month period'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 'Certain business-to-business communications'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Access', 'Certain employee data until January 1, 2023'),

-- CCPA Deletion right exemptions
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 'Complete a transaction, provide a good or service requested by the consumer'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 'Detect security incidents or protect against malicious activities'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 'Debug to identify and repair errors'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 'Exercise free speech or ensure another consumer\'s right to exercise free speech'),
((SELECT id FROM law WHERE name = 'CCPA'), 'Erasure', 'Comply with legal obligations');

-- Seed consent_profile data
INSERT INTO `consent_profile` (`email`, `name`, `user_id`) VALUES
('john.doe@example.com', 'John Doe', 'user123'),
('jane.smith@example.com', 'Jane Smith', 'user456'),
('bob.johnson@example.com', 'Bob Johnson', 'user789'),
('alice.williams@example.com', 'Alice Williams', 'user101'),
('charlie.brown@example.com', 'Charlie Brown', 'user202'),
('diana.prince@example.com', 'Diana Prince', 'user303'),
('edward.stark@example.com', 'Edward Stark', 'user404'),
('fiona.gallagher@example.com', 'Fiona Gallagher', 'user505'),
('george.wilson@example.com', 'George Wilson', 'user606'),
('hannah.montana@example.com', 'Hannah Montana', 'user707');

-- Seed consent_record data for Marketing Campaigns purpose
INSERT INTO `consent_record` (`consent_profile_id`, `purpose_id`, `status`, `expiry_date`, `proof_of_consent`) VALUES
((SELECT id FROM consent_profile WHERE email = 'john.doe@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 YEAR), 'Consent granted via web form on 2025-01-15'),

((SELECT id FROM consent_profile WHERE email = 'jane.smith@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 YEAR), 'Consent granted via web form on 2025-01-16'),

((SELECT id FROM consent_profile WHERE email = 'bob.johnson@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'), 
 'denied', NULL, 'Consent denied via web form on 2025-01-17'),

((SELECT id FROM consent_profile WHERE email = 'alice.williams@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 YEAR), 'Consent granted via web form on 2025-01-18'),

((SELECT id FROM consent_profile WHERE email = 'charlie.brown@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'), 
 'withdrawn', NULL, 'Consent withdrawn via email on 2025-01-19');

-- Seed consent_record data for Customer Support purpose
INSERT INTO `consent_record` (`consent_profile_id`, `purpose_id`, `status`, `expiry_date`, `proof_of_consent`) VALUES
((SELECT id FROM consent_profile WHERE email = 'john.doe@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 2 YEAR), 'Consent granted via web form on 2025-01-15'),

((SELECT id FROM consent_profile WHERE email = 'jane.smith@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 2 YEAR), 'Consent granted via web form on 2025-01-16'),

((SELECT id FROM consent_profile WHERE email = 'bob.johnson@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 2 YEAR), 'Consent granted via web form on 2025-01-17'),

((SELECT id FROM consent_profile WHERE email = 'diana.prince@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 2 YEAR), 'Consent granted via web form on 2025-01-20'),

((SELECT id FROM consent_profile WHERE email = 'edward.stark@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 2 YEAR), 'Consent granted via web form on 2025-01-21');

-- Seed consent_record data for Product Analytics purpose
INSERT INTO `consent_record` (`consent_profile_id`, `purpose_id`, `status`, `expiry_date`, `proof_of_consent`) VALUES
((SELECT id FROM consent_profile WHERE email = 'john.doe@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 YEAR), 'Consent granted via web form on 2025-01-15'),

((SELECT id FROM consent_profile WHERE email = 'fiona.gallagher@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 YEAR), 'Consent granted via web form on 2025-01-22'),

((SELECT id FROM consent_profile WHERE email = 'george.wilson@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 YEAR), 'Consent granted via web form on 2025-01-23'),

((SELECT id FROM consent_profile WHERE email = 'hannah.montana@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'), 
 'denied', NULL, 'Consent denied via web form on 2025-01-24');

-- Seed consent_record data for Payment Processing purpose
INSERT INTO `consent_record` (`consent_profile_id`, `purpose_id`, `status`, `expiry_date`, `proof_of_consent`) VALUES
((SELECT id FROM consent_profile WHERE email = 'john.doe@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 3 YEAR), 'Consent granted via web form on 2025-01-15'),

((SELECT id FROM consent_profile WHERE email = 'jane.smith@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 3 YEAR), 'Consent granted via web form on 2025-01-16'),

((SELECT id FROM consent_profile WHERE email = 'alice.williams@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 3 YEAR), 'Consent granted via web form on 2025-01-18'),

((SELECT id FROM consent_profile WHERE email = 'diana.prince@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 3 YEAR), 'Consent granted via web form on 2025-01-20'),

((SELECT id FROM consent_profile WHERE email = 'george.wilson@example.com'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'), 
 'granted', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 3 YEAR), 'Consent granted via web form on 2025-01-23');

-- =============================================
-- POLICY INFERENCE API TABLES
-- =============================================

-- Create Policy table
CREATE TABLE IF NOT EXISTS `policy` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `policy_type` VARCHAR(100),
    `status` VARCHAR(50),
    `effective_date` DATE,
    `expiration_date` DATE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Purpose table
CREATE TABLE IF NOT EXISTS `purpose` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `purpose_category_id` INT,
    `risk_level` VARCHAR(50),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`purpose_category_id`) REFERENCES `purpose_category`(`id`) ON DELETE SET NULL
);

-- Create Framework table
CREATE TABLE IF NOT EXISTS `framework` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `version` VARCHAR(50),
    `category` VARCHAR(100),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Control table
CREATE TABLE IF NOT EXISTS `control` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `control_type` VARCHAR(100),
    `implementation_status` VARCHAR(50),
    `priority` VARCHAR(50),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Framework data
INSERT INTO `framework` (`name`, `description`, `version`, `category`) VALUES
('NIST CSF', 'The NIST Cybersecurity Framework provides a policy framework of computer security guidance for how organizations can assess and improve their ability to prevent, detect, and respond to cyber attacks.', '1.1', 'Security'),
('ISO 27001', 'ISO/IEC 27001 is an international standard on how to manage information security. It details requirements for establishing, implementing, maintaining and continually improving an information security management system (ISMS).', '2013', 'Security'),
('GDPR Controls', 'A set of controls derived from the General Data Protection Regulation (GDPR) requirements to ensure compliance with EU data protection law.', '2018', 'Privacy'),
('PCI DSS', 'The Payment Card Industry Data Security Standard (PCI DSS) is an information security standard for organizations that handle branded credit cards from the major card schemes.', '3.2.1', 'Industry-Specific'),
('HIPAA Security Rule', 'The HIPAA Security Rule establishes national standards to protect individuals\'s electronic personal health information that is created, received, used, or maintained by a covered entity.', '2003', 'Healthcare');

-- Seed Control data
INSERT INTO `control` (`name`, `description`, `control_type`, `implementation_status`, `priority`) VALUES
('Access Control', 'Implement role-based access controls to limit access to personal data based on business need-to-know', 'Technical', 'Implemented', 'High'),
('Data Encryption', 'Encrypt sensitive personal data both at rest and in transit using industry-standard encryption algorithms', 'Technical', 'Implemented', 'High'),
('Data Minimization', 'Collect and retain only the minimum amount of personal data necessary for the specified purpose', 'Administrative', 'Partially Implemented', 'Medium'),
('Audit Logging', 'Maintain detailed logs of all access to and modifications of personal data', 'Technical', 'Implemented', 'Medium'),
('Privacy Impact Assessment', 'Conduct privacy impact assessments for new processing activities or significant changes to existing ones', 'Administrative', 'Implemented', 'High'),
('Data Subject Rights Management', 'Implement processes to handle data subject rights requests (access, deletion, portability, etc.)', 'Administrative', 'Implemented', 'High'),
('Consent Management', 'Implement mechanisms to obtain, record, and manage valid consent for data processing activities', 'Administrative', 'Implemented', 'High'),
('Security Awareness Training', 'Provide regular security and privacy awareness training to all employees', 'Administrative', 'Implemented', 'Medium'),
('Vulnerability Management', 'Regularly scan for and remediate security vulnerabilities in systems processing personal data', 'Technical', 'Implemented', 'High'),
('Incident Response Plan', 'Develop and maintain an incident response plan for data breaches and security incidents', 'Administrative', 'Implemented', 'High'),
('Data Loss Prevention', 'Implement technical controls to prevent unauthorized exfiltration of sensitive data', 'Technical', 'Partially Implemented', 'High'),
('Multi-Factor Authentication', 'Require multiple forms of authentication for access to systems containing sensitive data', 'Technical', 'Implemented', 'High'),
('Network Segmentation', 'Segment networks to isolate systems processing sensitive data from the general network', 'Technical', 'Partially Implemented', 'Medium'),
('Data Backup', 'Regularly backup data and test restoration procedures', 'Technical', 'Implemented', 'Medium'),
('Disaster Recovery', 'Develop and maintain a disaster recovery plan for systems processing personal data', 'Administrative', 'Implemented', 'Medium');

-- Create Policy Purpose table
CREATE TABLE IF NOT EXISTS `policy_purpose` (
    `policy_id` INT NOT NULL,
    `purpose_id` INT NOT NULL,
    PRIMARY KEY (`policy_id`, `purpose_id`),
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`) ON DELETE CASCADE
);

-- Create Policy Purpose Data Element table
CREATE TABLE IF NOT EXISTS `policy_purpose_data_element` (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `policy_id` INTEGER NOT NULL,
    `purpose_id` INTEGER NOT NULL,
    `data_element_id` INTEGER NOT NULL,
    UNIQUE(`policy_id`, `purpose_id`, `data_element_id`),
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`),
    FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`),
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`)
);

-- Create Policy Data Element Usage table for default usage policies
CREATE TABLE IF NOT EXISTS `policy_data_element_usage` (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `policy_id` INTEGER NOT NULL,
    `data_element_id` INTEGER NOT NULL,
    `operation` VARCHAR(50) NOT NULL,
    `allowed` BOOLEAN NOT NULL,
    `restrictions` TEXT,
    UNIQUE(`policy_id`, `data_element_id`, `operation`),
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`),
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`)
);

-- Create Policy Data Element Retention table for default retention policies
CREATE TABLE IF NOT EXISTS `policy_data_element_retention` (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `policy_id` INTEGER NOT NULL,
    `data_element_id` INTEGER NOT NULL,
    `retention_period` TEXT NOT NULL,
    `retention_basis` TEXT,
    `exceptions` TEXT,
    UNIQUE(`policy_id`, `data_element_id`),
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`),
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`)
);

-- Create Policy Data Element Security table for default security policies
CREATE TABLE IF NOT EXISTS `policy_data_element_security` (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `policy_id` INTEGER NOT NULL,
    `data_element_id` INTEGER NOT NULL,
    `requires_encryption` BOOLEAN NOT NULL DEFAULT FALSE,
    `encryption_algorithm` TEXT,
    `requires_masking` BOOLEAN NOT NULL DEFAULT FALSE,
    `masking_format` TEXT,
    `requires_access_control` BOOLEAN NOT NULL DEFAULT FALSE,
    `access_control_type` TEXT,
    UNIQUE(`policy_id`, `data_element_id`),
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`),
    FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`)
);

-- Create Policy Purpose Data Usage table
CREATE TABLE IF NOT EXISTS `policy_purpose_data_usage` (
    `policy_purpose_data_element_id` INT NOT NULL,
    `operation` VARCHAR(50) NOT NULL,
    `allowed` BOOLEAN NOT NULL DEFAULT FALSE,
    `restrictions` TEXT,
    PRIMARY KEY (`policy_purpose_data_element_id`, `operation`),
    FOREIGN KEY (`policy_purpose_data_element_id`) REFERENCES `policy_purpose_data_element`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `policy_purpose_data_retention` (
    `policy_purpose_data_element_id` INT NOT NULL,
    `retention_period` VARCHAR(100) NOT NULL,
    `retention_trigger` VARCHAR(100) NOT NULL DEFAULT 'Collection',
    `retention_basis` VARCHAR(255),
    `exceptions` TEXT,
    PRIMARY KEY (`policy_purpose_data_element_id`),
    FOREIGN KEY (`policy_purpose_data_element_id`) REFERENCES `policy_purpose_data_element`(`id`) ON DELETE CASCADE
);

-- Insert policies
INSERT INTO policy (name, description, policy_type, status, effective_date) VALUES
('Data Access Control Policy', 'Defines rules for accessing data based on purpose limitation principles', 'Access Control', 'Active', '2025-01-01'),
('Data Retention Policy', 'Defines how long data should be retained based on purpose and legal requirements', 'Retention', 'Active', '2025-01-01'),
('Data Sharing Policy', 'Defines rules for sharing data with third parties', 'Sharing', 'Active', '2025-01-01'),
('Data Minimization Policy', 'Ensures only necessary data is collected and processed', 'Collection', 'Active', '2025-01-01'),
('Data Security Policy', 'Defines security controls for protecting data', 'Security', 'Active', '2025-01-01');

-- Insert purposes (after purpose categories are created)
INSERT INTO purpose (name, description, purpose_category_id, risk_level) VALUES
('Customer Support', 'Providing assistance and support to customers', (SELECT id FROM purpose_category WHERE name = 'Customer Service'), 'Low'),
('Fraud Detection', 'Identifying and preventing fraudulent activities', (SELECT id FROM purpose_category WHERE name = 'Security'), 'Medium'),
('Marketing Campaigns', 'Promoting products and services to customers', (SELECT id FROM purpose_category WHERE name = 'Marketing'), 'Medium'),
('Product Analytics', 'Analyzing product usage for improvement', (SELECT id FROM purpose_category WHERE name = 'Analytics'), 'Medium'),
('User Authentication', 'Verifying user identity for access control', (SELECT id FROM purpose_category WHERE name = 'Security'), 'High'),
('Regulatory Compliance', 'Meeting legal and regulatory requirements', (SELECT id FROM purpose_category WHERE name = 'Legal'), 'High'),
('Payment Processing', 'Processing financial transactions', (SELECT id FROM purpose_category WHERE name = 'Financial'), 'High'),
('Service Delivery', 'Providing core services to users', (SELECT id FROM purpose_category WHERE name = 'Operations'), 'Medium'),
('Research and Development', 'Developing new products and features', (SELECT id FROM purpose_category WHERE name = 'Product Development'), 'Medium'),
('Employee Management', 'Managing employee data and performance', (SELECT id FROM purpose_category WHERE name = 'HR'), 'Medium'),
('Default Role Assignment', 'Default purpose for newly created roles with baseline policies', (SELECT id FROM purpose_category WHERE name = 'Operations'), 'Medium');

-- Insert policy-purpose relationships
INSERT INTO policy_purpose (policy_id, purpose_id) VALUES
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Customer Support')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Fraud Detection')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Marketing Campaigns')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Product Analytics')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'User Authentication')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Regulatory Compliance')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Payment Processing')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Service Delivery')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Research and Development')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Employee Management')),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM purpose WHERE name = 'Default Role Assignment')),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM purpose WHERE name = 'Default Role Assignment')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Default Role Assignment'));

-- Insert policy-purpose-data element relationships for all purposes
INSERT INTO policy_purpose_data_element (policy_id, purpose_id, data_element_id, access_allowed) VALUES

-- Default Role Assignment purpose with all data elements for Data Access Control Policy
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Date of Birth'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Biometric Data'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Bank Account Number'), TRUE),

-- Default Role Assignment purpose with all data elements for Data Retention Policy
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Date of Birth'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Biometric Data'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Bank Account Number'), TRUE),

-- Default Role Assignment purpose with all data elements for Data Security Policy
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Date of Birth'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Biometric Data'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Default Role Assignment'),
 (SELECT id FROM data_element WHERE name = 'Bank Account Number'), TRUE),

-- Original policy-purpose-data element relationships

-- Customer Support purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), FALSE),

-- Marketing Campaigns purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), FALSE),

-- Payment Processing purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Bank Account Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), FALSE),

-- Product Analytics purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), FALSE),

-- Employee Management purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Date of Birth'), TRUE),

-- Fraud Detection purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), FALSE),

-- User Authentication purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), FALSE),

-- Regulatory Compliance purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Regulatory Compliance'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Regulatory Compliance'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Regulatory Compliance'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Regulatory Compliance'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Regulatory Compliance'),
 (SELECT id FROM data_element WHERE name = 'Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Regulatory Compliance'),
 (SELECT id FROM data_element WHERE name = 'Date of Birth'), TRUE),

-- Service Delivery purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), FALSE),

-- Research and Development purpose
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), FALSE),

((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), FALSE);

-- Insert policy-purpose-data usage rules for all purposes
INSERT INTO policy_purpose_data_usage (policy_purpose_data_element_id, operation, allowed, restrictions) VALUES

-- Default Role Assignment purpose
-- Full Name
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'write', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'share', TRUE, 'Only with authorized parties'),

-- Name
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Name')), 'write', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Name')), 'share', TRUE, 'Only with authorized parties'),

-- Email Address
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'write', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'share', TRUE, 'Only with authorized parties'),

-- Phone Number
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), 'write', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), 'share', TRUE, 'Only with authorized parties'),

-- Address
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Address')), 'write', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Address')), 'share', TRUE, 'Only with authorized parties'),

-- Sensitive data elements with more restrictive defaults
-- Social Security Number
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'read', TRUE, 'Only for identity verification'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'write', TRUE, 'Only for initial collection'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'share', FALSE, NULL),

-- Credit Card Number
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), 'read', TRUE, 'Only for payment processing'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), 'write', TRUE, 'Only for initial collection'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), 'share', FALSE, NULL),

-- Bank Account Number
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Bank Account Number')), 'read', TRUE, 'Only for payment processing'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Bank Account Number')), 'write', TRUE, 'Only for initial collection'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Bank Account Number')), 'share', FALSE, NULL),

-- Customer Support purpose
-- Customer Support purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), 'read', TRUE, 'Limited to last 12 months of purchases'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'write', TRUE, 'Only for updating customer contact information'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), 'write', TRUE, 'Only for updating customer contact information'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'share', FALSE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), 'share', FALSE, NULL),

-- Marketing Campaigns purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), 'read', TRUE, 'Limited to product categories only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'write', TRUE, 'Only for campaign tracking'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'share', TRUE, 'Only with approved marketing partners'),

-- Payment Processing purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), 'read', TRUE, 'Last 4 digits only except during transaction processing'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Bank Account Number')), 'read', TRUE, 'Last 4 digits only except during transaction processing'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), 'write', TRUE, 'Only during transaction processing'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), 'share', TRUE, 'Only with payment processors'),

-- Product Analytics purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, 'Anonymized where possible'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), 'read', TRUE, 'Aggregated data only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), 'read', TRUE, 'Truncated for anonymization'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), 'read', TRUE, 'Hashed for anonymization'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), 'write', TRUE, 'For analytics tracking only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), 'share', FALSE, NULL),

-- Employee Management purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'read', TRUE, 'HR department only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Date of Birth')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'write', TRUE, 'HR department only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'write', TRUE, 'HR department only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'share', TRUE, 'Only for tax and legal compliance'),

-- Fraud Detection purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), 'write', TRUE, 'For fraud detection logs only'),

-- User Authentication purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'User Authentication') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'User Authentication') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'User Authentication') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'User Authentication') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'User Authentication') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'write', TRUE, 'Only for authentication logs'),

-- Regulatory Compliance purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Regulatory Compliance') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Regulatory Compliance') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Regulatory Compliance') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Regulatory Compliance') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'read', TRUE, 'Only for required regulatory reporting'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Regulatory Compliance') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'share', TRUE, 'Only with authorized regulatory bodies'),

-- Service Delivery purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Address')), 'read', TRUE, NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), 'write', TRUE, 'Only for service-related communications'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Address')), 'share', TRUE, 'Only with delivery partners'),

-- Research and Development purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Research and Development') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), 'read', TRUE, 'Anonymized data only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Research and Development') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), 'read', TRUE, 'Anonymized data only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Research and Development') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), 'read', TRUE, 'Anonymized data only'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Access Control Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Research and Development') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), 'read', TRUE, 'Anonymized data only');

-- Insert policy_purpose_data_element entries for Data Retention Policy
INSERT INTO policy_purpose_data_element (policy_id, purpose_id, data_element_id, access_allowed) VALUES
-- Customer Support purpose
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Phone Number'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),

-- Marketing Campaigns purpose
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

-- Fraud Detection purpose
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

-- Payment Processing purpose
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Bank Account Number'), TRUE),

-- Product Analytics purpose
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),

-- Employee Management purpose
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE);

-- Insert policy-purpose-data retention rules
INSERT INTO policy_purpose_data_retention (policy_purpose_data_element_id, retention_period, retention_trigger, retention_basis, exceptions) VALUES
-- Customer Support purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), '2 years', 'Last Interaction', 'Customer service quality', NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), '2 years', 'Last Interaction', 'Customer service quality', NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), '2 years', 'Last Interaction', 'Customer service quality', NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), '2 years', 'Last Interaction', 'Customer service quality', 'Retain longer if required for warranty purposes'),

-- Marketing Campaigns purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), '1 year', 'Campaign End', 'Marketing effectiveness', NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), '1 year', 'Campaign End', 'Marketing effectiveness', NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), '1 year', 'Campaign End', 'Marketing effectiveness', NULL),

-- Fraud Detection purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), '5 years', 'Incident Resolution', 'Legal requirement', 'Required for fraud investigation purposes'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), '5 years', 'Incident Resolution', 'Legal requirement', 'Required for fraud investigation purposes'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), '5 years', 'Incident Resolution', 'Legal requirement', 'Required for fraud investigation purposes'),

-- Payment Processing purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), '7 years', 'Transaction Completion', 'Financial regulations', NULL),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), 'Minimum required', 'Purpose Fulfillment', 'Data minimization principle', 'Retain longer only if required by law'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Bank Account Number')), 'Minimum required', 'Purpose Fulfillment', 'Data minimization principle', 'Retain longer only if required by law'),

-- Product Analytics purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), '90 days', 'Collection', 'Business need', 'Anonymized after 30 days'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), '90 days', 'Collection', 'Business need', 'Anonymized after 30 days'),

-- Employee Management purpose
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), '7 years', 'Employment End', 'Employment regulations', 'Retain longer if required by law'),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Retention Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), 'Minimum required', 'Purpose Fulfillment', 'Data minimization principle', 'Retain longer only if required by law');

-- =============================================
-- REGULATORY INTELLIGENCE TABLES
-- =============================================

-- Create Obligation table
CREATE TABLE IF NOT EXISTS `obligation` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `source` VARCHAR(255),
    `control_type` VARCHAR(100),
    `status` VARCHAR(50) DEFAULT 'Open',
    `policy_id` INT NULL,
    `risk_accepted` BOOLEAN DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE SET NULL
);

-- Create Sensitivity Obligation mapping table
CREATE TABLE IF NOT EXISTS `sensitivity_obligation` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `sensitivity_id` INT NOT NULL,
    `obligation_id` INT NOT NULL,
    `priority` INT DEFAULT 5,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`obligation_id`) REFERENCES `obligation`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_sensitivity_obligation` (`sensitivity_id`, `obligation_id`)
);

-- Create Sensitivity Policy mapping table
CREATE TABLE IF NOT EXISTS `sensitivity_policy_mapping` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `sensitivity_id` INT NOT NULL,
    `policy_id` INT NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_sensitivity_policy` (`sensitivity_id`, `policy_id`)
);

-- Create Obligation Policy mapping table
CREATE TABLE IF NOT EXISTS `obligation_policy` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `obligation_id` INT NOT NULL,
    `policy_id` INT NOT NULL,
    `control_type` VARCHAR(100),
    `relevance_score` FLOAT DEFAULT 1.0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`obligation_id`) REFERENCES `obligation`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_obligation_policy` (`obligation_id`, `policy_id`)
);

-- Create Obligation Risk mapping table
CREATE TABLE IF NOT EXISTS `obligation_risk` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `obligation_id` INT NOT NULL,
    `risk_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`obligation_id`) REFERENCES `obligation`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`risk_id`) REFERENCES `risk`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_obligation_risk` (`obligation_id`, `risk_id`)
);

-- Create Framework Control mapping table
CREATE TABLE IF NOT EXISTS `framework_control` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `framework_id` INT NOT NULL,
    `control_id` INT NOT NULL,
    `relevance_score` FLOAT DEFAULT 1.0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`framework_id`) REFERENCES `framework`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`control_id`) REFERENCES `control`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_framework_control` (`framework_id`, `control_id`)
);

-- Create Policy Control mapping table
CREATE TABLE IF NOT EXISTS `policy_control` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `policy_id` INT NOT NULL,
    `control_id` INT NOT NULL,
    `relevance_score` FLOAT DEFAULT 1.0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`control_id`) REFERENCES `control`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_policy_control` (`policy_id`, `control_id`)
);

-- Create Risk Control mapping table
CREATE TABLE IF NOT EXISTS `risk_control` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `risk_id` INT NOT NULL,
    `control_id` INT NOT NULL,
    `mitigation_level` VARCHAR(50) DEFAULT 'Medium',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`risk_id`) REFERENCES `risk`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`control_id`) REFERENCES `control`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `unique_risk_control` (`risk_id`, `control_id`)
);

-- =============================================
-- SEED SENSITIVITY OBLIGATIONS
-- =============================================

-- Insert standard obligations for sensitivity levels
INSERT INTO `sensitivity_obligation` (`sensitivity_id`, `obligation_id`, `priority`)
VALUES
-- Special Category (highest sensitivity)
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM obligation WHERE name = 'Encrypt Data at Rest'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM obligation WHERE name = 'Encrypt Data in Transit'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM obligation WHERE name = 'Implement Access Controls'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM obligation WHERE name = 'Implement Data Masking'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM obligation WHERE name = 'Maintain Access Logs'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM obligation WHERE name = 'Implement Data Retention Controls'), 'High'),

-- Restricted (high sensitivity)
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM obligation WHERE name = 'Encrypt Data at Rest'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM obligation WHERE name = 'Encrypt Data in Transit'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM obligation WHERE name = 'Implement Access Controls'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM obligation WHERE name = 'Implement Data Masking'), 'High'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM obligation WHERE name = 'Maintain Access Logs'), 'High'),

-- Confidential (medium sensitivity)
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM obligation WHERE name = 'Encrypt Data at Rest'), 'Medium'),
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM obligation WHERE name = 'Encrypt Data in Transit'), 'Medium'),
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM obligation WHERE name = 'Implement Access Controls'), 'Medium'),
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM obligation WHERE name = 'Maintain Access Logs'), 'Medium'),

-- Internal (low sensitivity)
((SELECT id FROM sensitivity WHERE name = 'Internal'), (SELECT id FROM obligation WHERE name = 'Implement Access Controls'), 'Low'),

-- Public (minimal sensitivity)
-- No obligations required for public data

-- =============================================
-- SEED SENSITIVITY POLICY MAPPINGS
-- =============================================

-- Map sensitivity levels to appropriate policies
INSERT INTO `sensitivity_policy_mapping` (`sensitivity_id`, `policy_id`, `description`)
VALUES
-- Public data sensitivity mappings
((SELECT id FROM sensitivity WHERE name = 'Public'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Public data requires basic access controls'),
((SELECT id FROM sensitivity WHERE name = 'Public'), (SELECT id FROM policy WHERE name = 'Data Retention Policy'), 'Public data still requires retention policies'),

-- Internal data sensitivity mappings
((SELECT id FROM sensitivity WHERE name = 'Internal'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Internal data requires organization-level access controls'),
((SELECT id FROM sensitivity WHERE name = 'Internal'), (SELECT id FROM policy WHERE name = 'Data Retention Policy'), 'Internal data requires standard retention policies'),
((SELECT id FROM sensitivity WHERE name = 'Internal'), (SELECT id FROM policy WHERE name = 'Data Sharing Policy'), 'Internal data has sharing restrictions'),

-- Confidential data sensitivity mappings
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Confidential data requires strict access controls'),
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM policy WHERE name = 'Data Retention Policy'), 'Confidential data requires careful retention management'),
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM policy WHERE name = 'Data Sharing Policy'), 'Confidential data has significant sharing restrictions'),
((SELECT id FROM sensitivity WHERE name = 'Confidential'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Confidential data requires security measures'),

-- Restricted data sensitivity mappings
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Restricted data requires very strict access controls'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM policy WHERE name = 'Data Retention Policy'), 'Restricted data requires careful retention management'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM policy WHERE name = 'Data Sharing Policy'), 'Restricted data has severe sharing restrictions'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Restricted data requires enhanced security measures'),
((SELECT id FROM sensitivity WHERE name = 'Restricted'), (SELECT id FROM policy WHERE name = 'Data Minimization Policy'), 'Restricted data should be minimized where possible'),

-- Special Category data sensitivity mappings
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Special Category data requires the strictest access controls'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM policy WHERE name = 'Data Retention Policy'), 'Special Category data requires careful retention management'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM policy WHERE name = 'Data Sharing Policy'), 'Special Category data has the most severe sharing restrictions'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Special Category data requires the highest security measures'),
((SELECT id FROM sensitivity WHERE name = 'Special Category'), (SELECT id FROM policy WHERE name = 'Data Minimization Policy'), 'Special Category data should be strictly minimized');

-- =============================================
-- SEED SAMPLE RISKS
-- =============================================

-- Insert sample risks
INSERT INTO `risk` (`name`, `description`, `category`, `likelihood`, `impact`)
VALUES
('Unauthorized Data Access', 'Unauthorized individuals gain access to sensitive personal data due to inadequate access controls', 'Security', 'High', 'High'),
('Data Breach', 'Personal data is exposed, lost, altered, or accessed without authorization', 'Security', 'Medium', 'High'),
('Excessive Data Collection', 'Collection of personal data beyond what is necessary for the stated purpose', 'Privacy', 'High', 'Medium'),
('Improper Data Retention', 'Retention of personal data beyond the necessary period for the stated purpose', 'Privacy', 'High', 'Medium'),
('Inadequate Consent Management', 'Failure to obtain, record, or manage valid consent for data processing activities', 'Consent', 'Medium', 'High'),
('Cross-Border Transfer Violations', 'Transfer of personal data to jurisdictions without adequate protection or proper transfer mechanisms', 'Transfer', 'Medium', 'High'),
('Insufficient Data Subject Rights Management', 'Inability to fulfill data subject requests (access, deletion, portability, etc.) within required timeframes', 'Rights', 'Medium', 'Medium'),
('Inadequate Security Controls', 'Lack of appropriate technical and organizational measures to protect personal data', 'Security', 'Medium', 'High'),
('Vendor Non-Compliance', 'Third-party processors handling personal data without adequate contractual controls or compliance verification', 'Third Party', 'High', 'Medium'),
('Incomplete Data Inventory', 'Incomplete or inaccurate records of data processing activities and data assets', 'Governance', 'High', 'Medium');

-- =============================================
-- SEED SAMPLE OBLIGATIONS
-- =============================================

-- Insert sample obligations
INSERT INTO `obligation` (`name`, `description`, `source`, `control_type`, `status`, `risk_accepted`)
VALUES
('Encrypt Data at Rest', 'All personal data must be encrypted when stored using industry-standard encryption algorithms.', 'GDPR Article 32', 'Encryption', 'Open', FALSE),
('Encrypt Data in Transit', 'All personal data must be encrypted during transmission using secure protocols (TLS 1.2+).', 'GDPR Article 32', 'Encryption', 'Open', FALSE),
('Implement Access Controls', 'Restrict access to personal data to authorized personnel only using role-based access controls.', 'HIPAA Security Rule', 'Access Control', 'Open', FALSE),
('Maintain Access Logs', 'Maintain logs of all access to sensitive personal data for auditing purposes.', 'HIPAA Security Rule', 'Monitoring', 'In Progress', FALSE),
('Implement Data Masking', 'Mask sensitive data in non-production environments and when displayed to users without need-to-know.', 'Internal Security Policy', 'Masking', 'In Progress', FALSE),
('Implement Data Retention Controls', 'Define and enforce data retention periods for all personal data with automated deletion.', 'CCPA Section 1798.100', 'Retention', 'Implemented', FALSE),
('Monitor Data Access', 'Implement monitoring systems to detect and alert on suspicious access patterns to sensitive data.', 'ISO 27001', 'Monitoring', 'Open', FALSE),
('Implement Least Privilege', 'Ensure users have only the minimum privileges necessary to perform their job functions.', 'NIST SP 800-53', 'Access Control', 'Open', FALSE),
-- Removed 'Implement Data Classification' obligation
('Conduct Regular Security Assessments', 'Perform regular security assessments to identify and mitigate vulnerabilities.', 'ISO 27001', 'General', 'In Progress', FALSE);

-- =============================================
-- SEED OBLIGATION-POLICY MAPPINGS
-- =============================================

-- Insert sample obligation-policy mappings
INSERT INTO `obligation_policy` (`obligation_id`, `policy_id`, `control_type`, `relevance_score`)
VALUES
-- Encrypt Data at Rest mappings
((SELECT id FROM obligation WHERE name = 'Encrypt Data at Rest'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Encryption', 1.0),
((SELECT id FROM obligation WHERE name = 'Encrypt Data at Rest'), (SELECT id FROM policy WHERE name = 'Data Minimization Policy'), 'Encryption', 0.6),

-- Encrypt Data in Transit mappings
((SELECT id FROM obligation WHERE name = 'Encrypt Data in Transit'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Encryption', 1.0),
((SELECT id FROM obligation WHERE name = 'Encrypt Data in Transit'), (SELECT id FROM policy WHERE name = 'Data Sharing Policy'), 'Encryption', 0.8),

-- Implement Access Controls mappings
((SELECT id FROM obligation WHERE name = 'Implement Access Controls'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Access Control', 1.0),
((SELECT id FROM obligation WHERE name = 'Implement Access Controls'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Access Control', 0.7),

-- Maintain Access Logs mappings
((SELECT id FROM obligation WHERE name = 'Maintain Access Logs'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Monitoring', 0.9),
((SELECT id FROM obligation WHERE name = 'Maintain Access Logs'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Monitoring', 0.6),

-- Implement Data Masking mappings
((SELECT id FROM obligation WHERE name = 'Implement Data Masking'), (SELECT id FROM policy WHERE name = 'Data Minimization Policy'), 'Masking', 1.0),
((SELECT id FROM obligation WHERE name = 'Implement Data Masking'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Masking', 0.7),

-- Implement Data Retention Controls mappings
((SELECT id FROM obligation WHERE name = 'Implement Data Retention Controls'), (SELECT id FROM policy WHERE name = 'Data Retention Policy'), 'Retention', 1.0),

-- Monitor Data Access mappings
((SELECT id FROM obligation WHERE name = 'Monitor Data Access'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Monitoring', 0.8),
((SELECT id FROM obligation WHERE name = 'Monitor Data Access'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'Monitoring', 0.6),

-- Implement Least Privilege mappings
((SELECT id FROM obligation WHERE name = 'Implement Least Privilege'), (SELECT id FROM policy WHERE name = 'Data Access Control Policy'), 'Access Control', 1.0),

-- Removed 'Implement Data Classification' mappings

-- Conduct Regular Security Assessments mappings
((SELECT id FROM obligation WHERE name = 'Conduct Regular Security Assessments'), (SELECT id FROM policy WHERE name = 'Data Security Policy'), 'General', 0.7);

-- =============================================
-- SEED OBLIGATION-RISK MAPPINGS
-- =============================================

-- Insert sample obligation-risk mappings
INSERT INTO `obligation_risk` (`obligation_id`, `risk_id`)
VALUES
-- Encrypt Data at Rest risk mappings
((SELECT id FROM obligation WHERE name = 'Encrypt Data at Rest'), (SELECT id FROM risk WHERE name = 'Data Breach')), 
((SELECT id FROM obligation WHERE name = 'Encrypt Data at Rest'), (SELECT id FROM risk WHERE name = 'Unauthorized Data Access')),

-- Encrypt Data in Transit risk mappings
((SELECT id FROM obligation WHERE name = 'Encrypt Data in Transit'), (SELECT id FROM risk WHERE name = 'Data Breach')),

-- Implement Access Controls risk mappings
((SELECT id FROM obligation WHERE name = 'Implement Access Controls'), (SELECT id FROM risk WHERE name = 'Unauthorized Data Access')),

-- Maintain Access Logs risk mappings
((SELECT id FROM obligation WHERE name = 'Maintain Access Logs'), (SELECT id FROM risk WHERE name = 'Unauthorized Data Access')),

-- Implement Data Masking risk mappings
((SELECT id FROM obligation WHERE name = 'Implement Data Masking'), (SELECT id FROM risk WHERE name = 'Excessive Data Collection')),

-- Implement Data Retention Controls risk mappings
((SELECT id FROM obligation WHERE name = 'Implement Data Retention Controls'), (SELECT id FROM risk WHERE name = 'Improper Data Retention')),

-- Monitor Data Access risk mappings
((SELECT id FROM obligation WHERE name = 'Monitor Data Access'), (SELECT id FROM risk WHERE name = 'Unauthorized Data Access')),

-- Implement Least Privilege risk mappings
((SELECT id FROM obligation WHERE name = 'Implement Least Privilege'), (SELECT id FROM risk WHERE name = 'Unauthorized Data Access')),

-- Removed 'Implement Data Classification' risk mappings

-- Conduct Regular Security Assessments risk mappings
((SELECT id FROM obligation WHERE name = 'Conduct Regular Security Assessments'), (SELECT id FROM risk WHERE name = 'Inadequate Security Controls'));

-- =============================================
-- SEED FRAMEWORK-CONTROL MAPPINGS
-- =============================================

-- Insert sample framework-control mappings
INSERT INTO `framework_control` (`framework_id`, `control_id`, `relevance_score`)
VALUES
-- NIST CSF mappings
((SELECT id FROM framework WHERE name = 'NIST CSF'), (SELECT id FROM control WHERE name = 'Access Control'), 1.0),
((SELECT id FROM framework WHERE name = 'NIST CSF'), (SELECT id FROM control WHERE name = 'Data Encryption'), 1.0),
((SELECT id FROM framework WHERE name = 'NIST CSF'), (SELECT id FROM control WHERE name = 'Audit Logging'), 0.9),
((SELECT id FROM framework WHERE name = 'NIST CSF'), (SELECT id FROM control WHERE name = 'Vulnerability Management'), 1.0),
((SELECT id FROM framework WHERE name = 'NIST CSF'), (SELECT id FROM control WHERE name = 'Incident Response Plan'), 1.0),

-- ISO 27001 mappings
((SELECT id FROM framework WHERE name = 'ISO 27001'), (SELECT id FROM control WHERE name = 'Access Control'), 1.0),
((SELECT id FROM framework WHERE name = 'ISO 27001'), (SELECT id FROM control WHERE name = 'Data Encryption'), 1.0),
((SELECT id FROM framework WHERE name = 'ISO 27001'), (SELECT id FROM control WHERE name = 'Security Awareness Training'), 0.9),
((SELECT id FROM framework WHERE name = 'ISO 27001'), (SELECT id FROM control WHERE name = 'Vulnerability Management'), 1.0),
((SELECT id FROM framework WHERE name = 'ISO 27001'), (SELECT id FROM control WHERE name = 'Incident Response Plan'), 1.0),
((SELECT id FROM framework WHERE name = 'ISO 27001'), (SELECT id FROM control WHERE name = 'Audit Logging'), 0.9),

-- GDPR Controls mappings
((SELECT id FROM framework WHERE name = 'GDPR Controls'), (SELECT id FROM control WHERE name = 'Data Encryption'), 1.0),
((SELECT id FROM framework WHERE name = 'GDPR Controls'), (SELECT id FROM control WHERE name = 'Data Minimization'), 1.0),
((SELECT id FROM framework WHERE name = 'GDPR Controls'), (SELECT id FROM control WHERE name = 'Privacy Impact Assessment'), 1.0),
((SELECT id FROM framework WHERE name = 'GDPR Controls'), (SELECT id FROM control WHERE name = 'Data Subject Rights Management'), 1.0),
((SELECT id FROM framework WHERE name = 'GDPR Controls'), (SELECT id FROM control WHERE name = 'Consent Management'), 1.0),

-- PCI DSS mappings
((SELECT id FROM framework WHERE name = 'PCI DSS'), (SELECT id FROM control WHERE name = 'Data Encryption'), 1.0),
((SELECT id FROM framework WHERE name = 'PCI DSS'), (SELECT id FROM control WHERE name = 'Access Control'), 1.0),
((SELECT id FROM framework WHERE name = 'PCI DSS'), (SELECT id FROM control WHERE name = 'Vulnerability Management'), 1.0),
((SELECT id FROM framework WHERE name = 'PCI DSS'), (SELECT id FROM control WHERE name = 'Audit Logging'), 1.0),
((SELECT id FROM framework WHERE name = 'PCI DSS'), (SELECT id FROM control WHERE name = 'Network Segmentation'), 1.0);

-- =============================================
-- SEED POLICY-CONTROL MAPPINGS
-- =============================================

-- Insert sample policy-control mappings
INSERT INTO `policy_control` (`policy_id`, `control_id`, `relevance_score`)
VALUES
-- Data Security Policy mappings
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM control WHERE name = 'Data Encryption'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM control WHERE name = 'Access Control'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM control WHERE name = 'Vulnerability Management'), 0.9),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM control WHERE name = 'Audit Logging'), 0.8),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM control WHERE name = 'Data Loss Prevention'), 1.0),

-- Data Retention Policy mappings
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM control WHERE name = 'Data Minimization'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM control WHERE name = 'Data Backup'), 0.8),

-- Data Sharing Policy mappings
((SELECT id FROM policy WHERE name = 'Data Sharing Policy'), (SELECT id FROM control WHERE name = 'Consent Management'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Sharing Policy'), (SELECT id FROM control WHERE name = 'Data Subject Rights Management'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Sharing Policy'), (SELECT id FROM control WHERE name = 'Privacy Impact Assessment'), 0.9),
((SELECT id FROM policy WHERE name = 'Data Sharing Policy'), (SELECT id FROM control WHERE name = 'Data Minimization'), 0.8),

-- Data Minimization Policy mappings
((SELECT id FROM policy WHERE name = 'Data Minimization Policy'), (SELECT id FROM control WHERE name = 'Data Minimization'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Minimization Policy'), (SELECT id FROM control WHERE name = 'Privacy Impact Assessment'), 0.9),

-- Data Access Control Policy mappings
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM control WHERE name = 'Access Control'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM control WHERE name = 'Multi-Factor Authentication'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM control WHERE name = 'Audit Logging'), 0.9),

-- Additional Data Security Policy mappings
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM control WHERE name = 'Incident Response Plan'), 1.0),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM control WHERE name = 'Disaster Recovery'), 0.9);

-- =============================================
-- DEFAULT SECURITY SETTINGS TABLE
CREATE TABLE IF NOT EXISTS `default_security_settings` (
    `id`                           INT PRIMARY KEY DEFAULT 1, -- Assuming a single row for global defaults
    `default_encryption_algorithm` VARCHAR(100),
    `created_at`                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at`                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `pk_default_settings` CHECK (`id` = 1) -- Ensure only one row can exist
);

INSERT INTO default_security_settings (default_encryption_algorithm)
VALUES ('AES-256-GCM')
ON DUPLICATE KEY UPDATE
   default_encryption_algorithm = VALUES(default_encryption_algorithm);

-- POLICY PURPOSE DATA SECURITY TABLE
CREATE TABLE IF NOT EXISTS `policy_purpose_data_security` (
    `policy_purpose_data_element_id` INT NOT NULL,
    `encryption_required`  BOOLEAN     NOT NULL DEFAULT FALSE,
    `encryption_algorithm` VARCHAR(100),
    `masking_required`     BOOLEAN     NOT NULL DEFAULT FALSE,
    `masking_format`       VARCHAR(100),
    `access_logging`       BOOLEAN     NOT NULL DEFAULT FALSE,
    PRIMARY KEY (`policy_purpose_data_element_id`),
    FOREIGN KEY (`policy_purpose_data_element_id`) REFERENCES `policy_purpose_data_element`(`id`) ON DELETE CASCADE
);

-- Insert policy-purpose relationships for Data Security Policy
DELETE FROM policy_purpose WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy');
INSERT INTO policy_purpose (policy_id, purpose_id) VALUES
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Customer Support')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Fraud Detection')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Marketing Campaigns')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Product Analytics')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Payment Processing')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Service Delivery')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Research and Development')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'Employee Management')),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM purpose WHERE name = 'User Authentication'));

-- Insert policy_purpose_data_element entries for Data Security Policy
INSERT INTO policy_purpose_data_element (policy_id, purpose_id, data_element_id, access_allowed) VALUES
-- Customer Support
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Customer Support'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

-- Fraud Detection
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Fraud Detection'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

-- Marketing Campaigns
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Marketing Campaigns'),
 (SELECT id FROM data_element WHERE name = 'Customer ID'), TRUE),

-- Product Analytics
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Product Analytics'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

-- Payment Processing
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Credit Card Number'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Payment Processing'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

-- Service Delivery
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Service Delivery'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),

-- Research and Development
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'Purchase History'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Research and Development'),
 (SELECT id FROM data_element WHERE name = 'IP Address'), TRUE),

-- Employee Management
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'Employee Management'),
 (SELECT id FROM data_element WHERE name = 'Full Name'), TRUE),

-- User Authentication
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'Email Address'), TRUE),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), 
 (SELECT id FROM purpose WHERE name = 'User Authentication'),
 (SELECT id FROM data_element WHERE name = 'Device ID'), TRUE);

-- Seed Policy Purpose Data Security
DELETE FROM policy_purpose_data_security;
INSERT INTO policy_purpose_data_security
    (`policy_purpose_data_element_id`, `encryption_required`, `encryption_algorithm`, `masking_required`, `masking_format`, `access_logging`) 
VALUES
-- Default Role Assignment
-- Standard data elements with basic security
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), TRUE, 'AES-256', FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Name')), TRUE, 'AES-256', FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), TRUE, 'AES-256', TRUE, 'xxxx@####.com', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Phone Number')), TRUE, 'AES-256', TRUE, '###-###-####', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Address')), TRUE, 'AES-256', TRUE, '#### ***** St, City, ST #####', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), TRUE, 'AES-128', TRUE, '###.###.###.###', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), TRUE, 'AES-128', FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), TRUE, 'AES-256', TRUE, '######', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), TRUE, 'AES-256', FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Date of Birth')), TRUE, 'AES-256', TRUE, '##/##/####', TRUE),

-- Highly sensitive data elements with stronger security
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), TRUE, 'AES-256', TRUE, '###-##-####', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), TRUE, 'AES-256', TRUE, '####-####-####-####', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Bank Account Number')), TRUE, 'AES-256', TRUE, '########', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Default Role Assignment') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Biometric Data')), TRUE, 'AES-256', TRUE, NULL, TRUE),

-- Customer Support
-- Customer Support
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), FALSE, NULL, FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Customer Support') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), FALSE, NULL, TRUE, 'xxxx@####.com', TRUE),

-- Fraud Detection
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), FALSE, NULL, FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Fraud Detection') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), FALSE, NULL, TRUE, '###.###.###.###', TRUE),

-- Marketing Campaigns
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), FALSE, NULL, TRUE, 'xxxx@####.com', FALSE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Marketing Campaigns') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Customer ID')), FALSE, NULL, TRUE, '######', FALSE),

-- Product Analytics
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), FALSE, NULL, FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Product Analytics') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), FALSE, NULL, TRUE, '###.###.###.###', TRUE),

-- Payment Processing
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Credit Card Number')), FALSE, NULL, TRUE, '####-XXXX-XXXX-####', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Payment Processing') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), FALSE, NULL, FALSE, NULL, TRUE),

-- Service Delivery
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), FALSE, NULL, FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Service Delivery') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), FALSE, NULL, TRUE, 'xxxx@####.com', TRUE),

-- Research and Development
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Research and Development') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Purchase History')), FALSE, NULL, FALSE, NULL, TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Research and Development') AND data_element_id = (SELECT id FROM data_element WHERE name = 'IP Address')), FALSE, NULL, TRUE, '###.###.###.###', TRUE),

-- Employee Management
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Social Security Number')), FALSE, NULL, TRUE, 'XXX-XX-####', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'Employee Management') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Full Name')), FALSE, NULL, FALSE, NULL, TRUE),

-- User Authentication
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'User Authentication') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Email Address')), FALSE, NULL, TRUE, 'xxxx@####.com', TRUE),
((SELECT id FROM policy_purpose_data_element WHERE policy_id = (SELECT id FROM policy WHERE name = 'Data Security Policy') AND purpose_id = (SELECT id FROM purpose WHERE name = 'User Authentication') AND data_element_id = (SELECT id FROM data_element WHERE name = 'Device ID')), FALSE, NULL, FALSE, NULL, TRUE);


-- =============================================
-- SEED RISK-CONTROL MAPPINGS
-- =============================================

-- Insert sample risk-control mappings
INSERT INTO `risk_control` (`risk_id`, `control_id`, `mitigation_level`)
VALUES
-- Data Breach risk mappings
((SELECT id FROM risk WHERE name = 'Data Breach'), (SELECT id FROM control WHERE name = 'Data Encryption'), 'High'),
((SELECT id FROM risk WHERE name = 'Data Breach'), (SELECT id FROM control WHERE name = 'Access Control'), 'High'),
((SELECT id FROM risk WHERE name = 'Data Breach'), (SELECT id FROM control WHERE name = 'Vulnerability Management'), 'High'),
((SELECT id FROM risk WHERE name = 'Data Breach'), (SELECT id FROM control WHERE name = 'Security Awareness Training'), 'Medium'),
((SELECT id FROM risk WHERE name = 'Data Breach'), (SELECT id FROM control WHERE name = 'Data Loss Prevention'), 'High'),

-- Unauthorized Data Access risk mappings
((SELECT id FROM risk WHERE name = 'Unauthorized Data Access'), (SELECT id FROM control WHERE name = 'Access Control'), 'High'),
((SELECT id FROM risk WHERE name = 'Unauthorized Data Access'), (SELECT id FROM control WHERE name = 'Multi-Factor Authentication'), 'High'),
((SELECT id FROM risk WHERE name = 'Unauthorized Data Access'), (SELECT id FROM control WHERE name = 'Audit Logging'), 'Medium'),
((SELECT id FROM risk WHERE name = 'Unauthorized Data Access'), (SELECT id FROM control WHERE name = 'Network Segmentation'), 'Medium'),

-- Excessive Data Collection risk mappings
((SELECT id FROM risk WHERE name = 'Excessive Data Collection'), (SELECT id FROM control WHERE name = 'Data Minimization'), 'High'),
((SELECT id FROM risk WHERE name = 'Excessive Data Collection'), (SELECT id FROM control WHERE name = 'Privacy Impact Assessment'), 'Medium'),

-- Improper Data Retention risk mappings
((SELECT id FROM risk WHERE name = 'Improper Data Retention'), (SELECT id FROM control WHERE name = 'Data Minimization'), 'High'),

-- Inadequate Consent Management risk mappings
((SELECT id FROM risk WHERE name = 'Inadequate Consent Management'), (SELECT id FROM control WHERE name = 'Consent Management'), 'High'),

-- Insufficient Data Subject Rights Management risk mappings
((SELECT id FROM risk WHERE name = 'Insufficient Data Subject Rights Management'), (SELECT id FROM control WHERE name = 'Data Subject Rights Management'), 'High'),

-- Inadequate Security Controls risk mappings
((SELECT id FROM risk WHERE name = 'Inadequate Security Controls'), (SELECT id FROM control WHERE name = 'Privacy Impact Assessment'), 'High'),
((SELECT id FROM risk WHERE name = 'Inadequate Security Controls'), (SELECT id FROM control WHERE name = 'Vulnerability Management'), 'High'),
((SELECT id FROM risk WHERE name = 'Inadequate Security Controls'), (SELECT id FROM control WHERE name = 'Security Awareness Training'), 'Medium');

-- Seed Policy Data Element Usage data
INSERT INTO `policy_data_element_usage` (`policy_id`, `data_element_id`, `operation`, `allowed`, `restrictions`) VALUES
-- Data Security Policy usage rules
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Social Security Number'), 'read', TRUE, 'Only for employment verification'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Social Security Number'), 'write', TRUE, 'Must be encrypted'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Social Security Number'), 'share', FALSE, 'Prohibited except as required by law'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Credit Card Number'), 'read', TRUE, 'Only for payment processing'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Credit Card Number'), 'write', TRUE, 'Must be encrypted and tokenized'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Credit Card Number'), 'share', FALSE, 'Prohibited except with payment processors'),

-- Data Access Control Policy usage rules
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM data_element WHERE name = 'Email Address'), 'read', TRUE, 'With explicit consent'),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM data_element WHERE name = 'Email Address'), 'write', TRUE, 'Only with opt-in consent'),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM data_element WHERE name = 'Phone Number'), 'read', TRUE, 'With explicit consent'),
((SELECT id FROM policy WHERE name = 'Data Access Control Policy'), (SELECT id FROM data_element WHERE name = 'Phone Number'), 'share', FALSE, 'Prohibited without specific opt-in');

-- Seed Policy Data Element Retention data
INSERT INTO `policy_data_element_retention` (`policy_id`, `data_element_id`, `retention_period`, `retention_basis`, `exceptions`) VALUES
-- Data Retention Policy retention rules
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM data_element WHERE name = 'Social Security Number'), '7 years', 'Legal requirement', 'Litigation hold'),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM data_element WHERE name = 'Credit Card Number'), '2 years after last transaction', 'Business need', 'Ongoing subscription'),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM data_element WHERE name = 'Email Address'), '3 years after account closure', 'Business need', 'Ongoing relationship'),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM data_element WHERE name = 'Phone Number'), '3 years after account closure', 'Business need', 'Ongoing relationship'),
((SELECT id FROM policy WHERE name = 'Data Retention Policy'), (SELECT id FROM data_element WHERE name = 'Purchase History'), '5 years', 'Tax requirements', 'Litigation hold');

-- Seed Policy Data Element Security data
INSERT INTO `policy_data_element_security` (`policy_id`, `data_element_id`, `requires_encryption`, `encryption_algorithm`, `requires_masking`, `masking_format`, `requires_access_control`, `access_control_type`) VALUES
-- Data Security Policy security rules
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Social Security Number'), TRUE, 'AES-256', TRUE, 'Show only last 4 digits', TRUE, 'Role-based'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Credit Card Number'), TRUE, 'AES-256', TRUE, 'Show only last 4 digits', TRUE, 'Role-based'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Bank Account Number'), TRUE, 'AES-256', TRUE, 'Show only last 4 digits', TRUE, 'Role-based'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Date of Birth'), FALSE, NULL, TRUE, 'Show only year', TRUE, 'Role-based'),
((SELECT id FROM policy WHERE name = 'Data Security Policy'), (SELECT id FROM data_element WHERE name = 'Email Address'), FALSE, NULL, TRUE, 'Partial - Show only domain', TRUE, 'Role-based');
