import pymysql.cursors
import json

class GlossaryRepository:
    def __init__(self, connection):
        """Initialize the GlossaryRepository with a database connection."""
        self.connection = connection
        self.setup_tables()
        
    def setup_tables(self):
        """Create all the necessary tables for the glossary if they don't exist."""
        self.create_law_table()
        self.create_jurisdiction_table()
        self.create_legal_basis_table()
        self.create_data_element_table()
        self.create_data_subject_type_table()
        self.create_data_category_table()
        self.create_sensitivity_table()
        self.create_purpose_category_table()
        self.create_breach_type_table()
        self.create_policy_table()
        self.create_purpose_table()
        self.create_framework_table()
        self.create_control_table()
        self.create_external_roles_table()
        
    def create_law_table(self):
        """Create the Law table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `scope` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_jurisdiction_table(self):
        """Create the Jurisdiction table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `jurisdiction` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_legal_basis_table(self):
        """Create the Legal Basis table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `legal_basis` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_data_element_table(self):
        """Create the Data Element table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_element` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `default_masking_format` VARCHAR(100) NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def get_data_element_by_id(self, element_id):
        """Get a data element by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        query = """
        SELECT id, name, description, default_masking_format 
        FROM data_element 
        WHERE id = %s
        """
        cursor.execute(query, (element_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_data_element_by_name(self, element_name):
        """Get a data element by its name."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        query = """
        SELECT id, name, description, default_masking_format 
        FROM data_element 
        WHERE name = %s
        """
        cursor.execute(query, (element_name,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_all_data_elements(self):
        """Get all data elements."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        query = """
        SELECT id, name, description, default_masking_format 
        FROM data_element 
        ORDER BY name
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
        
    def create_data_subject_type_table(self):
        """Create the Data Subject Type table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_subject_type` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_data_category_table(self):
        """Create the Data Category table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `data_category` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_sensitivity_table(self):
        """Create the Sensitivity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `sensitivity` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        

        
    def create_purpose_category_table(self):
        """Create the Purpose Category table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `purpose_category` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_breach_type_table(self):
        """Create the Breach Type table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `breach_type` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `category` VARCHAR(100),
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
        
    def create_purpose_table(self):
        """Create the Purpose table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `purpose` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `purpose_category_id` INT,
            `risk_level` VARCHAR(50),
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`purpose_category_id`) REFERENCES `purpose_category`(`id`) ON DELETE SET NULL
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_framework_table(self):
        """Create the Framework table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `framework` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `version` VARCHAR(50),
            `category` VARCHAR(100),
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_control_table(self):
        """Create the Control table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `control` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `control_type` VARCHAR(100),
            `implementation_status` VARCHAR(50),
            `priority` VARCHAR(50),
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
    
    # Law methods
    def add_law(self, name, description, scope):
        """Add a new law to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law (name, description, scope)
            VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query, (name, description, scope))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law: {e}")
            return None
        finally:
            cursor.close()
    
    def get_laws(self):
        """Get all laws from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, scope FROM law;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving laws: {e}")
            return []
        finally:
            cursor.close()
    
    def get_law_by_id(self, law_id):
        """Get a law by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, scope FROM law WHERE id = %s;", (law_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving law by ID {law_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def update_law(self, law_id, name, description, scope):
        """Update an existing law."""
        cursor = self.connection.cursor()
        try:
            update_query = """
            UPDATE law
            SET name = %s, description = %s, scope = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (name, description, scope, law_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating law: {e}")
            return False
        finally:
            cursor.close()
    
    def delete_law(self, law_id):
        """Delete a law by its ID."""
        cursor = self.connection.cursor()
        try:
            delete_query = "DELETE FROM law WHERE id = %s;"
            cursor.execute(delete_query, (law_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law: {e}")
            return False
        finally:
            cursor.close()
    
    # Jurisdiction methods
    def add_jurisdiction(self, name):
        """Add a new jurisdiction to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO jurisdiction (name)
            VALUES (%s);
            """
            cursor.execute(insert_query, (name,))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding jurisdiction: {e}")
            return None
        finally:
            cursor.close()
    
    def get_jurisdictions(self):
        """Get all jurisdictions from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name FROM jurisdiction;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving jurisdictions: {e}")
            return []
        finally:
            cursor.close()
    
    def get_jurisdiction_by_id(self, jurisdiction_id):
        """Get a jurisdiction by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name FROM jurisdiction WHERE id = %s;", (jurisdiction_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving jurisdiction by ID {jurisdiction_id}: {e}")
            return None
        finally:
            cursor.close()
    
    # Legal Basis methods
    def add_legal_basis(self, name, description):
        """Add a new legal basis to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO legal_basis (name, description)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding legal basis: {e}")
            return None
        finally:
            cursor.close()
    
    def get_legal_bases(self):
        """Get all legal bases from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM legal_basis;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving legal bases: {e}")
            return []
        finally:
            cursor.close()
    
    def get_legal_basis_by_id(self, legal_basis_id):
        """Get a legal basis by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM legal_basis WHERE id = %s;", (legal_basis_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving legal basis by ID {legal_basis_id}: {e}")
            return None
        finally:
            cursor.close()
    
    # Data Element methods
    def add_data_element(self, name, description):
        """Add a new data element to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_element (name, description)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding data element: {e}")
            return None
        finally:
            cursor.close()
    
    def get_data_elements(self):
        """Get all data elements from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_element;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data elements: {e}")
            return []
        finally:
            cursor.close()
    
    def get_data_element_by_id(self, data_element_id):
        """Get a data element by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_element WHERE id = %s;", (data_element_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving data element by ID {data_element_id}: {e}")
            return None
        finally:
            cursor.close()
    
    # Data Subject Type methods
    def add_data_subject_type(self, name, description):
        """Add a new data subject type to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_subject_type (name, description)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding data subject type: {e}")
            return None
        finally:
            cursor.close()
    
    def get_data_subject_types(self):
        """Get all data subject types from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_subject_type;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data subject types: {e}")
            return []
        finally:
            cursor.close()
    
    def get_data_subject_type_by_id(self, data_subject_type_id):
        """Get a data subject type by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_subject_type WHERE id = %s;", (data_subject_type_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving data subject type by ID {data_subject_type_id}: {e}")
            return None
        finally:
            cursor.close()
    
    # Data Category methods
    def add_data_category(self, name, description):
        """Add a new data category to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO data_category (name, description)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding data category: {e}")
            return None
        finally:
            cursor.close()
    
    def get_data_categories(self):
        """Get all data categories from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_category;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data categories: {e}")
            return []
        finally:
            cursor.close()
    
    def get_data_category_by_id(self, data_category_id):
        """Get a data category by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM data_category WHERE id = %s;", (data_category_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving data category by ID {data_category_id}: {e}")
            return None
        finally:
            cursor.close()
    
    # Sensitivity methods
    def add_sensitivity(self, name, description):
        """Add a new sensitivity level to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO sensitivity (name, description)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding sensitivity: {e}")
            return None
        finally:
            cursor.close()
    
    def get_sensitivities(self):
        """Get all sensitivity levels from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM sensitivity;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving sensitivities: {e}")
            return []
        finally:
            cursor.close()
    
    def get_sensitivity_by_id(self, sensitivity_id):
        """Get a sensitivity level by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM sensitivity WHERE id = %s;", (sensitivity_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving sensitivity by ID {sensitivity_id}: {e}")
            return None
        finally:
            cursor.close()
    

    # Purpose Category methods
    def add_purpose_category(self, name, description):
        """Add a new purpose category to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO purpose_category (name, description)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding purpose category: {e}")
            return None
        finally:
            cursor.close()
    
    def get_purpose_categories(self):
        """Get all purpose categories from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM purpose_category;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving purpose categories: {e}")
            return []
        finally:
            cursor.close()
    
    def get_purpose_category_by_id(self, purpose_category_id):
        """Get a purpose category by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description FROM purpose_category WHERE id = %s;", (purpose_category_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving purpose category by ID {purpose_category_id}: {e}")
            return None
        finally:
            cursor.close()
    
    # Breach Type methods
    def get_breach_types(self):
        """Get all breach types from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, category FROM breach_type;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving breach types: {e}")
            return []
        finally:
            cursor.close()
    
    def get_breach_type_by_id(self, breach_type_id):
        """Get a breach type by its ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT id, name, description, category FROM breach_type WHERE id = %s;", (breach_type_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving breach type by ID {breach_type_id}: {e}")
            return None
        finally:
            cursor.close()
            
    def add_breach_type(self, name, description, category=None):
        """Add a new breach type to the database.
        
        Args:
            name (str): The name of the breach type
            description (str): A description of the breach type
            category (str, optional): The category of the breach type
            
        Returns:
            int: The ID of the newly created breach type or None if there was an error
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO breach_type (name, description, category) VALUES (%s, %s, %s);",
                (name, description, category)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding breach type: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    # Seed data methods
    def seed_data(self):
        """Seed the database with initial data."""
        self.seed_laws()
        self.seed_jurisdictions()
        self.seed_legal_bases()
        self.seed_data_elements()
        self.seed_breach_types()
        self.seed_data_subject_types()
        self.seed_data_categories()
        self.seed_sensitivities()

        self.seed_purpose_categories()
    
    def seed_laws(self):
        """Seed the database with initial law data."""
        laws = [
            {
                "name": "GDPR",
                "description": "General Data Protection Regulation - A comprehensive data protection law in the EU.",
                "scope": "Applies to organizations processing personal data of individuals in the EU, regardless of the organization's location."
            },
            {
                "name": "CCPA",
                "description": "California Consumer Privacy Act - Enhances privacy rights and consumer protection for residents of California.",
                "scope": "Applies to for-profit businesses that collect personal information from California residents and meet certain thresholds."
            },
            {
                "name": "CPRA",
                "description": "California Privacy Rights Act - Expands and amends the CCPA, introducing additional privacy protections.",
                "scope": "Applies to for-profit businesses that collect personal information from California residents and meet certain thresholds."
            },
            {
                "name": "LGPD",
                "description": "Lei Geral de Proteção de Dados - Brazil's General Data Protection Law.",
                "scope": "Applies to any business or organization that processes the personal data of individuals in Brazil, regardless of where the organization is based."
            },
            {
                "name": "PIPEDA",
                "description": "Personal Information Protection and Electronic Documents Act - Canada's federal privacy law for private-sector organizations.",
                "scope": "Applies to private-sector organizations across Canada that collect, use or disclose personal information in the course of commercial activities."
            }
        ]
        
        for law in laws:
            self.add_law(law["name"], law["description"], law["scope"])
    
    def seed_jurisdictions(self):
        """Seed the database with initial jurisdiction data."""
        jurisdictions = [
            {"name": "European Union"},
            {"name": "California, USA"},
            {"name": "Brazil"},
            {"name": "Canada"},
            {"name": "United Kingdom"},
            {"name": "Australia"},
            {"name": "Japan"},
            {"name": "South Korea"},
            {"name": "India"},
            {"name": "China"}
        ]
        
        for jurisdiction in jurisdictions:
            self.add_jurisdiction(jurisdiction["name"])
    
    def seed_legal_bases(self):
        """Seed the database with initial legal basis data."""
        legal_bases = [
            {
                "name": "Consent",
                "description": "The data subject has given clear consent for processing their personal data for a specific purpose."
            },
            {
                "name": "Contract",
                "description": "Processing is necessary for the performance of a contract with the data subject or to take steps to enter into a contract."
            },
            {
                "name": "Legal Obligation",
                "description": "Processing is necessary for compliance with a legal obligation to which the controller is subject."
            },
            {
                "name": "Vital Interests",
                "description": "Processing is necessary to protect the vital interests of the data subject or another person."
            },
            {
                "name": "Public Task",
                "description": "Processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority."
            },
            {
                "name": "Legitimate Interests",
                "description": "Processing is necessary for the purposes of legitimate interests pursued by the controller or a third party, except where such interests are overridden by the interests or rights of the data subject."
            }
        ]
        
        for legal_basis in legal_bases:
            self.add_legal_basis(legal_basis["name"], legal_basis["description"])
    
    def seed_data_elements(self):
        """Seed the database with initial data element data."""
        data_elements = [
            {
                "name": "Name",
                "description": "An individual's first name, last name, or full name."
            },
            {
                "name": "Email Address",
                "description": "An individual's email address used for electronic communication."
            },
            {
                "name": "Phone Number",
                "description": "An individual's telephone number used for voice communication."
            },
            {
                "name": "Address",
                "description": "An individual's physical address including street, city, state, and postal code."
            },
            {
                "name": "IP Address",
                "description": "A unique identifier assigned to a device connected to a network."
            },
            {
                "name": "Device ID",
                "description": "A unique identifier assigned to a specific device."
            },
            {
                "name": "Social Security Number",
                "description": "A unique identifier assigned to an individual for tax and identification purposes in the United States."
            },
            {
                "name": "Credit Card Number",
                "description": "A unique number assigned to a credit card for payment processing."
            },
            {
                "name": "Date of Birth",
                "description": "An individual's date of birth."
            },
            {
                "name": "Biometric Data",
                "description": "Physical or behavioral characteristics that can be used to identify an individual, such as fingerprints or facial recognition data."
            }
        ]
        
        for data_element in data_elements:
            self.add_data_element(data_element["name"], data_element["description"])
    
    def seed_data_subject_types(self):
        """Seed the database with initial data subject type data."""
        data_subject_types = [
            {
                "name": "Customer",
                "description": "An individual who purchases goods or services from an organization."
            },
            {
                "name": "Employee",
                "description": "An individual who works for an organization under an employment contract."
            },
            {
                "name": "Contractor",
                "description": "An individual who provides services to an organization but is not an employee."
            },
            {
                "name": "Job Applicant",
                "description": "An individual who applies for a job at an organization."
            },
            {
                "name": "Website Visitor",
                "description": "An individual who visits an organization's website."
            },
            {
                "name": "Minor",
                "description": "An individual under the age of 18 or the age of majority in their jurisdiction."
            },
            {
                "name": "Patient",
                "description": "An individual receiving medical care or treatment."
            },
            {
                "name": "Student",
                "description": "An individual enrolled in an educational institution."
            }
        ]
        
        for data_subject_type in data_subject_types:
            self.add_data_subject_type(data_subject_type["name"], data_subject_type["description"])
    
    def seed_data_categories(self):
        """Seed the database with initial data category data."""
        data_categories = [
            {
                "name": "Personal Identifiers",
                "description": "Information that can directly identify an individual, such as name, email address, or phone number."
            },
            {
                "name": "Financial Information",
                "description": "Information related to an individual's financial status, such as bank account details, credit card numbers, or income."
            },
            {
                "name": "Health Information",
                "description": "Information related to an individual's health status, medical history, or treatment."
            },
            {
                "name": "Biometric Information",
                "description": "Physical or behavioral characteristics that can be used to identify an individual, such as fingerprints or facial recognition data."
            },
            {
                "name": "Location Data",
                "description": "Information about an individual's physical location, such as GPS coordinates or IP address geolocation."
            },
            {
                "name": "Online Activity",
                "description": "Information about an individual's online behavior, such as browsing history or search queries."
            },
            {
                "name": "Employment Information",
                "description": "Information related to an individual's employment, such as job title, salary, or performance reviews."
            },
            {
                "name": "Education Information",
                "description": "Information related to an individual's education, such as degrees, grades, or academic records."
            }
        ]
        
        for data_category in data_categories:
            self.add_data_category(data_category["name"], data_category["description"])
    
    def seed_sensitivities(self):
        """Seed the database with initial sensitivity data."""
        sensitivities = [
            {
                "name": "Public",
                "description": "Information that is publicly available and poses minimal risk if disclosed."
            },
            {
                "name": "Internal",
                "description": "Information that is intended for internal use within an organization but poses minimal risk if disclosed."
            },
            {
                "name": "Confidential",
                "description": "Information that requires protection and poses moderate risk if disclosed."
            },
            {
                "name": "Restricted",
                "description": "Information that requires strict protection and poses significant risk if disclosed."
            },
            {
                "name": "Special Category",
                "description": "Information that is considered sensitive under data protection laws, such as health data, biometric data, or data revealing racial or ethnic origin."
            }
        ]
        
        for sensitivity in sensitivities:
            self.add_sensitivity(sensitivity["name"], sensitivity["description"])
    

    def seed_purpose_categories(self):
        """Seed the database with initial purpose category data."""
        purpose_categories = [
            {
                "name": "Contractual Necessity",
                "description": "Processing necessary for the performance of a contract with the data subject"
            },
            {
                "name": "Legal Compliance",
                "description": "Processing necessary for compliance with a legal obligation"
            },
            {
                "name": "Vital Interests",
                "description": "Processing necessary to protect vital interests of the data subject or another person"
            },
            {
                "name": "Public Interest",
                "description": "Processing necessary for the performance of a task carried out in the public interest"
            },
            {
                "name": "Legitimate Business Interests",
                "description": "Processing necessary for the legitimate interests pursued by the controller or a third party"
            },
            {
                "name": "Marketing and Advertising",
                "description": "Processing for direct marketing, advertising, and promotional activities"
            },
            {
                "name": "Research and Development",
                "description": "Processing for scientific, historical research, or statistical purposes"
            },
            {
                "name": "Service Provision",
                "description": "Processing necessary to provide the requested service to the data subject"
            },
            {
                "name": "Security and Fraud Prevention",
                "description": "Processing for security, fraud detection, prevention, and investigation"
            },
            {
                "name": "Analytics and Improvement",
                "description": "Processing for analytics, measurement, and service improvement"
            },
            {
                "name": "Employment Management",
                "description": "Processing related to employment, workforce management, and HR functions"
            },
            {
                "name": "Healthcare Provision",
                "description": "Processing for healthcare services, treatment, and management"
            }
        ]
        
        for purpose_category in purpose_categories:
            try:
                self.add_purpose_category(
                    name=purpose_category["name"],
                    description=purpose_category["description"]
                )
            except Exception as e:
                print(f"Error seeding purpose category: {e}")
            
    def seed_breach_types(self):
        """Seed the database with initial breach type data."""
        breach_types = [
            # Cyber Attacks category
            ("Phishing Attack", "Cybercriminals impersonate trusted entities to deceive individuals into providing sensitive information such as usernames, passwords, and credit card details.", "Cyber Attack"),
            ("Malware Attack", "Harmful programs such as viruses, spyware, and Trojans that infiltrate systems through infected email attachments, malicious websites, or removable media.", "Cyber Attack"),
            ("Ransomware Attack", "Malware that encrypts a victim's files, making them inaccessible without a decryption key, followed by a ransom demand for the key.", "Cyber Attack"),
            ("SQL Injection", "Attackers insert malicious SQL code into a database query, allowing them to access, modify, or delete database contents.", "Cyber Attack"),
            ("Man-in-the-Middle Attack", "The attacker intercepts and manipulates communication between two parties without their knowledge.", "Cyber Attack"),
            ("Denial of Service (DoS)", "Attacks that aim to disrupt the normal functioning of a network, service, or website by overwhelming it with a flood of traffic.", "Cyber Attack"),
            ("Distributed Denial of Service (DDoS)", "Similar to DoS but using multiple compromised systems to launch the attack, making it more powerful and harder to mitigate.", "Cyber Attack"),
            ("Advanced Persistent Threat (APT)", "Highly sophisticated and persistent attacks, often conducted by well-funded cybercriminals or nation-states, aiming to infiltrate and control networks for prolonged periods.", "Cyber Attack"),
            ("Zero-day Exploit", "Attacks that exploit previously unknown vulnerabilities in software or hardware before developers have had a chance to create and release patches.", "Cyber Attack"),
            ("Credential Stuffing", "Attackers use stolen account credentials from one service to gain unauthorized access to other services where users have reused the same credentials.", "Cyber Attack"),
            ("API Abuse", "Exploiting vulnerabilities in application programming interfaces to gain unauthorized access to data or functionality.", "Cyber Attack"),
            
            # Insider Threats category
            ("Malicious Insider", "Data theft or sabotage by a disgruntled employee or contractor with legitimate access to systems and data.", "Insider Threat"),
            ("Accidental Exposure", "Unintentional disclosure of sensitive information by employees through mistakes or negligence.", "Insider Threat"),
            ("Privilege Misuse", "Authorized users accessing data or systems beyond what is necessary for their job functions.", "Insider Threat"),
            ("Compromised Insider", "An employee whose credentials have been stolen or who has been manipulated through social engineering.", "Insider Threat"),
            
            # Physical Breaches category
            ("Device Theft", "Theft of physical devices such as laptops, smartphones, or storage media containing sensitive data.", "Physical Breach"),
            ("Unauthorized Physical Access", "Gaining unauthorized entry to facilities where sensitive data is stored or processed.", "Physical Breach"),
            ("Dumpster Diving", "Retrieving discarded documents or media containing sensitive information from trash containers.", "Physical Breach"),
            ("Tailgating", "Following an authorized person into a secure area without proper authentication.", "Physical Breach"),
            
            # Supply Chain Breaches category
            ("Third-Party Vendor Breach", "Security incidents at third-party vendors that compromise data they process or store on behalf of their clients.", "Supply Chain Breach"),
            ("Software Supply Chain Attack", "Compromising software updates or components to distribute malware to target organizations, as seen in the SolarWinds attack.", "Supply Chain Breach"),
            ("Hardware Supply Chain Attack", "Tampering with hardware components during manufacturing or distribution to introduce vulnerabilities or backdoors.", "Supply Chain Breach"),
        ]
        
        cursor = self.connection.cursor()
        try:
            for name, description, category in breach_types:
                cursor.execute("SELECT id FROM breach_type WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO breach_type (name, description, category) VALUES (%s, %s, %s);",
                        (name, description, category)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding breach types: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
            
    # Policy methods
    def add_policy(self, name, description, policy_type=None, status=None, effective_date=None, expiration_date=None):
        """Add a new policy to the database.
        
        Args:
            name (str): The name of the policy
            description (str): A description of the policy
            policy_type (str, optional): The type of policy (e.g., 'Access Control', 'Retention')
            status (str, optional): The status of the policy (e.g., 'Active', 'Draft')
            effective_date (str, optional): The effective date of the policy (YYYY-MM-DD)
            expiration_date (str, optional): The expiration date of the policy (YYYY-MM-DD)
            
        Returns:
            int: The ID of the newly created policy or None if there was an error
        """
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
    
    def get_policies(self):
        """Get all policies from the database.
        
        Returns:
            list: A list of dictionaries containing policy information
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, name, description, policy_type, status, effective_date, expiration_date FROM policy;")
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
    
    def get_policy_by_id(self, policy_id):
        """Get a policy by its ID.
        
        Args:
            policy_id (int): The ID of the policy to retrieve
            
        Returns:
            dict: A dictionary containing policy information or None if not found
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT id, name, description, policy_type, status, effective_date, expiration_date FROM policy WHERE id = %s;",
                (policy_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "policy_type": row[3],
                    "status": row[4],
                    "effective_date": row[5],
                    "expiration_date": row[6]
                }
            return None
        except Exception as e:
            print(f"Error getting policy by ID: {e}")
            return None
        finally:
            cursor.close()
    
    # Purpose methods
    def add_purpose(self, name, description, purpose_category_id=None, risk_level=None):
        """Add a new purpose to the database.
        
        Args:
            name (str): The name of the purpose
            description (str): A description of the purpose
            purpose_category_id (int, optional): The ID of the purpose category
            risk_level (str, optional): The risk level of the purpose (e.g., 'Low', 'Medium', 'High')
            
        Returns:
            int: The ID of the newly created purpose or None if there was an error
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO purpose (name, description, purpose_category_id, risk_level) VALUES (%s, %s, %s, %s);",
                (name, description, purpose_category_id, risk_level)
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding purpose: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def get_purposes(self):
        """Get all purposes from the database.
        
        Returns:
            list: A list of dictionaries containing purpose information
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT p.id, p.name, p.description, p.purpose_category_id, pc.name as category_name, p.risk_level 
                FROM purpose p
                LEFT JOIN purpose_category pc ON p.purpose_category_id = pc.id;
            """)
            purposes = []
            for row in cursor.fetchall():
                purposes.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "purpose_category_id": row[3],
                    "category_name": row[4],
                    "risk_level": row[5]
                })
            return purposes
        except Exception as e:
            print(f"Error getting purposes: {e}")
            return []
        finally:
            cursor.close()
    
    def get_purpose_by_id(self, purpose_id):
        """Get a purpose by its ID.
        
        Args:
            purpose_id (int): The ID of the purpose to retrieve
            
        Returns:
            dict: A dictionary containing purpose information or None if not found
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT p.id, p.name, p.description, p.purpose_category_id, pc.name as category_name, p.risk_level 
                FROM purpose p
                LEFT JOIN purpose_category pc ON p.purpose_category_id = pc.id
                WHERE p.id = %s;
            """, (purpose_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "purpose_category_id": row[3],
                    "category_name": row[4],
                    "risk_level": row[5]
                }
            return None
        except Exception as e:
            print(f"Error getting purpose by ID: {e}")
            return None
        finally:
            cursor.close()
    
    def create_external_roles_table(self):
        cursor = self.connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS external_roles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            source_system VARCHAR(255) NOT NULL,
            source_role_name VARCHAR(255) NOT NULL,
            UNIQUE(source_system, source_role_name)
        );
        '''
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def add_external_role(self, name, description, source_system, source_role_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT IGNORE INTO external_roles (name, description, source_system, source_role_name) VALUES (%s, %s, %s, %s);",
                (name, description, source_system, source_role_name)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error adding external role: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def get_external_roles(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, name, description, source_system, source_role_name FROM external_roles;")
            roles = cursor.fetchall()
            return roles
        except Exception as e:
            print(f"Error fetching external roles: {e}")
            return []
        finally:
            cursor.close()

    def seed_policies(self):
        """Seed the database with initial policy data."""
        policies = [
            ("Data Access Control Policy", "Defines rules for accessing data based on purpose limitation principles", "Access Control", "Active", "2025-01-01", None),
            ("Data Retention Policy", "Defines how long data should be retained based on purpose and legal requirements", "Retention", "Active", "2025-01-01", None),
            ("Data Sharing Policy", "Defines rules for sharing data with third parties", "Sharing", "Active", "2025-01-01", None),
            ("Data Minimization Policy", "Ensures only necessary data is collected and processed", "Collection", "Active", "2025-01-01", None),
            ("Data Security Policy", "Defines security controls for protecting data", "Security", "Active", "2025-01-01", None)
        ]
        
        cursor = self.connection.cursor()
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
    
    def seed_purposes(self):
        """Seed the database with initial purpose data."""
        # First, get purpose category IDs
        cursor = self.connection.cursor()
        purpose_category_ids = {}
        try:
            cursor.execute("SELECT id, name FROM purpose_category;")
            for row in cursor.fetchall():
                purpose_category_ids[row[1]] = row[0]
            
            # Define purposes with their categories
            purposes = [
                ("Customer Support", "Providing assistance and support to customers", "Customer Service", "Low"),
                ("Fraud Detection", "Identifying and preventing fraudulent activities", "Security", "Medium"),
                ("Marketing Campaigns", "Promoting products and services to customers", "Marketing", "Medium"),
                ("Product Analytics", "Analyzing product usage for improvement", "Analytics", "Medium"),
                ("User Authentication", "Verifying user identity for access control", "Security", "High"),
                ("Regulatory Compliance", "Meeting legal and regulatory requirements", "Legal", "High"),
                ("Payment Processing", "Processing financial transactions", "Financial", "High"),
                ("Service Delivery", "Providing core services to users", "Operations", "Medium"),
                ("Research and Development", "Developing new products and features", "Product Development", "Medium"),
                ("Employee Management", "Managing employee data and performance", "HR", "Medium")
            ]
            
            for name, description, category, risk_level in purposes:
                cursor.execute("SELECT id FROM purpose WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    category_id = purpose_category_ids.get(category)
                    cursor.execute(
                        "INSERT INTO purpose (name, description, purpose_category_id, risk_level) VALUES (%s, %s, %s, %s);",
                        (name, description, category_id, risk_level)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding purposes: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def seed_all_data(self):
        """Seed all glossary tables with initial data."""
        self.seed_laws()
        self.seed_jurisdictions()
        self.seed_legal_bases()
        self.seed_data_elements()
        self.seed_data_subject_types()
        self.seed_data_categories()
        self.seed_sensitivities()
        self.seed_purpose_categories()
        self.seed_breach_types()
        self.seed_policies()
        self.seed_purposes()
        self.seed_frameworks()
        self.seed_controls()
        
    # Framework methods
    def add_framework(self, name, description, version, category):
        """Add a new framework to the database.
        
        Args:
            name (str): The name of the framework
            description (str): The description of the framework
            version (str): The version of the framework
            category (str): The category of the framework
            
        Returns:
            int: The ID of the newly added framework or None if an error occurred
        """
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO framework (name, description, version, category)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (name, description, version, category))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding framework: {e}")
            return None
        finally:
            cursor.close()
    
    def get_frameworks(self):
        """Get all frameworks from the database.
        
        Returns:
            list: A list of dictionaries containing framework information
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, name, description, version, category FROM framework;")
            frameworks = []
            for row in cursor.fetchall():
                frameworks.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "version": row[3],
                    "category": row[4]
                })
            return frameworks
        except Exception as e:
            print(f"Error getting frameworks: {e}")
            return []
        finally:
            cursor.close()
    
    def get_risks(self):
        """Get all risks from the database.
        
        Returns:
            list: A list of dictionaries containing risk information
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, name, description, category, likelihood, impact FROM risk;")
            risks = []
            for row in cursor.fetchall():
                risks.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "category": row[3],
                    "likelihood": row[4],
                    "impact": row[5]
                })
            return risks
        except Exception as e:
            print(f"Error getting risks: {e}")
            return []
        finally:
            cursor.close()
    
    def get_framework_by_id(self, framework_id):
        """Get a framework by its ID.
        
        Args:
            framework_id (int): The ID of the framework to retrieve
            
        Returns:
            dict: A dictionary containing framework information or None if not found
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT id, name, description, version, category 
                FROM framework 
                WHERE id = %s;
            """, (framework_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "version": row[3],
                    "category": row[4]
                }
            return None
        except Exception as e:
            print(f"Error getting framework by ID {framework_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def seed_frameworks(self):
        """Seed the database with initial framework data."""
        frameworks = [
            ("NIST CSF", "NIST Cybersecurity Framework", "2.0", "Security"),
            ("ISO 27001", "Information Security Management System Standard", "2022", "Security"),
            ("GDPR Controls", "General Data Protection Regulation Controls Framework", "1.0", "Privacy"),
            ("HIPAA Security Rule", "Health Insurance Portability and Accountability Act Security Standards", "2013", "Healthcare"),
            ("PCI DSS", "Payment Card Industry Data Security Standard", "4.0", "Financial"),
            ("SOC 2", "Service Organization Control 2", "2017", "Compliance"),
            ("CCPA Framework", "California Consumer Privacy Act Controls Framework", "1.0", "Privacy"),
            ("NIST 800-53", "Security and Privacy Controls for Information Systems and Organizations", "Rev. 5", "Government")
        ]
        
        cursor = self.connection.cursor()
        try:
            for name, description, version, category in frameworks:
                cursor.execute("SELECT id FROM framework WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO framework (name, description, version, category) VALUES (%s, %s, %s, %s);",
                        (name, description, version, category)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding frameworks: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
            
    # Control methods
    def add_control(self, name, description, control_type, implementation_status, priority):
        """Add a new control to the database.
        
        Args:
            name (str): The name of the control
            description (str): The description of the control
            control_type (str): The type of control (e.g., 'Technical', 'Administrative', 'Physical')
            implementation_status (str): The implementation status of the control
            priority (str): The priority of the control (e.g., 'High', 'Medium', 'Low')
            
        Returns:
            int: The ID of the newly added control or None if an error occurred
        """
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO control (name, description, control_type, implementation_status, priority)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (name, description, control_type, implementation_status, priority))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding control: {e}")
            return None
        finally:
            cursor.close()
    
    def get_controls(self):
        """Get all controls from the database.
        
        Returns:
            list: A list of dictionaries containing control information
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, name, description, control_type, implementation_status, priority FROM control;")
            controls = []
            for row in cursor.fetchall():
                controls.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "control_type": row[3],
                    "implementation_status": row[4],
                    "priority": row[5]
                })
            return controls
        except Exception as e:
            print(f"Error getting controls: {e}")
            return []
        finally:
            cursor.close()
    
    def get_control_by_id(self, control_id):
        """Get a control by its ID.
        
        Args:
            control_id (int): The ID of the control to retrieve
            
        Returns:
            dict: A dictionary containing control information or None if not found
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT id, name, description, control_type, implementation_status, priority 
                FROM control 
                WHERE id = %s;
            """, (control_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "control_type": row[3],
                    "implementation_status": row[4],
                    "priority": row[5]
                }
            return None
        except Exception as e:
            print(f"Error getting control by ID {control_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def seed_controls(self):
        """Seed the database with initial control data."""
        controls = [
            ("Access Control", "Limit access to information systems to authorized users", "Technical", "Implemented", "High"),
            ("Data Encryption", "Encrypt sensitive data at rest and in transit", "Technical", "Implemented", "High"),
            ("Security Awareness Training", "Educate users about security best practices", "Administrative", "Implemented", "Medium"),
            ("Incident Response Plan", "Procedures for responding to security incidents", "Administrative", "Implemented", "High"),
            ("Vulnerability Management", "Identify and remediate security vulnerabilities", "Technical", "Implemented", "High"),
            ("Data Backup", "Regular backup of critical data", "Technical", "Implemented", "Medium"),
            ("Physical Access Controls", "Restrict physical access to facilities", "Physical", "Implemented", "Medium"),
            ("Network Segmentation", "Divide network into segments to limit access", "Technical", "Implemented", "Medium"),
            ("Secure Configuration", "Implement secure configurations for systems", "Technical", "Implemented", "High"),
            ("Audit Logging", "Record and monitor system activities", "Technical", "Implemented", "Medium"),
            ("Data Loss Prevention", "Prevent unauthorized data exfiltration", "Technical", "Implemented", "High"),
            ("Vendor Management", "Assess and manage third-party security risks", "Administrative", "Implemented", "Medium"),
            ("Change Management", "Control changes to systems and applications", "Administrative", "Implemented", "Medium"),
            ("Disaster Recovery", "Recover systems after a disaster", "Administrative", "Implemented", "High"),
            ("Penetration Testing", "Test systems for security vulnerabilities", "Technical", "Implemented", "Medium"),
            ("Multi-Factor Authentication", "Require multiple forms of authentication", "Technical", "Implemented", "High"),
            ("Data Minimization", "Collect only necessary personal data", "Administrative", "Implemented", "Medium"),
            ("Privacy Impact Assessment", "Assess privacy risks of new projects", "Administrative", "Implemented", "Medium"),
            ("Data Subject Rights Management", "Process data subject rights requests", "Administrative", "Implemented", "High"),
            ("Consent Management", "Obtain and manage user consent", "Administrative", "Implemented", "High")
        ]
        
        cursor = self.connection.cursor()
        try:
            for name, description, control_type, implementation_status, priority in controls:
                cursor.execute("SELECT id FROM control WHERE name = %s;", (name,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO control (name, description, control_type, implementation_status, priority) VALUES (%s, %s, %s, %s, %s);",
                        (name, description, control_type, implementation_status, priority)
                    )
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding controls: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
