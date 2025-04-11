import pymysql.cursors
import json

class RegulatoryMetadataRepository:
    def __init__(self, connection):
        """Initialize the RegulatoryMetadataRepository with a database connection."""
        self.connection = connection
        self.setup_tables()
        
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
        self.create_law_context_data_subject_type_data_category_sensitivity_table()
        self.create_context_data_subject_type_data_category_sensitivity_table()
        self.create_law_transfer_table()
        self.create_law_data_subject_access_request_notification_requirements_table()
        self.create_law_purpose_category_legal_basis_table()
        self.create_legal_basis_requirements_table()
        
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
        
    def create_law_context_data_subject_type_data_category_sensitivity_table(self):
        """Create the Law Context Data Subject Type Data Category Sensitivity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `law_context_data_subject_type_data_category_sensitivity` (
            `law_id` INT NOT NULL,
            `context_id` INT NOT NULL,
            `data_subject_type_id` INT NOT NULL,
            `data_category_id` INT NOT NULL,
            `sensitivity_id` INT NOT NULL,
            PRIMARY KEY (`law_id`, `context_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`),
            FOREIGN KEY (`law_id`) REFERENCES `law`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`context_id`) REFERENCES `context`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_context_data_subject_type_data_category_sensitivity_table(self):
        """Create the Context Data Subject Type Data Category Sensitivity table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `context_data_subject_type_data_category_sensitivity` (
            `context_id` INT NOT NULL,
            `data_subject_type_id` INT NOT NULL,
            `data_category_id` INT NOT NULL,
            `sensitivity_id` INT NOT NULL,
            PRIMARY KEY (`context_id`, `data_subject_type_id`, `data_category_id`, `sensitivity_id`),
            FOREIGN KEY (`context_id`) REFERENCES `context`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_subject_type_id`) REFERENCES `data_subject_type`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`data_category_id`) REFERENCES `data_category`(`id`) ON DELETE CASCADE,
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
    
    def get_data_category_data_elements(self):
        """Get all data category data element relationships from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT dcde.data_category_id, dc.name as data_category_name, 
                   dcde.data_element_id, de.name as data_element_name
            FROM data_category_data_element dcde
            JOIN data_category dc ON dcde.data_category_id = dc.id
            JOIN data_element de ON dcde.data_element_id = de.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data category data element relationships: {e}")
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
    
    # Law Context Data Subject Type Data Category Sensitivity methods
    def add_law_context_data_subject_type_data_category_sensitivity(self, law_id, context_id, data_subject_type_id, data_category_id, sensitivity_id):
        """Add a new law context data subject type data category sensitivity relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO law_context_data_subject_type_data_category_sensitivity 
            (law_id, context_id, data_subject_type_id, data_category_id, sensitivity_id)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (law_id, context_id, data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding law context data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_law_context_data_subject_type_data_category_sensitivities(self):
        """Get all law context data subject type data category sensitivity relationships from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT lcdstdcs.law_id, l.name as law_name,
                   lcdstdcs.context_id, c.name as context_name,
                   lcdstdcs.data_subject_type_id, dst.name as data_subject_type_name,
                   lcdstdcs.data_category_id, dc.name as data_category_name,
                   lcdstdcs.sensitivity_id, s.name as sensitivity_name
            FROM law_context_data_subject_type_data_category_sensitivity lcdstdcs
            JOIN law l ON lcdstdcs.law_id = l.id
            JOIN context c ON lcdstdcs.context_id = c.id
            JOIN data_subject_type dst ON lcdstdcs.data_subject_type_id = dst.id
            JOIN data_category dc ON lcdstdcs.data_category_id = dc.id
            JOIN sensitivity s ON lcdstdcs.sensitivity_id = s.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving law context data subject type data category sensitivity relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_law_context_data_subject_type_data_category_sensitivity(self, law_id, context_id, data_subject_type_id, data_category_id, sensitivity_id):
        """Delete a law context data subject type data category sensitivity relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = """
            DELETE FROM law_context_data_subject_type_data_category_sensitivity 
            WHERE law_id = %s AND context_id = %s AND data_subject_type_id = %s AND data_category_id = %s AND sensitivity_id = %s;
            """
            cursor.execute(delete_query, (law_id, context_id, data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting law context data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    # Context Data Subject Type Data Category Sensitivity methods
    def add_context_data_subject_type_data_category_sensitivity(self, context_id, data_subject_type_id, data_category_id, sensitivity_id):
        """Add a new context data subject type data category sensitivity relationship to the database."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO context_data_subject_type_data_category_sensitivity 
            (context_id, data_subject_type_id, data_category_id, sensitivity_id)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (context_id, data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding context data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def get_context_data_subject_type_data_category_sensitivities(self):
        """Get all context data subject type data category sensitivity relationships from the database."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT cdstdcs.context_id, c.name as context_name,
                   cdstdcs.data_subject_type_id, dst.name as data_subject_type_name,
                   cdstdcs.data_category_id, dc.name as data_category_name,
                   cdstdcs.sensitivity_id, s.name as sensitivity_name
            FROM context_data_subject_type_data_category_sensitivity cdstdcs
            JOIN context c ON cdstdcs.context_id = c.id
            JOIN data_subject_type dst ON cdstdcs.data_subject_type_id = dst.id
            JOIN data_category dc ON cdstdcs.data_category_id = dc.id
            JOIN sensitivity s ON cdstdcs.sensitivity_id = s.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving context data subject type data category sensitivity relationships: {e}")
            return []
        finally:
            cursor.close()
    
    def delete_context_data_subject_type_data_category_sensitivity(self, context_id, data_subject_type_id, data_category_id, sensitivity_id):
        """Delete a context data subject type data category sensitivity relationship from the database."""
        cursor = self.connection.cursor()
        try:
            delete_query = """
            DELETE FROM context_data_subject_type_data_category_sensitivity 
            WHERE context_id = %s AND data_subject_type_id = %s AND data_category_id = %s AND sensitivity_id = %s;
            """
            cursor.execute(delete_query, (context_id, data_subject_type_id, data_category_id, sensitivity_id))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting context data subject type data category sensitivity relationship: {e}")
            return False
        finally:
            cursor.close()
    
    def seed_all_data(self):
        """Seed all regulatory metadata tables with initial data."""
        self.seed_law_jurisdictions()
        self.seed_law_legal_bases()
        self.seed_law_incident_breach_guidances()
        self.seed_law_purpose_category_legal_bases()
        self.seed_law_transfers()
        self.seed_law_data_subject_access_request_notification_requirements()
        
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
            

