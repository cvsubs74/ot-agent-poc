import pymysql.cursors
import json
from datetime import datetime

class ConsentRepository:
    def __init__(self, connection):
        """Initialize the ConsentRepository with a database connection."""
        self.connection = connection
        
    def setup_tables(self):
        """Create all the necessary tables for consent management if they don't exist."""
        # Skip table creation in test mode
        if self.connection is None:
            return
            
        self.create_consent_profile_table()
        self.create_consent_record_table()
    
    def create_consent_profile_table(self):
        """Create the consent_profile table to store user profiles."""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consent_profile (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                email VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE(email),
                UNIQUE(user_id)
            );
        ''')
        self.connection.commit()
    
    def create_consent_record_table(self):
        """Create the consent_record table to map users to purposes with their consent status."""
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consent_record (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                consent_profile_id INTEGER NOT NULL,
                purpose_id INTEGER NOT NULL,
                status ENUM('granted', 'denied', 'withdrawn', 'expired') NOT NULL,
                consent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expiry_date TIMESTAMP NULL,
                proof_of_consent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE(consent_profile_id, purpose_id),
                FOREIGN KEY (consent_profile_id) REFERENCES consent_profile(id) ON DELETE CASCADE,
                FOREIGN KEY (purpose_id) REFERENCES purpose(id) ON DELETE CASCADE
            );
        ''')
        self.connection.commit()
    
    # Consent Profile Methods
    
    def get_consent_profiles(self, limit=100, offset=0):
        """Get all consent profiles with pagination."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT id, email, name, user_id, created_at, updated_at
                FROM consent_profile
                ORDER BY name
                LIMIT %s OFFSET %s
            ''', (limit, offset))
            profiles = cursor.fetchall()
            return profiles
        except Exception as e:
            print(f"Error getting consent profiles: {e}")
            return []
    
    def get_consent_profile_by_id(self, profile_id):
        """Get a consent profile by ID."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT id, email, name, user_id, created_at, updated_at
                FROM consent_profile
                WHERE id = %s
            ''', (profile_id,))
            profile = cursor.fetchone()
            return profile
        except Exception as e:
            print(f"Error getting consent profile by ID: {e}")
            return None
    
    def get_consent_profile_by_email(self, email):
        """Get a consent profile by email."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT id, email, name, user_id, created_at, updated_at
                FROM consent_profile
                WHERE email = %s
            ''', (email,))
            profile = cursor.fetchone()
            return profile
        except Exception as e:
            print(f"Error getting consent profile by email: {e}")
            return None
    
    def get_consent_profile_by_user_id(self, user_id):
        """Get a consent profile by user ID."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT id, email, name, user_id, created_at, updated_at
                FROM consent_profile
                WHERE user_id = %s
            ''', (user_id,))
            profile = cursor.fetchone()
            return profile
        except Exception as e:
            print(f"Error getting consent profile by user ID: {e}")
            return None
    
    def create_consent_profile(self, email, name, user_id):
        """Create a new consent profile."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO consent_profile (email, name, user_id)
                VALUES (%s, %s, %s)
            ''', (email, name, user_id))
            self.connection.commit()
            return cursor.lastrowid
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:  # Duplicate entry error
                print(f"Consent profile already exists for email {email} or user ID {user_id}")
                return None
            else:
                print(f"Error creating consent profile: {e}")
                return None
        except Exception as e:
            print(f"Error creating consent profile: {e}")
            return None
    
    def update_consent_profile(self, profile_id, email=None, name=None, user_id=None):
        """Update an existing consent profile."""
        cursor = self.connection.cursor()
        try:
            updates = []
            params = []
            
            if email is not None:
                updates.append("email = %s")
                params.append(email)
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            
            if user_id is not None:
                updates.append("user_id = %s")
                params.append(user_id)
            
            if not updates:
                return True  # Nothing to update
            
            params.append(profile_id)
            
            cursor.execute(f'''
                UPDATE consent_profile
                SET {', '.join(updates)}
                WHERE id = %s
            ''', tuple(params))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating consent profile: {e}")
            return False
    
    def delete_consent_profile(self, profile_id):
        """Delete a consent profile."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                DELETE FROM consent_profile
                WHERE id = %s
            ''', (profile_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting consent profile: {e}")
            return False
    
    # Consent Record Methods
    
    def get_consent_records(self, limit=100, offset=0):
        """Get all consent records with pagination."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT cr.id, cr.consent_profile_id, cp.email, cp.name, 
                       cr.purpose_id, p.name as purpose_name, 
                       cr.status, cr.consent_date, cr.expiry_date, 
                       cr.proof_of_consent, cr.created_at, cr.updated_at
                FROM consent_record cr
                JOIN consent_profile cp ON cr.consent_profile_id = cp.id
                JOIN purpose p ON cr.purpose_id = p.id
                ORDER BY cr.updated_at DESC
                LIMIT %s OFFSET %s
            ''', (limit, offset))
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"Error getting consent records: {e}")
            return []
    
    def get_consent_records_by_profile(self, profile_id):
        """Get consent records for a specific profile."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT cr.id, cr.consent_profile_id, cp.email, cp.name, 
                       cr.purpose_id, p.name as purpose_name, 
                       cr.status, cr.consent_date, cr.expiry_date, 
                       cr.proof_of_consent, cr.created_at, cr.updated_at
                FROM consent_record cr
                JOIN consent_profile cp ON cr.consent_profile_id = cp.id
                JOIN purpose p ON cr.purpose_id = p.id
                WHERE cr.consent_profile_id = %s
                ORDER BY p.name
            ''', (profile_id,))
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"Error getting consent records for profile {profile_id}: {e}")
            return []
    
    def get_consent_records_by_purpose(self, purpose_id):
        """Get consent records for a specific purpose."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT cr.id, cr.consent_profile_id, cp.email, cp.name, 
                       cr.purpose_id, p.name as purpose_name, 
                       cr.status, cr.consent_date, cr.expiry_date, 
                       cr.proof_of_consent, cr.created_at, cr.updated_at
                FROM consent_record cr
                JOIN consent_profile cp ON cr.consent_profile_id = cp.id
                JOIN purpose p ON cr.purpose_id = p.id
                WHERE cr.purpose_id = %s
                ORDER BY cp.name
            ''', (purpose_id,))
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"Error getting consent records for purpose {purpose_id}: {e}")
            return []
    
    def get_consent_record(self, profile_id, purpose_id):
        """Get a specific consent record."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT cr.id, cr.consent_profile_id, cp.email, cp.name, 
                       cr.purpose_id, p.name as purpose_name, 
                       cr.status, cr.consent_date, cr.expiry_date, 
                       cr.proof_of_consent, cr.created_at, cr.updated_at
                FROM consent_record cr
                JOIN consent_profile cp ON cr.consent_profile_id = cp.id
                JOIN purpose p ON cr.purpose_id = p.id
                WHERE cr.consent_profile_id = %s AND cr.purpose_id = %s
            ''', (profile_id, purpose_id))
            record = cursor.fetchone()
            return record
        except Exception as e:
            print(f"Error getting consent record: {e}")
            return None
    
    def create_consent_record(self, profile_id, purpose_id, status, expiry_date=None, proof_of_consent=None):
        """Create a new consent record."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO consent_record (consent_profile_id, purpose_id, status, expiry_date, proof_of_consent)
                VALUES (%s, %s, %s, %s, %s)
            ''', (profile_id, purpose_id, status, expiry_date, proof_of_consent))
            self.connection.commit()
            return cursor.lastrowid
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:  # Duplicate entry error
                print(f"Consent record already exists for profile {profile_id} and purpose {purpose_id}")
                return self.update_consent_record(profile_id, purpose_id, status, expiry_date, proof_of_consent)
            else:
                print(f"Error creating consent record: {e}")
                return None
        except Exception as e:
            print(f"Error creating consent record: {e}")
            return None
    
    def update_consent_record(self, profile_id, purpose_id, status=None, expiry_date=None, proof_of_consent=None):
        """Update an existing consent record."""
        cursor = self.connection.cursor()
        try:
            updates = []
            params = []
            
            if status is not None:
                updates.append("status = %s")
                params.append(status)
            
            if expiry_date is not None:
                updates.append("expiry_date = %s")
                params.append(expiry_date)
            
            if proof_of_consent is not None:
                updates.append("proof_of_consent = %s")
                params.append(proof_of_consent)
            
            if not updates:
                return True  # Nothing to update
            
            updates.append("consent_date = CURRENT_TIMESTAMP")
            
            params.extend([profile_id, purpose_id])
            
            cursor.execute(f'''
                UPDATE consent_record
                SET {', '.join(updates)}
                WHERE consent_profile_id = %s AND purpose_id = %s
            ''', tuple(params))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating consent record: {e}")
            return False
    
    def delete_consent_record(self, record_id):
        """Delete a consent record."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                DELETE FROM consent_record
                WHERE id = %s
            ''', (record_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting consent record: {e}")
            return False
    
    def get_consents(self, limit=100, offset=0):
        """Get all consent records from the database.
        
        Args:
            limit: Maximum number of records to return
            offset: Offset for pagination
            
        Returns:
            List of consent records as tuples (id, profile_id, purpose_id, status, created_at, updated_at)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT id, consent_profile_id, purpose_id, status, created_at, updated_at
                FROM consent_record
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            ''', (limit, offset))
            consents = cursor.fetchall()
            return consents
        except Exception as e:
            print(f"Error getting consents: {e}")
            return []
    
    def get_consents_for_role_purpose(self, role_id, purpose_id):
        """Get all consents for a specific role and purpose combination."""
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                SELECT cr.id, cr.consent_profile_id, cp.email, cp.name, cp.user_id,
                       cr.purpose_id, p.name as purpose_name, 
                       cr.status, cr.consent_date, cr.expiry_date
                FROM consent_record cr
                JOIN consent_profile cp ON cr.consent_profile_id = cp.id
                JOIN purpose p ON cr.purpose_id = p.id
                JOIN purpose_role pr ON cr.purpose_id = pr.purpose_id
                WHERE pr.external_role_id = %s AND cr.purpose_id = %s
                AND cr.status = 'granted' AND (cr.expiry_date IS NULL OR cr.expiry_date > NOW())
                ORDER BY cp.name
            ''', (role_id, purpose_id))
            records = cursor.fetchall()
            return records
        except Exception as e:
            print(f"Error getting consents for role {role_id} and purpose {purpose_id}: {e}")
            return []
    
    def get_consent_filter_condition(self, role_id, purpose_id):
        """Generate a SQL filter condition for row-level filtering based on consents."""
        try:
            # Get the consents for this role and purpose
            consents = self.get_consents_for_role_purpose(role_id, purpose_id)
            
            if not consents:
                return "1=0"  # No consents, no access
            
            # Extract user IDs from consents
            user_ids = [consent['user_id'] for consent in consents]
            
            # Build the filter condition
            # This assumes there's a user_id column in the target table
            # The actual implementation might need to be adjusted based on the schema
            filter_condition = f"user_id IN ({', '.join(['%s'] * len(user_ids))})"
            
            return filter_condition, user_ids
        except Exception as e:
            print(f"Error generating consent filter condition: {e}")
            return "1=0", []  # Default to no access on error
