-- Privacy Regulation Database Seed Script
-- This script creates and populates all tables for the GlossaryRepository and RegulatoryMetadataRepository

-- Drop existing tables if they exist (in reverse order of creation to handle foreign key constraints)
DROP TABLE IF EXISTS data_subject_right_exemptions;
DROP TABLE IF EXISTS data_subject_right_implementation_steps;
DROP TABLE IF EXISTS legal_basis_requirements;
DROP TABLE IF EXISTS law_purpose_category_legal_basis;
DROP TABLE IF EXISTS law_data_subject_access_request_notification_requirements;
DROP TABLE IF EXISTS law_transfer;
DROP TABLE IF EXISTS law_context_data_subject_type_data_category_sensitivity;
DROP TABLE IF EXISTS context_data_subject_type_data_category_sensitivity;
DROP TABLE IF EXISTS data_subject_type_data_element_sensitivity;
DROP TABLE IF EXISTS data_subject_type_data_category_sensitivity;
DROP TABLE IF EXISTS law_data_subject_type_data_category_sensitivity;
DROP TABLE IF EXISTS law_data_subject_type_data_element_sensitivity;
DROP TABLE IF EXISTS data_category_data_element;
DROP TABLE IF EXISTS law_incident_breach_guidance;
DROP TABLE IF EXISTS law_legal_basis;
DROP TABLE IF EXISTS law_jurisdiction;
DROP TABLE IF EXISTS policy_data_domain;
DROP TABLE IF EXISTS policy_dataset;
DROP TABLE IF EXISTS dataset;
DROP TABLE IF EXISTS policy;
DROP TABLE IF EXISTS data_domain;
DROP TABLE IF EXISTS asset;
DROP TABLE IF EXISTS context;
DROP TABLE IF EXISTS sensitivity;
DROP TABLE IF EXISTS data_category;
DROP TABLE IF EXISTS data_subject_type;
DROP TABLE IF EXISTS data_element;
DROP TABLE IF EXISTS breach_type;
DROP TABLE IF EXISTS purpose_category;
DROP TABLE IF EXISTS legal_basis;
DROP TABLE IF EXISTS jurisdiction;
DROP TABLE IF EXISTS law;

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
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

-- Create Context table
CREATE TABLE IF NOT EXISTS `context` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- REGULATORY METADATA TABLES
-- =============================================

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

-- Create Law Context Data Subject Type Data Category Sensitivity table
CREATE TABLE IF NOT EXISTS `law_context_data_subject_type_data_category_sensitivity` (
    `law_id` INT NOT NULL,
    `context_id` INT NOT NULL,
    `data_subject_type_id` INT NOT NULL,
    `data_category_id` INT NOT NULL,
    `sensitivity_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`law_id`, `context_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`),
    FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`context_id`) REFERENCES `context`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
);

-- Create Context Data Subject Type Data Category Sensitivity table
CREATE TABLE IF NOT EXISTS `context_data_subject_type_data_category_sensitivity` (
    `context_id` INT NOT NULL,
    `data_subject_type_id` INT NOT NULL,
    `data_category_id` INT NOT NULL,
    `sensitivity_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`context_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`),
    FOREIGN KEY (`context_id`) REFERENCES `context`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
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
('Name', 'An individual\'s first name, last name, or full name.'),
('Email Address', 'An individual\'s email address used for electronic communication.'),
('Phone Number', 'An individual\'s telephone number used for voice communication.'),
('Address', 'An individual\'s physical address including street, city, state, and postal code.'),
('IP Address', 'A unique identifier assigned to a device connected to a network.'),
('Device ID', 'A unique identifier assigned to a specific device.'),
('Social Security Number', 'A unique identifier assigned to an individual for tax and identification purposes in the United States.'),
('Credit Card Number', 'A unique number assigned to a credit card for payment processing.'),
('Date of Birth', 'An individual\'s date of birth.'),
('Biometric Data', 'Physical or behavioral characteristics that can be used to identify an individual, such as fingerprints or facial recognition data.');

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

