import sqlite3
import json
import datetime

class DataAccessRepository:
    """Repository for managing data access requests and grants."""
    
    def __init__(self, connection=None):
        """Initialize the repository with a database connection."""
        self.connection = connection
        self.ensure_tables_exist()
    
    def ensure_tables_exist(self):
        """Ensure that the required tables exist in the database."""
        if not self.connection:
            return
            
        cursor = self.connection.cursor()
        try:
            # Create data_access_request table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_access_request (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    requester_name VARCHAR(255),
                    requester_email VARCHAR(255),
                    asset_id INT,
                    asset_name VARCHAR(255),
                    tables TEXT,
                    purposes TEXT,
                    purpose_ids TEXT,
                    role_name VARCHAR(255),
                    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
                    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    approval_date TIMESTAMP NULL,
                    expiry_date TIMESTAMP NULL,
                    ddl TEXT,
                    policy_json TEXT,
                    notes TEXT
                );
            """)
            self.connection.commit()
        except Exception as e:
            print(f"Error ensuring tables exist: {e}")
        finally:
            cursor.close()
            
    def create_request(self, requester_name, requester_email, asset_id, asset_name, 
                      tables, purposes, purpose_ids, role_name, ddl, policy_json, notes=""):
        """
        Create a new data access request.
        
        Args:
            requester_name: Name of the person requesting access
            requester_email: Email of the requester
            asset_id: ID of the asset being requested
            asset_name: Name of the asset
            tables: List of tables requested
            purposes: List of purpose names
            purpose_ids: List of purpose IDs
            role_name: Name of the role created
            ddl: Generated DDL script
            policy_json: Policy JSON used to generate the DDL
            notes: Additional notes about the request
            
        Returns:
            ID of the created request
        """
        if not self.connection:
            return -1
            
        cursor = self.connection.cursor()
        try:
            # Print debug information
            print(f"Creating data access request for {requester_name}, asset: {asset_name}")
            
            # Convert lists to JSON strings for storage
            tables_json = json.dumps(tables)
            purposes_json = json.dumps(purposes)
            purpose_ids_json = json.dumps(purpose_ids)
            
            # Get current timestamp
            now = datetime.datetime.now().isoformat()
            
            # Insert the request - using %s placeholders for MySQL instead of ? for SQLite
            cursor.execute("""
                INSERT INTO data_access_request (
                    requester_name, requester_email, asset_id, asset_name,
                    tables, purposes, purpose_ids, role_name, status,
                    request_date, ddl, policy_json, notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                requester_name, requester_email, asset_id, asset_name,
                tables_json, purposes_json, purpose_ids_json, role_name, "Pending",
                now, ddl, policy_json, notes
            ))
            
            # Get the ID of the inserted row
            last_row_id = cursor.lastrowid
            print(f"Request created with ID: {last_row_id}")
            
            # Commit the transaction
            self.connection.commit()
            return last_row_id
        except Exception as e:
            print(f"Error creating data access request: {e}")
            return -1
        finally:
            cursor.close()
    
    def approve_request(self, request_id, approval_date=None, expiry_date=None):
        """
        Approve a data access request.
        
        Args:
            request_id: ID of the request to approve
            approval_date: Date of approval (defaults to now)
            expiry_date: Date when access expires (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connection:
            return False
            
        cursor = self.connection.cursor()
        try:
            # Get current timestamp if approval_date not provided
            if not approval_date:
                approval_date = datetime.datetime.now().isoformat()
                
            # Update the request status
            cursor.execute("""
                UPDATE data_access_request
                SET status = %s, approval_date = %s, expiry_date = %s
                WHERE id = %s
            """, ("Approved", approval_date, expiry_date, request_id))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error approving data access request: {e}")
            return False
        finally:
            cursor.close()
    
    def reject_request(self, request_id, notes=""):
        """
        Reject a data access request.
        
        Args:
            request_id: ID of the request to reject
            notes: Reason for rejection
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connection:
            return False
            
        cursor = self.connection.cursor()
        try:
            # Update the request status
            cursor.execute("""
                UPDATE data_access_request
                SET status = %s, notes = %s
                WHERE id = %s
            """, ("Rejected", notes, request_id))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error rejecting data access request: {e}")
            return False
        finally:
            cursor.close()
    
    def get_all_requests(self):
        """
        Get all data access requests.
        
        Returns:
            List of data access requests
        """
        if not self.connection:
            # Return sample data for testing when no connection is available
            return [
                {
                    "id": 1,
                    "requester_name": "John Doe",
                    "requester_email": "john.doe@example.com",
                    "asset_id": 1,
                    "asset_name": "CRM System",
                    "tables": ["crm.customers", "crm.purchases"],
                    "purposes": ["Marketing", "Analytics"],
                    "purpose_ids": [1, 2],
                    "role_name": "DATA_ACCESS_ABC123",
                    "status": "Pending",
                    "request_date": "2025-04-30T06:00:00",
                    "approval_date": None,
                    "expiry_date": None,
                    "notes": "Sample request for testing"
                }
            ]
            
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT id, requester_name, requester_email, asset_id, asset_name,
                       tables, purposes, purpose_ids, role_name, status,
                       request_date, approval_date, expiry_date, notes
                FROM data_access_request
                ORDER BY request_date DESC
            """)
            
            requests = []
            for row in cursor.fetchall():
                try:
                    # Handle JSON parsing with error handling
                    tables = json.loads(row[5]) if row[5] else []
                    purposes = json.loads(row[6]) if row[6] else []
                    purpose_ids = json.loads(row[7]) if row[7] else []
                    
                    request = {
                        "id": row[0],
                        "requester_name": row[1],
                        "requester_email": row[2],
                        "asset_id": row[3],
                        "asset_name": row[4],
                        "tables": tables,
                        "purposes": purposes,
                        "purpose_ids": purpose_ids,
                        "role_name": row[8],
                        "status": row[9],
                        "request_date": row[10],
                        "approval_date": row[11],
                        "expiry_date": row[12],
                        "notes": row[13]
                    }
                    requests.append(request)
                except Exception as e:
                    print(f"Error processing row {row[0]}: {e}")
                    continue
                
            return requests
        except Exception as e:
            print(f"Error getting data access requests: {e}")
            return []
        finally:
            cursor.close()
    
    def get_request(self, request_id):
        """
        Get a specific data access request.
        
        Args:
            request_id: ID of the request to get
            
        Returns:
            Data access request or None if not found
        """
        if not self.connection:
            # Return sample data for testing when no connection is available
            if request_id == 1:
                return {
                    "id": 1,
                    "requester_name": "John Doe",
                    "requester_email": "john.doe@example.com",
                    "asset_id": 1,
                    "asset_name": "CRM System",
                    "tables": ["crm.customers", "crm.purchases"],
                    "purposes": ["Marketing", "Analytics"],
                    "purpose_ids": [1, 2],
                    "role_name": "DATA_ACCESS_ABC123",
                    "status": "Pending",
                    "request_date": "2025-04-30T06:00:00",
                    "approval_date": None,
                    "expiry_date": None,
                    "ddl": "-- Sample DDL\nCREATE ROLE IF NOT EXISTS DATA_ACCESS_ABC123;",
                    "policy_json": "{\"asset_name\": \"CRM System\", \"tables\": [\"crm.customers\", \"crm.purchases\"]}",
                    "notes": "Sample request for testing"
                }
            return None
            
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT id, requester_name, requester_email, asset_id, asset_name,
                       tables, purposes, purpose_ids, role_name, status,
                       request_date, approval_date, expiry_date, ddl, policy_json, notes
                FROM data_access_request
                WHERE id = %s
            """, (request_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            try:
                # Handle JSON parsing with error handling
                tables = json.loads(row[5]) if row[5] else []
                purposes = json.loads(row[6]) if row[6] else []
                purpose_ids = json.loads(row[7]) if row[7] else []
                
                request = {
                    "id": row[0],
                    "requester_name": row[1],
                    "requester_email": row[2],
                    "asset_id": row[3],
                    "asset_name": row[4],
                    "tables": tables,
                    "purposes": purposes,
                    "purpose_ids": purpose_ids,
                    "role_name": row[8],
                    "status": row[9],
                    "request_date": row[10],
                    "approval_date": row[11],
                    "expiry_date": row[12],
                    "ddl": row[13],
                    "policy_json": row[14],
                    "notes": row[15]
                }
                    
                return request
            except Exception as e:
                print(f"Error processing request {request_id}: {e}")
                return None
        except Exception as e:
            print(f"Error getting data access request: {e}")
            return None
        finally:
            cursor.close()
