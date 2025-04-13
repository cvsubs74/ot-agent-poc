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
        self.create_asset_data_element_table()
        self.create_processing_activity_table()
        self.create_processing_activity_purpose_table()
        self.create_processing_activity_asset_data_element_table()
        
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
        
    def create_asset_data_element_table(self):
        """Create the Asset Data Element relationship table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `asset_data_element` (
            `asset_id` INT NOT NULL,
            `data_element_id` INT NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`asset_id`, `data_element_id`),
            FOREIGN KEY (`asset_id`) REFERENCES `asset`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_element_id`) REFERENCES `data_element`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_processing_activity_table(self):
        """Create the Processing Activity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `processing_activity` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `status` VARCHAR(50),
            `start_date` DATE,
            `end_date` DATE,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def create_processing_activity_purpose_table(self):
        """Create the Processing Activity Purpose relationship table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `processing_activity_purpose` (
            `processing_activity_id` INT NOT NULL,
            `purpose_id` INT NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`processing_activity_id`, `purpose_id`),
            FOREIGN KEY (`processing_activity_id`) REFERENCES `processing_activity`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`purpose_id`) REFERENCES `purpose`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    def create_processing_activity_asset_data_element_table(self):
        """Create the Processing Activity Asset Data Element relationship table."""
        cursor = self.connection.cursor()
        create_table_query = """
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
    
    # Asset Data Element methods
    def get_asset_data_elements(self, asset_id=None):
        """Get data elements associated with an asset.
        
        Args:
            asset_id (int, optional): The ID of the asset to get data elements for.
                If None, returns all asset-data element relationships.
        
        Returns:
            list: A list of dictionaries containing asset-data element relationships.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if asset_id:
                query = """
                SELECT ade.asset_id, a.name as asset_name, ade.data_element_id, de.name as data_element_name, de.description as data_element_description
                FROM asset_data_element ade
                JOIN asset a ON ade.asset_id = a.id
                JOIN data_element de ON ade.data_element_id = de.id
                WHERE ade.asset_id = %s
                ORDER BY a.name, de.name
                """
                cursor.execute(query, (asset_id,))
            else:
                query = """
                SELECT ade.asset_id, a.name as asset_name, ade.data_element_id, de.name as data_element_name, de.description as data_element_description
                FROM asset_data_element ade
                JOIN asset a ON ade.asset_id = a.id
                JOIN data_element de ON ade.data_element_id = de.id
                ORDER BY a.name, de.name
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving asset data elements: {e}")
            return []
        finally:
            cursor.close()
    
    def add_asset_data_element(self, asset_id, data_element_id):
        """Associate a data element with an asset.
        
        Args:
            asset_id (int): The ID of the asset.
            data_element_id (int): The ID of the data element.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO asset_data_element (asset_id, data_element_id) VALUES (%s, %s);",
                (asset_id, data_element_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding asset data element: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def remove_asset_data_element(self, asset_id, data_element_id):
        """Remove an association between a data element and an asset.
        
        Args:
            asset_id (int): The ID of the asset.
            data_element_id (int): The ID of the data element.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM asset_data_element WHERE asset_id = %s AND data_element_id = %s;",
                (asset_id, data_element_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error removing asset data element: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    # Processing Activity methods
    def get_processing_activities(self):
        """Get all processing activities from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, status, start_date, end_date FROM processing_activity;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving processing activities: {e}")
            return []
        finally:
            cursor.close()
    
    def get_processing_activity_by_id(self, processing_activity_id):
        """Get a processing activity by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, status, start_date, end_date FROM processing_activity WHERE id = %s;", (processing_activity_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving processing activity by ID {processing_activity_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def add_processing_activity(self, name, description=None, status=None, start_date=None, end_date=None):
        """Add a new processing activity to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO processing_activity (name, description, status, start_date, end_date) VALUES (%s, %s, %s, %s, %s);",
                (name, description, status, start_date, end_date)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding processing activity: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    # Processing Activity Purpose methods
    def get_processing_activity_purposes(self, processing_activity_id=None):
        """Get purposes associated with a processing activity.
        
        Args:
            processing_activity_id (int, optional): The ID of the processing activity to get purposes for.
                If None, returns all processing activity-purpose relationships.
        
        Returns:
            list: A list of dictionaries containing processing activity-purpose relationships.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if processing_activity_id:
                query = """
                SELECT pap.processing_activity_id, pa.name as processing_activity_name, pap.purpose_id, p.name as purpose_name, 
                       pc.name as purpose_category, p.risk_level as purpose_risk_level, p.description as purpose_description
                FROM processing_activity_purpose pap
                JOIN processing_activity pa ON pap.processing_activity_id = pa.id
                JOIN purpose p ON pap.purpose_id = p.id
                LEFT JOIN purpose_category pc ON p.purpose_category_id = pc.id
                WHERE pap.processing_activity_id = %s
                ORDER BY pa.name, p.name
                """
                cursor.execute(query, (processing_activity_id,))
            else:
                query = """
                SELECT pap.processing_activity_id, pa.name as processing_activity_name, pap.purpose_id, p.name as purpose_name, 
                       pc.name as purpose_category, p.risk_level as purpose_risk_level, p.description as purpose_description
                FROM processing_activity_purpose pap
                JOIN processing_activity pa ON pap.processing_activity_id = pa.id
                JOIN purpose p ON pap.purpose_id = p.id
                LEFT JOIN purpose_category pc ON p.purpose_category_id = pc.id
                ORDER BY pa.name, p.name
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving processing activity purposes: {e}")
            return []
        finally:
            cursor.close()
    
    def add_processing_activity_purpose(self, processing_activity_id, purpose_id):
        """Associate a purpose with a processing activity.
        
        Args:
            processing_activity_id (int): The ID of the processing activity.
            purpose_id (int): The ID of the purpose.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO processing_activity_purpose (processing_activity_id, purpose_id) VALUES (%s, %s);",
                (processing_activity_id, purpose_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding processing activity purpose: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def remove_processing_activity_purpose(self, processing_activity_id, purpose_id):
        """Remove an association between a purpose and a processing activity.
        
        Args:
            processing_activity_id (int): The ID of the processing activity.
            purpose_id (int): The ID of the purpose.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM processing_activity_purpose WHERE processing_activity_id = %s AND purpose_id = %s;",
                (processing_activity_id, purpose_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error removing processing activity purpose: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    # Processing Activity Asset Data Element methods
    def get_processing_activity_asset_data_elements(self, processing_activity_id=None):
        """Get asset data elements associated with a processing activity.
        
        Args:
            processing_activity_id (int, optional): The ID of the processing activity to get asset data elements for.
                If None, returns all processing activity-asset-data element relationships.
        
        Returns:
            list: A list of dictionaries containing processing activity-asset-data element relationships.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if processing_activity_id:
                query = """
                SELECT paade.processing_activity_id, pa.name as processing_activity_name, 
                       paade.asset_id, a.name as asset_name, a.description as asset_description,
                       paade.data_element_id, de.name as data_element_name, de.description as data_element_description
                FROM processing_activity_asset_data_element paade
                JOIN processing_activity pa ON paade.processing_activity_id = pa.id
                JOIN asset a ON paade.asset_id = a.id
                JOIN data_element de ON paade.data_element_id = de.id
                WHERE paade.processing_activity_id = %s
                ORDER BY pa.name, a.name, de.name
                """
                cursor.execute(query, (processing_activity_id,))
            else:
                query = """
                SELECT paade.processing_activity_id, pa.name as processing_activity_name, 
                       paade.asset_id, a.name as asset_name, a.description as asset_description,
                       paade.data_element_id, de.name as data_element_name, de.description as data_element_description
                FROM processing_activity_asset_data_element paade
                JOIN processing_activity pa ON paade.processing_activity_id = pa.id
                JOIN asset a ON paade.asset_id = a.id
                JOIN data_element de ON paade.data_element_id = de.id
                ORDER BY pa.name, a.name, de.name
                """
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving processing activity asset data elements: {e}")
            return []
        finally:
            cursor.close()
    
    def add_processing_activity_asset_data_element(self, processing_activity_id, asset_id, data_element_id):
        """Associate an asset data element with a processing activity.
        
        Args:
            processing_activity_id (int): The ID of the processing activity.
            asset_id (int): The ID of the asset.
            data_element_id (int): The ID of the data element.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO processing_activity_asset_data_element (processing_activity_id, asset_id, data_element_id) VALUES (%s, %s, %s);",
                (processing_activity_id, asset_id, data_element_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding processing activity asset data element: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def remove_processing_activity_asset_data_element(self, processing_activity_id, asset_id, data_element_id):
        """Remove an association between an asset data element and a processing activity.
        
        Args:
            processing_activity_id (int): The ID of the processing activity.
            asset_id (int): The ID of the asset.
            data_element_id (int): The ID of the data element.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM processing_activity_asset_data_element WHERE processing_activity_id = %s AND asset_id = %s AND data_element_id = %s;",
                (processing_activity_id, asset_id, data_element_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error removing processing activity asset data element: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    # Seeding methods
    def seed_data(self):
        """Seed the database with initial data."""
        self.seed_assets()
        self.seed_policies()
        self.seed_asset_data_elements()
        self.seed_processing_activities()
        self.seed_processing_activity_purposes()
        self.seed_processing_activity_asset_data_elements()
    
    def seed_assets(self):
        """Seed the database with initial assets."""
        
    def seed_processing_activities(self):
        """Seed the database with initial processing activities."""
        cursor = self.connection.cursor()
        try:
            # First check if we already have data
            cursor.execute("SELECT COUNT(*) as count FROM processing_activity")
            result = cursor.fetchone()
            if result and result[0] > 0:
                print("Processing activities already seeded.")
                return
                
            # Define the processing activities
            processing_activities = [
                ("Customer Data Management", "Managing customer data for account management and support", "Active", "2025-01-01", None),
                ("Marketing Campaign Analysis", "Analyzing customer data for targeted marketing campaigns", "Active", "2025-01-15", None),
                ("Employee Onboarding", "Processing employee data during the onboarding process", "Active", "2025-02-01", None),
                ("Financial Transactions Processing", "Processing financial transaction data for accounting purposes", "Active", "2025-01-10", None),
                ("Website User Analytics", "Collecting and analyzing website user behavior data", "Active", "2025-01-05", None)
            ]
            
            # Insert the processing activities
            for activity in processing_activities:
                cursor.execute(
                    "INSERT INTO processing_activity (name, description, status, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
                    activity
                )
            
            self.connection.commit()
            print("Processing activities seeded successfully.")
        except Exception as e:
            print(f"Error seeding processing activities: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_processing_activity_purposes(self):
        """Seed the database with initial processing activity-purpose relationships."""
        cursor = self.connection.cursor()
        try:
            # First check if we already have data
            cursor.execute("SELECT COUNT(*) as count FROM processing_activity_purpose")
            result = cursor.fetchone()
            if result and result[0] > 0:
                print("Processing activity purposes already seeded.")
                return
                
            # Define the relationships between processing activities and purposes
            relationships = [
                # Customer Data Management - Customer Support and Service Delivery purposes
                {"processing_activity_name": "Customer Data Management", "purpose_name": "Customer Support"},
                {"processing_activity_name": "Customer Data Management", "purpose_name": "Service Delivery"},
                # Marketing Campaign Analysis - Marketing Campaigns and Product Analytics purposes
                {"processing_activity_name": "Marketing Campaign Analysis", "purpose_name": "Marketing Campaigns"},
                {"processing_activity_name": "Marketing Campaign Analysis", "purpose_name": "Product Analytics"},
                # Employee Onboarding - Employee Management purpose
                {"processing_activity_name": "Employee Onboarding", "purpose_name": "Employee Management"},
                # Financial Transactions Processing - Payment Processing and Regulatory Compliance purposes
                {"processing_activity_name": "Financial Transactions Processing", "purpose_name": "Payment Processing"},
                {"processing_activity_name": "Financial Transactions Processing", "purpose_name": "Regulatory Compliance"},
                # Website User Analytics - Product Analytics and Research and Development purposes
                {"processing_activity_name": "Website User Analytics", "purpose_name": "Product Analytics"},
                {"processing_activity_name": "Website User Analytics", "purpose_name": "Research and Development"}
            ]
            
            # Insert the relationships
            for relationship in relationships:
                processing_activity_name = relationship["processing_activity_name"]
                purpose_name = relationship["purpose_name"]
                
                # Get the processing activity ID
                cursor.execute("SELECT id FROM processing_activity WHERE name = %s", (processing_activity_name,))
                processing_activity_result = cursor.fetchone()
                if not processing_activity_result:
                    print(f"Processing activity {processing_activity_name} not found.")
                    continue
                processing_activity_id = processing_activity_result[0]
                
                # Get the purpose ID
                cursor.execute("SELECT id FROM purpose WHERE name = %s", (purpose_name,))
                purpose_result = cursor.fetchone()
                if not purpose_result:
                    print(f"Purpose {purpose_name} not found.")
                    continue
                purpose_id = purpose_result[0]
                
                # Insert the relationship
                cursor.execute(
                    "INSERT INTO processing_activity_purpose (processing_activity_id, purpose_id) VALUES (%s, %s)",
                    (processing_activity_id, purpose_id)
                )
            
            self.connection.commit()
            print("Processing activity purposes seeded successfully.")
        except Exception as e:
            print(f"Error seeding processing activity purposes: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_processing_activity_asset_data_elements(self):
        """Seed the database with initial processing activity-asset-data element relationships."""
        cursor = self.connection.cursor()
        try:
            # First check if we already have data
            cursor.execute("SELECT COUNT(*) as count FROM processing_activity_asset_data_element")
            result = cursor.fetchone()
            if result and result[0] > 0:
                print("Processing activity asset data elements already seeded.")
                return
                
            # Define the relationships between processing activities, assets, and data elements
            relationships = [
                # Customer Data Management - CRM System - Customer data elements
                {"processing_activity_name": "Customer Data Management", "asset_name": "CRM System", "data_element_names": ["Full Name", "Email Address", "Phone Number", "Address", "Customer ID"]},
                # Marketing Campaign Analysis - Marketing Platform - Customer and behavior data elements
                {"processing_activity_name": "Marketing Campaign Analysis", "asset_name": "Marketing Platform", "data_element_names": ["Full Name", "Email Address", "Customer ID", "IP Address", "Device ID"]},
                # Employee Onboarding - HR Portal - Employee data elements
                {"processing_activity_name": "Employee Onboarding", "asset_name": "HR Portal", "data_element_names": ["Full Name", "Email Address", "Phone Number", "Address", "Date of Birth", "Social Security Number"]},
                # Financial Transactions Processing - Financial Database - Financial data elements
                {"processing_activity_name": "Financial Transactions Processing", "asset_name": "Financial Database", "data_element_names": ["Full Name", "Customer ID", "Credit Card Number", "Bank Account Number"]},
                # Website User Analytics - Marketing Platform - User behavior data elements
                {"processing_activity_name": "Website User Analytics", "asset_name": "Marketing Platform", "data_element_names": ["IP Address", "Device ID"]},
                # Customer Data Management - ERP System - Customer data elements
                {"processing_activity_name": "Customer Data Management", "asset_name": "ERP System", "data_element_names": ["Full Name", "Email Address", "Customer ID"]}
            ]
            
            # Insert the relationships
            for relationship in relationships:
                processing_activity_name = relationship["processing_activity_name"]
                asset_name = relationship["asset_name"]
                data_element_names = relationship["data_element_names"]
                
                # Get the processing activity ID
                cursor.execute("SELECT id FROM processing_activity WHERE name = %s", (processing_activity_name,))
                processing_activity_result = cursor.fetchone()
                if not processing_activity_result:
                    print(f"Processing activity {processing_activity_name} not found.")
                    continue
                processing_activity_id = processing_activity_result[0]
                
                # Get the asset ID
                cursor.execute("SELECT id FROM asset WHERE name = %s", (asset_name,))
                asset_result = cursor.fetchone()
                if not asset_result:
                    print(f"Asset {asset_name} not found.")
                    continue
                asset_id = asset_result[0]
                
                # Get the data element IDs and insert the relationships
                for data_element_name in data_element_names:
                    cursor.execute("SELECT id FROM data_element WHERE name = %s", (data_element_name,))
                    data_element_result = cursor.fetchone()
                    if not data_element_result:
                        print(f"Data element {data_element_name} not found.")
                        continue
                    data_element_id = data_element_result[0]
                    
                    # Insert the relationship
                    cursor.execute(
                        "INSERT INTO processing_activity_asset_data_element (processing_activity_id, asset_id, data_element_id) VALUES (%s, %s, %s)",
                        (processing_activity_id, asset_id, data_element_id)
                    )
            
            self.connection.commit()
            print("Processing activity asset data elements seeded successfully.")
        except Exception as e:
            print(f"Error seeding processing activity asset data elements: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
        
    def seed_asset_data_elements(self):
        """Seed the database with initial asset-data element relationships."""
        cursor = self.connection.cursor()
        try:
            # First check if we already have data
            cursor.execute("SELECT COUNT(*) as count FROM asset_data_element")
            result = cursor.fetchone()
            if result and result[0] > 0:
                print("Asset data element relationships already seeded.")
                return
                
            # Define the relationships between assets and data elements
            relationships = [
                # CRM System
                {"asset_name": "CRM System", "data_element_names": ["Full Name", "Email Address", "Phone Number", "Address", "Customer ID", "Purchase History"]},
                # ERP System
                {"asset_name": "ERP System", "data_element_names": ["Full Name", "Email Address", "Customer ID", "Purchase History"]},
                # HR Portal
                {"asset_name": "HR Portal", "data_element_names": ["Full Name", "Email Address", "Phone Number", "Address", "Date of Birth", "Social Security Number"]},
                # Marketing Platform
                {"asset_name": "Marketing Platform", "data_element_names": ["Full Name", "Email Address", "Phone Number", "Customer ID", "IP Address", "Device ID"]},
                # Financial Database
                {"asset_name": "Financial Database", "data_element_names": ["Full Name", "Customer ID", "Credit Card Number", "Bank Account Number"]}
            ]
            
            # Insert the relationships
            for relationship in relationships:
                asset_name = relationship["asset_name"]
                data_element_names = relationship["data_element_names"]
                
                # Get the asset ID
                cursor.execute("SELECT id FROM asset WHERE name = %s", (asset_name,))
                asset_result = cursor.fetchone()
                if not asset_result:
                    print(f"Asset {asset_name} not found.")
                    continue
                asset_id = asset_result[0]
                
                # Get the data element IDs and insert the relationships
                for data_element_name in data_element_names:
                    cursor.execute("SELECT id FROM data_element WHERE name = %s", (data_element_name,))
                    data_element_result = cursor.fetchone()
                    if not data_element_result:
                        print(f"Data element {data_element_name} not found.")
                        continue
                    data_element_id = data_element_result[0]
                    
                    # Insert the relationship
                    cursor.execute(
                        "INSERT INTO asset_data_element (asset_id, data_element_id) VALUES (%s, %s)",
                        (asset_id, data_element_id)
                    )
            
            self.connection.commit()
            print("Asset data element relationships seeded successfully.")
        except Exception as e:
            print(f"Error seeding asset data elements: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
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