-- Seed Context data
INSERT INTO `context` (`name`, `description`) VALUES
('Marketing', 'Processing personal data for marketing purposes, such as sending promotional emails or targeted advertising.'),
('Customer Service', 'Processing personal data to provide customer service, such as responding to inquiries or resolving complaints.'),
('Human Resources', 'Processing personal data for human resources purposes, such as payroll, benefits administration, or performance management.'),
('Finance', 'Processing personal data for financial purposes, such as billing, accounting, or tax compliance.'),
('Legal', 'Processing personal data for legal purposes, such as contract enforcement, litigation, or regulatory compliance.'),
('IT Security', 'Processing personal data for IT security purposes, such as access control, threat detection, or incident response.'),
('Research', 'Processing personal data for research purposes, such as market research, scientific research, or product development.');

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

-- Create Data Domain table
CREATE TABLE IF NOT EXISTS `data_domain` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Policy table
CREATE TABLE IF NOT EXISTS `policy` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `policy_type` VARCHAR(100),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Dataset table
CREATE TABLE IF NOT EXISTS `dataset` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `asset_id` INT NOT NULL,
    `source_system` VARCHAR(255),
    `data_domain_id` INT,
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`asset_id`) REFERENCES `asset`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_domain_id`) REFERENCES `data_domain`(`id`) ON DELETE SET NULL
);

-- Create Policy-Dataset relationship table
CREATE TABLE IF NOT EXISTS `policy_dataset` (
    `policy_id` INT NOT NULL,
    `dataset_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`policy_id`, `dataset_id`),
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`dataset_id`) REFERENCES `dataset`(`id`) ON DELETE CASCADE
);

-- Create Policy-Data Domain relationship table
CREATE TABLE IF NOT EXISTS `policy_data_domain` (
    `policy_id` INT NOT NULL,
    `data_domain_id` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`policy_id`, `data_domain_id`),
    FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`data_domain_id`) REFERENCES `data_domain`(`id`) ON DELETE CASCADE
);

-- Seed Asset data
INSERT INTO `asset` (`name`, `description`) VALUES
('CRM System', 'Customer Relationship Management system containing customer data and interactions'),
('ERP System', 'Enterprise Resource Planning system for managing business processes'),
('HR Portal', 'Human Resources portal for employee data management'),
('Marketing Platform', 'Platform for managing marketing campaigns and customer engagement'),
('Financial Database', 'Database containing financial records and transactions');

-- Seed Data Domain data
INSERT INTO `data_domain` (`name`, `description`) VALUES
('Customer Data', 'Data related to customers and their interactions'),
('Employee Data', 'Data related to employees and HR processes'),
('Financial Data', 'Data related to financial transactions and records'),
('Marketing Data', 'Data related to marketing campaigns and analytics'),
('Operational Data', 'Data related to business operations and processes');

-- Seed Policy data
INSERT INTO `policy` (`name`, `description`, `policy_type`) VALUES
('Data Retention', 'Policy governing how long data should be retained', 'Retention'),
('Data Access Control', 'Policy governing who can access specific data', 'Access Control'),
('Data Encryption', 'Policy governing encryption requirements for data', 'Security'),
('Data Backup', 'Policy governing backup requirements for data', 'Backup'),
('Data Quality', 'Policy governing data quality standards', 'Quality'),
('Data Classification', 'Policy governing classification of data sensitivity', 'Classification'),
('Data Sharing', 'Policy governing how data can be shared with third parties', 'Sharing');

-- Seed Dataset data
INSERT INTO `dataset` (`name`, `asset_id`, `source_system`, `data_domain_id`, `description`) VALUES
('Customer Profiles', 1, 'Salesforce', 1, 'Core customer profile information'),
('Customer Interactions', 1, 'Salesforce', 1, 'Records of customer interactions and support tickets'),
('Employee Records', 3, 'Workday', 2, 'Core employee records and personal information'),
('Payroll Data', 3, 'Workday', 3, 'Employee payroll and compensation data'),
('Financial Transactions', 5, 'Oracle', 3, 'Records of financial transactions'),
('Marketing Campaigns', 4, 'HubSpot', 4, 'Marketing campaign data and metrics'),
('Customer Segmentation', 4, 'HubSpot', 4, 'Customer segmentation data for targeted marketing'),
('Inventory Data', 2, 'SAP', 5, 'Inventory and supply chain data'),
('Sales Data', 2, 'SAP', 3, 'Sales records and revenue data'),
('Customer Analytics', 4, 'Tableau', 1, 'Customer behavior analytics and insights');

