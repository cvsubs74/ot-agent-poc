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
        self.create_risk_table()
        self.create_obligation_policy_table()
        self.create_obligation_risk_table()
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
        
    def create_risk_table(self):
        """Create the Risk table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `risk` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `category` VARCHAR(100),
            `likelihood` VARCHAR(50) DEFAULT 'Medium',
            `impact` VARCHAR(50) DEFAULT 'Medium',
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_obligation_policy_table(self):
        """Create the Obligation Policy mapping table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `obligation_policy` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `obligation_id` INT NOT NULL,
            `policy_id` INT NOT NULL,
            `control_type` VARCHAR(100),
            `relevance_score` FLOAT DEFAULT 1.0,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`obligation_id`) REFERENCES `obligation`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`policy_id`) REFERENCES `policy`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `unique_obligation_policy` (`obligation_id`, `policy_id`)
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def create_obligation_risk_table(self):
        """Create the Obligation Risk mapping table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `obligation_risk` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `obligation_id` INT NOT NULL,
            `risk_id` INT NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (`obligation_id`) REFERENCES `obligation`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`risk_id`) REFERENCES `risk`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `unique_obligation_risk` (`obligation_id`, `risk_id`)
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
            
    # Risk methods
    def add_risk(self, name, description, category=None, likelihood='Medium', impact='Medium'):
        """Add a new risk to the database."""
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO risk (name, description, category, likelihood, impact)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, description, category, likelihood, impact))
            self.connection.commit()
            risk_id = cursor.lastrowid
            return risk_id
        except Exception as e:
            print(f"Error adding risk: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
        
    def get_risk_by_id(self, risk_id):
        """Get a risk by its ID."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT id, name, description, category, likelihood, impact, created_at
            FROM risk
            WHERE id = %s
            """
            cursor.execute(query, (risk_id,))
            row = cursor.fetchone()
            if not row:
                return None
                
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "category": row[3],
                "likelihood": row[4],
                "impact": row[5],
                "created_at": row[6]
            }
        except Exception as e:
            print(f"Error getting risk by ID: {e}")
            return None
        finally:
            cursor.close()
        
    def get_risks(self, category=None, likelihood=None, impact=None):
        """Get all risks from the database with optional filters."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT id, name, description, category, likelihood, impact, created_at
            FROM risk
            """
            
            params = []
            where_clauses = []
            
            if category:
                where_clauses.append("category = %s")
                params.append(category)
                
            if likelihood:
                where_clauses.append("likelihood = %s")
                params.append(likelihood)
                
            if impact:
                where_clauses.append("impact = %s")
                params.append(impact)
                
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            
            risks = []
            for row in cursor.fetchall():
                risks.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "category": row[3],
                    "likelihood": row[4],
                    "impact": row[5],
                    "created_at": row[6]
                })
            return risks
        except Exception as e:
            print(f"Error getting risks: {e}")
            return []
        finally:
            cursor.close()
        
    def update_risk(self, risk_id, name=None, description=None, category=None, likelihood=None, impact=None):
        """Update an existing risk."""
        cursor = self.connection.cursor()
        try:
            query = "UPDATE risk SET "
            params = []
            updates = []
            
            if name:
                updates.append("name = %s")
                params.append(name)
                
            if description:
                updates.append("description = %s")
                params.append(description)
                
            if category:
                updates.append("category = %s")
                params.append(category)
                
            if likelihood:
                updates.append("likelihood = %s")
                params.append(likelihood)
                
            if impact:
                updates.append("impact = %s")
                params.append(impact)
                
            if not updates:
                return False
                
            query += ", ".join(updates) + " WHERE id = %s"
            params.append(risk_id)
            
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating risk: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
        
    def delete_risk(self, risk_id):
        """Delete a risk by its ID."""
        cursor = self.connection.cursor()
        try:
            query = "DELETE FROM risk WHERE id = %s"
            cursor.execute(query, (risk_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting risk: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    # Obligation-Policy mapping methods
    def map_obligation_to_policy(self, obligation_id, policy_id, control_type=None, relevance_score=1.0):
        """Map an obligation to a policy."""
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO obligation_policy (obligation_id, policy_id, control_type, relevance_score)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE control_type = VALUES(control_type), relevance_score = VALUES(relevance_score)
            """
            cursor.execute(query, (obligation_id, policy_id, control_type, relevance_score))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error mapping obligation to policy: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
            
    def get_obligation_policies(self, obligation_id=None, policy_id=None, control_type=None):
        """Get obligation-policy mappings with optional filters."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT op.id, op.obligation_id, o.name as obligation_name, o.description as obligation_description,
                   op.policy_id, p.name as policy_name, p.description as policy_description,
                   op.control_type, op.relevance_score, op.created_at
            FROM obligation_policy op
            JOIN obligation o ON op.obligation_id = o.id
            JOIN policy p ON op.policy_id = p.id
            """
            
            params = []
            where_clauses = []
            
            if obligation_id:
                where_clauses.append("op.obligation_id = %s")
                params.append(obligation_id)
                
            if policy_id:
                where_clauses.append("op.policy_id = %s")
                params.append(policy_id)
                
            if control_type:
                where_clauses.append("op.control_type = %s")
                params.append(control_type)
                
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            query += " ORDER BY op.relevance_score DESC, op.created_at DESC"
            
            cursor.execute(query, params)
            
            mappings = []
            for row in cursor.fetchall():
                mappings.append({
                    "id": row[0],
                    "obligation_id": row[1],
                    "obligation_name": row[2],
                    "obligation_description": row[3],
                    "policy_id": row[4],
                    "policy_name": row[5],
                    "policy_description": row[6],
                    "control_type": row[7],
                    "relevance_score": row[8],
                    "created_at": row[9]
                })
            return mappings
        except Exception as e:
            print(f"Error getting obligation-policy mappings: {e}")
            return []
        finally:
            cursor.close()
            
    def delete_obligation_policy_mapping(self, mapping_id):
        """Delete an obligation-policy mapping."""
        cursor = self.connection.cursor()
        try:
            query = "DELETE FROM obligation_policy WHERE id = %s"
            cursor.execute(query, (mapping_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting obligation-policy mapping: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def get_policies_for_obligation(self, obligation_id):
        """Get all policies mapped to a specific obligation."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT p.id, p.name, p.description, p.status, op.relevance_score
            FROM policy p
            JOIN obligation_policy op ON p.id = op.policy_id
            WHERE op.obligation_id = %s
            ORDER BY op.relevance_score DESC
            """
            cursor.execute(query, (obligation_id,))
            
            policies = []
            for row in cursor.fetchall():
                policies.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "status": row[3],
                    "relevance_score": row[4]
                })
            return policies
        except Exception as e:
            print(f"Error getting policies for obligation: {e}")
            return []
        finally:
            cursor.close()
            
    # Obligation-Risk mapping methods
    def map_obligation_to_risk(self, obligation_id, risk_id):
        """Map an obligation to a risk."""
        cursor = self.connection.cursor()
        try:
            query = """
            INSERT INTO obligation_risk (obligation_id, risk_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE created_at = CURRENT_TIMESTAMP
            """
            cursor.execute(query, (obligation_id, risk_id))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error mapping obligation to risk: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
            
    def get_obligation_risks(self, obligation_id=None, risk_id=None):
        """Get obligation-risk mappings with optional filters."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT or_.id, or_.obligation_id, o.name as obligation_name, o.description as obligation_description,
                   or_.risk_id, r.name as risk_name, r.description as risk_description,
                   r.category, r.likelihood, r.impact, or_.created_at
            FROM obligation_risk or_
            JOIN obligation o ON or_.obligation_id = o.id
            JOIN risk r ON or_.risk_id = r.id
            """
            
            params = []
            where_clauses = []
            
            if obligation_id:
                where_clauses.append("or_.obligation_id = %s")
                params.append(obligation_id)
                
            if risk_id:
                where_clauses.append("or_.risk_id = %s")
                params.append(risk_id)
                
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                
            query += " ORDER BY or_.created_at DESC"
            
            cursor.execute(query, params)
            
            mappings = []
            for row in cursor.fetchall():
                mappings.append({
                    "id": row[0],
                    "obligation_id": row[1],
                    "obligation_name": row[2],
                    "obligation_description": row[3],
                    "risk_id": row[4],
                    "risk_name": row[5],
                    "risk_description": row[6],
                    "category": row[7],
                    "likelihood": row[8],
                    "impact": row[9],
                    "created_at": row[10]
                })
            return mappings
        except Exception as e:
            print(f"Error getting obligation-risk mappings: {e}")
            return []
        finally:
            cursor.close()
            
    def delete_obligation_risk_mapping(self, mapping_id):
        """Delete an obligation-risk mapping."""
        cursor = self.connection.cursor()
        try:
            query = "DELETE FROM obligation_risk WHERE id = %s"
            cursor.execute(query, (mapping_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting obligation-risk mapping: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    def get_risks_for_obligation(self, obligation_id):
        """Get all risks mapped to a specific obligation."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT r.id, r.name, r.description, r.category, r.likelihood, r.impact
            FROM risk r
            JOIN obligation_risk or_ ON r.id = or_.risk_id
            WHERE or_.obligation_id = %s
            ORDER BY r.impact DESC, r.likelihood DESC
            """
            cursor.execute(query, (obligation_id,))
            
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
            print(f"Error getting risks for obligation: {e}")
            return []
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
                   o.id as obligation_id, o.name as obligation_name, o.description as obligation_description,
                   o.control_type, so.priority
            FROM sensitivity_obligation so
            JOIN sensitivity s ON so.sensitivity_id = s.id
            JOIN obligation o ON so.obligation_id = o.id
            """
            
            params = []
            where_clauses = []
            
            if sensitivity_id:
                where_clauses.append("so.sensitivity_id = %s")
                params.append(sensitivity_id)
                
            if control_type:
                where_clauses.append("o.control_type = %s")
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
                    "obligation_id": row[3],
                    "obligation_name": row[4],
                    "obligation_description": row[5],
                    "control_type": row[6],
                    "priority": row[7]
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
            
            # Get obligation IDs
            cursor.execute("SELECT id, name FROM obligation;")
            obligations = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Skip if no sensitivities or obligations found or if mappings already exist
            if not sensitivities or not obligations:
                return
                
            cursor.execute("SELECT COUNT(*) FROM sensitivity_obligation;")
            if cursor.fetchone()[0] > 0:
                return
            
            # Define standard mappings between sensitivities and obligations
            mappings = [
                # High Sensitivity
                ("High", "Encrypt Data at Rest", "High"),
                ("High", "Encrypt Data in Transit", "High"),
                ("High", "Implement Access Controls", "High"),
                ("High", "Implement Data Masking", "High"),
                ("High", "Maintain Access Logs", "High"),
                ("High", "Implement Data Retention Controls", "Medium"),
                
                # Medium Sensitivity
                ("Medium", "Encrypt Data at Rest", "Medium"),
                ("Medium", "Encrypt Data in Transit", "Medium"),
                ("Medium", "Implement Access Controls", "Medium"),
                ("Medium", "Maintain Access Logs", "Medium"),
                
                # Low Sensitivity
                ("Low", "Implement Access Controls", "Low"),
                ("Low", "Implement Data Classification", "Low")
            ]
            
            # Insert mappings
            for sensitivity_name, obligation_name, priority in mappings:
                sensitivity_id = sensitivities.get(sensitivity_name)
                obligation_id = obligations.get(obligation_name)
                
                if sensitivity_id and obligation_id:
                    cursor.execute(
                        """INSERT INTO sensitivity_obligation 
                           (sensitivity_id, obligation_id, priority)
                           VALUES (%s, %s, %s);""",
                        (sensitivity_id, obligation_id, priority)
                    )
                else:
                    print(f"Warning: Could not find sensitivity '{sensitivity_name}' or obligation '{obligation_name}'")
            
            self.connection.commit()
        except Exception as e:
            print(f"Error seeding sensitivity obligations: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
