import pymysql.cursors
import json

class PolicyRepository:
    def __init__(self, connection):
        """Initialize the PolicyRepository with a database connection."""
        self.connection = connection
        
    def setup_tables(self):
        """Create all the necessary tables for policy management if they don't exist."""
        # Skip table creation in test mode
        if self.connection is None:
            return
            
        self.create_policy_purpose_role_table()
    
    def create_policy_purpose_role_table(self):
        """Create the purpose_role table to map purposes to roles."""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purpose_role (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                purpose_id INTEGER NOT NULL,
                external_role_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE(purpose_id, external_role_id),
                FOREIGN KEY (purpose_id) REFERENCES purpose(id),
                FOREIGN KEY (external_role_id) REFERENCES external_roles(id)
            );
        ''')
        self.connection.commit()
    
    # Purpose-Role Mapping Methods
    
    def get_purpose_roles(self):
        """Get all purpose-role mappings."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT pr.id, pr.purpose_id, p.name as purpose_name, pr.external_role_id, er.name as role_name, 
                       er.source_system, a.name as asset_name
                FROM purpose_role pr
                JOIN purpose p ON pr.purpose_id = p.id
                JOIN external_roles er ON pr.external_role_id = er.id
                LEFT JOIN asset a ON er.asset_id = a.id
                ORDER BY p.name, er.name;
            ''')
            purpose_roles = cursor.fetchall()
            return purpose_roles
        except Exception as e:
            print(f"Error getting purpose-role mappings: {e}")
            return []
    
    def get_purpose_roles_by_purpose(self, purpose_id):
        """Get purpose-role mappings for a specific purpose."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT pr.id, pr.purpose_id, p.name as purpose_name, pr.external_role_id, er.name as role_name, 
                       er.source_system, a.name as asset_name
                FROM purpose_role pr
                JOIN purpose p ON pr.purpose_id = p.id
                JOIN external_roles er ON pr.external_role_id = er.id
                LEFT JOIN asset a ON er.asset_id = a.id
                WHERE pr.purpose_id = %s
                ORDER BY er.name;
            ''', (purpose_id,))
            purpose_roles = cursor.fetchall()
            return purpose_roles
        except Exception as e:
            print(f"Error getting purpose-role mappings for purpose {purpose_id}: {e}")
            return []
    
    def get_purpose_roles_by_role(self, role_id):
        """Get purpose-role mappings for a specific role."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT pr.id, pr.purpose_id, p.name as purpose_name, pr.external_role_id, er.name as role_name, 
                       er.source_system, a.name as asset_name
                FROM purpose_role pr
                JOIN purpose p ON pr.purpose_id = p.id
                JOIN external_roles er ON pr.external_role_id = er.id
                LEFT JOIN asset a ON er.asset_id = a.id
                WHERE pr.external_role_id = %s
                ORDER BY p.name;
            ''', (role_id,))
            purpose_roles = cursor.fetchall()
            return purpose_roles
        except Exception as e:
            print(f"Error getting purpose-role mappings for role {role_id}: {e}")
            return []
    
    def add_purpose_role(self, purpose_id, role_id):
        """Add a purpose-role mapping."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO purpose_role (purpose_id, external_role_id)
                VALUES (%s, %s)
            ''', (purpose_id, role_id))
            self.connection.commit()
            return True
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:  # Duplicate entry error
                print(f"Purpose-role mapping already exists for purpose {purpose_id} and role {role_id}")
                return False
            else:
                print(f"Error adding purpose-role mapping: {e}")
                return False
        except Exception as e:
            print(f"Error adding purpose-role mapping: {e}")
            return False
    
    def delete_purpose_role(self, purpose_role_id):
        """Delete a purpose-role mapping."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                DELETE FROM purpose_role
                WHERE id = %s
            ''', (purpose_role_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting purpose-role mapping: {e}")
            return False
    
    # Policy Management Methods
    
    def create_policy(self, name, description, policy_type, status, effective_date=None, expiration_date=None):
        """Create a new policy."""
        cursor = self.connection.cursor()
        try:
            if effective_date and expiration_date:
                cursor.execute('''
                    INSERT INTO policy (name, description, policy_type, status, effective_date, expiration_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (name, description, policy_type, status, effective_date, expiration_date))
            else:
                cursor.execute('''
                    INSERT INTO policy (name, description, policy_type, status)
                    VALUES (%s, %s, %s, %s)
                ''', (name, description, policy_type, status))
            
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating policy: {e}")
            return None
    
    def get_policies(self, policy_type=None, status=None):
        """Get all policies with optional filtering."""
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM policy"
            params = []
            
            if policy_type or status:
                query += " WHERE"
                
                if policy_type:
                    query += " policy_type = %s"
                    params.append(policy_type)
                    
                    if status:
                        query += " AND status = %s"
                        params.append(status)
                elif status:
                    query += " status = %s"
                    params.append(status)
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, tuple(params) if params else None)
            policies = cursor.fetchall()
            return policies
        except Exception as e:
            print(f"Error getting policies: {e}")
            return []
    
    def get_policy(self, policy_id):
        """Get a specific policy by ID."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM policy WHERE id = %s", (policy_id,))
            policy = cursor.fetchone()
            return policy
        except Exception as e:
            print(f"Error getting policy {policy_id}: {e}")
            return None
    
    def update_policy(self, policy_id, name=None, description=None, policy_type=None, status=None, 
                     effective_date=None, expiration_date=None):
        """Update an existing policy."""
        cursor = self.connection.cursor()
        try:
            # Build the update query dynamically based on provided parameters
            query = "UPDATE policy SET "
            params = []
            updates = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            if policy_type is not None:
                updates.append("policy_type = %s")
                params.append(policy_type)
            if status is not None:
                updates.append("status = %s")
                params.append(status)
            if effective_date is not None:
                updates.append("effective_date = %s")
                params.append(effective_date)
            if expiration_date is not None:
                updates.append("expiration_date = %s")
                params.append(expiration_date)
            
            if not updates:
                return False  # Nothing to update
            
            query += ", ".join(updates)
            query += " WHERE id = %s"
            params.append(policy_id)
            
            cursor.execute(query, tuple(params))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating policy {policy_id}: {e}")
            return False
    
    def delete_policy(self, policy_id):
        """Delete a policy."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM policy WHERE id = %s", (policy_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting policy {policy_id}: {e}")
            return False
    
    # Policy Purpose Mappings
    
    def add_policy_purpose(self, policy_id, purpose_id):
        """Add a policy-purpose mapping."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO policy_purpose (policy_id, purpose_id)
                VALUES (%s, %s)
            ''', (policy_id, purpose_id))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding policy-purpose mapping: {e}")
            return None
    
    # Policy Data Element Mappings
    
    def add_policy_data_element(self, policy_purpose_id, data_element_id):
        """Add a policy-data element mapping."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO policy_purpose_data_element (policy_purpose_id, data_element_id)
                VALUES (%s, %s)
            ''', (policy_purpose_id, data_element_id))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding policy-data element mapping: {e}")
            return None
    
    # Policy Type-Specific Methods
    
    def add_policy_data_usage(self, policy_purpose_data_element_id, operations):
        """Add access control policy details."""
        cursor = self.connection.cursor()
        try:
            # First, ensure the policy data element has access control enabled
            cursor.execute('''
                UPDATE policy_purpose_data_element 
                SET requires_access_control = TRUE, access_control_type = 'standard'
                WHERE id = %s
            ''', (policy_purpose_data_element_id,))
            
            # Then add the operations
            for operation in operations:
                cursor.execute('''
                    INSERT INTO policy_purpose_data_usage (policy_purpose_data_element_id, operation)
                    VALUES (%s, %s)
                ''', (policy_purpose_data_element_id, operation))
                
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding policy data usage: {e}")
            return False
    
    def add_policy_data_retention(self, policy_purpose_data_element_id, retention_period, retention_trigger, 
                                 retention_basis, auto_delete=True):
        """Add retention policy details."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO policy_purpose_data_retention 
                (policy_purpose_data_element_id, retention_period, retention_trigger, retention_basis, auto_delete)
                VALUES (%s, %s, %s, %s, %s)
            ''', (policy_purpose_data_element_id, retention_period, retention_trigger, retention_basis, auto_delete))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding policy data retention: {e}")
            return False
    
    def add_policy_data_security(self, policy_purpose_data_element_id, encryption_required, encryption_algorithm=None, 
                               masking_required=False, masking_format=None, logging_enabled=True):
        """Add security policy details."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO policy_purpose_data_security 
                (policy_purpose_data_element_id, encryption_required, encryption_algorithm, 
                masking_required, masking_format, logging_enabled)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (policy_purpose_data_element_id, encryption_required, encryption_algorithm, 
                  masking_required, masking_format, logging_enabled))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding policy data security: {e}")
            return False
    

