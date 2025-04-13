import pymysql.cursors
import json

class ObligationRepository:
    def __init__(self, connection):
        """Initialize the ObligationRepository with a database connection."""
        self.connection = connection
        self.setup_tables()
        
    def setup_tables(self):
        """Create all the necessary tables for obligations if they don't exist."""
        self.create_obligations_table()
        self.create_sensitivity_obligation_table()
        self.seed_sensitivity_obligations()
        
    def create_obligations_table(self):
        """Create the Obligations table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `obligation` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `source` VARCHAR(255),
            `control_type` VARCHAR(100),
            `status` VARCHAR(50) DEFAULT 'Open',
            `policy_id` INT NULL,
            `risk_accepted` BOOLEAN DEFAULT FALSE,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE SET NULL
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_sensitivity_obligation_table(self):
        """Create the Sensitivity Obligation mapping table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `sensitivity_obligation` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `sensitivity_id` INT NOT NULL,
            `obligation_name` VARCHAR(255) NOT NULL,
            `obligation_description` TEXT,
            `control_type` VARCHAR(100),
            `priority` VARCHAR(50) DEFAULT 'Medium',
            FOREIGN KEY (`sensitivity_id`) REFERENCES `sensitivity`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def add_obligation(self, name, description, source=None, control_type=None, status="Open"):
        """Add a new obligation to the database."""
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO obligation (name, description, source, control_type, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, description, source, control_type, status))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding obligation: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
            
    def get_obligations(self, status=None, control_type=None, policy_linked=None):
        """Get all obligations from the database with optional filters."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT o.id, o.name, o.description, o.source, o.control_type, o.status, 
                   o.policy_id, p.name as policy_name, o.risk_accepted, o.created_at
            FROM obligation o
            LEFT JOIN policy p ON o.policy_id = p.id
            """
            
            params = []
            where_clauses = []
            
            if status:
                where_clauses.append("o.status = %s")
                params.append(status)
                
            if control_type:
                where_clauses.append("o.control_type = %s")
                params.append(control_type)
                
            if policy_linked is not None:
                if policy_linked:
                    where_clauses.append("o.policy_id IS NOT NULL")
                else:
                    where_clauses.append("o.policy_id IS NULL")
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            query += " ORDER BY o.created_at DESC"
            
            cursor.execute(query, params)
            
            obligations = []
            for row in cursor.fetchall():
                obligations.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "source": row[3],
                    "control_type": row[4],
                    "status": row[5],
                    "policy_id": row[6],
                    "policy_name": row[7],
                    "risk_accepted": row[8],
                    "created_at": row[9]
                })
            return obligations
        except Exception as e:
            print(f"Error getting obligations: {e}")
            return []
        finally:
            cursor.close()
            
    def update_obligation(self, obligation_id, name=None, description=None, source=None, 
                         control_type=None, status=None, policy_id=None, risk_accepted=None):
        """Update an existing obligation in the database."""
        cursor = self.connection.cursor()
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
                
            if description is not None:
                updates.append("description = %s")
                params.append(description)
                
            if source is not None:
                updates.append("source = %s")
                params.append(source)
                
            if control_type is not None:
                updates.append("control_type = %s")
                params.append(control_type)
                
            if status is not None:
                updates.append("status = %s")
                params.append(status)
                
            if policy_id is not None:
                updates.append("policy_id = %s")
                params.append(policy_id)
                
            if risk_accepted is not None:
                updates.append("risk_accepted = %s")
                params.append(risk_accepted)
                
            if not updates:
                return False
                
            query = f"UPDATE obligation SET {', '.join(updates)} WHERE id = %s"
            params.append(obligation_id)
            
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating obligation: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def delete_obligation(self, obligation_id):
        """Delete an obligation from the database."""
        cursor = self.connection.cursor()
        try:
            query = "DELETE FROM obligation WHERE id = %s"
            cursor.execute(query, (obligation_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting obligation: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def add_sensitivity_obligation(self, sensitivity_id, obligation_name, obligation_description, 
                                  control_type, priority="Medium"):
        """Add a new sensitivity-obligation mapping to the database."""
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO sensitivity_obligation 
            (sensitivity_id, obligation_name, obligation_description, control_type, priority)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (sensitivity_id, obligation_name, obligation_description, 
                                  control_type, priority))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding sensitivity obligation: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
            
    def get_sensitivity_obligations(self, sensitivity_id=None, control_type=None):
        """Get all sensitivity-obligation mappings from the database with optional filters."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT so.id, so.sensitivity_id, s.name as sensitivity_name, 
                   so.obligation_name, so.obligation_description, 
                   so.control_type, so.priority
            FROM sensitivity_obligation so
            JOIN sensitivity s ON so.sensitivity_id = s.id
            """
            
            params = []
            where_clauses = []
            
            if sensitivity_id:
                where_clauses.append("so.sensitivity_id = %s")
                params.append(sensitivity_id)
                
            if control_type:
                where_clauses.append("so.control_type = %s")
                params.append(control_type)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            query += " ORDER BY so.sensitivity_id, so.priority"
            
            cursor.execute(query, params)
            
            mappings = []
            for row in cursor.fetchall():
                mappings.append({
                    "id": row[0],
                    "sensitivity_id": row[1],
                    "sensitivity_name": row[2],
                    "obligation_name": row[3],
                    "obligation_description": row[4],
                    "control_type": row[5],
                    "priority": row[6]
                })
            return mappings
        except Exception as e:
            print(f"Error getting sensitivity obligations: {e}")
            return []
        finally:
            cursor.close()
            
    def generate_obligations_from_sensitivity(self, sensitivity_id):
        """Generate obligations based on a sensitivity level."""
        cursor = self.connection.cursor()
        try:
            # Get all standard obligations for this sensitivity level
            query = """
            SELECT obligation_name, obligation_description, control_type
            FROM sensitivity_obligation
            WHERE sensitivity_id = %s
            """
            cursor.execute(query, (sensitivity_id,))
            
            sensitivity_obligations = cursor.fetchall()
            
            # Get sensitivity name for source attribution
            cursor.execute("SELECT name FROM sensitivity WHERE id = %s", (sensitivity_id,))
            sensitivity_row = cursor.fetchone()
            sensitivity_name = sensitivity_row[0] if sensitivity_row else "Unknown"
            
            # Create actual obligations from the templates
            created_obligation_ids = []
            for so in sensitivity_obligations:
                obligation_name = so[0]
                obligation_description = so[1]
                control_type = so[2]
                
                # Check if this obligation already exists
                cursor.execute(
                    "SELECT id FROM obligation WHERE name = %s AND control_type = %s",
                    (obligation_name, control_type)
                )
                existing = cursor.fetchone()
                
                if not existing:
                    source = f"Sensitivity: {sensitivity_name}"
                    cursor.execute(
                        """INSERT INTO obligation 
                           (name, description, source, control_type, status)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (obligation_name, obligation_description, source, control_type, "Open")
                    )
                    created_obligation_ids.append(cursor.lastrowid)
            
            self.connection.commit()
            return created_obligation_ids
        except Exception as e:
            print(f"Error generating obligations from sensitivity: {e}")
            self.connection.rollback()
            return []
        finally:
            cursor.close()
            
    def seed_sensitivity_obligations(self):
        """Seed the database with initial sensitivity-obligation mappings."""
        cursor = self.connection.cursor()
        try:
            # Get sensitivity IDs
            cursor.execute("SELECT id, name FROM sensitivity;")
            sensitivities = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Skip if no sensitivities found or if mappings already exist
            if not sensitivities:
                return
                
            cursor.execute("SELECT COUNT(*) FROM sensitivity_obligation;")
            if cursor.fetchone()[0] > 0:
                return
            
            # Define standard obligations for each sensitivity level
            mappings = [
                # High Sensitivity
                (
                    "High", 
                    "Encrypt Data at Rest", 
                    "All highly sensitive data must be encrypted when stored using industry-standard encryption algorithms.",
                    "Encryption",
                    "High"
                ),
                (
                    "High", 
                    "Encrypt Data in Transit", 
                    "All highly sensitive data must be transmitted using secure protocols (TLS 1.2+) with strong encryption.",
                    "Encryption",
                    "High"
                ),
                (
                    "High", 
                    "Implement Access Controls", 
                    "Access to highly sensitive data must be restricted to authorized personnel only, using role-based access controls.",
                    "Access Control",
                    "High"
                ),
                (
                    "High", 
                    "Data Masking", 
                    "Highly sensitive data must be masked when displayed to users without a need-to-know or in non-production environments.",
                    "Masking",
                    "High"
                ),
                (
                    "High", 
                    "Audit Logging", 
                    "All access to highly sensitive data must be logged and monitored for suspicious activity.",
                    "Monitoring",
                    "High"
                ),
                (
                    "High", 
                    "Enforce Retention Limits", 
                    "Highly sensitive data must be deleted or anonymized after the defined retention period expires.",
                    "Retention",
                    "Medium"
                ),
                
                # Medium Sensitivity
                (
                    "Medium", 
                    "Encrypt Sensitive Fields", 
                    "Specific sensitive fields should be encrypted when stored.",
                    "Encryption",
                    "Medium"
                ),
                (
                    "Medium", 
                    "Secure Transmission", 
                    "Medium sensitivity data should be transmitted using secure protocols.",
                    "Encryption",
                    "Medium"
                ),
                (
                    "Medium", 
                    "Basic Access Controls", 
                    "Access to medium sensitivity data should be limited to authenticated users with appropriate permissions.",
                    "Access Control",
                    "Medium"
                ),
                (
                    "Medium", 
                    "Audit Critical Operations", 
                    "Critical operations on medium sensitivity data should be logged.",
                    "Monitoring",
                    "Medium"
                ),
                
                # Low Sensitivity
                (
                    "Low", 
                    "Basic Authentication", 
                    "Access to low sensitivity data should require basic authentication.",
                    "Access Control",
                    "Low"
                ),
                (
                    "Low", 
                    "Standard Protections", 
                    "Apply standard organizational security controls to low sensitivity data.",
                    "General",
                    "Low"
                )
            ]
            
            # Insert mappings
            for sensitivity_name, obligation_name, obligation_description, control_type, priority in mappings:
                sensitivity_id = sensitivities.get(sensitivity_name)
                if sensitivity_id:
                    cursor.execute(
                        """INSERT INTO sensitivity_obligation 
                           (sensitivity_id, obligation_name, obligation_description, control_type, priority)
                           VALUES (%s, %s, %s, %s, %s);""",
                        (sensitivity_id, obligation_name, obligation_description, control_type, priority)
                    )
            
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding sensitivity obligations: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
