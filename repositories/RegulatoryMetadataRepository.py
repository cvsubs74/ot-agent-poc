import pymysql.cursors
import json

class RegulatoryMetadataRepository:

    def __init__(self, connection):
        self.connection = connection
        # self.setup_tables()

    # --- POLICY OVERRIDE TABLES: CRUD Methods ---
    def create_policy_override_role_purpose_data_usage_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS policy_override_role_purpose_data_usage (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                policy_purpose_data_element_id INTEGER NOT NULL,
                external_role_id INTEGER NOT NULL,
                operation VARCHAR(50) NOT NULL,
                allowed BOOLEAN NOT NULL,
                restrictions TEXT,
                UNIQUE(policy_purpose_data_element_id, external_role_id, operation),
                FOREIGN KEY (policy_purpose_data_element_id) REFERENCES policy_purpose_data_element(id),
                FOREIGN KEY (external_role_id) REFERENCES external_roles(id)
            );
        ''')
        self.connection.commit()
        cursor.close()

    def create_policy_override_role_purpose_data_retention_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS policy_override_role_purpose_data_retention (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                policy_purpose_data_element_id INTEGER NOT NULL,
                external_role_id INTEGER NOT NULL,
                retention_period TEXT NOT NULL,
                retention_justification TEXT,
                UNIQUE(policy_purpose_data_element_id, external_role_id),
                FOREIGN KEY (policy_purpose_data_element_id) REFERENCES policy_purpose_data_element(id),
                FOREIGN KEY (external_role_id) REFERENCES external_roles(id)
            );
        ''')
        self.connection.commit()
        cursor.close()

    def create_policy_override_role_purpose_data_security_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS policy_override_role_purpose_data_security (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                policy_purpose_data_element_id INTEGER NOT NULL,
                external_role_id INTEGER NOT NULL,
                security_rule_id INTEGER NOT NULL,
                UNIQUE(policy_purpose_data_element_id, external_role_id, security_rule_id),
                FOREIGN KEY (policy_purpose_data_element_id) REFERENCES policy_purpose_data_element(id),
                FOREIGN KEY (external_role_id) REFERENCES external_roles(id)
                -- Removed foreign key constraint to security_rules table as it doesn't exist yet
                -- FOREIGN KEY (security_rule_id) REFERENCES security_rules(id)
            );
        ''')
        self.connection.commit()
        cursor.close()

    # --- CRUD for Data Usage Override ---
    def add_policy_override_role_purpose_data_usage(self, policy_purpose_data_element_id, external_role_id, operation, allowed, restrictions=None):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO policy_override_role_purpose_data_usage (policy_purpose_data_element_id, external_role_id, operation, allowed, restrictions)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE allowed=VALUES(allowed), restrictions=VALUES(restrictions)
        ''', (policy_purpose_data_element_id, external_role_id, operation, allowed, restrictions))
        self.connection.commit()
        cursor.close()

    def get_all_policy_override_role_purpose_data_usage(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM policy_override_role_purpose_data_usage')
        rows = cursor.fetchall()
        desc = cursor.description
        cursor.close()
        return [dict(zip([col[0] for col in desc], row)) for row in rows]
        
    def get_policy_override_role_purpose_data_usages(self, policy_purpose_data_element_id=None, external_role_id=None):
        """Get policy override role purpose data usages for specific policy_purpose_data_element_id and external_role_id."""
        cursor = self.connection.cursor()
        query = '''
            SELECT o.*, p.policy_id, p.purpose_id, p.data_element_id, 
                   pol.name as policy_name, pur.name as purpose_name, de.name as data_element_name,
                   er.name as role_name, er.source_system
            FROM policy_override_role_purpose_data_usage o
            JOIN policy_purpose_data_element p ON o.policy_purpose_data_element_id = p.id
            JOIN policies pol ON p.policy_id = pol.id
            JOIN purposes pur ON p.purpose_id = pur.id
            JOIN data_elements de ON p.data_element_id = de.id
            JOIN external_roles er ON o.external_role_id = er.id
            WHERE 1=1
        '''
        params = []
        
        if policy_purpose_data_element_id is not None:
            query += ' AND o.policy_purpose_data_element_id = %s'
            params.append(policy_purpose_data_element_id)
            
        if external_role_id is not None:
            query += ' AND o.external_role_id = %s'
            params.append(external_role_id)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        desc = cursor.description
        cursor.close()
        return [dict(zip([col[0] for col in desc], row)) for row in rows]

    def delete_policy_override_role_purpose_data_usage(self, override_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM policy_override_role_purpose_data_usage WHERE id = %s', (override_id,))
        self.connection.commit()
        cursor.close()

    # --- CRUD for Data Retention Override ---
    def add_policy_override_role_purpose_data_retention(self, policy_purpose_data_element_id, external_role_id, retention_period, retention_justification=None):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO policy_override_role_purpose_data_retention (policy_purpose_data_element_id, external_role_id, retention_period, retention_justification)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE retention_period=VALUES(retention_period), retention_justification=VALUES(retention_justification)
        ''', (policy_purpose_data_element_id, external_role_id, retention_period, retention_justification))
        self.connection.commit()
        cursor.close()

    def get_all_policy_override_role_purpose_data_retention(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM policy_override_role_purpose_data_retention')
        rows = cursor.fetchall()
        desc = cursor.description
        cursor.close()
        return [dict(zip([col[0] for col in desc], row)) for row in rows]
        
    def get_policy_override_role_purpose_data_retentions(self, policy_purpose_data_element_id=None, external_role_id=None):
        """Get policy override role purpose data retentions for specific policy_purpose_data_element_id and external_role_id."""
        cursor = self.connection.cursor()
        query = '''
            SELECT o.*, p.policy_id, p.purpose_id, p.data_element_id, 
                   pol.name as policy_name, pur.name as purpose_name, de.name as data_element_name,
                   er.name as role_name, er.source_system
            FROM policy_override_role_purpose_data_retention o
            JOIN policy_purpose_data_element p ON o.policy_purpose_data_element_id = p.id
            JOIN policies pol ON p.policy_id = pol.id
            JOIN purposes pur ON p.purpose_id = pur.id
            JOIN data_elements de ON p.data_element_id = de.id
            JOIN external_roles er ON o.external_role_id = er.id
            WHERE 1=1
        '''
        params = []
        
        if policy_purpose_data_element_id is not None:
            query += ' AND o.policy_purpose_data_element_id = %s'
            params.append(policy_purpose_data_element_id)
            
        if external_role_id is not None:
            query += ' AND o.external_role_id = %s'
            params.append(external_role_id)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        desc = cursor.description
        cursor.close()
        return [dict(zip([col[0] for col in desc], row)) for row in rows]

    def delete_policy_override_role_purpose_data_retention(self, override_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM policy_override_role_purpose_data_retention WHERE id = %s', (override_id,))
        self.connection.commit()
        cursor.close()

    # --- CRUD for Data Security Override ---
    def add_policy_override_role_purpose_data_security(self, policy_purpose_data_element_id, external_role_id, security_rule_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO policy_override_role_purpose_data_security (policy_purpose_data_element_id, external_role_id, security_rule_id)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE policy_purpose_data_element_id=VALUES(policy_purpose_data_element_id)
        ''', (policy_purpose_data_element_id, external_role_id, security_rule_id))
        self.connection.commit()
        cursor.close()

    def get_all_policy_override_role_purpose_data_security(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM policy_override_role_purpose_data_security')
        rows = cursor.fetchall()
        desc = cursor.description
        cursor.close()
        return [dict(zip([col[0] for col in desc], row)) for row in rows]
        
    def get_policy_override_role_purpose_data_security(self, policy_purpose_data_element_id=None, external_role_id=None):
        """Get policy override role purpose data security for specific policy_purpose_data_element_id and external_role_id."""
        cursor = self.connection.cursor()
        query = '''
            SELECT o.*, p.policy_id, p.purpose_id, p.data_element_id, 
                   pol.name as policy_name, pur.name as purpose_name, de.name as data_element_name,
                   er.name as role_name, er.source_system, sr.*
            FROM policy_override_role_purpose_data_security o
            JOIN policy_purpose_data_element p ON o.policy_purpose_data_element_id = p.id
            JOIN policies pol ON p.policy_id = pol.id
            JOIN purposes pur ON p.purpose_id = pur.id
            JOIN data_elements de ON p.data_element_id = de.id
            JOIN external_roles er ON o.external_role_id = er.id
            JOIN security_rules sr ON o.security_rule_id = sr.id
            WHERE 1=1
        '''
        params = []
        
        if policy_purpose_data_element_id is not None:
            query += ' AND o.policy_purpose_data_element_id = %s'
            params.append(policy_purpose_data_element_id)
            
        if external_role_id is not None:
            query += ' AND o.external_role_id = %s'
            params.append(external_role_id)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        desc = cursor.description
        cursor.close()
        return [dict(zip([col[0] for col in desc], row)) for row in rows]

    def delete_policy_override_role_purpose_data_security(self, override_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM policy_override_role_purpose_data_security WHERE id = %s', (override_id,))
        self.connection.commit()
        cursor.close()        
        
    def setup_tables(self):
        """Create all the necessary tables for the regulatory metadata if they don't exist."""
        self.create_law_jurisdiction_table()
        self.create_law_legal_basis_table()
        self.create_law_incident_breach_guidance_table()
        self.create_data_category_data_element_table()
        self.create_law_data_subject_type_data_element_sensitivity_table()
        self.create_law_data_subject_type_data_category_sensitivity_table()
        self.create_data_subject_type_data_category_sensitivity_table()
        self.create_data_subject_type_data_element_sensitivity_table()
        self.create_law_transfer_table()
        self.create_law_data_subject_access_request_notification_requirements_table()
        self.create_law_purpose_category_legal_basis_table()
        self.create_legal_basis_requirements_table()
        self.create_data_subject_right_implementation_steps_table()
        self.create_data_subject_right_exemptions_table()
        self.create_policy_purpose_table()
        self.create_policy_purpose_data_element_table()
        self.create_policy_purpose_data_usage_table()
        self.create_policy_purpose_data_retention_table()
        self.create_policy_purpose_data_security_table()
        self.create_framework_control_table()
        self.create_policy_control_table()
        self.create_risk_control_table()
        
    def create_law_jurisdiction_table(self):
        """Create the Law Jurisdiction table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_jurisdiction` (
            `law_id` INT NOT NULL,
            `jurisdiction_id` INT NOT NULL,
            PRIMARY KEY (`law_id`, `jurisdiction_id`),
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`jurisdiction_id`) REFERENCES `jurisdiction`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_law_legal_basis_table(self):
        """Create the Law Legal Basis table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_legal_basis` (
            `law_id` INT NOT NULL,
            `legal_basis_id` INT NOT NULL,
            PRIMARY KEY (`law_id`, `legal_basis_id`),
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`legal_basis_id`) REFERENCES `legal_basis`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_law_incident_breach_guidance_table(self):
        """Create the Law Incident Breach Guidance table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_incident_breach_guidance` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `threshold` VARCHAR(255),
            `timeframe` VARCHAR(255),
            `authority` VARCHAR(255),
            `content` TEXT,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_data_category_data_element_table(self):
        """Create the Data Category Data Element table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_category_data_element` (
            `data_category_id` INT NOT NULL,
            `data_element_id` INT NOT NULL,
            PRIMARY KEY (`data_category_id`, `data_element_id`),
            FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_law_data_subject_type_data_element_sensitivity_table(self):
        """Create the Law Data Subject Type Data Element Sensitivity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_data_subject_type_data_element_sensitivity` (
            `law_id` INT NOT NULL,
            `data_subject_type_id` INT NOT NULL,
            `data_element_id` INT NOT NULL,
            `sensitivity_id` INT NOT NULL,
            PRIMARY KEY (`law_id`, `data_subject_type_id`, `data_element_id`, `sensitivity_id`),
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_law_data_subject_type_data_category_sensitivity_table(self):
        """Create the Law Data Subject Type Data Category Sensitivity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_data_subject_type_data_category_sensitivity` (
            `law_id` INT NOT NULL,
            `data_subject_type_id` INT NOT NULL,
            `data_category_id` INT NOT NULL,
            `sensitivity_id` INT NOT NULL,
            PRIMARY KEY (`law_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`),
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def create_data_subject_type_data_category_sensitivity_table(self):
        """Create the Data Subject Type Data Category Sensitivity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_subject_type_data_category_sensitivity` (
            `data_subject_type_id` INT NOT NULL,
            `data_category_id` INT NOT NULL,
            `sensitivity_id` INT NOT NULL,
            PRIMARY KEY (`data_subject_type_id`, `data_category_id`, `sensitivity_id`),
            FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_data_subject_type_data_element_sensitivity_table(self):
        """Create the Data Subject Type Data Element Sensitivity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_subject_type_data_element_sensitivity` (
            `data_subject_type_id` INT NOT NULL,
            `data_element_id` INT NOT NULL,
            `sensitivity_id` INT NOT NULL,
            PRIMARY KEY (`data_subject_type_id`, `data_element_id`, `sensitivity_id`),
            FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        

        
    def create_law_transfer_table(self):
        """Create the Law Transfer table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_transfer` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `adequacy_countries` TEXT,
            `transfer_mechanisms` TEXT,
            `additional_requirements` TEXT,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_law_data_subject_access_request_notification_requirements_table(self):
        """Create the Law Data Subject Access Request Notification Requirements table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_data_subject_access_request_notification_requirements` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `conditions` TEXT,
            `timeframe` VARCHAR(255),
            `exemptions` TEXT,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_law_purpose_category_legal_basis_table(self):
        """Create the Law Purpose Category Legal Basis table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_purpose_category_legal_basis` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `purpose_category_id` INT NOT NULL,
            `legal_basis_id` INT NOT NULL,
            `preference_order` INT DEFAULT 1,
            `description` TEXT,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`purpose_category_id`) REFERENCES `purpose_category`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`legal_basis_id`) REFERENCES `legal_basis`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `unique_law_purpose_legal_basis` (`law_id`, `purpose_category_id`, `legal_basis_id`)
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_legal_basis_requirements_table(self):
        """Create the Legal Basis Requirements table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `legal_basis_requirements` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `legal_basis_id` INT NOT NULL,
            `requirement` TEXT NOT NULL,
            FOREIGN KEY (`legal_basis_id`) REFERENCES `legal_basis`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_data_subject_right_implementation_steps_table(self):
        """Create the Data Subject Right Implementation Steps table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_subject_right_implementation_steps` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `right_type` VARCHAR(255) NOT NULL,
            `step_order` INT NOT NULL,
            `description` TEXT NOT NULL,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `unique_law_right_step` (`law_id`, `right_type`, `step_order`)
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_data_subject_right_exemptions_table(self):
        """Create the Data Subject Right Exemptions table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_subject_right_exemptions` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `right_type` VARCHAR(255) NOT NULL,
            `exemption` TEXT NOT NULL,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_policy_purpose_data_security_table(self):
        """Create the Policy Purpose Data Security table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_purpose_data_security` (
            `policy_id`            INT         NOT NULL,
            `purpose_id`           INT         NOT NULL,
            `data_element_id`      INT         NOT NULL,
            `encryption_required`  BOOLEAN     NOT NULL DEFAULT FALSE,
            `encryption_algorithm` VARCHAR(100),
            `masking_required`     BOOLEAN     NOT NULL DEFAULT FALSE,
            `masking_format`       VARCHAR(100),
            `access_logging`       BOOLEAN     NOT NULL DEFAULT FALSE,
            PRIMARY KEY (`policy_id`,`purpose_id`,`data_element_id`),
            FOREIGN KEY (`policy_id`)       REFERENCES `policy`(`id`)            ON DELETE CASCADE,
            FOREIGN KEY (`purpose_id`)      REFERENCES `purpose`(`id`)           ON DELETE CASCADE,
            FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`)       ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def add_policy_purpose_data_security(self, policy_purpose_data_element_id, encryption_required, encryption_algorithm, masking_required, masking_format, access_logging):
        """Add a new policy purpose data security rule.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy_purpose_data_element
            encryption_required (bool): Whether encryption is required
            encryption_algorithm (str): The encryption algorithm to use
            masking_required (bool): Whether masking is required
            masking_format (str): The masking format to use
            access_logging (bool): Whether access logging is required
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO policy_purpose_data_security
            (policy_purpose_data_element_id, encryption_required, encryption_algorithm, masking_required, masking_format, access_logging)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (policy_purpose_data_element_id, encryption_required, encryption_algorithm, masking_required, masking_format, access_logging))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding policy purpose data security: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def get_policy_purpose_data_security(self, policy_id=None, purpose_id=None, data_element_id=None):
        """Retrieve policy purpose data security rules with optional filters."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT p.name as policy_name, pu.name as purpose_name, de.name as data_element_name,
                   s.encryption_required, s.encryption_algorithm, s.masking_required, s.masking_format, s.access_logging
            FROM policy_purpose_data_security s
            JOIN policy_purpose_data_element ppde ON s.policy_purpose_data_element_id = ppde.id
            JOIN policy p ON ppde.policy_id = p.id
            JOIN purpose pu ON ppde.purpose_id = pu.id
            JOIN data_element de ON ppde.data_element_id = de.id
            WHERE 1=1
            """
            params = []
            if policy_id:
                query += " AND ppde.policy_id = %s"
                params.append(policy_id)
            if purpose_id:
                query += " AND ppde.purpose_id = %s"
                params.append(purpose_id)
            if data_element_id:
                query += " AND ppde.data_element_id = %s"
                params.append(data_element_id)
            cursor.execute(query, params)
            results = []
            for row in cursor.fetchall():
                results.append({
                    "policy_name": row[0],
                    "purpose_name": row[1],
                    "data_element_name": row[2],
                    "encryption_required": row[3],
                    "encryption_algorithm": row[4],
                    "masking_required": row[5],
                    "masking_format": row[6],
                    "access_logging": row[7]
                })
            return results
        except Exception as e:
            print(f"Error getting policy purpose data security: {e}")
            return []
        finally:
            cursor.close()
            
    def get_policy_purpose_data_retentions(self, policy_purpose_data_element_id=None):
        """Get policy purpose data retention information."""
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT ppdr.id, ppdr.policy_purpose_data_element_id, ppdr.retention_period, ppdr.retention_basis, 
                       ppdr.exceptions, ppde.policy_id, p.name as policy_name, ppde.purpose_id, pu.name as purpose_name, 
                       ppde.data_element_id, de.name as data_element_name
                FROM policy_purpose_data_retention ppdr
                JOIN policy_purpose_data_element ppde ON ppdr.policy_purpose_data_element_id = ppde.id
                JOIN policy p ON ppde.policy_id = p.id
                JOIN purpose pu ON ppde.purpose_id = pu.id
                JOIN data_element de ON ppde.data_element_id = de.id
            """
            params = []
            
            if policy_purpose_data_element_id:
                query += " WHERE ppdr.policy_purpose_data_element_id = %s"
                params.append(policy_purpose_data_element_id)
                
            cursor.execute(query, params)
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'policy_purpose_data_element_id': row[1],
                    'retention_period': row[2],
                    'retention_basis': row[3],
                    'exceptions': row[4],
                    'policy_id': row[5],
                    'policy_name': row[6],
                    'purpose_id': row[7],
                    'purpose_name': row[8],
                    'data_element_id': row[9],
                    'data_element_name': row[10]
                })
            return results
        except Exception as e:
            print(f"Error getting policy purpose data retentions: {e}")
            return []
        finally:
            cursor.close()

    # Methods for the new policy_data_element tables
    
    def get_policy_data_element_usage(self, policy_id=None, data_element_id=None):
        """Get policy data element usage information.
        
        Args:
            policy_id: Optional policy ID to filter by
            data_element_id: Optional data element ID to filter by
            
        Returns:
            List of dictionaries containing policy data element usage information
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT pdeu.id, pdeu.policy_id, p.name as policy_name, pdeu.data_element_id, 
                       de.name as data_element_name, pdeu.operation, pdeu.allowed, pdeu.restrictions
                FROM policy_data_element_usage pdeu
                JOIN policy p ON pdeu.policy_id = p.id
                JOIN data_element de ON pdeu.data_element_id = de.id
            """
            params = []
            conditions = []
            
            if policy_id:
                conditions.append("pdeu.policy_id = %s")
                params.append(policy_id)
                
            if data_element_id:
                conditions.append("pdeu.data_element_id = %s")
                params.append(data_element_id)
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            cursor.execute(query, params)
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'policy_id': row[1],
                    'policy_name': row[2],
                    'data_element_id': row[3],
                    'data_element_name': row[4],
                    'operation': row[5],
                    'allowed': bool(row[6]),
                    'restrictions': row[7]
                })
            return results
        except Exception as e:
            print(f"Error getting policy data element usage: {e}")
            return []
        finally:
            cursor.close()
    
    def get_policy_data_element_retention(self, policy_id=None, data_element_id=None):
        """Get policy data element retention information.
        
        Args:
            policy_id: Optional policy ID to filter by
            data_element_id: Optional data element ID to filter by
            
        Returns:
            List of dictionaries containing policy data element retention information
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT pder.id, pder.policy_id, p.name as policy_name, pder.data_element_id, 
                       de.name as data_element_name, pder.retention_period, pder.retention_basis, pder.exceptions
                FROM policy_data_element_retention pder
                JOIN policy p ON pder.policy_id = p.id
                JOIN data_element de ON pder.data_element_id = de.id
            """
            params = []
            conditions = []
            
            if policy_id:
                conditions.append("pder.policy_id = %s")
                params.append(policy_id)
                
            if data_element_id:
                conditions.append("pder.data_element_id = %s")
                params.append(data_element_id)
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            cursor.execute(query, params)
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'policy_id': row[1],
                    'policy_name': row[2],
                    'data_element_id': row[3],
                    'data_element_name': row[4],
                    'retention_period': row[5],
                    'retention_basis': row[6],
                    'exceptions': row[7]
                })
            return results
        except Exception as e:
            print(f"Error getting policy data element retention: {e}")
            return []
        finally:
            cursor.close()
    
    def get_policy_data_element_security(self, policy_id=None, data_element_id=None):
        """Get policy data element security information.
        
        Args:
            policy_id: Optional policy ID to filter by
            data_element_id: Optional data element ID to filter by
            
        Returns:
            List of dictionaries containing policy data element security information
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT pdes.id, pdes.policy_id, p.name as policy_name, pdes.data_element_id, 
                       de.name as data_element_name, pdes.requires_encryption, pdes.encryption_algorithm,
                       pdes.requires_masking, pdes.masking_format, pdes.requires_access_control, pdes.access_control_type
                FROM policy_data_element_security pdes
                JOIN policy p ON pdes.policy_id = p.id
                JOIN data_element de ON pdes.data_element_id = de.id
            """
            params = []
            conditions = []
            
            if policy_id:
                conditions.append("pdes.policy_id = %s")
                params.append(policy_id)
                
            if data_element_id:
                conditions.append("pdes.data_element_id = %s")
                params.append(data_element_id)
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            cursor.execute(query, params)
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'policy_id': row[1],
                    'policy_name': row[2],
                    'data_element_id': row[3],
                    'data_element_name': row[4],
                    'requires_encryption': bool(row[5]),
                    'encryption_algorithm': row[6],
                    'requires_masking': bool(row[7]),
                    'masking_format': row[8],
                    'requires_access_control': bool(row[9]),
                    'access_control_type': row[10]
                })
            return results
        except Exception as e:
            print(f"Error getting policy data element security: {e}")
            return []
        finally:
            cursor.close()
        
    def get_data_element_policies(self, data_element_id):
        """Get all policies associated with a data element across all policy types.
        
        Args:
            data_element_id: The data element ID to get policies for
            
        Returns:
            Dictionary containing usage, retention, and security policies for the data element
        """
        usage_policies = self.get_policy_data_element_usage(data_element_id=data_element_id)
        retention_policies = self.get_policy_data_element_retention(data_element_id=data_element_id)
        security_policies = self.get_policy_data_element_security(data_element_id=data_element_id)
        
        return {
            'usage': usage_policies,
            'retention': retention_policies,
            'security': security_policies
        }
    
    # Law Jurisdiction methods
    def add_law_jurisdiction(self, law_id, jurisdiction_id):
        """Add a new law-jurisdiction relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_jurisdiction (law_id, jurisdiction_id)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (law_id, jurisdiction_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law-jurisdiction relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_law_jurisdictions(self, law_id=None):
        """Get all law-jurisdiction relationships from the database.
        If law_id is provided, only get relationships for that law."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if law_id:
                query = """
                SELECT lj.law_id, lj.jurisdiction_id, l.name as law_name, j.name as jurisdiction_name
                FROM law_jurisdiction lj
                JOIN law l ON lj.law_id = l.id
                JOIN jurisdiction j ON lj.jurisdiction_id = j.id
                WHERE lj.law_id = %s;
                """
                cursor.execute(query, (law_id,))
            else:
                query = """
                SELECT lj.law_id, lj.jurisdiction_id, l.name as law_name, j.name as jurisdiction_name
                FROM law_jurisdiction lj
                JOIN law l ON lj.law_id = l.id
                JOIN jurisdiction j ON lj.jurisdiction_id = j.id;
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law-jurisdiction relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def get_jurisdiction_laws(self, jurisdiction_id):
        """Get all laws for a specific jurisdiction."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT lj.law_id, lj.jurisdiction_id, l.name as law_name, j.name as jurisdiction_name
            FROM law_jurisdiction lj
            JOIN law l ON lj.law_id = l.id
            JOIN jurisdiction j ON lj.jurisdiction_id = j.id
            WHERE lj.jurisdiction_id = %s;
            """
            cursor.execute(query, (jurisdiction_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving laws for jurisdiction ID {jurisdiction_id}: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_law_jurisdiction(self, law_id, jurisdiction_id):
        """Delete a law-jurisdiction relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM law_jurisdiction WHERE law_id = %s AND jurisdiction_id = %s;"
            cursor.execute(delete_query, (law_id, jurisdiction_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law-jurisdiction relationship: {e}")
            return False
        finally:
            cursor.close()
    
    # Seed data methods
    def seed_law_jurisdictions(self):
        """Seed the database with initial law-jurisdiction data."""
        law_jurisdictions = [
            {"law_name": "GDPR", "jurisdiction_name": "European Union"},
            {"law_name": "CCPA", "jurisdiction_name": "California, USA"},
            {"law_name": "CPRA", "jurisdiction_name": "California, USA"},
            {"law_name": "LGPD", "jurisdiction_name": "Brazil"},
            {"law_name": "PIPEDA", "jurisdiction_name": "Canada"},
            {"law_name": "GDPR", "jurisdiction_name": "United Kingdom"} # UK still follows GDPR principles post-Brexit
        ]
        
        # Get law and jurisdiction IDs from their names
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        for relation in law_jurisdictions:
            try:
                # Get law ID
                cursor.execute("SELECT id FROM law WHERE name = %s;", (relation["law_name"],))
                law_result = cursor.fetchone()
                if not law_result:
                    print(f"Law '{relation['law_name']}' not found.")
                    continue
                law_id = law_result["id"]
                
                # Get jurisdiction ID
                cursor.execute("SELECT id FROM jurisdiction WHERE name = %s;", (relation["jurisdiction_name"],))
                jurisdiction_result = cursor.fetchone()
                if not jurisdiction_result:
                    print(f"Jurisdiction '{relation['jurisdiction_name']}' not found.")
                    continue
                jurisdiction_id = jurisdiction_result["id"]
                
                # Add the relationship
                self.add_law_jurisdiction(law_id, jurisdiction_id)
            except Exception as e:
                print(f"Error seeding law-jurisdiction relationship: {e}")
        
        cursor.close()
    
    # Law Legal Basis methods
    def add_law_legal_basis(self, law_id, legal_basis_id):
        """Add a new law-legal basis relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_legal_basis (law_id, legal_basis_id)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (law_id, legal_basis_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law-legal basis relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_law_legal_bases(self, law_id=None):
        """Get all law-legal basis relationships from the database.
        If law_id is provided, only get relationships for that law."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if law_id:
                query = """
                SELECT llb.law_id, llb.legal_basis_id, l.name as law_name, lb.name as legal_basis_name, lb.description as legal_basis_description
                FROM law_legal_basis llb
                JOIN law l ON llb.law_id = l.id
                JOIN legal_basis lb ON llb.legal_basis_id = lb.id
                WHERE llb.law_id = %s;
                """
                cursor.execute(query, (law_id,))
            else:
                query = """
                SELECT llb.law_id, llb.legal_basis_id, l.name as law_name, lb.name as legal_basis_name, lb.description as legal_basis_description
                FROM law_legal_basis llb
                JOIN law l ON llb.law_id = l.id
                JOIN legal_basis lb ON llb.legal_basis_id = lb.id;
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law-legal basis relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_law_legal_basis(self, law_id, legal_basis_id):
        """Delete a law-legal basis relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM law_legal_basis WHERE law_id = %s AND legal_basis_id = %s;"
            cursor.execute(delete_query, (law_id, legal_basis_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law-legal basis relationship: {e}")
            return False
        finally:
            cursor.close()
    
    # Law Incident Breach Guidance methods
    def add_law_incident_breach_guidance(self, law_id, threshold, timeframe, authority, content):
        """Add a new law incident breach guidance to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_incident_breach_guidance (law_id, threshold, timeframe, authority, content)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, threshold, timeframe, authority, content))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law incident breach guidance: {e}")
            return None
        finally:
            cursor.close()
    
    def get_law_incident_breach_guidances(self, law_id=None):
        """Get all law incident breach guidances from the database.
        If law_id is provided, only get guidances for that law."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if law_id:
                query = """
                SELECT libg.id, libg.law_id, l.name as law_name, libg.threshold, libg.timeframe, libg.authority, libg.content
                FROM law_incident_breach_guidance libg
                JOIN law l ON libg.law_id = l.id
                WHERE libg.law_id = %s;
                """
                cursor.execute(query, (law_id,))
            else:
                query = """
                SELECT libg.id, libg.law_id, l.name as law_name, libg.threshold, libg.timeframe, libg.authority, libg.content
                FROM law_incident_breach_guidance libg
                JOIN law l ON libg.law_id = l.id;
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law incident breach guidances: {e}")
            return []
        finally:
            cursor.close()
    
    def update_law_incident_breach_guidance(self, guidance_id, threshold, timeframe, authority, content):
        """Update an existing law incident breach guidance."""
        cursor = self.connection.cursor()
        try:
            update_query = """
            UPDATE law_incident_breach_guidance
            SET threshold = %s, timeframe = %s, authority = %s, content = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (threshold, timeframe, authority, content, guidance_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating law incident breach guidance: {e}")
            return False
        finally:
            cursor.close()
    
    def delete_law_incident_breach_guidance(self, guidance_id):
        """Delete a law incident breach guidance from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM law_incident_breach_guidance WHERE id = %s;"
            cursor.execute(delete_query, (guidance_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law incident breach guidance: {e}")
            return False
        finally:
            cursor.close()
    
    # Seed methods for law legal basis and breach notification
    def seed_law_legal_bases(self):
        """Seed the database with initial law-legal basis data."""
        law_legal_bases = [
            {"law_name": "GDPR", "legal_basis_name": "Consent"},
            {"law_name": "GDPR", "legal_basis_name": "Contract"},
            {"law_name": "GDPR", "legal_basis_name": "Legal Obligation"},
            {"law_name": "GDPR", "legal_basis_name": "Vital Interests"},
            {"law_name": "GDPR", "legal_basis_name": "Public Task"},
            {"law_name": "GDPR", "legal_basis_name": "Legitimate Interests"},
            {"law_name": "CCPA", "legal_basis_name": "Consent"},
            {"law_name": "CCPA", "legal_basis_name": "Contract"},
            {"law_name": "LGPD", "legal_basis_name": "Consent"},
            {"law_name": "LGPD", "legal_basis_name": "Legal Obligation"},
            {"law_name": "LGPD", "legal_basis_name": "Legitimate Interests"},
            {"law_name": "PIPEDA", "legal_basis_name": "Consent"},
            {"law_name": "PIPEDA", "legal_basis_name": "Legal Obligation"}
        ]
        
        # Get law and legal basis IDs from their names
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        for relation in law_legal_bases:
            try:
                # Get law ID
                cursor.execute("SELECT id FROM law WHERE name = %s;", (relation["law_name"],))
                law_result = cursor.fetchone()
                if not law_result:
                    print(f"Law '{relation['law_name']}' not found.")
                    continue
                law_id = law_result["id"]
                
                # Get legal basis ID
                cursor.execute("SELECT id FROM legal_basis WHERE name = %s;", (relation["legal_basis_name"],))
                legal_basis_result = cursor.fetchone()
                if not legal_basis_result:
                    print(f"Legal basis '{relation['legal_basis_name']}' not found.")
                    continue
                legal_basis_id = legal_basis_result["id"]
                
                # Add the relationship
                self.add_law_legal_basis(law_id, legal_basis_id)
            except Exception as e:
                print(f"Error seeding law-legal basis relationship: {e}")
        
        cursor.close()
    
    def seed_law_incident_breach_guidances(self):
        """Seed the database with initial law incident breach guidance data."""
        law_incident_breach_guidances = [
            {
                "law_name": "GDPR",
                "threshold": "Any breach that poses a risk to the rights and freedoms of individuals",
                "timeframe": "72 hours",
                "authority": "Supervisory Authority",
                "content": "Under GDPR, organizations must notify the relevant supervisory authority of a personal data breach within 72 hours of becoming aware of it, unless the breach is unlikely to result in a risk to the rights and freedoms of individuals. The notification must include the nature of the breach, categories of data, approximate number of data subjects affected, likely consequences, and measures taken to address the breach."
            },
            {
                "law_name": "CCPA",
                "threshold": "Unauthorized acquisition of unencrypted personal information",
                "timeframe": "Most expedient time possible",
                "authority": "California Attorney General",
                "content": "The CCPA does not explicitly include breach notification requirements, but California has a separate breach notification law (California Civil Code 1798.82) that requires businesses to notify California residents when their unencrypted personal information was acquired by an unauthorized person."
            },
            {
                "law_name": "LGPD",
                "threshold": "Security incidents that may result in risk or damage to data subjects",
                "timeframe": "Reasonable time period",
                "authority": "National Data Protection Authority (ANPD)",
                "content": "Under LGPD, data controllers must report data breaches that may result in risk or damage to data subjects to the ANPD within a reasonable time period. The notification must include a description of the affected data, information about the data subjects involved, security measures used, risks related to the incident, and measures taken to reverse or mitigate the effects of the damage."
            },
            {
                "law_name": "PIPEDA",
                "threshold": "Breach of security safeguards involving personal information that poses a real risk of significant harm",
                "timeframe": "As soon as feasible",
                "authority": "Privacy Commissioner of Canada",
                "content": "Under PIPEDA, organizations must report to the Privacy Commissioner of Canada any breach of security safeguards involving personal information under their control if it is reasonable to believe that the breach creates a real risk of significant harm to an individual. Organizations must also notify affected individuals and keep records of all breaches."
            }
        ]
        
        # Get law IDs from their names
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        for guidance in law_incident_breach_guidances:
            try:
                # Get law ID
                cursor.execute("SELECT id FROM law WHERE name = %s;", (guidance["law_name"],))
                law_result = cursor.fetchone()
                if not law_result:
                    print(f"Law '{guidance['law_name']}' not found.")
                    continue
                law_id = law_result["id"]
                
                # Add the guidance
                self.add_law_incident_breach_guidance(
                    law_id,
                    guidance["threshold"],
                    guidance["timeframe"],
                    guidance["authority"],
                    guidance["content"]
                )
            except Exception as e:
                print(f"Error seeding law incident breach guidance: {e}")
        
        cursor.close()
        
    # Law Transfer methods
    def add_law_transfer(self, law_id, adequacy_countries, transfer_mechanisms, additional_requirements):
        """Add a new law transfer to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_transfer (law_id, adequacy_countries, transfer_mechanisms, additional_requirements)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, adequacy_countries, transfer_mechanisms, additional_requirements))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law transfer: {e}")
            return None
        finally:
            cursor.close()
    
    def get_law_transfers(self, law_id=None):
        """Get all law transfers from the database.
        If law_id is provided, only get transfers for that law."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if law_id:
                query = """
                SELECT lt.id, lt.law_id, l.name as law_name, lt.adequacy_countries, lt.transfer_mechanisms, lt.additional_requirements
                FROM law_transfer lt
                JOIN law l ON lt.law_id = l.id
                WHERE lt.law_id = %s;
                """
                cursor.execute(query, (law_id,))
            else:
                query = """
                SELECT lt.id, lt.law_id, l.name as law_name, lt.adequacy_countries, lt.transfer_mechanisms, lt.additional_requirements
                FROM law_transfer lt
                JOIN law l ON lt.law_id = l.id;
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law transfers: {e}")
            return []
        finally:
            cursor.close()
    
    def update_law_transfer(self, transfer_id, adequacy_countries, transfer_mechanisms, additional_requirements):
        """Update an existing law transfer."""
        cursor = self.connection.cursor()
        try:
            update_query = """
            UPDATE law_transfer
            SET adequacy_countries = %s, transfer_mechanisms = %s, additional_requirements = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (adequacy_countries, transfer_mechanisms, additional_requirements, transfer_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating law transfer: {e}")
            return False
        finally:
            cursor.close()
    
    def delete_law_transfer(self, transfer_id):
        """Delete a law transfer from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM law_transfer WHERE id = %s;"
            cursor.execute(delete_query, (transfer_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law transfer: {e}")
            return False
        finally:
            cursor.close()
    
    # Law Data Subject Access Request Notification Requirements methods
    def add_law_data_subject_access_request_notification_requirement(self, law_id, name, description, conditions, timeframe, exemptions):
        """Add a new law data subject access request notification requirement to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_data_subject_access_request_notification_requirements 
            (law_id, name, description, conditions, timeframe, exemptions)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, name, description, conditions, timeframe, exemptions))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law data subject access request notification requirement: {e}")
            return None
        finally:
            cursor.close()
    
    def get_law_data_subject_access_request_notification_requirements(self, law_id=None):
        """Get all law data subject access request notification requirements from the database.
        If law_id is provided, only get requirements for that law."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if law_id:
                query = """
                SELECT ldsarnr.id, ldsarnr.law_id, l.name as law_name, ldsarnr.name, ldsarnr.description, 
                       ldsarnr.conditions, ldsarnr.timeframe, ldsarnr.exemptions
                FROM law_data_subject_access_request_notification_requirements ldsarnr
                JOIN law l ON ldsarnr.law_id = l.id
                WHERE ldsarnr.law_id = %s;
                """
                cursor.execute(query, (law_id,))
            else:
                query = """
                SELECT ldsarnr.id, ldsarnr.law_id, l.name as law_name, ldsarnr.name, ldsarnr.description, 
                       ldsarnr.conditions, ldsarnr.timeframe, ldsarnr.exemptions
                FROM law_data_subject_access_request_notification_requirements ldsarnr
                JOIN law l ON ldsarnr.law_id = l.id;
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law data subject access request notification requirements: {e}")
            return []
        finally:
            cursor.close()
    
    def update_law_data_subject_access_request_notification_requirement(self, requirement_id, name, description, conditions, timeframe, exemptions):
        """Update an existing law data subject access request notification requirement."""
        cursor = self.connection.cursor()
        try:
            update_query = """
            UPDATE law_data_subject_access_request_notification_requirements
            SET name = %s, description = %s, conditions = %s, timeframe = %s, exemptions = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (name, description, conditions, timeframe, exemptions, requirement_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating law data subject access request notification requirement: {e}")
            return False
        finally:
            cursor.close()
    
    def delete_law_data_subject_access_request_notification_requirement(self, requirement_id):
        """Delete a law data subject access request notification requirement from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM law_data_subject_access_request_notification_requirements WHERE id = %s;"
            cursor.execute(delete_query, (requirement_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law data subject access request notification requirement: {e}")
            return False
        finally:
            cursor.close()
    
    def seed_law_transfers(self):
        """Seed the database with initial law transfer data."""
        law_transfers = [
            {
                "law_name": "GDPR",
                "adequacy_countries": "Andorra, Argentina, Canada (commercial organizations), Faroe Islands, Guernsey, Israel, Isle of Man, Japan, Jersey, New Zealand, Republic of Korea, Switzerland, United Kingdom, Uruguay",
                "transfer_mechanisms": "Standard Contractual Clauses (SCCs), Binding Corporate Rules (BCRs), Codes of Conduct, Certification Mechanisms",
                "additional_requirements": "Transfer Impact Assessment (TIA), Supplementary Measures"
            },
            {
                "law_name": "LGPD",
                "adequacy_countries": "Countries with adequate level of protection as determined by ANPD",
                "transfer_mechanisms": "Standard Contractual Clauses, Binding Corporate Rules, Codes of Conduct, Certification, Specific Contractual Clauses",
                "additional_requirements": "Specific authorization from the ANPD may be required"
            },
            {
                "law_name": "PIPEDA",
                "adequacy_countries": "Countries with substantially similar legislation",
                "transfer_mechanisms": "Contractual or other means",
                "additional_requirements": None
            },
            {
                "law_name": "CCPA",
                "adequacy_countries": None,
                "transfer_mechanisms": "Service provider contracts",
                "additional_requirements": None
            }
        ]
        
        # Get law IDs from their names
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        for transfer in law_transfers:
            try:
                # Get law ID
                cursor.execute("SELECT id FROM law WHERE name = %s;", (transfer["law_name"],))
                law_result = cursor.fetchone()
                if not law_result:
                    print(f"Law '{transfer['law_name']}' not found.")
                    continue
                law_id = law_result["id"]
                
                # Add the transfer
                self.add_law_transfer(
                    law_id,
                    transfer["adequacy_countries"],
                    transfer["transfer_mechanisms"],
                    transfer["additional_requirements"]
                )
            except Exception as e:
                print(f"Error seeding law transfer: {e}")
        
        cursor.close()
    
    def seed_law_data_subject_access_request_notification_requirements(self):
        """Seed the database with initial law data subject access request notification requirements data."""
        requirements = [
            {
                "law_name": "GDPR",
                "name": "Right of Access",
                "description": "Data subjects have the right to obtain confirmation as to whether personal data concerning them is being processed, and if so, access to that data.",
                "conditions": "Valid identification may be required to verify the identity of the requestor.",
                "timeframe": "1 month (can be extended by 2 additional months where necessary)",
                "exemptions": "Requests that are manifestly unfounded or excessive; legal prohibitions; adversely affecting rights of others"
            },
            {
                "law_name": "GDPR",
                "name": "Right to Rectification",
                "description": "Data subjects have the right to have inaccurate personal data rectified or completed if it is incomplete.",
                "conditions": "Requestor must specify what data is inaccurate and provide correct information.",
                "timeframe": "1 month (can be extended by 2 additional months where necessary)",
                "exemptions": "Requests that are manifestly unfounded or excessive"
            },
            {
                "law_name": "GDPR",
                "name": "Right to Erasure",
                "description": "Data subjects have the right to have personal data erased in certain circumstances.",
                "conditions": "Applies when: data is no longer necessary, consent is withdrawn, subject objects, data unlawfully processed, legal obligation.",
                "timeframe": "1 month (can be extended by 2 additional months where necessary)",
                "exemptions": "Legal obligation to keep data; public interest; legal claims"
            },
            {
                "law_name": "CCPA",
                "name": "Right to Know",
                "description": "Consumers have the right to request that a business disclose what personal information it collects, uses, shares, or sells.",
                "conditions": "Verifiable consumer request required.",
                "timeframe": "45 days (can be extended by additional 45 days where necessary)",
                "exemptions": "Requests that are manifestly unfounded or excessive; cannot verify identity"
            },
            {
                "law_name": "CCPA",
                "name": "Right to Delete",
                "description": "Consumers have the right to request that a business delete personal information about them.",
                "conditions": "Verifiable consumer request required.",
                "timeframe": "45 days (can be extended by additional 45 days where necessary)",
                "exemptions": "Certain business purposes; legal obligations; security purposes"
            },
            {
                "law_name": "LGPD",
                "name": "Right of Access",
                "description": "Data subjects have the right to obtain confirmation of the existence of processing and access to their personal data.",
                "conditions": "Valid identification may be required.",
                "timeframe": "Immediately (simplified format) or 15 days (complete declaration)",
                "exemptions": "Commercial and industrial secrets"
            },
            {
                "law_name": "PIPEDA",
                "name": "Right of Access",
                "description": "Individuals have the right to access their personal information held by an organization.",
                "conditions": "Request must be in writing; reasonable assistance must be provided.",
                "timeframe": "30 days (can be extended where necessary)",
                "exemptions": "Legal privilege; confidential commercial information; would reveal third-party information"
            }
        ]
        
        # Get law IDs from their names
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        for req in requirements:
            try:
                # Get law ID
                cursor.execute("SELECT id FROM law WHERE name = %s;", (req["law_name"],))
                law_result = cursor.fetchone()
                if not law_result:
                    print(f"Law '{req['law_name']}' not found.")
                    continue
                law_id = law_result["id"]
                
                # Add the requirement
                self.add_law_data_subject_access_request_notification_requirement(
                    law_id,
                    req["name"],
                    req["description"],
                    req["conditions"],
                    req["timeframe"],
                    req["exemptions"]
                )
            except Exception as e:
                print(f"Error seeding law data subject access request notification requirement: {e}")
        
        cursor.close()
        
    # Data Category Data Element methods
    def add_data_category_data_element(self, data_category_id, data_element_id):
        """Add a new data category data element relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_category_data_element (data_category_id, data_element_id)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (data_category_id, data_element_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding data category data element relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_data_category_data_elements(self, category_id=None):
        """Get all data category data element relationships from the database.
        
        Args:
            category_id: If provided, only get elements for that category.
            
        Returns:
            A list of dictionaries containing data_category_id, data_category_name, data_element_id, and data_element_name.
        """
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT dcde.data_category_id, dc.name as data_category_name, dcde.data_element_id, de.name as data_element_name
            FROM data_category_data_element dcde
            JOIN data_element de ON dcde.data_element_id = de.id
            JOIN data_category dc ON dcde.data_category_id = dc.id
            """
            
            params = []
            if category_id:
                query += " WHERE dcde.data_category_id = %s"
                params.append(category_id)
                
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "data_category_id": row[0],
                    "data_category_name": row[1],
                    "data_element_id": row[2],
                    "data_element_name": row[3]
                })
                
            return results
        except Exception as e:
            print(f"Error getting data category data elements: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_data_category_data_element(self, data_category_id, data_element_id):
        """Delete a data category data element relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM data_category_data_element WHERE data_category_id = %s AND data_element_id = %s;"
            cursor.execute(delete_query, (data_category_id, data_element_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting data category data element relationship: {e}")
            return False
        finally:
            cursor.close()
    
    # Law Data Subject Type Data Element Sensitivity methods
    def add_law_data_subject_type_data_element_sensitivity(self, law_id, data_subject_type_id, data_element_id, sensitivity_id):
        """Add a new law data subject type data element sensitivity relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_data_subject_type_data_element_sensitivity 
            (law_id, data_subject_type_id, data_element_id, sensitivity_id)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, data_subject_type_id, data_element_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law data subject type data element sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_law_data_subject_type_data_element_sensitivities(self):
        """Get all law data subject type data element sensitivity relationships from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT ldstdes.law_id, l.name as law_name, 
                   ldstdes.data_subject_type_id, dst.name as data_subject_type_name,
                   ldstdes.data_element_id, de.name as data_element_name,
                   ldstdes.sensitivity_id, s.name as sensitivity_name
            FROM law_data_subject_type_data_element_sensitivity ldstdes
            JOIN law l ON ldstdes.law_id = l.id
            JOIN data_subject_type dst ON ldstdes.data_subject_type_id = dst.id
            JOIN data_element de ON ldstdes.data_element_id = de.id
            JOIN sensitivity s ON ldstdes.sensitivity_id = s.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law data subject type data element sensitivity relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_law_data_subject_type_data_element_sensitivity(self, law_id, data_subject_type_id, data_element_id, sensitivity_id):
        """Delete a law data subject type data element sensitivity relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = """
            DELETE FROM law_data_subject_type_data_element_sensitivity 
            WHERE law_id = %s AND data_subject_type_id = %s AND data_element_id = %s AND sensitivity_id = %s;
            """
            cursor.execute(delete_query, (law_id, data_subject_type_id, data_element_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law data subject type data element sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    # Law Data Subject Type Data Category Sensitivity methods
    def add_law_data_subject_type_data_category_sensitivity(self, law_id, data_subject_type_id, data_category_id, sensitivity_id):
        """Add a new law data subject type data category sensitivity relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_data_subject_type_data_category_sensitivity 
            (law_id, data_subject_type_id, data_category_id, sensitivity_id)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_law_data_subject_type_data_category_sensitivities(self):
        """Get all law data subject type data category sensitivity relationships from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT ldstdcs.law_id, l.name as law_name, 
                   ldstdcs.data_subject_type_id, dst.name as data_subject_type_name,
                   ldstdcs.data_category_id, dc.name as data_category_name,
                   ldstdcs.sensitivity_id, s.name as sensitivity_name
            FROM law_data_subject_type_data_category_sensitivity ldstdcs
            JOIN law l ON ldstdcs.law_id = l.id
            JOIN data_subject_type dst ON ldstdcs.data_subject_type_id = dst.id
            JOIN data_category dc ON ldstdcs.data_category_id = dc.id
            JOIN sensitivity s ON ldstdcs.sensitivity_id = s.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law data subject type data category sensitivity relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_law_data_subject_type_data_category_sensitivity(self, law_id, data_subject_type_id, data_category_id, sensitivity_id):
        """Delete a law data subject type data category sensitivity relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = """
            DELETE FROM law_data_subject_type_data_category_sensitivity 
            WHERE law_id = %s AND data_subject_type_id = %s AND data_category_id = %s AND sensitivity_id = %s;
            """
            cursor.execute(delete_query, (law_id, data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    # Data Subject Type Data Category Sensitivity methods
    def add_data_subject_type_data_category_sensitivity(self, data_subject_type_id, data_category_id, sensitivity_id):
        """Add a new data subject type data category sensitivity relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_subject_type_data_category_sensitivity 
            (data_subject_type_id, data_category_id, sensitivity_id)
            VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query, (data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_data_subject_type_data_category_sensitivities(self):
        """Get all data subject type data category sensitivity relationships from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT dstdcs.data_subject_type_id, dst.name as data_subject_type_name,
                   dstdcs.data_category_id, dc.name as data_category_name,
                   dstdcs.sensitivity_id, s.name as sensitivity_name
            FROM data_subject_type_data_category_sensitivity dstdcs
            JOIN data_subject_type dst ON dstdcs.data_subject_type_id = dst.id
            JOIN data_category dc ON dstdcs.data_category_id = dc.id
            JOIN sensitivity s ON dstdcs.sensitivity_id = s.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data subject type data category sensitivity relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_data_subject_type_data_category_sensitivity(self, data_subject_type_id, data_category_id, sensitivity_id):
        """Delete a data subject type data category sensitivity relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = """
            DELETE FROM data_subject_type_data_category_sensitivity 
            WHERE data_subject_type_id = %s AND data_category_id = %s AND sensitivity_id = %s;
            """
            cursor.execute(delete_query, (data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    # Data Subject Type Data Element Sensitivity methods
    def add_data_subject_type_data_element_sensitivity(self, data_subject_type_id, data_element_id, sensitivity_id):
        """Add a new data subject type data element sensitivity relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_subject_type_data_element_sensitivity 
            (data_subject_type_id, data_element_id, sensitivity_id)
            VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query, (data_subject_type_id, data_element_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding data subject type data element sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_data_subject_type_data_element_sensitivities(self):
        """Get all data subject type data element sensitivity relationships from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT dstdes.data_subject_type_id, dst.name as data_subject_type_name,
                   dstdes.data_element_id, de.name as data_element_name,
                   dstdes.sensitivity_id, s.name as sensitivity_name
            FROM data_subject_type_data_element_sensitivity dstdes
            JOIN data_subject_type dst ON dstdes.data_subject_type_id = dst.id
            JOIN data_element de ON dstdes.data_element_id = de.id
            JOIN sensitivity s ON dstdes.sensitivity_id = s.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data subject type data element sensitivity relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_data_subject_type_data_element_sensitivity(self, data_subject_type_id, data_element_id, sensitivity_id):
        """Delete a data subject type data element sensitivity relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = """
            DELETE FROM data_subject_type_data_element_sensitivity 
            WHERE data_subject_type_id = %s AND data_element_id = %s AND sensitivity_id = %s;
            """
            cursor.execute(delete_query, (data_subject_type_id, data_element_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting data subject type data element sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    

    def seed_all_data(self):
        """Seed all regulatory metadata tables with initial data."""
        self.seed_law_jurisdictions()
        self.seed_law_legal_bases()
        self.seed_law_incident_breach_guidances()
        self.seed_law_transfers()
        self.seed_law_data_subject_access_request_notification_requirements()
        self.seed_law_purpose_category_legal_bases()
        self.seed_data_subject_right_implementation_steps()
        self.seed_data_subject_right_exemptions()
        self.seed_policy_purpose_data_retentions()
        
    # Law Purpose Category Legal Basis methods
    def add_law_purpose_category_legal_basis(self, law_id, purpose_category_id, legal_basis_id, preference_order=1, description=None):
        """Add a new law purpose category legal basis relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_purpose_category_legal_basis (law_id, purpose_category_id, legal_basis_id, preference_order, description)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, purpose_category_id, legal_basis_id, preference_order, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law purpose category legal basis: {e}")
            return None
        finally:
            cursor.close()
    
    def get_law_purpose_category_legal_bases(self, law_id=None, purpose_category_id=None):
        """Get law purpose category legal basis relationships from the database.
        
        Args:
            law_id (int, optional): Filter by law ID
            purpose_category_id (int, optional): Filter by purpose category ID
            
        Returns:
            list: List of law purpose category legal basis relationships
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if law_id and purpose_category_id:
                query = """
                SELECT lpcb.id, l.id as law_id, l.name as law_name, 
                       pc.id as purpose_category_id, pc.name as purpose_category_name, 
                       lb.id as legal_basis_id, lb.name as legal_basis_name,
                       lpcb.preference_order, lpcb.description
                FROM law_purpose_category_legal_basis lpcb
                JOIN law l ON lpcb.law_id = l.id
                JOIN purpose_category pc ON lpcb.purpose_category_id = pc.id
                JOIN legal_basis lb ON lpcb.legal_basis_id = lb.id
                WHERE lpcb.law_id = %s AND lpcb.purpose_category_id = %s
                ORDER BY lpcb.preference_order;
                """
                cursor.execute(query, (law_id, purpose_category_id))
            elif law_id:
                query = """
                SELECT lpcb.id, l.id as law_id, l.name as law_name, 
                       pc.id as purpose_category_id, pc.name as purpose_category_name, 
                       lb.id as legal_basis_id, lb.name as legal_basis_name,
                       lpcb.preference_order, lpcb.description
                FROM law_purpose_category_legal_basis lpcb
                JOIN law l ON lpcb.law_id = l.id
                JOIN purpose_category pc ON lpcb.purpose_category_id = pc.id
                JOIN legal_basis lb ON lpcb.legal_basis_id = lb.id
                WHERE lpcb.law_id = %s
                ORDER BY pc.name, lpcb.preference_order;
                """
                cursor.execute(query, (law_id,))
            elif purpose_category_id:
                query = """
                SELECT lpcb.id, l.id as law_id, l.name as law_name, 
                       pc.id as purpose_category_id, pc.name as purpose_category_name, 
                       lb.id as legal_basis_id, lb.name as legal_basis_name,
                       lpcb.preference_order, lpcb.description
                FROM law_purpose_category_legal_basis lpcb
                JOIN law l ON lpcb.law_id = l.id
                JOIN purpose_category pc ON lpcb.purpose_category_id = pc.id
                JOIN legal_basis lb ON lpcb.legal_basis_id = lb.id
                WHERE lpcb.purpose_category_id = %s
                ORDER BY l.name, lpcb.preference_order;
                """
                cursor.execute(query, (purpose_category_id,))
            else:
                query = """
                SELECT lpcb.id, l.id as law_id, l.name as law_name, 
                       pc.id as purpose_category_id, pc.name as purpose_category_name, 
                       lb.id as legal_basis_id, lb.name as legal_basis_name,
                       lpcb.preference_order, lpcb.description
                FROM law_purpose_category_legal_basis lpcb
                JOIN law l ON lpcb.law_id = l.id
                JOIN purpose_category pc ON lpcb.purpose_category_id = pc.id
                JOIN legal_basis lb ON lpcb.legal_basis_id = lb.id
                ORDER BY l.name, pc.name, lpcb.preference_order;
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law purpose category legal bases: {e}")
            return []
        finally:
            cursor.close()
    
    def update_law_purpose_category_legal_basis(self, id, preference_order=None, description=None):
        """Update an existing law purpose category legal basis relationship."""
        cursor = self.connection.cursor()
        try:
            update_parts = []
            params = []
            
            if preference_order is not None:
                update_parts.append("preference_order = %s")
                params.append(preference_order)
            
            if description is not None:
                update_parts.append("description = %s")
                params.append(description)
            
            if not update_parts:
                return True  # Nothing to update
            
            params.append(id)  # For the WHERE clause
            
            update_query = f"""
            UPDATE law_purpose_category_legal_basis
            SET {', '.join(update_parts)}
            WHERE id = %s;
            """
            
            cursor.execute(update_query, params)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating law purpose category legal basis: {e}")
            return False
        finally:
            cursor.close()
    
    def delete_law_purpose_category_legal_basis(self, id):
        """Delete a law purpose category legal basis relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM law_purpose_category_legal_basis WHERE id = %s;"
            cursor.execute(delete_query, (id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law purpose category legal basis: {e}")
            return False
        finally:
            cursor.close()
            
    def seed_law_purpose_category_legal_bases(self):
        """Seed the database with initial law purpose category legal basis data."""
        # Get law IDs
        gdpr_id = self._get_law_id_by_name("GDPR")
        ccpa_id = self._get_law_id_by_name("CCPA")
        hipaa_id = self._get_law_id_by_name("HIPAA")
        
        # Get purpose category IDs
        contractual_necessity_id = self._get_purpose_category_id_by_name("Contractual Necessity")
        legal_compliance_id = self._get_purpose_category_id_by_name("Legal Compliance")
        vital_interests_id = self._get_purpose_category_id_by_name("Vital Interests")
        public_interest_id = self._get_purpose_category_id_by_name("Public Interest")
        legitimate_interests_id = self._get_purpose_category_id_by_name("Legitimate Business Interests")
        marketing_id = self._get_purpose_category_id_by_name("Marketing and Advertising")
        research_id = self._get_purpose_category_id_by_name("Research and Development")
        service_provision_id = self._get_purpose_category_id_by_name("Service Provision")
        security_id = self._get_purpose_category_id_by_name("Security and Fraud Prevention")
        analytics_id = self._get_purpose_category_id_by_name("Analytics and Improvement")
        employment_id = self._get_purpose_category_id_by_name("Employment Management")
        healthcare_id = self._get_purpose_category_id_by_name("Healthcare Provision")
        
        # Get legal basis IDs
        consent_id = self._get_legal_basis_id_by_name("Consent")
        contract_id = self._get_legal_basis_id_by_name("Contract")
        legal_obligation_id = self._get_legal_basis_id_by_name("Legal Obligation")
        vital_interest_id = self._get_legal_basis_id_by_name("Vital Interest")
        public_task_id = self._get_legal_basis_id_by_name("Public Task")
        legitimate_interest_id = self._get_legal_basis_id_by_name("Legitimate Interest")
        
        # GDPR mappings
        if gdpr_id:
            # Contractual Necessity -> Contract (1), Legitimate Interest (2)
            if contractual_necessity_id and contract_id and legitimate_interest_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, contractual_necessity_id, contract_id, 1, "Primary legal basis for processing necessary for contract performance")
                self.add_law_purpose_category_legal_basis(gdpr_id, contractual_necessity_id, legitimate_interest_id, 2, "Secondary legal basis if contract performance is not applicable")
            
            # Legal Compliance -> Legal Obligation (1)
            if legal_compliance_id and legal_obligation_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, legal_compliance_id, legal_obligation_id, 1, "Processing necessary for compliance with legal obligations")
            
            # Vital Interests -> Vital Interest (1), Legitimate Interest (2)
            if vital_interests_id and vital_interest_id and legitimate_interest_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, vital_interests_id, vital_interest_id, 1, "Processing necessary to protect vital interests")
                self.add_law_purpose_category_legal_basis(gdpr_id, vital_interests_id, legitimate_interest_id, 2, "Secondary legal basis if vital interest is not applicable")
            
            # Public Interest -> Public Task (1), Legal Obligation (2)
            if public_interest_id and public_task_id and legal_obligation_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, public_interest_id, public_task_id, 1, "Processing necessary for the performance of a task in the public interest")
                self.add_law_purpose_category_legal_basis(gdpr_id, public_interest_id, legal_obligation_id, 2, "Secondary legal basis if public task is not applicable")
            
            # Legitimate Business Interests -> Legitimate Interest (1), Consent (2)
            if legitimate_interests_id and legitimate_interest_id and consent_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, legitimate_interests_id, legitimate_interest_id, 1, "Processing necessary for legitimate interests")
                self.add_law_purpose_category_legal_basis(gdpr_id, legitimate_interests_id, consent_id, 2, "Secondary legal basis if legitimate interest is not applicable")
            
            # Marketing and Advertising -> Consent (1), Legitimate Interest (2)
            if marketing_id and consent_id and legitimate_interest_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, marketing_id, consent_id, 1, "Primary legal basis for marketing activities")
                self.add_law_purpose_category_legal_basis(gdpr_id, marketing_id, legitimate_interest_id, 2, "Secondary legal basis for existing customers (soft opt-in)")
            
            # Research and Development -> Legitimate Interest (1), Consent (2)
            if research_id and legitimate_interest_id and consent_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, research_id, legitimate_interest_id, 1, "Primary legal basis for research activities")
                self.add_law_purpose_category_legal_basis(gdpr_id, research_id, consent_id, 2, "Secondary legal basis for research involving special categories of data")
            
            # Service Provision -> Contract (1), Legitimate Interest (2)
            if service_provision_id and contract_id and legitimate_interest_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, service_provision_id, contract_id, 1, "Primary legal basis for service provision")
                self.add_law_purpose_category_legal_basis(gdpr_id, service_provision_id, legitimate_interest_id, 2, "Secondary legal basis if contract is not applicable")
            
            # Security and Fraud Prevention -> Legitimate Interest (1), Legal Obligation (2)
            if security_id and legitimate_interest_id and legal_obligation_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, security_id, legitimate_interest_id, 1, "Primary legal basis for security and fraud prevention")
                self.add_law_purpose_category_legal_basis(gdpr_id, security_id, legal_obligation_id, 2, "Secondary legal basis if required by law")
            
            # Analytics and Improvement -> Legitimate Interest (1), Consent (2)
            if analytics_id and legitimate_interest_id and consent_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, analytics_id, legitimate_interest_id, 1, "Primary legal basis for analytics and improvement")
                self.add_law_purpose_category_legal_basis(gdpr_id, analytics_id, consent_id, 2, "Secondary legal basis if legitimate interest is not applicable")
            
            # Employment Management -> Contract (1), Legal Obligation (2), Legitimate Interest (3)
            if employment_id and contract_id and legal_obligation_id and legitimate_interest_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, employment_id, contract_id, 1, "Primary legal basis for employment management")
                self.add_law_purpose_category_legal_basis(gdpr_id, employment_id, legal_obligation_id, 2, "Secondary legal basis for legal requirements")
                self.add_law_purpose_category_legal_basis(gdpr_id, employment_id, legitimate_interest_id, 3, "Tertiary legal basis for legitimate employer interests")
            
            # Healthcare Provision -> Vital Interest (1), Legal Obligation (2), Consent (3)
            if healthcare_id and vital_interest_id and legal_obligation_id and consent_id:
                self.add_law_purpose_category_legal_basis(gdpr_id, healthcare_id, vital_interest_id, 1, "Primary legal basis for emergency healthcare")
                self.add_law_purpose_category_legal_basis(gdpr_id, healthcare_id, legal_obligation_id, 2, "Secondary legal basis for legal requirements")
                self.add_law_purpose_category_legal_basis(gdpr_id, healthcare_id, consent_id, 3, "Tertiary legal basis for non-emergency healthcare")
        
        # CCPA mappings
        if ccpa_id and consent_id:
            # For CCPA, most processing is allowed with notice, but consent (opt-out) is required for certain activities
            purpose_categories = [
                contractual_necessity_id, legal_compliance_id, vital_interests_id, public_interest_id,
                legitimate_interests_id, marketing_id, research_id, service_provision_id,
                security_id, analytics_id, employment_id, healthcare_id
            ]
            
            for purpose_category_id in purpose_categories:
                if purpose_category_id:
                    self.add_law_purpose_category_legal_basis(ccpa_id, purpose_category_id, consent_id, 1, "Opt-out consent required for CCPA compliance")
        
        # HIPAA mappings
        if hipaa_id and healthcare_id and consent_id and legal_obligation_id:
            self.add_law_purpose_category_legal_basis(hipaa_id, healthcare_id, consent_id, 1, "Authorization required for uses and disclosures of PHI")
            self.add_law_purpose_category_legal_basis(hipaa_id, healthcare_id, legal_obligation_id, 2, "Required disclosures to individuals and HHS")
    
    def _get_purpose_category_id_by_name(self, name):
        """Helper method to get purpose category ID by name."""
        cursor = self.connection.cursor()
        try:
            query = "SELECT id FROM purpose_category WHERE name = %s;"
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting purpose category ID: {e}")
            return None
        finally:
            cursor.close()
            
    # Legal Basis Requirements methods
    def add_legal_basis_requirement(self, legal_basis_id, requirement):
        """Add a new requirement for a legal basis.
        
        Args:
            legal_basis_id (int): The ID of the legal basis
            requirement (str): The compliance requirement text
            
        Returns:
            int: The ID of the newly created requirement or None if failed
        """
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO legal_basis_requirements (legal_basis_id, requirement) VALUES (%s, %s);"
            cursor.execute(query, (legal_basis_id, requirement))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding legal basis requirement: {e}")
            return None
        finally:
            cursor.close()
            
    def get_legal_basis_requirements(self, legal_basis_id=None):
        """Get requirements for legal bases.
        
        Args:
            legal_basis_id (int, optional): The ID of the legal basis to filter by. If None, get all requirements.
            
        Returns:
            list: A list of dictionaries containing the requirements data
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if legal_basis_id:
                query = """
                SELECT lbr.id, lbr.requirement, lb.id as legal_basis_id, lb.name as legal_basis_name 
                FROM legal_basis_requirements lbr
                JOIN legal_basis lb ON lbr.legal_basis_id = lb.id
                WHERE lbr.legal_basis_id = %s;
                """
                cursor.execute(query, (legal_basis_id,))
            else:
                query = """
                SELECT lbr.id, lbr.requirement, lb.id as legal_basis_id, lb.name as legal_basis_name 
                FROM legal_basis_requirements lbr
                JOIN legal_basis lb ON lbr.legal_basis_id = lb.id;
                """
                cursor.execute(query)
            
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting legal basis requirements: {e}")
            return []
        finally:
            cursor.close()
            
    def delete_legal_basis_requirement(self, requirement_id):
        """Delete a legal basis requirement.
        
        Args:
            requirement_id (int): The ID of the requirement to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            query = "DELETE FROM legal_basis_requirements WHERE id = %s;"
            cursor.execute(query, (requirement_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting legal basis requirement: {e}")
            return False
        finally:
            cursor.close()
    
    # Data Subject Right Implementation Steps methods
    def create_data_subject_right_implementation_steps_table(self):
        """Create the Data Subject Right Implementation Steps table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_subject_right_implementation_steps` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `right_type` VARCHAR(255) NOT NULL,
            `step_order` INT NOT NULL,
            `description` TEXT NOT NULL,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `unique_law_right_step` (`law_id`, `right_type`, `step_order`)
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def add_data_subject_right_implementation_step(self, law_id, right_type, step_order, description):
        """Add a new implementation step for a data subject right.
        
        Args:
            law_id (int): The ID of the law
            right_type (str): The type of right (e.g., "Access", "Erasure")
            step_order (int): The order of the step in the implementation process
            description (str): The description of the implementation step
            
        Returns:
            int: The ID of the newly created step, or None if there was an error
        """
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_subject_right_implementation_steps 
            (law_id, right_type, step_order, description) 
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, right_type, step_order, description))
            self.connection.commit()
            step_id = cursor.lastrowid
            return step_id
        except Exception as e:
            print(f"Error adding data subject right implementation step: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def get_data_subject_right_implementation_steps(self, law_id=None, right_type=None):
        """Get implementation steps for data subject rights, optionally filtered by law and right type.
        
        Args:
            law_id (int, optional): The ID of the law to filter by
            right_type (str, optional): The type of right to filter by
            
        Returns:
            list: A list of dictionaries containing the implementation steps data
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if law_id and right_type:
                select_query = """
                SELECT dsris.id, l.name as law_name, dsris.right_type, dsris.step_order, dsris.description
                FROM data_subject_right_implementation_steps dsris
                JOIN law l ON dsris.law_id = l.id
                WHERE dsris.law_id = %s AND dsris.right_type = %s
                ORDER BY dsris.step_order;
                """
                cursor.execute(select_query, (law_id, right_type))
            elif law_id:
                select_query = """
                SELECT dsris.id, l.name as law_name, dsris.right_type, dsris.step_order, dsris.description
                FROM data_subject_right_implementation_steps dsris
                JOIN law l ON dsris.law_id = l.id
                WHERE dsris.law_id = %s
                ORDER BY dsris.right_type, dsris.step_order;
                """
                cursor.execute(select_query, (law_id,))
            else:
                select_query = """
                SELECT dsris.id, l.name as law_name, dsris.right_type, dsris.step_order, dsris.description
                FROM data_subject_right_implementation_steps dsris
                JOIN law l ON dsris.law_id = l.id
                ORDER BY l.name, dsris.right_type, dsris.step_order;
                """
                cursor.execute(select_query)
                
            steps = cursor.fetchall()
            return steps
        except Exception as e:
            print(f"Error getting data subject right implementation steps: {e}")
            return []
        finally:
            cursor.close()
    
    def update_data_subject_right_implementation_step(self, step_id, right_type, step_order, description):
        """Update an existing implementation step for a data subject right.
        
        Args:
            step_id (int): The ID of the step to update
            right_type (str): The type of right
            step_order (int): The order of the step
            description (str): The description of the step
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            update_query = """
            UPDATE data_subject_right_implementation_steps
            SET right_type = %s, step_order = %s, description = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (right_type, step_order, description, step_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating data subject right implementation step: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def delete_data_subject_right_implementation_step(self, step_id):
        """Delete an implementation step for a data subject right.
        
        Args:
            step_id (int): The ID of the step to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM data_subject_right_implementation_steps WHERE id = %s;"
            cursor.execute(delete_query, (step_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting data subject right implementation step: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    # Data Subject Right Exemptions methods
    def create_data_subject_right_exemptions_table(self):
        """Create the Data Subject Right Exemptions table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_subject_right_exemptions` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `law_id` INT NOT NULL,
            `right_type` VARCHAR(255) NOT NULL,
            `exemption` TEXT NOT NULL,
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def add_data_subject_right_exemption(self, law_id, right_type, exemption):
        """Add a new exemption for a data subject right.
        
        Args:
            law_id (int): The ID of the law
            right_type (str): The type of right (e.g., "Access", "Erasure")
            exemption (str): The description of the exemption
            
        Returns:
            int: The ID of the newly created exemption, or None if there was an error
        """
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_subject_right_exemptions 
            (law_id, right_type, exemption) 
            VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, right_type, exemption))
            self.connection.commit()
            exemption_id = cursor.lastrowid
            return exemption_id
        except Exception as e:
            print(f"Error adding data subject right exemption: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def get_data_subject_right_exemptions(self, law_id=None, right_type=None):
        """Get exemptions for data subject rights, optionally filtered by law and right type.
        
        Args:
            law_id (int, optional): The ID of the law to filter by
            right_type (str, optional): The type of right to filter by
            
        Returns:
            list: A list of dictionaries containing the exemptions data
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            if law_id and right_type:
                select_query = """
                SELECT dsre.id, l.name as law_name, dsre.right_type, dsre.exemption
                FROM data_subject_right_exemptions dsre
                JOIN law l ON dsre.law_id = l.id
                WHERE dsre.law_id = %s AND dsre.right_type = %s;
                """
                cursor.execute(select_query, (law_id, right_type))
            elif law_id:
                select_query = """
                SELECT dsre.id, l.name as law_name, dsre.right_type, dsre.exemption
                FROM data_subject_right_exemptions dsre
                JOIN law l ON dsre.law_id = l.id
                WHERE dsre.law_id = %s
                ORDER BY dsre.right_type;
                """
                cursor.execute(select_query, (law_id,))
            else:
                select_query = """
                SELECT dsre.id, l.name as law_name, dsre.right_type, dsre.exemption
                FROM data_subject_right_exemptions dsre
                JOIN law l ON dsre.law_id = l.id
                ORDER BY l.name, dsre.right_type;
                """
                cursor.execute(select_query)
                
            exemptions = cursor.fetchall()
            return exemptions
        except Exception as e:
            print(f"Error getting data subject right exemptions: {e}")
            return []
        finally:
            cursor.close()
    
    def update_data_subject_right_exemption(self, exemption_id, right_type, exemption):
        """Update an existing exemption for a data subject right.
        
        Args:
            exemption_id (int): The ID of the exemption to update
            right_type (str): The type of right
            exemption (str): The description of the exemption
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            update_query = """
            UPDATE data_subject_right_exemptions
            SET right_type = %s, exemption = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (right_type, exemption, exemption_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating data subject right exemption: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def delete_data_subject_right_exemption(self, exemption_id):
        """Delete an exemption for a data subject right.
        
        Args:
            exemption_id (int): The ID of the exemption to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM data_subject_right_exemptions WHERE id = %s;"
            cursor.execute(delete_query, (exemption_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting data subject right exemption: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def seed_data_subject_right_implementation_steps(self):
        """Seed the data subject right implementation steps table with initial data."""
        # Check if data already exists
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM data_subject_right_implementation_steps;")
        result = cursor.fetchone()
        cursor.close()
        
        if result and result['count'] > 0:
            return  # Data already exists

        # Get law IDs
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM law;")
        laws = cursor.fetchall()
        cursor.close()
        
        law_map = {law['name']: law['id'] for law in laws}
        
        # Add implementation steps for GDPR Access right
        if 'GDPR' in law_map:
            gdpr_id = law_map['GDPR']
            # Access right steps
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 1, "Confirm receipt of the request within 3 business days")
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 2, "Verify the identity of the requestor")
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 3, "Search all relevant systems and databases for personal data")
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 4, "Compile the information in a clear, accessible format")
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 5, "Include information about processing purposes, categories of data, recipients, retention periods, and other rights")
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 6, "Review for third-party data or exemptions before disclosure")
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 7, "Provide the response securely to the data subject")
            self.add_data_subject_right_implementation_step(gdpr_id, "Access", 8, "Document the fulfillment of the request")
            
            # Erasure right steps
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 1, "Confirm receipt of the request within 3 business days")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 2, "Verify the identity of the requestor")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 3, "Determine if one of the grounds for erasure applies")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 4, "Identify all systems and databases containing the data")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 5, "Check for any legal basis to retain certain data")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 6, "Implement technical erasure in all systems")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 7, "Notify third parties of the erasure request where data has been shared")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 8, "Provide confirmation of erasure to the data subject")
            self.add_data_subject_right_implementation_step(gdpr_id, "Erasure", 9, "Document the fulfillment of the request")
        
        # Add implementation steps for CCPA/CPRA Access right
        if 'CCPA' in law_map:
            ccpa_id = law_map['CCPA']
            # Access right steps
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 1, "Confirm receipt of the request within 10 business days")
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 2, "Verify the identity of the requestor")
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 3, "Search all relevant systems for personal information collected in the past 12 months")
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 4, "Compile the information in a readily usable format")
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 5, "Include categories of sources, business purpose, and third parties shared with")
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 6, "Provide two or more designated methods for submitting requests")
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 7, "Deliver the information free of charge")
            self.add_data_subject_right_implementation_step(ccpa_id, "Access", 8, "Document the fulfillment of the request")
            
            # Deletion right steps
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 1, "Confirm receipt of the request within 10 business days")
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 2, "Verify the identity of the requestor")
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 3, "Identify all systems and databases containing the consumer's personal information")
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 4, "Check for any exceptions that allow retention")
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 5, "Delete the personal information from your records")
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 6, "Direct service providers to delete the consumer's personal information")
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 7, "Notify the consumer that their request has been fulfilled")
            self.add_data_subject_right_implementation_step(ccpa_id, "Erasure", 8, "Document the deletion process and maintain records")
    
    def seed_data_subject_right_exemptions(self):
        """Seed the data subject right exemptions table with initial data."""
        # Check if data already exists
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM data_subject_right_exemptions;")
        result = cursor.fetchone()
        cursor.close()
        
        if result and result['count'] > 0:
            return  # Data already exists

        # Get law IDs
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM law;")
        laws = cursor.fetchall()
        cursor.close()
        
        law_map = {law['name']: law['id'] for law in laws}
        
        # Add exemptions for GDPR rights
        if 'GDPR' in law_map:
            gdpr_id = law_map['GDPR']
            # Access right exemptions
            self.add_data_subject_right_exemption(gdpr_id, "Access", "Information protected by legal professional privilege")
            self.add_data_subject_right_exemption(gdpr_id, "Access", "Confidential references")
            self.add_data_subject_right_exemption(gdpr_id, "Access", "Management forecasting or planning if disclosure would prejudice the business")
            self.add_data_subject_right_exemption(gdpr_id, "Access", "Negotiations with the data subject if disclosure would prejudice those negotiations")
            self.add_data_subject_right_exemption(gdpr_id, "Access", "Third-party data where disclosure would breach confidentiality")
            
            # Erasure right exemptions
            self.add_data_subject_right_exemption(gdpr_id, "Erasure", "Legal obligation to retain the data")
            self.add_data_subject_right_exemption(gdpr_id, "Erasure", "Public interest in public health")
            self.add_data_subject_right_exemption(gdpr_id, "Erasure", "Archiving purposes in the public interest")
            self.add_data_subject_right_exemption(gdpr_id, "Erasure", "Establishment, exercise, or defense of legal claims")
            self.add_data_subject_right_exemption(gdpr_id, "Erasure", "Freedom of expression and information")
        
        # Add exemptions for CCPA/CPRA rights
        if 'CCPA' in law_map:
            ccpa_id = law_map['CCPA']
            # Access right exemptions
            self.add_data_subject_right_exemption(ccpa_id, "Access", "Cannot provide specific pieces of information if disclosure creates substantial security risk")
            self.add_data_subject_right_exemption(ccpa_id, "Access", "Not required to provide access more than twice in a 12-month period")
            self.add_data_subject_right_exemption(ccpa_id, "Access", "Certain business-to-business communications")
            self.add_data_subject_right_exemption(ccpa_id, "Access", "Certain employee data until January 1, 2023")
            
            # Deletion right exemptions
            self.add_data_subject_right_exemption(ccpa_id, "Erasure", "Complete a transaction, provide a good or service requested by the consumer")
            self.add_data_subject_right_exemption(ccpa_id, "Erasure", "Detect security incidents or protect against malicious activities")
            self.add_data_subject_right_exemption(ccpa_id, "Erasure", "Debug to identify and repair errors")
            self.add_data_subject_right_exemption(ccpa_id, "Erasure", "Exercise free speech or ensure another consumer's right to exercise free speech")
            self.add_data_subject_right_exemption(ccpa_id, "Erasure", "Comply with legal obligations")
    

    
    def get_data_subject_right_guidance(self, law_name, right_type):
        """Get comprehensive guidance for a data subject right based on law and right type.
        
        Args:
            law_name (str): The name of the law (e.g., "GDPR", "CCPA")
            right_type (str): The type of right (e.g., "Access", "Erasure")
            
        Returns:
            dict: A dictionary containing guidance information or None if not found
        """
        try:
            # Get the law ID
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM law WHERE name = %s", (law_name,))
            law_result = cursor.fetchone()
            if not law_result:
                return None
                
            law_id = law_result[0]
            
            # Get implementation steps
            implementation_steps = []
            cursor.execute("""
                SELECT description 
                FROM data_subject_right_implementation_steps 
                WHERE law_id = %s AND right_type = %s 
                ORDER BY step_order
            """, (law_id, right_type))
            steps_results = cursor.fetchall()
            for step in steps_results:
                implementation_steps.append(step[0])
                
            # Get exemptions
            exemptions = []
            cursor.execute("""
                SELECT exemption 
                FROM data_subject_right_exemptions 
                WHERE law_id = %s AND right_type = %s
            """, (law_id, right_type))
            exemptions_results = cursor.fetchall()
            for exemption in exemptions_results:
                exemptions.append(exemption[0])
                
            # If no implementation steps were found, return None
            if not implementation_steps:
                return None
                
            # Get additional guidance details from the Data Subject Access Request table
            # Map the right_type to the corresponding name in the notification requirements table
            right_name_map = {
                "Access": "Right of Access",
                "Erasure": "Right to Erasure",
                "Rectification": "Right to Rectification"
            }
            
            right_name = right_name_map.get(right_type, right_type)
            
            cursor.execute("""
                SELECT timeframe, conditions, exemptions
                FROM law_data_subject_access_request_notification_requirements
                WHERE law_id = %s AND name = %s;
            """, (law_id, right_name))
            guidance_details = cursor.fetchone()
            
            guidance = {
                "implementation_steps": implementation_steps,
                "exemptions": exemptions
            }
            
            if guidance_details:
                # Parse the timeframe to extract extension information
                timeframe = guidance_details[0]
                extension_possible = "Yes" if "can be extended" in timeframe.lower() else "No"
                extension_conditions = guidance_details[1] if guidance_details[1] else ""
                
                guidance.update({
                    "timeframe": timeframe.split("(")[0].strip() if "(" in timeframe else timeframe,
                    "extension_possible": extension_possible,
                    "extension_conditions": extension_conditions,
                    "verification_requirements": guidance_details[1] if guidance_details[1] else ""
                })
            
            return guidance
        except Exception as e:
            print(f"Error retrieving data subject right guidance: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
                
    # Policy Purpose methods
    def create_policy_purpose_table(self):
        """Create the Policy Purpose table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_purpose` (
            `policy_id` INT NOT NULL,
            `purpose_id` INT NOT NULL,
            PRIMARY KEY (`policy_id`, `purpose_id`),
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_policy_purpose_data_element_table(self):
        """Create the Policy Purpose Data Element table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_purpose_data_element` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `policy_id` INT NOT NULL,
            `purpose_id` INT NOT NULL,
            `data_element_id` INT NOT NULL,
            `access_allowed` BOOLEAN NOT NULL DEFAULT TRUE,
            UNIQUE KEY `unique_policy_purpose_data_element` (`policy_id`, `purpose_id`, `data_element_id`),
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_policy_purpose_data_usage_table(self):
        """Create the Policy Purpose Data Usage table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_purpose_data_usage` (
            `policy_id` INT NOT NULL,
            `purpose_id` INT NOT NULL,
            `data_element_id` INT NOT NULL,
            `operation` VARCHAR(50) NOT NULL,
            `allowed` BOOLEAN NOT NULL DEFAULT FALSE,
            `restrictions` TEXT,
            PRIMARY KEY (`policy_id`, `purpose_id`, `data_element_id`, `operation`),
            FOREIGN KEY (`policy_id`, `purpose_id`, `data_element_id`) 
                REFERENCES `policy_purpose_data_element`(`policy_id`, `purpose_id`, `data_element_id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_policy_purpose_data_retention_table(self):
        """Create the Policy Purpose Data Retention table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_purpose_data_retention` (
            `policy_id` INT NOT NULL,
            `purpose_id` INT NOT NULL,
            `data_element_id` INT NOT NULL,
            `retention_period` VARCHAR(100) NOT NULL,
            `retention_trigger` VARCHAR(100) NOT NULL DEFAULT 'Collection',
            `retention_basis` VARCHAR(255),
            `exceptions` TEXT,
            PRIMARY KEY (`policy_id`, `purpose_id`, `data_element_id`),
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def add_policy_purpose(self, policy_id, purpose_id):
        """Add a new policy-purpose relationship to the database.
        
        Args:
            policy_id (int): The ID of the policy
            purpose_id (int): The ID of the purpose
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy_purpose (policy_id, purpose_id) VALUES (%s, %s);",
                (policy_id, purpose_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding policy-purpose relationship: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def add_policy_purpose_data_element(self, policy_id, purpose_id, data_element_id, access_allowed=True):
        """Add a new policy-purpose-data element relationship to the database.
        
        Args:
            policy_id (int): The ID of the policy
            purpose_id (int): The ID of the purpose
            data_element_id (int): The ID of the data element
            access_allowed (bool, optional): Whether access is allowed. Defaults to True.
            
        Returns:
            int: The ID of the new record if successful, None otherwise
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy_purpose_data_element (policy_id, purpose_id, data_element_id, access_allowed) VALUES (%s, %s, %s, %s);",
                (policy_id, purpose_id, data_element_id, access_allowed)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding policy-purpose-data element relationship: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
            
    def add_policy_purpose_data_usage(self, policy_purpose_data_element_id, operation, allowed=False, restrictions=None):
        """Add a new policy-purpose-data element usage rule to the database.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy_purpose_data_element
            operation (str): The operation (e.g., 'read', 'write', 'share')
            allowed (bool, optional): Whether the operation is allowed. Defaults to False.
            restrictions (str, optional): Any restrictions on the operation. Defaults to None.
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy_purpose_data_usage (policy_purpose_data_element_id, operation, allowed, restrictions) VALUES (%s, %s, %s, %s);",
                (policy_purpose_data_element_id, operation, allowed, restrictions)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding policy-purpose-data usage rule: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def get_policy_purposes(self, policy_id=None):
        """Get all policy-purpose relationships from the database.
        
        Args:
            policy_id (int, optional): The ID of the policy to filter by. Defaults to None.
            
        Returns:
            list: A list of dictionaries containing policy-purpose relationship information
        """
        cursor = self.connection.cursor()
        try:
            if policy_id:
                cursor.execute("""
                    SELECT pp.policy_id, p.name as policy_name, pp.purpose_id, pu.name as purpose_name
                    FROM policy_purpose pp
                    JOIN policy p ON pp.policy_id = p.id
                    JOIN purpose pu ON pp.purpose_id = pu.id
                    WHERE pp.policy_id = %s;
                """, (policy_id,))
            else:
                cursor.execute("""
                    SELECT pp.policy_id, p.name as policy_name, pp.purpose_id, pu.name as purpose_name
                    FROM policy_purpose pp
                    JOIN policy p ON pp.policy_id = p.id
                    JOIN purpose pu ON pp.purpose_id = pu.id;
                """)
            
            relationships = []
            for row in cursor.fetchall():
                relationships.append({
                    "policy_id": row[0],
                    "policy_name": row[1],
                    "purpose_id": row[2],
                    "purpose_name": row[3]
                })
            return relationships
        except Exception as e:
            print(f"Error getting policy-purpose relationships: {e}")
            return []
        finally:
            cursor.close()
            
    def get_policy_purpose_data_elements(self, policy_id=None, purpose_id=None):
        """Get all policy-purpose-data element relationships from the database.
        
        Args:
            policy_id (int, optional): The ID of the policy to filter by. Defaults to None.
            purpose_id (int, optional): The ID of the purpose to filter by. Defaults to None.
            
        Returns:
            list: A list of dictionaries containing policy-purpose-data element relationship information
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT ppde.id, ppde.policy_id, p.name as policy_name, ppde.purpose_id, pu.name as purpose_name,
                       ppde.data_element_id, de.name as data_element_name, ppde.access_allowed
                FROM policy_purpose_data_element ppde
                JOIN policy p ON ppde.policy_id = p.id
                JOIN purpose pu ON ppde.purpose_id = pu.id
                JOIN data_element de ON ppde.data_element_id = de.id
            """
            
            params = []
            where_clauses = []
            
            if policy_id:
                where_clauses.append("ppde.policy_id = %s")
                params.append(policy_id)
            
            if purpose_id:
                where_clauses.append("ppde.purpose_id = %s")
                params.append(purpose_id)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            cursor.execute(query, params)
            
            relationships = []
            for row in cursor.fetchall():
                relationships.append({
                    "id": row[0],
                    "policy_id": row[1],
                    "policy_name": row[2],
                    "purpose_id": row[3],
                    "purpose_name": row[4],
                    "data_element_id": row[5],
                    "data_element_name": row[6],
                    "access_allowed": row[7]
                })
            return relationships
        except Exception as e:
            print(f"Error getting policy-purpose-data element relationships: {e}")
            return []
        finally:
            cursor.close()
            
    def get_policy_purpose_data_usages(self, policy_id=None, purpose_id=None, data_element_id=None):
        """Get all policy-purpose-data element usage rules from the database.
        
        Args:
            policy_id (int, optional): The ID of the policy to filter by. Defaults to None.
            purpose_id (int, optional): The ID of the purpose to filter by. Defaults to None.
            data_element_id (int, optional): The ID of the data element to filter by. Defaults to None.
            
        Returns:
            list: A list of dictionaries containing policy-purpose-data element usage rule information
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT ppde.policy_id, p.name as policy_name, p.policy_type,
                       ppde.purpose_id, pu.name as purpose_name,
                       ppde.data_element_id, de.name as data_element_name,
                       ppdu.operation, ppdu.allowed, ppdu.restrictions
                FROM policy_purpose_data_usage ppdu
                JOIN policy_purpose_data_element ppde ON ppdu.policy_purpose_data_element_id = ppde.id
                JOIN policy p ON ppde.policy_id = p.id
                JOIN purpose pu ON ppde.purpose_id = pu.id
                JOIN data_element de ON ppde.data_element_id = de.id
            """
            
            conditions = []
            params = []
            
            if policy_id:
                conditions.append("ppde.policy_id = %s")
                params.append(policy_id)
            
            if purpose_id:
                conditions.append("ppde.purpose_id = %s")
                params.append(purpose_id)
            
            if data_element_id:
                conditions.append("ppde.data_element_id = %s")
                params.append(data_element_id)
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            cursor.execute(query, params)
            
            usages = []
            for row in cursor.fetchall():
                usages.append({
                    "policy_id": row[0],
                    "policy_name": row[1],
                    "policy_type": row[2],
                    "purpose_id": row[3],
                    "purpose_name": row[4],
                    "data_element_id": row[5],
                    "data_element_name": row[6],
                    "operation": row[7],
                    "allowed": bool(row[8]),
                    "restrictions": row[9]
                })
            return usages
        except Exception as e:
            print(f"Error getting policy-purpose-data element usage rules: {e}")
            return []
        finally:
            cursor.close()
            
    def get_policies(self, policy_type=None):
        """Get all policies from the database.
        
        Args:
            policy_type (str, optional): The type of policy to filter by. Defaults to None.
            
        Returns:
            list: A list of dictionaries containing policy information
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT p.id, p.name, p.description, p.policy_type, p.status, p.effective_date, p.expiration_date
                FROM policy p
            """
            
            params = []
            if policy_type:
                query += " WHERE p.policy_type = %s"
                params.append(policy_type)
            
            cursor.execute(query, params)
            
            policies = []
            for row in cursor.fetchall():
                policies.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "policy_type": row[3],
                    "status": row[4],
                    "effective_date": row[5],
                    "expiration_date": row[6]
                })
            return policies
        except Exception as e:
            print(f"Error getting policies: {e}")
            return []
        finally:
            cursor.close()
            
    def seed_policy_purposes(self):
        """Seed the database with initial policy-purpose data."""
        # Get policy and purpose IDs
        cursor = self.connection.cursor()
        try:
            # Get policies
            cursor.execute("SELECT id, name FROM policy;")
            policies = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Get purposes
            cursor.execute("SELECT id, name FROM purpose;")
            purposes = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Define policy-purpose relationships
            relationships = [
                ("Data Access Control Policy", "Customer Support"),
                ("Data Access Control Policy", "Fraud Detection"),
                ("Data Access Control Policy", "Marketing Campaigns"),
                ("Data Access Control Policy", "Product Analytics"),
                ("Data Access Control Policy", "User Authentication"),
                ("Data Access Control Policy", "Regulatory Compliance"),
                ("Data Access Control Policy", "Payment Processing"),
                ("Data Access Control Policy", "Service Delivery"),
                ("Data Access Control Policy", "Research and Development"),
                ("Data Access Control Policy", "Employee Management")
            ]
            
            for policy_name, purpose_name in relationships:
                policy_id = policies.get(policy_name)
                purpose_id = purposes.get(purpose_name)
                
                if policy_id and purpose_id:
                    cursor.execute("SELECT 1 FROM policy_purpose WHERE policy_id = %s AND purpose_id = %s;", (policy_id, purpose_id))
                    if not cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO policy_purpose (policy_id, purpose_id) VALUES (%s, %s);",
                            (policy_id, purpose_id)
                        )
            
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding policy-purpose relationships: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def create_framework_control_table(self):
        """Create the Framework Control mapping table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `framework_control` (
            `framework_id` INT NOT NULL,
            `control_id` INT NOT NULL,
            `relevance_score` FLOAT NOT NULL,
            PRIMARY KEY (`framework_id`, `control_id`),
            FOREIGN KEY (`framework_id`) REFERENCES `framework`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`control_id`) REFERENCES `control`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def create_policy_control_table(self):
        """Create the Policy Control mapping table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_control` (
            `policy_id` INT NOT NULL,
            `control_id` INT NOT NULL,
            `relevance_score` FLOAT NOT NULL,
            PRIMARY KEY (`policy_id`, `control_id`),
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`control_id`) REFERENCES `control`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def create_risk_control_table(self):
        """Create the Risk Control mapping table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `risk_control` (
            `risk_id` INT NOT NULL,
            `control_id` INT NOT NULL,
            `mitigation_level` VARCHAR(50) NOT NULL,
            PRIMARY KEY (`risk_id`, `control_id`),
            FOREIGN KEY (`risk_id`) REFERENCES `risk`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`control_id`) REFERENCES `control`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def get_framework_controls(self, framework_id=None, control_id=None):
        """Get framework control mappings."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT fc.framework_id, f.name as framework_name, f.category as framework_category, f.version,
                   fc.control_id, c.name as control_name, c.control_type, c.implementation_status, c.priority,
                   fc.relevance_score
            FROM framework_control fc
            JOIN framework f ON fc.framework_id = f.id
            JOIN control c ON fc.control_id = c.id
            """
            
            params = []
            where_clauses = []
            
            if framework_id:
                where_clauses.append("fc.framework_id = %s")
                params.append(framework_id)
            
            if control_id:
                where_clauses.append("fc.control_id = %s")
                params.append(control_id)
                
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "framework_id": row[0],
                    "framework_name": row[1],
                    "framework_category": row[2],
                    "framework_version": row[3],
                    "control_id": row[4],
                    "control_name": row[5],
                    "control_type": row[6],
                    "implementation_status": row[7],
                    "priority": row[8],
                    "relevance_score": float(row[9])
                })
                
            return results
        except Exception as e:
            print(f"Error getting framework controls: {e}")
            return []
        finally:
            cursor.close()
    
    def get_policy_controls(self, policy_id=None, control_id=None):
        """Get policy control mappings."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT pc.policy_id, p.name as policy_name, p.policy_type,
                   pc.control_id, c.name as control_name, c.control_type, c.implementation_status, c.priority,
                   pc.relevance_score
            FROM policy_control pc
            JOIN policy p ON pc.policy_id = p.id
            JOIN control c ON pc.control_id = c.id
            """
            
            params = []
            where_clauses = []
            
            if policy_id:
                where_clauses.append("pc.policy_id = %s")
                params.append(policy_id)
            
            if control_id:
                where_clauses.append("pc.control_id = %s")
                params.append(control_id)
                
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "policy_id": row[0],
                    "policy_name": row[1],
                    "policy_type": row[2],
                    "control_id": row[3],
                    "control_name": row[4],
                    "control_type": row[5],
                    "implementation_status": row[6],
                    "priority": row[7],
                    "relevance_score": float(row[8])
                })
                
            return results
        except Exception as e:
            print(f"Error getting policy controls: {e}")
            return []
        finally:
            cursor.close()
    
    def get_risk_controls(self, risk_id=None, control_id=None):
        """Get risk control mappings."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT rc.risk_id, r.name as risk_name, r.category as risk_category, r.likelihood, r.impact,
                   rc.control_id, c.name as control_name, c.control_type, c.implementation_status, c.priority,
                   rc.mitigation_level
            FROM risk_control rc
            JOIN risk r ON rc.risk_id = r.id
            JOIN control c ON rc.control_id = c.id
            """
            
            params = []
            where_clauses = []
            
            if risk_id:
                where_clauses.append("rc.risk_id = %s")
                params.append(risk_id)
            
            if control_id:
                where_clauses.append("rc.control_id = %s")
                params.append(control_id)
                
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "risk_id": row[0],
                    "risk_name": row[1],
                    "risk_category": row[2],
                    "risk_likelihood": row[3],
                    "risk_impact": row[4],
                    "control_id": row[5],
                    "control_name": row[6],
                    "control_type": row[7],
                    "implementation_status": row[8],
                    "priority": row[9],
                    "mitigation_level": row[10]
                })
                
            return results
        except Exception as e:
            print(f"Error getting risk controls: {e}")
            return []
        finally:
            cursor.close()
            
    def add_policy_purpose_data_retention(self, policy_purpose_data_element_id, retention_period, retention_trigger='Collection', retention_basis=None, exceptions=None):
        """Add a new policy-purpose-data element retention rule to the database.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy_purpose_data_element
            retention_period (str): The retention period (e.g., '30 days', '1 year', '7 years')
            retention_trigger (str, optional): What triggers the retention period. Defaults to 'Collection'.
            retention_basis (str, optional): The basis for the retention period. Defaults to None.
            exceptions (str, optional): Any exceptions to the retention rule. Defaults to None.
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy_purpose_data_retention (policy_purpose_data_element_id, retention_period, retention_trigger, retention_basis, exceptions) VALUES (%s, %s, %s, %s, %s)",
                (policy_purpose_data_element_id, retention_period, retention_trigger, retention_basis, exceptions)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding policy-purpose-data retention rule: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def get_policy_purpose_data_retentions(self, policy_id=None, purpose_id=None, data_element_id=None):
        """Get all policy-purpose-data element retention rules from the database.
        
        Args:
            policy_id (int, optional): The ID of the policy to filter by. Defaults to None.
            purpose_id (int, optional): The ID of the purpose to filter by. Defaults to None.
            data_element_id (int, optional): The ID of the data element to filter by. Defaults to None.
            
        Returns:
            list: A list of dictionaries containing policy-purpose-data element retention rule information
        """
        cursor = self.connection.cursor()
        try:
            query = """
                SELECT ppde.policy_id, p.name as policy_name, p.policy_type,
                       ppde.purpose_id, pu.name as purpose_name,
                       ppde.data_element_id, de.name as data_element_name,
                       ppdr.retention_period, ppdr.retention_trigger, ppdr.retention_basis, ppdr.exceptions
                FROM policy_purpose_data_retention ppdr
                JOIN policy_purpose_data_element ppde ON ppdr.policy_purpose_data_element_id = ppde.id
                JOIN policy p ON ppde.policy_id = p.id
                JOIN purpose pu ON ppde.purpose_id = pu.id
                JOIN data_element de ON ppde.data_element_id = de.id
            """
            
            conditions = []
            params = []
            
            if policy_id:
                conditions.append("ppde.policy_id = %s")
                params.append(policy_id)
            
            if purpose_id:
                conditions.append("ppde.purpose_id = %s")
                params.append(purpose_id)
            
            if data_element_id:
                conditions.append("ppde.data_element_id = %s")
                params.append(data_element_id)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            cursor.execute(query, params)
            
            retentions = []
            for row in cursor.fetchall():
                retentions.append({
                    "policy_id": row[0],
                    "policy_name": row[1],
                    "policy_type": row[2],
                    "purpose_id": row[3],
                    "purpose_name": row[4],
                    "data_element_id": row[5],
                    "data_element_name": row[6],
                    "retention_period": row[7],
                    "retention_trigger": row[8],
                    "retention_basis": row[9],
                    "exceptions": row[10]
                })
            return retentions
        except Exception as e:
            print(f"Error getting policy-purpose-data element retention rules: {e}")
            return []
        finally:
            cursor.close()
            
    def get_policy_purpose_data_element_id(self, policy_id, purpose_id, data_element_id):
        """Get the ID of a policy_purpose_data_element entry based on policy, purpose, and data element IDs.
        
        Args:
            policy_id (int): The ID of the policy
            purpose_id (int): The ID of the purpose
            data_element_id (int): The ID of the data element
            
        Returns:
            int: The ID of the policy_purpose_data_element entry, or None if not found
        """
        cursor = self.connection.cursor()
        try:
            query = """SELECT id FROM policy_purpose_data_element 
                      WHERE policy_id = %s AND purpose_id = %s AND data_element_id = %s"""
            cursor.execute(query, (policy_id, purpose_id, data_element_id))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting policy_purpose_data_element_id: {e}")
            return None
        finally:
            cursor.close()
            
    def update_policy_purpose_data_retention(self, policy_purpose_data_element_id, retention_period, retention_trigger=None, retention_basis=None, exceptions=None):
        """Update an existing policy-purpose-data element retention rule.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy_purpose_data_element
            retention_period (str): The retention period (e.g., '30 days', '1 year', '7 years')
            retention_trigger (str, optional): What triggers the retention period
            retention_basis (str, optional): The basis for the retention period
            exceptions (str, optional): Any exceptions to the retention rule
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            # Build the update query dynamically based on which fields are provided
            update_parts = ["retention_period = %s"]
            params = [retention_period]
            
            if retention_trigger is not None:
                update_parts.append("retention_trigger = %s")
                params.append(retention_trigger)
                
            if retention_basis is not None:
                update_parts.append("retention_basis = %s")
                params.append(retention_basis)
                
            if exceptions is not None:
                update_parts.append("exceptions = %s")
                params.append(exceptions)
                
            # Add the WHERE clause parameter
            params.append(policy_purpose_data_element_id)
            
            query = f"""UPDATE policy_purpose_data_retention 
                      SET {', '.join(update_parts)} 
                      WHERE policy_purpose_data_element_id = %s;"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating policy-purpose-data retention rule: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def delete_policy_purpose_data_retention(self, policy_purpose_data_element_id):
        """Delete a policy-purpose-data element retention rule from the database.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy_purpose_data_element
            
        Returns:
            bool: True if successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM policy_purpose_data_retention WHERE policy_purpose_data_element_id = %s;",
                (policy_purpose_data_element_id,)
            )
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting policy-purpose-data retention rule: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def seed_policy_purpose_data_retentions(self):
        """Seed the database with initial policy-purpose-data retention rules."""
        # Get existing policy purpose data element relationships
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT id, policy_id, purpose_id, data_element_id FROM policy_purpose_data_element
                   WHERE (policy_id, purpose_id) IN (SELECT policy_id, purpose_id FROM policy_purpose)"""
            )
            
            for row in cursor.fetchall():
                ppde_id, policy_id, purpose_id, data_element_id = row
                
                # Define retention periods based on purpose and data element
                retention_period = "1 year"  # Default
                retention_trigger = "Collection"  # Default
                retention_basis = "Business need"
                exceptions = None
                
                # Get purpose name
                purpose_cursor = self.connection.cursor()
                purpose_cursor.execute("SELECT name FROM purpose WHERE id = %s", (purpose_id,))
                purpose_name = purpose_cursor.fetchone()[0]
                purpose_cursor.close()
                
                # Get data element name
                data_element_cursor = self.connection.cursor()
                data_element_cursor.execute("SELECT name FROM data_element WHERE id = %s", (data_element_id,))
                data_element_name = data_element_cursor.fetchone()[0]
                data_element_cursor.close()
                
                # Set retention periods based on purpose and data element
                if purpose_name == "Customer Support":
                    retention_period = "2 years"
                    retention_trigger = "Last Interaction"
                    retention_basis = "Customer service quality"
                elif purpose_name == "Fraud Detection":
                    retention_period = "5 years"
                    retention_trigger = "Incident Resolution"
                    retention_basis = "Legal requirement"
                elif purpose_name == "Marketing Campaigns":
                    retention_period = "1 year"
                    retention_trigger = "Campaign End"
                    retention_basis = "Marketing effectiveness"
                elif purpose_name == "Payment Processing":
                    retention_period = "7 years"
                    retention_trigger = "Transaction Completion"
                    retention_basis = "Financial regulations"
                elif purpose_name == "Product Analytics":
                    retention_period = "90 days"
                    retention_trigger = "Collection"
                    retention_basis = "Business need"
                elif purpose_name == "Employee Management":
                    retention_period = "7 years"
                    retention_trigger = "Employment End"
                    retention_basis = "Employment regulations"
                    
                # Adjust based on sensitive data elements
                if data_element_name in ["Credit Card Number", "Social Security Number", "Bank Account Number"]:
                    retention_period = "Minimum required"
                    retention_trigger = "Purpose Fulfillment"
                    retention_basis = "Data minimization principle"
                    exceptions = "Retain longer only if required by law"
                
                # Add the retention rule
                self.add_policy_purpose_data_retention(
                    ppde_id, 
                    retention_period, retention_trigger, retention_basis, exceptions
                )
                
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding policy-purpose-data retention rules: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
"""
This file contains methods to be added to the RegulatoryMetadataRepository class
for handling policy data element tables.
"""

# Add these methods to RegulatoryMetadataRepository class

def get_policy_data_element_usage(self, policy_id=None, data_element_id=None):
    """Retrieve policy data element usage rules with optional filters.
    
    Args:
        policy_id: Optional policy ID to filter by
        data_element_id: Optional data element ID to filter by
        
    Returns:
        List of dictionaries containing policy data element usage rules
    """
    cursor = self.connection.cursor()
    try:
        query = """
        SELECT p.name as policy_name, de.name as data_element_name,
               u.operation, u.allowed, u.restrictions
        FROM policy_data_element_usage u
        JOIN policy p ON u.policy_id = p.id
        JOIN data_element de ON u.data_element_id = de.id
        WHERE 1=1
        """
        params = []
        if policy_id:
            query += " AND u.policy_id = %s"
            params.append(policy_id)
        if data_element_id:
            query += " AND u.data_element_id = %s"
            params.append(data_element_id)
            
        cursor.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append({
                "policy_name": row[0],
                "data_element_name": row[1],
                "operation": row[2],
                "allowed": row[3],
                "restrictions": row[4]
            })
        return results
    except Exception as e:
        print(f"Error getting policy data element usage: {e}")
        return []
    finally:
        cursor.close()

def get_policy_data_element_retention(self, policy_id=None, data_element_id=None):
    """Retrieve policy data element retention rules with optional filters.
    
    Args:
        policy_id: Optional policy ID to filter by
        data_element_id: Optional data element ID to filter by
        
    Returns:
        List of dictionaries containing policy data element retention rules
    """
    cursor = self.connection.cursor()
    try:
        query = """
        SELECT p.name as policy_name, de.name as data_element_name,
               r.retention_period, r.retention_basis, r.exceptions
        FROM policy_data_element_retention r
        JOIN policy p ON r.policy_id = p.id
        JOIN data_element de ON r.data_element_id = de.id
        WHERE 1=1
        """
        params = []
        if policy_id:
            query += " AND r.policy_id = %s"
            params.append(policy_id)
        if data_element_id:
            query += " AND r.data_element_id = %s"
            params.append(data_element_id)
            
        cursor.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append({
                "policy_name": row[0],
                "data_element_name": row[1],
                "retention_period": row[2],
                "retention_basis": row[3],
                "exceptions": row[4]
            })
        return results
    except Exception as e:
        print(f"Error getting policy data element retention: {e}")
        return []
    finally:
        cursor.close()

def get_policy_data_element_security(self, policy_id=None, data_element_id=None):
    """Retrieve policy data element security rules with optional filters.
    
    Args:
        policy_id: Optional policy ID to filter by
        data_element_id: Optional data element ID to filter by
        
    Returns:
        List of dictionaries containing policy data element security rules
    """
    cursor = self.connection.cursor()
    try:
        query = """
        SELECT p.name as policy_name, de.name as data_element_name,
               s.requires_encryption, s.encryption_algorithm, 
               s.requires_masking, s.masking_format,
               s.requires_access_control, s.access_control_type
        FROM policy_data_element_security s
        JOIN policy p ON s.policy_id = p.id
        JOIN data_element de ON s.data_element_id = de.id
        WHERE 1=1
        """
        params = []
        if policy_id:
            query += " AND s.policy_id = %s"
            params.append(policy_id)
        if data_element_id:
            query += " AND s.data_element_id = %s"
            params.append(data_element_id)
            
        cursor.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append({
                "policy_name": row[0],
                "data_element_name": row[1],
                "requires_encryption": row[2],
                "encryption_algorithm": row[3],
                "requires_masking": row[4],
                "masking_format": row[5],
                "requires_access_control": row[6],
                "access_control_type": row[7]
            })
        return results
    except Exception as e:
        print(f"Error getting policy data element security: {e}")
        return []
    finally:
        cursor.close()
