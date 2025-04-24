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
    

