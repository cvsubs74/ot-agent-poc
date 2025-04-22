import pymysql.cursors
import random
import string
import datetime

class CatalogRepository:
    def __init__(self, connection):
        self.connection = connection
        
    def get_catalog_entries_by_asset(self, asset_id):
        """Get all catalog entries for a specific asset."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT c.id, c.schema_name, c.table_name, c.column_name, c.data_type, 
                   c.data_element_id, de.name as data_element_name, c.sample_data, c.last_scanned
            FROM catalog c
            LEFT JOIN data_element de ON c.data_element_id = de.id
            WHERE c.asset_id = %s
            ORDER BY c.schema_name, c.table_name, c.column_name
            """
            cursor.execute(query, (asset_id,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "schema_name": row[1],
                    "table_name": row[2],
                    "column_name": row[3],
                    "data_type": row[4],
                    "data_element_id": row[5],
                    "data_element_name": row[6],
                    "sample_data": row[7],
                    "last_scanned": row[8]
                })
            return results
        except Exception as e:
            print(f"Error getting catalog entries: {e}")
            return []
        finally:
            cursor.close()
            
    def get_policy_implementations_by_catalog(self, catalog_id):
        """Get all policy implementations for a specific catalog entry."""
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT pi.id, pi.policy_id, p.name as policy_name, 
                   pi.is_masked, pi.masking_format, pi.is_encrypted, pi.encryption_algorithm,
                   pi.has_access_control, pi.access_control_type, pi.has_retention_policy, 
                   pi.retention_period, pi.has_audit_logging, pi.audit_level,
                   pi.implementation_status, pi.last_verified
            FROM policy_implementation pi
            JOIN policy p ON pi.policy_id = p.id
            WHERE pi.catalog_id = %s
            """
            cursor.execute(query, (catalog_id,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "policy_id": row[1],
                    "policy_name": row[2],
                    "is_masked": bool(row[3]),
                    "masking_format": row[4],
                    "is_encrypted": bool(row[5]),
                    "encryption_algorithm": row[6],
                    "has_access_control": bool(row[7]),
                    "access_control_type": row[8],
                    "has_retention_policy": bool(row[9]),
                    "retention_period": row[10],
                    "has_audit_logging": bool(row[11]),
                    "audit_level": row[12],
                    "implementation_status": row[13],
                    "last_verified": row[14]
                })
            return results
        except Exception as e:
            print(f"Error getting policy implementations: {e}")
            return []
        finally:
            cursor.close()
            
    def scan_asset(self, asset_id):
        """Simulate scanning an asset to discover database metadata and classify columns."""
        cursor = self.connection.cursor()
        try:
            # First, delete any existing catalog entries for this asset
            # This is just for the simulation - in a real system you might want to update instead
            cursor.execute("DELETE FROM catalog WHERE asset_id = %s", (asset_id,))
            
            # Get asset information
            cursor.execute("SELECT name FROM asset WHERE id = %s", (asset_id,))
            asset_name = cursor.fetchone()[0]
            
            # Get available data elements for classification
            cursor.execute("SELECT id, name FROM data_element")
            data_elements = cursor.fetchall()
            
            # Generate simulated database schema based on asset type
            catalog_entries = []
            
            if "CRM" in asset_name:
                # Simulate CRM database schema
                catalog_entries.extend(self._generate_crm_schema(asset_id, data_elements))
            elif "HR" in asset_name:
                # Simulate HR database schema
                catalog_entries.extend(self._generate_hr_schema(asset_id, data_elements))
            elif "Financial" in asset_name:
                # Simulate Financial database schema
                catalog_entries.extend(self._generate_financial_schema(asset_id, data_elements))
            elif "Marketing" in asset_name:
                # Simulate Marketing database schema
                catalog_entries.extend(self._generate_marketing_schema(asset_id, data_elements))
            else:
                # Generic database schema
                catalog_entries.extend(self._generate_generic_schema(asset_id, data_elements))
            
            # Insert the new catalog entries
            for entry in catalog_entries:
                cursor.execute("""
                INSERT INTO catalog (asset_id, schema_name, table_name, column_name, data_type, data_element_id, sample_data, last_scanned)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                """, (
                    entry["asset_id"],
                    entry["schema_name"],
                    entry["table_name"],
                    entry["column_name"],
                    entry["data_type"],
                    entry["data_element_id"],
                    entry["sample_data"]
                ))
            
            # Update asset_data_element table based on classifications
            cursor.execute("""
            INSERT IGNORE INTO asset_data_element (asset_id, data_element_id)
            SELECT DISTINCT asset_id, data_element_id
            FROM catalog
            WHERE asset_id = %s AND data_element_id IS NOT NULL
            """, (asset_id,))
            
            # Generate policy implementations for sensitive data
            self._generate_policy_implementations(asset_id)
            
            self.connection.commit()
            return len(catalog_entries)
        except Exception as e:
            print(f"Error scanning asset: {e}")
            self.connection.rollback()
            return 0
        finally:
            cursor.close()
    
    def _generate_crm_schema(self, asset_id, data_elements):
        """Generate a simulated CRM database schema."""
        schema_name = "crm"
        tables = {
            "customers": [
                {"name": "customer_id", "type": "INT", "data_element": "Customer ID", "sample": str(random.randint(10000, 99999))},
                {"name": "first_name", "type": "VARCHAR", "data_element": "Name", "sample": random.choice(["John", "Jane", "Michael", "Emily", "David"])},
                {"name": "last_name", "type": "VARCHAR", "data_element": "Name", "sample": random.choice(["Smith", "Johnson", "Williams", "Jones", "Brown"])},
                {"name": "full_name", "type": "VARCHAR", "data_element": "Full Name", "sample": "John Smith"},
                {"name": "email", "type": "VARCHAR", "data_element": "Email Address", "sample": f"{self._random_string(5)}@example.com"},
                {"name": "phone", "type": "VARCHAR", "data_element": "Phone Number", "sample": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"},
                {"name": "address", "type": "VARCHAR", "data_element": "Address", "sample": f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar'])} St"},
                {"name": "city", "type": "VARCHAR", "data_element": "Address", "sample": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])},
                {"name": "state", "type": "VARCHAR", "data_element": "Address", "sample": random.choice(["CA", "NY", "TX", "FL", "IL"])},
                {"name": "zip", "type": "VARCHAR", "data_element": "Address", "sample": f"{random.randint(10000, 99999)}"},
                {"name": "date_of_birth", "type": "DATE", "data_element": "Date of Birth", "sample": self._random_date()},
                {"name": "ssn", "type": "VARCHAR", "data_element": "Social Security Number", "sample": f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"},
                {"name": "registration_date", "type": "DATE", "data_element": None, "sample": self._random_date()},
            ],
            "purchases": [
                {"name": "purchase_id", "type": "INT", "data_element": None, "sample": str(random.randint(50000, 59999))},
                {"name": "customer_id", "type": "INT", "data_element": "Customer ID", "sample": str(random.randint(10000, 99999))},
                {"name": "product_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "purchase_date", "type": "DATE", "data_element": None, "sample": self._random_date()},
                {"name": "amount", "type": "DECIMAL", "data_element": None, "sample": f"{random.randint(10, 1000)}.{random.randint(0, 99):02d}"},
                {"name": "payment_method", "type": "VARCHAR", "data_element": None, "sample": random.choice(["Credit Card", "PayPal", "Bank Transfer", "Cash"])},
                {"name": "credit_card", "type": "VARCHAR", "data_element": "Credit Card Number", "sample": f"**** **** **** {random.randint(1000, 9999)}"},
                {"name": "purchase_history", "type": "TEXT", "data_element": "Purchase History", "sample": "Previous purchases: Product A, Product B"},
            ],
            "interactions": [
                {"name": "interaction_id", "type": "INT", "data_element": None, "sample": str(random.randint(100000, 999999))},
                {"name": "customer_id", "type": "INT", "data_element": "Customer ID", "sample": str(random.randint(10000, 99999))},
                {"name": "interaction_date", "type": "DATETIME", "data_element": None, "sample": f"{self._random_date()} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"},
                {"name": "channel", "type": "VARCHAR", "data_element": None, "sample": random.choice(["Email", "Phone", "Web", "In-person"])},
                {"name": "notes", "type": "TEXT", "data_element": None, "sample": "Customer inquired about product features and pricing."},
                {"name": "device_id", "type": "VARCHAR", "data_element": "Device ID", "sample": f"DEV-{self._random_string(8)}"},
                {"name": "ip_address", "type": "VARCHAR", "data_element": "IP Address", "sample": f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"},
            ]
        }
        
        return self._create_catalog_entries(asset_id, schema_name, tables, data_elements)
    
    def _generate_hr_schema(self, asset_id, data_elements):
        """Generate a simulated HR database schema."""
        schema_name = "hr"
        tables = {
            "employees": [
                {"name": "employee_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "first_name", "type": "VARCHAR", "data_element": "First Name", "sample": random.choice(["John", "Jane", "Michael", "Emily", "David"])},
                {"name": "last_name", "type": "VARCHAR", "data_element": "Last Name", "sample": random.choice(["Smith", "Johnson", "Williams", "Jones", "Brown"])},
                {"name": "email", "type": "VARCHAR", "data_element": "Email Address", "sample": f"{self._random_string(5)}@company.com"},
                {"name": "ssn", "type": "VARCHAR", "data_element": "Social Security Number", "sample": f"XXX-XX-{random.randint(1000, 9999)}"},
                {"name": "dob", "type": "DATE", "data_element": "Date of Birth", "sample": f"{random.randint(1960, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"},
                {"name": "hire_date", "type": "DATE", "data_element": None, "sample": self._random_date()},
                {"name": "department", "type": "VARCHAR", "data_element": None, "sample": random.choice(["HR", "IT", "Finance", "Marketing", "Operations"])},
                {"name": "position", "type": "VARCHAR", "data_element": "Job Title", "sample": random.choice(["Manager", "Director", "Analyst", "Developer", "Specialist"])},
                {"name": "salary", "type": "DECIMAL", "data_element": "Salary Information", "sample": f"{random.randint(50000, 150000)}.00"},
                {"name": "bank_account", "type": "VARCHAR", "data_element": "Bank Account Number", "sample": f"XXXX{random.randint(1000, 9999)}"},
            ],
            "payroll": [
                {"name": "payroll_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "employee_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "pay_date", "type": "DATE", "data_element": None, "sample": self._random_date()},
                {"name": "gross_pay", "type": "DECIMAL", "data_element": "Salary Information", "sample": f"{random.randint(2000, 10000)}.00"},
                {"name": "net_pay", "type": "DECIMAL", "data_element": "Salary Information", "sample": f"{random.randint(1500, 8000)}.00"},
                {"name": "tax_withheld", "type": "DECIMAL", "data_element": "Tax Information", "sample": f"{random.randint(500, 3000)}.00"},
            ],
            "benefits": [
                {"name": "benefit_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "employee_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "health_plan", "type": "VARCHAR", "data_element": "Health Insurance Information", "sample": random.choice(["Gold", "Silver", "Bronze", "None"])},
                {"name": "retirement_plan", "type": "VARCHAR", "data_element": None, "sample": random.choice(["401k", "Pension", "None"])},
                {"name": "vacation_days", "type": "INT", "data_element": None, "sample": str(random.randint(10, 30))},
            ]
        }
        
        return self._create_catalog_entries(asset_id, schema_name, tables, data_elements)
    
    def _generate_financial_schema(self, asset_id, data_elements):
        """Generate a simulated Financial database schema."""
        schema_name = "finance"
        tables = {
            "accounts": [
                {"name": "account_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "customer_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "account_number", "type": "VARCHAR", "data_element": "Bank Account Number", "sample": f"ACCT-{random.randint(100000, 999999)}"},
                {"name": "account_type", "type": "VARCHAR", "data_element": None, "sample": random.choice(["Checking", "Savings", "Investment", "Credit"])},
                {"name": "balance", "type": "DECIMAL", "data_element": "Account Balance", "sample": f"{random.randint(100, 100000)}.{random.randint(0, 99):02d}"},
                {"name": "open_date", "type": "DATE", "data_element": None, "sample": self._random_date()},
            ],
            "transactions": [
                {"name": "transaction_id", "type": "INT", "data_element": None, "sample": str(random.randint(100000, 999999))},
                {"name": "account_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "transaction_date", "type": "DATETIME", "data_element": None, "sample": f"{self._random_date()} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"},
                {"name": "amount", "type": "DECIMAL", "data_element": "Transaction Amount", "sample": f"{random.randint(10, 5000)}.{random.randint(0, 99):02d}"},
                {"name": "transaction_type", "type": "VARCHAR", "data_element": None, "sample": random.choice(["Deposit", "Withdrawal", "Transfer", "Payment"])},
                {"name": "description", "type": "VARCHAR", "data_element": None, "sample": "Monthly subscription payment"},
            ],
            "payments": [
                {"name": "payment_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "account_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "payment_date", "type": "DATE", "data_element": None, "sample": self._random_date()},
                {"name": "amount", "type": "DECIMAL", "data_element": "Payment Amount", "sample": f"{random.randint(10, 1000)}.{random.randint(0, 99):02d}"},
                {"name": "payment_method", "type": "VARCHAR", "data_element": "Payment Method", "sample": random.choice(["Credit Card", "Bank Transfer", "Check", "Cash"])},
                {"name": "credit_card_number", "type": "VARCHAR", "data_element": "Credit Card Number", "sample": f"XXXX-XXXX-XXXX-{random.randint(1000, 9999)}"},
                {"name": "expiry_date", "type": "VARCHAR", "data_element": "Credit Card Expiry Date", "sample": f"{random.randint(1, 12):02d}/{random.randint(23, 30)}"},
            ]
        }
        
        return self._create_catalog_entries(asset_id, schema_name, tables, data_elements)
    
    def _generate_marketing_schema(self, asset_id, data_elements):
        """Generate a simulated Marketing database schema."""
        schema_name = "marketing"
        tables = {
            "campaigns": [
                {"name": "campaign_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "campaign_name", "type": "VARCHAR", "data_element": None, "sample": f"Campaign {self._random_string(8)}"},
                {"name": "start_date", "type": "DATE", "data_element": None, "sample": self._random_date()},
                {"name": "end_date", "type": "DATE", "data_element": None, "sample": self._random_date(start_year=2025, end_year=2026)},
                {"name": "budget", "type": "DECIMAL", "data_element": None, "sample": f"{random.randint(5000, 100000)}.00"},
                {"name": "status", "type": "VARCHAR", "data_element": None, "sample": random.choice(["Active", "Planned", "Completed", "Cancelled"])},
            ],
            "contacts": [
                {"name": "contact_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "first_name", "type": "VARCHAR", "data_element": "First Name", "sample": random.choice(["John", "Jane", "Michael", "Emily", "David"])},
                {"name": "last_name", "type": "VARCHAR", "data_element": "Last Name", "sample": random.choice(["Smith", "Johnson", "Williams", "Jones", "Brown"])},
                {"name": "email", "type": "VARCHAR", "data_element": "Email Address", "sample": f"{self._random_string(5)}@example.com"},
                {"name": "phone", "type": "VARCHAR", "data_element": "Phone Number", "sample": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"},
                {"name": "opt_in", "type": "BOOLEAN", "data_element": "Marketing Preferences", "sample": random.choice(["0", "1"])},
                {"name": "source", "type": "VARCHAR", "data_element": None, "sample": random.choice(["Website", "Event", "Referral", "Social Media"])},
            ],
            "campaign_analytics": [
                {"name": "analytics_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "campaign_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "date", "type": "DATE", "data_element": None, "sample": self._random_date()},
                {"name": "impressions", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 100000))},
                {"name": "clicks", "type": "INT", "data_element": None, "sample": str(random.randint(100, 10000))},
                {"name": "conversions", "type": "INT", "data_element": None, "sample": str(random.randint(10, 1000))},
                {"name": "revenue", "type": "DECIMAL", "data_element": None, "sample": f"{random.randint(1000, 50000)}.{random.randint(0, 99):02d}"},
            ]
        }
        
        return self._create_catalog_entries(asset_id, schema_name, tables, data_elements)
    
    def _generate_generic_schema(self, asset_id, data_elements):
        """Generate a generic database schema."""
        schema_name = "app"
        tables = {
            "users": [
                {"name": "user_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "username", "type": "VARCHAR", "data_element": "Username", "sample": f"user_{self._random_string(8)}"},
                {"name": "email", "type": "VARCHAR", "data_element": "Email Address", "sample": f"{self._random_string(5)}@example.com"},
                {"name": "created_at", "type": "DATETIME", "data_element": None, "sample": f"{self._random_date()} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"},
            ],
            "data": [
                {"name": "data_id", "type": "INT", "data_element": None, "sample": str(random.randint(10000, 99999))},
                {"name": "user_id", "type": "INT", "data_element": None, "sample": str(random.randint(1000, 9999))},
                {"name": "data_type", "type": "VARCHAR", "data_element": None, "sample": random.choice(["Type A", "Type B", "Type C"])},
                {"name": "content", "type": "TEXT", "data_element": None, "sample": f"Sample content {self._random_string(20)}"},
                {"name": "created_at", "type": "DATETIME", "data_element": None, "sample": f"{self._random_date()} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"},
            ]
        }
        
        return self._create_catalog_entries(asset_id, schema_name, tables, data_elements)
    
    def _create_catalog_entries(self, asset_id, schema_name, tables, data_elements):
        """Create catalog entries from table definitions."""
        entries = []
        
        # Create a mapping of data element names to IDs for quick lookup
        data_element_map = {de[1]: de[0] for de in data_elements}
        
        for table_name, columns in tables.items():
            for column in columns:
                data_element_id = None
                if column["data_element"] and column["data_element"] in data_element_map:
                    data_element_id = data_element_map[column["data_element"]]
                
                entries.append({
                    "asset_id": asset_id,
                    "schema_name": schema_name,
                    "table_name": table_name,
                    "column_name": column["name"],
                    "data_type": column["type"],
                    "data_element_id": data_element_id,
                    "sample_data": column["sample"]
                })
        
        return entries
    
    def _generate_policy_implementations(self, asset_id):
        """Generate policy implementations for sensitive data in the catalog."""
        cursor = self.connection.cursor()
        try:
            # Get policies
            cursor.execute("SELECT id, name FROM policy")
            policies = cursor.fetchall()
            policy_map = {p[1]: p[0] for p in policies}
            
            # Get catalog entries with sensitive data elements
            cursor.execute("""
            SELECT c.id, de.name as data_element_name
            FROM catalog c
            JOIN data_element de ON c.data_element_id = de.id
            WHERE c.asset_id = %s AND de.name IN (
                'Social Security Number', 'Credit Card Number', 'Bank Account Number',
                'Email Address', 'Phone Number', 'Home Address', 'Date of Birth',
                'Salary Information', 'Health Insurance Information'
            )
            """, (asset_id,))
            
            sensitive_entries = cursor.fetchall()
            
            # For each sensitive entry, create policy implementations
            for entry in sensitive_entries:
                catalog_id = entry[0]
                data_element_name = entry[1]
                
                # Different policies based on data element type
                if data_element_name in ['Social Security Number', 'Credit Card Number', 'Bank Account Number']:
                    # Data Security Policy
                    if 'Data Security Policy' in policy_map:
                        cursor.execute("""
                        INSERT INTO policy_implementation (
                            catalog_id, policy_id, is_masked, masking_format,
                            is_encrypted, encryption_algorithm, has_access_control,
                            access_control_type, has_retention_policy, retention_period,
                            has_audit_logging, audit_level, implementation_status
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            catalog_id,
                            policy_map['Data Security Policy'],
                            True,
                            'Show only last 4 digits',
                            True,
                            'AES-256',
                            True,
                            'Role-based',
                            True,
                            '7 years',
                            True,
                            'Full',
                            random.choice(['Partially Implemented', 'Fully Implemented'])
                        ))
                
                elif data_element_name in ['Email Address', 'Phone Number']:
                    # Data Security Policy
                    if 'Data Security Policy' in policy_map:
                        cursor.execute("""
                        INSERT INTO policy_implementation (
                            catalog_id, policy_id, is_masked, masking_format,
                            is_encrypted, encryption_algorithm, has_access_control,
                            access_control_type, has_retention_policy, retention_period,
                            has_audit_logging, audit_level, implementation_status
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            catalog_id,
                            policy_map['Data Security Policy'],
                            True,
                            'Partial masking',
                            False,
                            None,
                            True,
                            'Role-based',
                            True,
                            '2 years',
                            True,
                            'Basic',
                            random.choice(['Not Implemented', 'Partially Implemented'])
                        ))
                
                elif data_element_name in ['Salary Information', 'Health Insurance Information']:
                    # Data Access Control Policy
                    if 'Data Access Control Policy' in policy_map:
                        cursor.execute("""
                        INSERT INTO policy_implementation (
                            catalog_id, policy_id, is_masked, masking_format,
                            is_encrypted, encryption_algorithm, has_access_control,
                            access_control_type, has_retention_policy, retention_period,
                            has_audit_logging, audit_level, implementation_status
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            catalog_id,
                            policy_map['Data Access Control Policy'],
                            True,
                            'Full masking for non-authorized roles',
                            False,
                            None,
                            True,
                            'Role-based',
                            True,
                            '7 years',
                            True,
                            'Full',
                            random.choice(['Partially Implemented', 'Fully Implemented'])
                        ))
        
        except Exception as e:
            print(f"Error generating policy implementations: {e}")
            raise
    
    def _random_string(self, length):
        """Generate a random string of specified length."""
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    
    def _random_date(self, start_year=2020, end_year=2025):
        """Generate a random date between start_year and end_year."""
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Using 28 to avoid month/leap year issues
        return f"{year}-{month:02d}-{day:02d}"