-- Seed Policy-Dataset relationships
INSERT INTO `policy_dataset` (`policy_id`, `dataset_id`) VALUES
(1, 1), -- Data Retention -> Customer Profiles
(2, 1), -- Data Access Control -> Customer Profiles
(3, 1), -- Data Encryption -> Customer Profiles
(1, 3), -- Data Retention -> Employee Records
(2, 3), -- Data Access Control -> Employee Records
(3, 3), -- Data Encryption -> Employee Records
(1, 5), -- Data Retention -> Financial Transactions
(4, 5), -- Data Backup -> Financial Transactions
(6, 5), -- Data Classification -> Financial Transactions
(5, 6), -- Data Quality -> Marketing Campaigns
(7, 6), -- Data Sharing -> Marketing Campaigns
(4, 8), -- Data Backup -> Inventory Data
(5, 8); -- Data Quality -> Inventory Data

-- Seed Policy-Data Domain relationships
INSERT INTO `policy_data_domain` (`policy_id`, `data_domain_id`) VALUES
(1, 1), -- Data Retention -> Customer Data
(2, 1), -- Data Access Control -> Customer Data
(7, 1), -- Data Sharing -> Customer Data
(1, 2), -- Data Retention -> Employee Data
(2, 2), -- Data Access Control -> Employee Data
(3, 2), -- Data Encryption -> Employee Data
(1, 3), -- Data Retention -> Financial Data
(4, 3), -- Data Backup -> Financial Data
(6, 3), -- Data Classification -> Financial Data
(5, 4), -- Data Quality -> Marketing Data
(7, 4), -- Data Sharing -> Marketing Data
(4, 5), -- Data Backup -> Operational Data
(5, 5); -- Data Quality -> Operational Data

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

-- Seed Law Context Data Subject Type Data Category Sensitivity relationships
INSERT INTO `law_context_data_subject_type_data_category_sensitivity` (`law_id`, `context_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`)
SELECT l.id, c.id, dst.id, dc.id, s.id
FROM `law` l, `context` c, `data_subject_type` dst, `data_category` dc, `sensitivity` s
WHERE 
    (l.name = 'GDPR' AND c.name = 'Marketing' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'GDPR' AND c.name = 'Customer Service' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'GDPR' AND c.name = 'Human Resources' AND dst.name = 'Employee' AND dc.name = 'Employment Information' AND s.name = 'Confidential') OR
    (l.name = 'GDPR' AND c.name = 'Finance' AND dst.name = 'Customer' AND dc.name = 'Financial Information' AND s.name = 'Restricted') OR
    (l.name = 'CCPA' AND c.name = 'Marketing' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'LGPD' AND c.name = 'Marketing' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (l.name = 'PIPEDA' AND c.name = 'Marketing' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal');

-- Seed Context Data Subject Type Data Category Sensitivity relationships
INSERT INTO `context_data_subject_type_data_category_sensitivity` (`context_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`)
SELECT c.id, dst.id, dc.id, s.id
FROM `context` c, `data_subject_type` dst, `data_category` dc, `sensitivity` s
WHERE 
    (c.name = 'Marketing' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (c.name = 'Customer Service' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (c.name = 'Human Resources' AND dst.name = 'Employee' AND dc.name = 'Employment Information' AND s.name = 'Confidential') OR
    (c.name = 'Finance' AND dst.name = 'Customer' AND dc.name = 'Financial Information' AND s.name = 'Restricted') OR
    (c.name = 'IT Security' AND dst.name = 'Employee' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal') OR
    (c.name = 'Research' AND dst.name = 'Customer' AND dc.name = 'Personal Identifiers' AND s.name = 'Internal');

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


