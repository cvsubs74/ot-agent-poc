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
            
    def update_policy_data_usage(self, policy_purpose_data_element_id, operations=None, allowed=None):
        """Update access control policy details.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy-purpose-data element relationship
            operations (list, optional): List of operations to update (e.g., ['read', 'write', 'share'])
            allowed (bool, optional): Whether the operations are allowed
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            if operations is None and allowed is None:
                return False  # Nothing to update
                
            success = True
            
            # If allowed status is provided, update all existing operations
            if allowed is not None:
                cursor.execute('''
                    UPDATE policy_purpose_data_usage
                    SET allowed = %s
                    WHERE policy_purpose_data_element_id = %s
                ''', (allowed, policy_purpose_data_element_id))
                success = success and cursor.rowcount > 0
            
            # If operations are provided, handle them
            if operations:
                # First, get existing operations
                cursor.execute('''
                    SELECT operation FROM policy_purpose_data_usage
                    WHERE policy_purpose_data_element_id = %s
                ''', (policy_purpose_data_element_id,))
                existing_operations = [row[0] for row in cursor.fetchall()]
                
                # Add new operations that don't exist yet
                for operation in operations:
                    if operation not in existing_operations:
                        cursor.execute('''
                            INSERT INTO policy_purpose_data_usage (policy_purpose_data_element_id, operation, allowed)
                            VALUES (%s, %s, %s)
                        ''', (policy_purpose_data_element_id, operation, allowed if allowed is not None else True))
                        success = success and cursor.lastrowid is not None
            
            self.connection.commit()
            return success
        except Exception as e:
            print(f"Error updating policy data usage: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
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
            
    def update_policy_data_retention(self, policy_purpose_data_element_id, retention_period=None, retention_trigger=None, 
                                    retention_basis=None, auto_delete=None):
        """Update retention policy details.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy-purpose-data element relationship
            retention_period (str, optional): The retention period (e.g., '7 years', '30 days')
            retention_trigger (str, optional): What triggers the retention period (e.g., 'creation', 'last_access')
            retention_basis (str, optional): The basis for retention (e.g., 'legal', 'business', 'regulatory')
            auto_delete (bool, optional): Whether to automatically delete data after retention period
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            # Build update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if retention_period is not None:
                update_parts.append("retention_period = %s")
                params.append(retention_period)
                
            if retention_trigger is not None:
                update_parts.append("retention_trigger = %s")
                params.append(retention_trigger)
                
            if retention_basis is not None:
                update_parts.append("retention_basis = %s")
                params.append(retention_basis)
                
            if auto_delete is not None:
                update_parts.append("auto_delete = %s")
                params.append(auto_delete)
                
            if not update_parts:
                return False  # Nothing to update
                
            # Add the policy_purpose_data_element_id to params
            params.append(policy_purpose_data_element_id)
            
            query = f"""UPDATE policy_purpose_data_retention 
                      SET {', '.join(update_parts)} 
                      WHERE policy_purpose_data_element_id = %s;"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating policy data retention: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
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
    
    def update_policy_data_security(self, policy_purpose_data_element_id, encryption_required=None, encryption_algorithm=None, 
                                  masking_required=None, masking_format=None, logging_enabled=None):
        """Update security policy details.
        
        Args:
            policy_purpose_data_element_id (int): The ID of the policy-purpose-data element relationship
            encryption_required (bool, optional): Whether encryption is required
            encryption_algorithm (str, optional): The encryption algorithm to use
            masking_required (bool, optional): Whether masking is required
            masking_format (str, optional): The masking format to use
            logging_enabled (bool, optional): Whether logging is enabled
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        cursor = self.connection.cursor()
        try:
            # Build update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if encryption_required is not None:
                update_parts.append("encryption_required = %s")
                params.append(encryption_required)
                
            if encryption_algorithm is not None:
                update_parts.append("encryption_algorithm = %s")
                params.append(encryption_algorithm)
                
            if masking_required is not None:
                update_parts.append("masking_required = %s")
                params.append(masking_required)
                
            if masking_format is not None:
                update_parts.append("masking_format = %s")
                params.append(masking_format)
                
            if logging_enabled is not None:
                update_parts.append("logging_enabled = %s")
                params.append(logging_enabled)
                
            if not update_parts:
                return False  # Nothing to update
                
            # Add the policy_purpose_data_element_id to params
            params.append(policy_purpose_data_element_id)
            
            query = f"""UPDATE policy_purpose_data_security 
                      SET {', '.join(update_parts)} 
                      WHERE policy_purpose_data_element_id = %s;"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating policy data security: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    

