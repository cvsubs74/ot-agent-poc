import pymysql.cursors
import json

class InventoryRepository:
    def __init__(self, connection):
        """Initialize the InventoryRepository with a database connection."""
        self.connection = connection
        self.setup_tables()
        
    def setup_tables(self):
        """Create all the necessary tables for the inventory if they don't exist."""
        self.create_asset_table()
        self.create_policy_table()
        
    def create_asset_table(self):
        """Create the Asset table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `asset` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_policy_table(self):
        """Create the Policy table."""
        cursor = self.connection.cursor()
        create_table_query = """
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
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    # Asset methods
    def get_assets(self):
        """Get all assets from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM asset;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving assets: {e}")
            return []
        finally:
            cursor.close()
    
    def get_asset_by_id(self, asset_id):
        """Get an asset by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM asset WHERE id = %s;", (asset_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving asset by ID {asset_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def add_asset(self, name, description=None):
        """Add a new asset to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO asset (name, description) VALUES (%s, %s);",
                (name, description)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding asset: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    # Policy methods
    def get_policies(self):
        """Get all policies from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, policy_type, status, effective_date, expiration_date FROM policy;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving policies: {e}")
            return []
        finally:
            cursor.close()
    
    def get_policy_by_id(self, policy_id):
        """Get a policy by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, policy_type, status, effective_date, expiration_date FROM policy WHERE id = %s;", (policy_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving policy by ID {policy_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def add_policy(self, name, description=None, policy_type=None, status=None, effective_date=None, expiration_date=None):
        """Add a new policy to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy (name, description, policy_type, status, effective_date, expiration_date) VALUES (%s, %s, %s, %s, %s, %s);",
                (name, description, policy_type, status, effective_date, expiration_date)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding policy: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    # Seeding methods
    def seed_data(self):
        """Seed the database with initial data."""
        self.seed_assets()
        self.seed_policies()
    
    def seed_assets(self):
        """Seed the database with initial assets."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        assets = [
            ("CRM System", "Customer Relationship Management system containing customer data and interactions"),
            ("ERP System", "Enterprise Resource Planning system for managing business processes"),
            ("HR System", "Human Resources system containing employee data and records"),
            ("Marketing Platform", "Platform for managing marketing campaigns and customer engagement"),
            ("Financial Database", "Database containing financial records and transactions")
        ]
        
        try:
            for name, description in assets:
                cursor.execute("SELECT id FROM asset WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO asset (name, description) VALUES (%s, %s);",
                        (name, description)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding assets: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_policies(self):
        """Seed the database with initial policies."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        policies = [
            ("Data Retention Policy", "Policy governing how long data should be retained", "Retention", "Active", "2025-01-01", None),
            ("Data Access Control Policy", "Policy governing who can access specific data", "Access Control", "Active", "2025-01-01", None),
            ("Data Encryption Policy", "Policy governing encryption requirements for data", "Security", "Active", "2025-01-01", None),
            ("Data Backup Policy", "Policy governing backup requirements for data", "Backup", "Active", "2025-01-01", None),
            ("Data Quality Policy", "Policy governing data quality standards", "Quality", "Active", "2025-01-01", None),
            ("Data Classification Policy", "Policy governing classification of data sensitivity", "Classification", "Active", "2025-01-01", None),
            ("Data Sharing Policy", "Policy governing how data can be shared with third parties", "Sharing", "Active", "2025-01-01", None)
        ]
        
        try:
            for name, description, policy_type, status, effective_date, expiration_date in policies:
                cursor.execute("SELECT id FROM policy WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO policy (name, description, policy_type, status, effective_date, expiration_date) VALUES (%s, %s, %s, %s, %s, %s);",
                        (name, description, policy_type, status, effective_date, expiration_date)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding policies: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
