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
        self.create_data_domain_table()
        self.create_dataset_table()
        self.create_policy_table()
        self.create_policy_dataset_table()
        self.create_policy_data_domain_table()
        
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
        
    def create_data_domain_table(self):
        """Create the DataDomain table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_domain` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_dataset_table(self):
        """Create the Dataset table with foreign keys to Asset and DataDomain."""
        cursor = self.connection.cursor()
        create_table_query = """
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
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_policy_dataset_table(self):
        """Create the many-to-many relationship table between Policy and Dataset."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_dataset` (
            `policy_id` INT NOT NULL,
            `dataset_id` INT NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`policy_id`, `dataset_id`),
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`dataset_id`) REFERENCES `dataset`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_policy_data_domain_table(self):
        """Create the many-to-many relationship table between Policy and DataDomain."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `policy_data_domain` (
            `policy_id` INT NOT NULL,
            `data_domain_id` INT NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`policy_id`, `data_domain_id`),
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_domain_id`) REFERENCES `data_domain`(`id`) ON DELETE CASCADE
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
    
    # DataDomain methods
    def get_data_domains(self):
        """Get all data domains from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_domain;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data domains: {e}")
            return []
        finally:
            cursor.close()
    
    def get_data_domain_by_id(self, data_domain_id):
        """Get a data domain by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_domain WHERE id = %s;", (data_domain_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving data domain by ID {data_domain_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def add_data_domain(self, name, description=None):
        """Add a new data domain to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO data_domain (name, description) VALUES (%s, %s);",
                (name, description)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding data domain: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    # Dataset methods
    def get_datasets(self):
        """Get all datasets from the database with their related asset and data domain information."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT d.id, d.name, d.source_system, d.description, 
                   a.id as asset_id, a.name as asset_name, 
                   dd.id as data_domain_id, dd.name as data_domain_name
            FROM dataset d
            JOIN asset a ON d.asset_id = a.id
            LEFT JOIN data_domain dd ON d.data_domain_id = dd.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving datasets: {e}")
            return []
        finally:
            cursor.close()
    
    def get_dataset_by_id(self, dataset_id):
        """Get a dataset by its ID with related asset and data domain information."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT d.id, d.name, d.source_system, d.description, 
                   a.id as asset_id, a.name as asset_name, 
                   dd.id as data_domain_id, dd.name as data_domain_name
            FROM dataset d
            JOIN asset a ON d.asset_id = a.id
            LEFT JOIN data_domain dd ON d.data_domain_id = dd.id
            WHERE d.id = %s;
            """
            cursor.execute(query, (dataset_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving dataset by ID {dataset_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def add_dataset(self, name, asset_id, source_system=None, data_domain_id=None, description=None):
        """Add a new dataset to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO dataset (name, asset_id, source_system, data_domain_id, description) VALUES (%s, %s, %s, %s, %s);",
                (name, asset_id, source_system, data_domain_id, description)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding dataset: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def get_datasets_by_asset_id(self, asset_id):
        """Get all datasets for a specific asset."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT d.id, d.name, d.source_system, d.description, 
                   a.id as asset_id, a.name as asset_name, 
                   dd.id as data_domain_id, dd.name as data_domain_name
            FROM dataset d
            JOIN asset a ON d.asset_id = a.id
            LEFT JOIN data_domain dd ON d.data_domain_id = dd.id
            WHERE d.asset_id = %s;
            """
            cursor.execute(query, (asset_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving datasets for asset ID {asset_id}: {e}")
            return []
        finally:
            cursor.close()
    
    def get_datasets_by_data_domain_id(self, data_domain_id):
        """Get all datasets for a specific data domain."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT d.id, d.name, d.source_system, d.description, 
                   a.id as asset_id, a.name as asset_name, 
                   dd.id as data_domain_id, dd.name as data_domain_name
            FROM dataset d
            JOIN asset a ON d.asset_id = a.id
            JOIN data_domain dd ON d.data_domain_id = dd.id
            WHERE d.data_domain_id = %s;
            """
            cursor.execute(query, (data_domain_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving datasets for data domain ID {data_domain_id}: {e}")
            return []
        finally:
            cursor.close()
    
    # Policy methods
    def get_policies(self):
        """Get all policies from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, policy_type FROM policy;")
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
            cursor.execute("SELECT id, name, description, policy_type FROM policy WHERE id = %s;", (policy_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving policy by ID {policy_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def add_policy(self, name, description=None, policy_type=None):
        """Add a new policy to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy (name, description, policy_type) VALUES (%s, %s, %s);",
                (name, description, policy_type)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding policy: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    # Policy-Dataset relationship methods
    def assign_policy_to_dataset(self, policy_id, dataset_id):
        """Assign a policy to a dataset."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy_dataset (policy_id, dataset_id) VALUES (%s, %s);",
                (policy_id, dataset_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error assigning policy {policy_id} to dataset {dataset_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def remove_policy_from_dataset(self, policy_id, dataset_id):
        """Remove a policy from a dataset."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM policy_dataset WHERE policy_id = %s AND dataset_id = %s;",
                (policy_id, dataset_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error removing policy {policy_id} from dataset {dataset_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def get_policies_for_dataset(self, dataset_id):
        """Get all policies assigned to a specific dataset."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT p.id, p.name, p.description, p.policy_type
            FROM policy p
            JOIN policy_dataset pd ON p.id = pd.policy_id
            WHERE pd.dataset_id = %s;
            """
            cursor.execute(query, (dataset_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving policies for dataset ID {dataset_id}: {e}")
            return []
        finally:
            cursor.close()
    
    def get_datasets_for_policy(self, policy_id):
        """Get all datasets assigned to a specific policy."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT d.id, d.name, d.source_system, d.description, 
                   a.id as asset_id, a.name as asset_name, 
                   dd.id as data_domain_id, dd.name as data_domain_name
            FROM dataset d
            JOIN asset a ON d.asset_id = a.id
            LEFT JOIN data_domain dd ON d.data_domain_id = dd.id
            JOIN policy_dataset pd ON d.id = pd.dataset_id
            WHERE pd.policy_id = %s;
            """
            cursor.execute(query, (policy_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving datasets for policy ID {policy_id}: {e}")
            return []
        finally:
            cursor.close()
    
    # Policy-DataDomain relationship methods
    def assign_policy_to_data_domain(self, policy_id, data_domain_id):
        """Assign a policy to a data domain."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO policy_data_domain (policy_id, data_domain_id) VALUES (%s, %s);",
                (policy_id, data_domain_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error assigning policy {policy_id} to data domain {data_domain_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def remove_policy_from_data_domain(self, policy_id, data_domain_id):
        """Remove a policy from a data domain."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "DELETE FROM policy_data_domain WHERE policy_id = %s AND data_domain_id = %s;",
                (policy_id, data_domain_id)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error removing policy {policy_id} from data domain {data_domain_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def get_policies_for_data_domain(self, data_domain_id):
        """Get all policies assigned to a specific data domain."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT p.id, p.name, p.description, p.policy_type
            FROM policy p
            JOIN policy_data_domain pdd ON p.id = pdd.policy_id
            WHERE pdd.data_domain_id = %s;
            """
            cursor.execute(query, (data_domain_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving policies for data domain ID {data_domain_id}: {e}")
            return []
        finally:
            cursor.close()
    
    def get_data_domains_for_policy(self, policy_id):
        """Get all data domains assigned to a specific policy."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT dd.id, dd.name, dd.description
            FROM data_domain dd
            JOIN policy_data_domain pdd ON dd.id = pdd.data_domain_id
            WHERE pdd.policy_id = %s;
            """
            cursor.execute(query, (policy_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data domains for policy ID {policy_id}: {e}")
            return []
        finally:
            cursor.close()
    
    # Seed data methods
    def seed_data(self):
        """Seed the database with initial inventory data."""
        self.seed_assets()
        self.seed_data_domains()
        self.seed_datasets()
        self.seed_policies()
        self.seed_policy_dataset_relationships()
        self.seed_policy_data_domain_relationships()
    
    def seed_assets(self):
        """Seed the database with initial asset data."""
        assets = [
            ("CRM System", "Customer Relationship Management system containing customer data and interactions"),
            ("ERP System", "Enterprise Resource Planning system for managing business processes"),
            ("HR Portal", "Human Resources portal for employee data management"),
            ("Marketing Platform", "Platform for managing marketing campaigns and customer engagement"),
            ("Financial Database", "Database containing financial records and transactions")
        ]
        
        cursor = self.connection.cursor()
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
    
    def seed_data_domains(self):
        """Seed the database with initial data domain data."""
        data_domains = [
            ("Customer Data", "Data related to customers and their interactions"),
            ("Employee Data", "Data related to employees and HR processes"),
            ("Financial Data", "Data related to financial transactions and records"),
            ("Marketing Data", "Data related to marketing campaigns and analytics"),
            ("Operational Data", "Data related to business operations and processes")
        ]
        
        cursor = self.connection.cursor()
        try:
            for name, description in data_domains:
                cursor.execute("SELECT id FROM data_domain WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO data_domain (name, description) VALUES (%s, %s);",
                        (name, description)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding data domains: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_datasets(self):
        """Seed the database with initial dataset data."""
        # Get asset IDs
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name FROM asset;")
        assets = {asset["name"]: asset["id"] for asset in cursor.fetchall()}
        
        # Get data domain IDs
        cursor.execute("SELECT id, name FROM data_domain;")
        data_domains = {domain["name"]: domain["id"] for domain in cursor.fetchall()}
        
        datasets = [
            ("Customer Profiles", assets["CRM System"], "Salesforce", data_domains["Customer Data"], "Core customer profile information"),
            ("Customer Interactions", assets["CRM System"], "Salesforce", data_domains["Customer Data"], "Records of customer interactions and support tickets"),
            ("Employee Records", assets["HR Portal"], "Workday", data_domains["Employee Data"], "Core employee records and personal information"),
            ("Payroll Data", assets["HR Portal"], "Workday", data_domains["Financial Data"], "Employee payroll and compensation data"),
            ("Financial Transactions", assets["Financial Database"], "Oracle", data_domains["Financial Data"], "Records of financial transactions"),
            ("Marketing Campaigns", assets["Marketing Platform"], "HubSpot", data_domains["Marketing Data"], "Marketing campaign data and metrics"),
            ("Customer Segmentation", assets["Marketing Platform"], "HubSpot", data_domains["Marketing Data"], "Customer segmentation data for targeted marketing"),
            ("Inventory Data", assets["ERP System"], "SAP", data_domains["Operational Data"], "Inventory and supply chain data"),
            ("Sales Data", assets["ERP System"], "SAP", data_domains["Financial Data"], "Sales records and revenue data"),
            ("Customer Analytics", assets["Marketing Platform"], "Tableau", data_domains["Customer Data"], "Customer behavior analytics and insights")
        ]
        
        try:
            for name, asset_id, source_system, data_domain_id, description in datasets:
                cursor.execute("SELECT id FROM dataset WHERE name = %s AND asset_id = %s;", (name, asset_id))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO dataset (name, asset_id, source_system, data_domain_id, description) VALUES (%s, %s, %s, %s, %s);",
                        (name, asset_id, source_system, data_domain_id, description)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding datasets: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_policies(self):
        """Seed the database with initial policy data."""
        policies = [
            ("Data Retention", "Policy governing how long data should be retained", "Retention"),
            ("Data Access Control", "Policy governing who can access specific data", "Access Control"),
            ("Data Encryption", "Policy governing encryption requirements for data", "Security"),
            ("Data Backup", "Policy governing backup requirements for data", "Backup"),
            ("Data Quality", "Policy governing data quality standards", "Quality"),
            ("Data Classification", "Policy governing classification of data sensitivity", "Classification"),
            ("Data Sharing", "Policy governing how data can be shared with third parties", "Sharing")
        ]
        
        cursor = self.connection.cursor()
        try:
            for name, description, policy_type in policies:
                cursor.execute("SELECT id FROM policy WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO policy (name, description, policy_type) VALUES (%s, %s, %s);",
                        (name, description, policy_type)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding policies: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_policy_dataset_relationships(self):
        """Seed the database with initial policy-dataset relationships."""
        # Get dataset IDs
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name FROM dataset;")
        datasets = {dataset["name"]: dataset["id"] for dataset in cursor.fetchall()}
        
        # Get policy IDs
        cursor.execute("SELECT id, name FROM policy;")
        policies = {policy["name"]: policy["id"] for policy in cursor.fetchall()}
        
        relationships = [
            (policies["Data Retention"], datasets["Customer Profiles"]),
            (policies["Data Access Control"], datasets["Customer Profiles"]),
            (policies["Data Encryption"], datasets["Customer Profiles"]),
            (policies["Data Retention"], datasets["Employee Records"]),
            (policies["Data Access Control"], datasets["Employee Records"]),
            (policies["Data Encryption"], datasets["Employee Records"]),
            (policies["Data Retention"], datasets["Financial Transactions"]),
            (policies["Data Backup"], datasets["Financial Transactions"]),
            (policies["Data Classification"], datasets["Financial Transactions"]),
            (policies["Data Quality"], datasets["Marketing Campaigns"]),
            (policies["Data Sharing"], datasets["Marketing Campaigns"]),
            (policies["Data Backup"], datasets["Inventory Data"]),
            (policies["Data Quality"], datasets["Inventory Data"])
        ]
        
        try:
            for policy_id, dataset_id in relationships:
                cursor.execute("SELECT policy_id FROM policy_dataset WHERE policy_id = %s AND dataset_id = %s;", (policy_id, dataset_id))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO policy_dataset (policy_id, dataset_id) VALUES (%s, %s);",
                        (policy_id, dataset_id)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding policy-dataset relationships: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_policy_data_domain_relationships(self):
        """Seed the database with initial policy-data domain relationships."""
        # Get data domain IDs
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name FROM data_domain;")
        data_domains = {domain["name"]: domain["id"] for domain in cursor.fetchall()}
        
        # Get policy IDs
        cursor.execute("SELECT id, name FROM policy;")
        policies = {policy["name"]: policy["id"] for policy in cursor.fetchall()}
        
        relationships = [
            (policies["Data Retention"], data_domains["Customer Data"]),
            (policies["Data Access Control"], data_domains["Customer Data"]),
            (policies["Data Sharing"], data_domains["Customer Data"]),
            (policies["Data Retention"], data_domains["Employee Data"]),
            (policies["Data Access Control"], data_domains["Employee Data"]),
            (policies["Data Encryption"], data_domains["Employee Data"]),
            (policies["Data Retention"], data_domains["Financial Data"]),
            (policies["Data Backup"], data_domains["Financial Data"]),
            (policies["Data Classification"], data_domains["Financial Data"]),
            (policies["Data Quality"], data_domains["Marketing Data"]),
            (policies["Data Sharing"], data_domains["Marketing Data"]),
            (policies["Data Backup"], data_domains["Operational Data"]),
            (policies["Data Quality"], data_domains["Operational Data"])
        ]
        
        try:
            for policy_id, data_domain_id in relationships:
                cursor.execute("SELECT policy_id FROM policy_data_domain WHERE policy_id = %s AND data_domain_id = %s;", (policy_id, data_domain_id))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO policy_data_domain (policy_id, data_domain_id) VALUES (%s, %s);",
                        (policy_id, data_domain_id)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding policy-data domain relationships: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
