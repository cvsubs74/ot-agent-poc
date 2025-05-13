-- Purpose-Based Access Control (PBAC) Policy Engine Tables

-- Policy Types table
CREATE TABLE IF NOT EXISTS policy_types (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    json_schema JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Regions table
CREATE TABLE IF NOT EXISTS regions (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Policies table
CREATE TABLE IF NOT EXISTS policies (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    policy_type_id INT NOT NULL,
    data_element_id INT,
    data_category_id INT,
    sensitivity_id INT,
    policy_config JSON NOT NULL,
    effective_from TIMESTAMP NULL,
    effective_to TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (policy_type_id) REFERENCES policy_types(id),
    FOREIGN KEY (data_element_id) REFERENCES data_element(id),
    FOREIGN KEY (data_category_id) REFERENCES data_category(id),
    FOREIGN KEY (sensitivity_id) REFERENCES sensitivity(id)
);

-- Policy Groups table
CREATE TABLE IF NOT EXISTS policy_groups (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    version VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE(name, version)
);

-- Policy Group Members table
CREATE TABLE IF NOT EXISTS policy_group_members (
    id INT NOT NULL AUTO_INCREMENT,
    policy_group_id INT NOT NULL,
    policy_id INT NOT NULL,
    target_system VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE(policy_group_id, policy_id, target_system),
    FOREIGN KEY (policy_group_id) REFERENCES policy_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE CASCADE
);

-- Context Policy Groups table
CREATE TABLE IF NOT EXISTS context_policy_groups (
    id INT NOT NULL AUTO_INCREMENT,
    purpose_id INT,
    external_role_id INT,
    region_id INT,
    policy_group_id INT NOT NULL,
    granularity_rank INT DEFAULT 0,
    manual_priority INT DEFAULT 0,
    context_tags JSON,
    effective_from TIMESTAMP NULL,
    effective_to TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (purpose_id) REFERENCES purpose(id),
    FOREIGN KEY (external_role_id) REFERENCES external_roles(id),
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (policy_group_id) REFERENCES policy_groups(id) ON DELETE CASCADE
);

-- Access Requests table
CREATE TABLE IF NOT EXISTS access_requests (
    id INT NOT NULL AUTO_INCREMENT,
    requester_id VARCHAR(100) NOT NULL,
    dataset_id INT,
    purpose_id INT NOT NULL,
    justification TEXT,
    status ENUM('pending', 'approved', 'rejected', 'expired') DEFAULT 'pending',
    approved_by VARCHAR(100),
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (purpose_id) REFERENCES purpose(id)
);

-- Purpose Members table
CREATE TABLE IF NOT EXISTS purpose_members (
    id INT NOT NULL AUTO_INCREMENT,
    purpose_id INT NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    granted_by VARCHAR(100),
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE(purpose_id, user_id),
    FOREIGN KEY (purpose_id) REFERENCES purpose(id) ON DELETE CASCADE
);

-- Access Events table
CREATE TABLE IF NOT EXISTS access_events (
    id INT NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(100) NOT NULL,
    dataset_id INT,
    purpose_id INT,
    decision ENUM('allowed', 'denied') NOT NULL,
    query_fingerprint VARCHAR(255),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (purpose_id) REFERENCES purpose(id)
);

-- Initial data for Policy Engine tables

-- Policy Types
INSERT INTO policy_types (name, description, json_schema) VALUES 
('Access Control', 'Defines who can access data elements for specific purposes', 
'{
  "type": "object",
  "properties": {
    "operation": {
      "type": "string",
      "enum": ["read", "write", "update", "delete", "share"]
    },
    "allowed": {
      "type": "boolean"
    },
    "restrictions": {
      "type": "string"
    }
  },
  "required": ["operation", "allowed"]
}'),
('Security', 'Defines security controls for protecting data', 
'{
  "type": "object",
  "properties": {
    "encryption_required": {
      "type": "boolean"
    },
    "encryption_algorithm": {
      "type": "string"
    },
    "masking_required": {
      "type": "boolean"
    },
    "masking_format": {
      "type": "string"
    },
    "access_logging": {
      "type": "boolean"
    }
  },
  "required": ["encryption_required", "masking_required", "access_logging"]
}'),
('Retention', 'Defines data retention periods and policies', 
'{
  "type": "object",
  "properties": {
    "retention_period": {
      "type": "string"
    },
    "retention_trigger": {
      "type": "string",
      "enum": ["Collection", "Last Access", "End of Relationship", "Specific Date"]
    },
    "retention_basis": {
      "type": "string"
    },
    "exceptions": {
      "type": "string"
    }
  },
  "required": ["retention_period", "retention_trigger"]
}');

-- Sample Regions
INSERT INTO regions (name, description) VALUES 
('GLOBAL', 'Global region - applies everywhere'),
('NA', 'North America'),
('EU', 'European Union'),
('APAC', 'Asia-Pacific region'),
('LATAM', 'Latin America');

-- Sample Policies
-- Note: These would typically be added through the application interface
-- The following are just examples to demonstrate the structure

-- Example MASKING policy for PII data
INSERT INTO policies (policy_type_id, sensitivity_id, policy_config, effective_from)
SELECT 
    (SELECT id FROM policy_types WHERE name = 'MASKING'),
    (SELECT id FROM sensitivity WHERE name = 'PII'),
    '{"masking_format": "partial", "preserve_length": true}',
    CURRENT_TIMESTAMP;

-- Example RLS_FILTER policy for regional data access
INSERT INTO policies (policy_type_id, data_category_id, policy_config, effective_from)
SELECT 
    (SELECT id FROM policy_types WHERE name = 'RLS_FILTER'),
    (SELECT id FROM data_category WHERE name = 'Customer Data'),
    '{"filter_type": "equality", "filter_column": "region", "filter_values": ["${user.region}"]}',
    CURRENT_TIMESTAMP;

-- Example DENY policy for highly sensitive data
INSERT INTO policies (policy_type_id, sensitivity_id, policy_config, effective_from)
SELECT 
    (SELECT id FROM policy_types WHERE name = 'DENY'),
    (SELECT id FROM sensitivity WHERE name = 'Highly Sensitive'),
    '{"reason": "Access to highly sensitive data requires explicit approval", "exception_process": "Submit access request with business justification"}',
    CURRENT_TIMESTAMP;

-- Sample Policy Group
INSERT INTO policy_groups (name, description, version, is_active)
VALUES ('Standard Data Protection', 'Standard set of data protection policies', '1.0', TRUE);

-- Link policies to the policy group
-- This would typically be done through the application
INSERT INTO policy_group_members (policy_group_id, policy_id, target_system)
SELECT 
    (SELECT id FROM policy_groups WHERE name = 'Standard Data Protection' AND version = '1.0'),
    id,
    'ALL'
FROM policies
LIMIT 3; -- Just link the first 3 policies as an example