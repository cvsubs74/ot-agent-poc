import pymysql.cursors
import json
from datetime import datetime

class PolicyDefinitionRepository:
    def __init__(self, connection):
        """Initialize the PolicyDefinitionRepository with a database connection."""
        self.connection = connection
        
    # Policy Type Methods
    def get_all_policy_types(self):
        """Get all policy types."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, json_schema, created_at, updated_at
                FROM policy_types
                ORDER BY name
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting policy types: {e}")
            return []
        finally:
            cursor.close()
    
    def get_policy_type_by_id(self, policy_type_id):
        """Get a policy type by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, json_schema, created_at, updated_at
                FROM policy_types
                WHERE id = %s
            """, (policy_type_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting policy type by ID {policy_type_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def get_policy_type_by_name(self, name):
        """Get a policy type by name."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, json_schema, created_at, updated_at
                FROM policy_types
                WHERE name = %s
            """, (name,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting policy type by name {name}: {e}")
            return None
        finally:
            cursor.close()
    
    def create_policy_type(self, name, json_schema, description=None):
        """Create a new policy type."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Validate JSON schema
            if isinstance(json_schema, str):
                json_obj = json.loads(json_schema)
            else:
                json_obj = json_schema
                json_schema = json.dumps(json_schema)
            
            cursor.execute("""
                INSERT INTO policy_types (name, description, json_schema)
                VALUES (%s, %s, %s)
            """, (name, description, json_schema))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating policy type: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def update_policy_type(self, policy_type_id, name=None, json_schema=None, description=None):
        """Update an existing policy type."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Build update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if name is not None:
                update_parts.append("name = %s")
                params.append(name)
                
            if description is not None:
                update_parts.append("description = %s")
                params.append(description)
                
            if json_schema is not None:
                # Validate JSON schema
                if isinstance(json_schema, str):
                    json_obj = json.loads(json_schema)
                else:
                    json_obj = json_schema
                    json_schema = json.dumps(json_schema)
                
                update_parts.append("json_schema = %s")
                params.append(json_schema)
                
            if not update_parts:
                return False  # Nothing to update
                
            # Add the policy_type_id to params
            params.append(policy_type_id)
            
            query = f"""UPDATE policy_types 
                      SET {', '.join(update_parts)} 
                      WHERE id = %s"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating policy type {policy_type_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def delete_policy_type(self, policy_type_id):
        """Delete a policy type."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                DELETE FROM policy_types
                WHERE id = %s
            """, (policy_type_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting policy type {policy_type_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    # Region Methods
    
    def get_all_regions(self):
        """Get all regions."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, created_at, updated_at
                FROM regions
                ORDER BY name
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting regions: {e}")
            return []
        finally:
            cursor.close()
    
    def get_region_by_id(self, region_id):
        """Get a region by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, created_at, updated_at
                FROM regions
                WHERE id = %s
            """, (region_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting region by ID {region_id}: {e}")
            return None
        finally:
            cursor.close()
    
    def get_region_by_name(self, name):
        """Get a region by name."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, created_at, updated_at
                FROM regions
                WHERE name = %s
            """, (name,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting region by name {name}: {e}")
            return None
        finally:
            cursor.close()
    
    def create_region(self, name, description=None):
        """Create a new region."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                INSERT INTO regions (name, description)
                VALUES (%s, %s)
            """, (name, description))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating region: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def update_region(self, region_id, name=None, description=None):
        """Update an existing region."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Build update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if name is not None:
                update_parts.append("name = %s")
                params.append(name)
                
            if description is not None:
                update_parts.append("description = %s")
                params.append(description)
                
            if not update_parts:
                return False  # Nothing to update
                
            # Add the region_id to params
            params.append(region_id)
            
            query = f"""UPDATE regions 
                      SET {', '.join(update_parts)} 
                      WHERE id = %s"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating region {region_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def delete_region(self, region_id):
        """Delete a region."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("DELETE FROM regions WHERE id = %s", (region_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting region: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    # Helper methods for data elements, categories, and sensitivities
    def get_data_element_by_id(self, data_element_id):
        """Get a data element by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, data_type, created_at, updated_at
                FROM data_element
                WHERE id = %s
            """, (data_element_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting data element by ID {data_element_id}: {e}")
            return None
        finally:
            cursor.close()
            
    def get_data_category_by_id(self, data_category_id):
        """Get a data category by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, created_at, updated_at
                FROM data_category
                WHERE id = %s
            """, (data_category_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting data category by ID {data_category_id}: {e}")
            return None
        finally:
            cursor.close()
            
    def get_sensitivity_by_id(self, sensitivity_id):
        """Get a sensitivity level by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, level, created_at, updated_at
                FROM sensitivity
                WHERE id = %s
            """, (sensitivity_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting sensitivity by ID {sensitivity_id}: {e}")
            return None
        finally:
            cursor.close()
            
    # Policy Methods
    
    def get_all_policies(self):
        """Get all policies."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT p.id, p.name, p.policy_type_id, pt.name as policy_type_name, 
                       p.data_element_id, de.name as data_element_name,
                       p.data_category_id, dc.name as data_category_name,
                       p.sensitivity_id, s.name as sensitivity_name,
                       p.policy_config, p.effective_from, p.effective_to,
                       p.created_at, p.updated_at
                FROM policies p
                JOIN policy_types pt ON p.policy_type_id = pt.id
                LEFT JOIN data_element de ON p.data_element_id = de.id
                LEFT JOIN data_category dc ON p.data_category_id = dc.id
                LEFT JOIN sensitivity s ON p.sensitivity_id = s.id
                ORDER BY p.id DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting policies: {e}")
            return []
        finally:
            cursor.close()

    def get_policy_by_id(self, policy_id):
        """Get a policy by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT p.id, p.name, p.policy_type_id, pt.name as policy_type_name, 
                       p.data_element_id, de.name as data_element_name,
                       p.data_category_id, dc.name as data_category_name,
                       p.sensitivity_id, s.name as sensitivity_name,
                       p.policy_config, p.effective_from, p.effective_to,
                       p.created_at, p.updated_at
                FROM policies p
                JOIN policy_types pt ON p.policy_type_id = pt.id
                LEFT JOIN data_element de ON p.data_element_id = de.id
                LEFT JOIN data_category dc ON p.data_category_id = dc.id
                LEFT JOIN sensitivity s ON p.sensitivity_id = s.id
                WHERE p.id = %s
            """, (policy_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting policy by ID {policy_id}: {e}")
            return None
        finally:
            cursor.close()

    def create_policy(self, policy_type_id, data_element_id=None, data_category_id=None, 
                      sensitivity_id=None, policy_config=None, effective_from=None, effective_to=None, name=None):
        """Create a new policy."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Validate policy configuration against schema
            policy_type = self.get_policy_type_by_id(policy_type_id)
            if not policy_type:
                print(f"Policy type with ID {policy_type_id} not found")
                return None
                
            # Convert policy_config to JSON string if it's a dict
            if isinstance(policy_config, dict):
                policy_config = json.dumps(policy_config)
            
            # Validate at least one target is specified
            if data_element_id is None and data_category_id is None and sensitivity_id is None:
                print("At least one of data_element_id, data_category_id, or sensitivity_id must be specified")
                return None
            
            # Generate a default name if none provided
            if name is None:
                # Get target name for the policy
                target_name = None
                if data_element_id:
                    element = self.get_data_element_by_id(data_element_id)
                    if element:
                        target_name = element.get('name')
                elif data_category_id:
                    category = self.get_data_category_by_id(data_category_id)
                    if category:
                        target_name = category.get('name')
                elif sensitivity_id:
                    sensitivity = self.get_sensitivity_by_id(sensitivity_id)
                    if sensitivity:
                        target_name = sensitivity.get('name')
                
                # Get policy type name
                policy_type_name = policy_type.get('name') if policy_type else 'Policy'
                
                # Create a default name
                name = f"{policy_type_name} for {target_name if target_name else 'Unknown Target'}"
            
            cursor.execute("""
                INSERT INTO policies 
                (policy_type_id, data_element_id, data_category_id, sensitivity_id, 
                 policy_config, effective_from, effective_to, name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (policy_type_id, data_element_id, data_category_id, sensitivity_id, 
                  policy_config, effective_from, effective_to, name))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating policy: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def update_policy(self, policy_id, policy_type_id=None, data_element_id=None, 
                      data_category_id=None, sensitivity_id=None, policy_config=None, 
                      effective_from=None, effective_to=None):
        """Update an existing policy."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Build update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if policy_type_id is not None:
                update_parts.append("policy_type_id = %s")
                params.append(policy_type_id)
                
            if data_element_id is not None:
                update_parts.append("data_element_id = %s")
                params.append(data_element_id)
                
            if data_category_id is not None:
                update_parts.append("data_category_id = %s")
                params.append(data_category_id)
                
            if sensitivity_id is not None:
                update_parts.append("sensitivity_id = %s")
                params.append(sensitivity_id)
                
            if policy_config is not None:
                # Convert policy_config to JSON string if it's a dict
                if isinstance(policy_config, dict):
                    policy_config = json.dumps(policy_config)
                update_parts.append("policy_config = %s")
                params.append(policy_config)
                
            if effective_from is not None:
                update_parts.append("effective_from = %s")
                params.append(effective_from)
                
            if effective_to is not None:
                update_parts.append("effective_to = %s")
                params.append(effective_to)
                
            if not update_parts:
                return False  # Nothing to update
                
            # Add the policy_id to params
            params.append(policy_id)
            
            query = f"""UPDATE policies 
                      SET {', '.join(update_parts)} 
                      WHERE id = %s"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating policy {policy_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def delete_policy(self, policy_id):
        """Delete a policy."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                DELETE FROM policies
                WHERE id = %s
            """, (policy_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting policy {policy_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    # Policy Group Methods
    
    def get_all_policy_groups(self):
        """Get all policy groups."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, version, is_active, created_at, updated_at
                FROM policy_groups
                ORDER BY name, version DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting policy groups: {e}")
            return []
        finally:
            cursor.close()

    def get_policy_group_by_id(self, policy_group_id):
        """Get a policy group by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, version, is_active, created_at, updated_at
                FROM policy_groups
                WHERE id = %s
            """, (policy_group_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting policy group by ID {policy_group_id}: {e}")
            return None
        finally:
            cursor.close()

    def get_policy_group_by_name_version(self, name, version):
        """Get a policy group by name and version."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, version, is_active, created_at, updated_at
                FROM policy_groups
                WHERE name = %s AND version = %s
            """, (name, version))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting policy group by name {name} and version {version}: {e}")
            return None
        finally:
            cursor.close()

    def create_policy_group(self, name, description=None, version="1.0", is_active=True):
        """Create a new policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                INSERT INTO policy_groups (name, description, version, is_active)
                VALUES (%s, %s, %s, %s)
            """, (name, description, version, is_active))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating policy group: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def update_policy_group(self, policy_group_id, name=None, description=None, version=None, is_active=None):
        """Update an existing policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Build update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if name is not None:
                update_parts.append("name = %s")
                params.append(name)
                
            if description is not None:
                update_parts.append("description = %s")
                params.append(description)
                
            if version is not None:
                update_parts.append("version = %s")
                params.append(version)
                
            if is_active is not None:
                update_parts.append("is_active = %s")
                params.append(is_active)
                
            if not update_parts:
                return False  # Nothing to update
                
            # Add the policy_group_id to params
            params.append(policy_group_id)
            
            query = f"""UPDATE policy_groups 
                      SET {', '.join(update_parts)} 
                      WHERE id = %s"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating policy group {policy_group_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def delete_policy_group(self, policy_group_id):
        """Delete a policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                DELETE FROM policy_groups
                WHERE id = %s
            """, (policy_group_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting policy group {policy_group_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def get_policies_in_group(self, policy_group_id):
        """Get all policies in a policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT pgm.id, pgm.policy_group_id, pgm.policy_id, pgm.target_system,
                       p.policy_type_id, pt.name as policy_type_name, 
                       p.data_element_id, de.name as data_element_name,
                       p.data_category_id, dc.name as data_category_name,
                       p.sensitivity_id, s.name as sensitivity_name,
                       p.policy_config, p.effective_from, p.effective_to
                FROM policy_group_members pgm
                JOIN policies p ON pgm.policy_id = p.id
                JOIN policy_types pt ON p.policy_type_id = pt.id
                LEFT JOIN data_element de ON p.data_element_id = de.id
                LEFT JOIN data_category dc ON p.data_category_id = dc.id
                LEFT JOIN sensitivity s ON p.sensitivity_id = s.id
                WHERE pgm.policy_group_id = %s
                ORDER BY pgm.id
            """, (policy_group_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting policies in group {policy_group_id}: {e}")
            return []
        finally:
            cursor.close()

    def add_policy_to_group(self, policy_group_id, policy_id, target_system=None):
        """Add a policy to a policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                INSERT INTO policy_group_members (policy_group_id, policy_id, target_system)
                VALUES (%s, %s, %s)
            """, (policy_group_id, policy_id, target_system))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding policy {policy_id} to group {policy_group_id}: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def remove_policy_from_group(self, policy_group_id, policy_id, target_system=None):
        """Remove a policy from a policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if target_system:
                cursor.execute("""
                    DELETE FROM policy_group_members
                    WHERE policy_group_id = %s AND policy_id = %s AND target_system = %s
                """, (policy_group_id, policy_id, target_system))
            else:
                cursor.execute("""
                    DELETE FROM policy_group_members
                    WHERE policy_group_id = %s AND policy_id = %s
                """, (policy_group_id, policy_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error removing policy {policy_id} from group {policy_group_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    # Context Policy Group Methods
    
    def get_all_context_policy_groups(self):
        """Get all context policy groups."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT cpg.id, cpg.purpose_id, p.name as purpose_name, 
                       cpg.external_role_id, er.name as external_role_name,
                       cpg.region_id, r.name as region_name,
                       cpg.policy_group_id, pg.name as policy_group_name, pg.version as policy_group_version,
                       cpg.granularity_rank, cpg.manual_priority, cpg.context_tags,
                       cpg.effective_from, cpg.effective_to, cpg.created_at, cpg.updated_at
                FROM context_policy_groups cpg
                LEFT JOIN purpose p ON cpg.purpose_id = p.id
                LEFT JOIN external_roles er ON cpg.external_role_id = er.id
                LEFT JOIN regions r ON cpg.region_id = r.id
                JOIN policy_groups pg ON cpg.policy_group_id = pg.id
                ORDER BY cpg.manual_priority DESC, cpg.granularity_rank DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting context policy groups: {e}")
            return []
        finally:
            cursor.close()

    def get_context_policy_groups_by_policy_group(self, policy_group_id):
        """Get all context policy groups for a specific policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT cpg.id, cpg.purpose_id, p.name as purpose_name, 
                       cpg.external_role_id, er.name as external_role_name,
                       cpg.region_id, r.name as region_name,
                       cpg.policy_group_id, pg.name as policy_group_name, pg.version as policy_group_version,
                       cpg.granularity_rank, cpg.manual_priority, cpg.context_tags,
                       cpg.effective_from, cpg.effective_to, cpg.created_at, cpg.updated_at
                FROM context_policy_groups cpg
                LEFT JOIN purpose p ON cpg.purpose_id = p.id
                LEFT JOIN external_roles er ON cpg.external_role_id = er.id
                LEFT JOIN regions r ON cpg.region_id = r.id
                JOIN policy_groups pg ON cpg.policy_group_id = pg.id
                WHERE cpg.policy_group_id = %s
                ORDER BY cpg.manual_priority DESC, cpg.granularity_rank DESC
            """, (policy_group_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting context policy groups for policy group {policy_group_id}: {e}")
            return []
        finally:
            cursor.close()
    
    def get_context_policy_group_by_id(self, context_id):
        """Get a context policy group by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT cpg.id, cpg.purpose_id, p.name as purpose_name, 
                       cpg.external_role_id, er.name as external_role_name,
                       cpg.region_id, r.name as region_name,
                       cpg.policy_group_id, pg.name as policy_group_name, pg.version as policy_group_version,
                       cpg.granularity_rank, cpg.manual_priority, cpg.context_tags,
                       cpg.effective_from, cpg.effective_to, cpg.created_at, cpg.updated_at
                FROM context_policy_groups cpg
                LEFT JOIN purpose p ON cpg.purpose_id = p.id
                LEFT JOIN external_roles er ON cpg.external_role_id = er.id
                LEFT JOIN regions r ON cpg.region_id = r.id
                JOIN policy_groups pg ON cpg.policy_group_id = pg.id
                WHERE cpg.id = %s
            """, (context_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting context policy group by ID {context_id}: {e}")
            return None
        finally:
            cursor.close()

    def create_context_policy_group(self, purpose_id=None, external_role_id=None, region_id=None, 
                                    policy_group_id=None, granularity_rank=0, manual_priority=0, 
                                    context_tags=None, effective_from=None, effective_to=None):
        """Create a new context policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Calculate granularity rank if not provided
            if granularity_rank is None:
                granularity_rank = 0
                if purpose_id is not None:
                    granularity_rank += 1
                if external_role_id is not None:
                    granularity_rank += 1
                if region_id is not None:
                    granularity_rank += 1
                    
            # Convert context_tags to JSON string if it's a dict
            if isinstance(context_tags, dict):
                context_tags = json.dumps(context_tags)
                
            # Validate that policy_group_id is provided
            if policy_group_id is None:
                print("policy_group_id must be specified")
                return None
                
            cursor.execute("""
                INSERT INTO context_policy_groups 
                (purpose_id, external_role_id, region_id, policy_group_id, 
                 granularity_rank, manual_priority, context_tags, effective_from, effective_to)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (purpose_id, external_role_id, region_id, policy_group_id, 
                  granularity_rank, manual_priority, context_tags, effective_from, effective_to))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating context policy group: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def update_context_policy_group(self, context_id, purpose_id=None, external_role_id=None, 
                                    region_id=None, policy_group_id=None, granularity_rank=None, 
                                    manual_priority=None, context_tags=None, effective_from=None, 
                                    effective_to=None):
        """Update an existing context policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Build update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if purpose_id is not None:
                update_parts.append("purpose_id = %s")
                params.append(purpose_id)
                
            if external_role_id is not None:
                update_parts.append("external_role_id = %s")
                params.append(external_role_id)
                
            if region_id is not None:
                update_parts.append("region_id = %s")
                params.append(region_id)
                
            if policy_group_id is not None:
                update_parts.append("policy_group_id = %s")
                params.append(policy_group_id)
                
            if granularity_rank is not None:
                update_parts.append("granularity_rank = %s")
                params.append(granularity_rank)
                
            if manual_priority is not None:
                update_parts.append("manual_priority = %s")
                params.append(manual_priority)
                
            if context_tags is not None:
                # Convert context_tags to JSON string if it's a dict
                if isinstance(context_tags, dict):
                    context_tags = json.dumps(context_tags)
                update_parts.append("context_tags = %s")
                params.append(context_tags)
                
            if effective_from is not None:
                update_parts.append("effective_from = %s")
                params.append(effective_from)
                
            if effective_to is not None:
                update_parts.append("effective_to = %s")
                params.append(effective_to)
                
            if not update_parts:
                return False  # Nothing to update
                
            # Add the context_id to params
            params.append(context_id)
            
            query = f"""UPDATE context_policy_groups 
                      SET {', '.join(update_parts)} 
                      WHERE id = %s"""
                      
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating context policy group {context_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def delete_context_policy_group(self, context_id):
        """Delete a context policy group."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                DELETE FROM context_policy_groups
                WHERE id = %s
            """, (context_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting context policy group {context_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
            
    # Access Request Methods
    
    def get_all_access_requests(self):
        """Get all access requests."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT ar.id, ar.requester_id, ar.dataset_id, ar.purpose_id, p.name as purpose_name,
                       ar.justification, ar.status, ar.approved_by, ar.expires_at,
                       ar.created_at, ar.updated_at
                FROM access_requests ar
                JOIN purpose p ON ar.purpose_id = p.id
                ORDER BY ar.created_at DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting access requests: {e}")
            return []
        finally:
            cursor.close()

    def get_access_request_by_id(self, request_id):
        """Get an access request by ID."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT ar.id, ar.requester_id, ar.dataset_id, ar.purpose_id, p.name as purpose_name,
                       ar.justification, ar.status, ar.approved_by, ar.expires_at,
                       ar.created_at, ar.updated_at
                FROM access_requests ar
                JOIN purpose p ON ar.purpose_id = p.id
                WHERE ar.id = %s
            """, (request_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error getting access request by ID {request_id}: {e}")
            return None
        finally:
            cursor.close()

    def create_access_request(self, requester_id, purpose_id, dataset_id=None, justification=None):
        """Create a new access request."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                INSERT INTO access_requests (requester_id, dataset_id, purpose_id, justification)
                VALUES (%s, %s, %s, %s)
            """, (requester_id, dataset_id, purpose_id, justification))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating access request: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def update_access_request_status(self, request_id, status, approved_by=None, expires_at=None):
        """Update an access request status."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                UPDATE access_requests
                SET status = %s, approved_by = %s, expires_at = %s
                WHERE id = %s
            """, (status, approved_by, expires_at, request_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating access request status {request_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def get_pending_access_requests_for_approver(self, approver_id):
        """Get pending access requests for an approver."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # This query assumes there's a way to determine which requests an approver can approve
            # You might need to adjust this based on your authorization model
            cursor.execute("""
                SELECT ar.id, ar.requester_id, ar.dataset_id, ar.purpose_id, p.name as purpose_name,
                       ar.justification, ar.status, ar.created_at, ar.updated_at
                FROM access_requests ar
                JOIN purpose p ON ar.purpose_id = p.id
                WHERE ar.status = 'pending'
                -- Add additional conditions to filter requests for this approver
                ORDER BY ar.created_at ASC
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting pending access requests for approver {approver_id}: {e}")
            return []
        finally:
            cursor.close()

    # Purpose Member Methods

    def get_all_purpose_members(self, purpose_id=None):
        """Get all purpose members, optionally filtered by purpose."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            if purpose_id:
                cursor.execute("""
                    SELECT pm.id, pm.purpose_id, p.name as purpose_name, 
                           pm.user_id, pm.granted_by, pm.expires_at,
                           pm.created_at, pm.updated_at
                    FROM purpose_members pm
                    JOIN purpose p ON pm.purpose_id = p.id
                    WHERE pm.purpose_id = %s
                    ORDER BY pm.created_at DESC
                """, (purpose_id,))
            else:
                cursor.execute("""
                    SELECT pm.id, pm.purpose_id, p.name as purpose_name, 
                           pm.user_id, pm.granted_by, pm.expires_at,
                           pm.created_at, pm.updated_at
                    FROM purpose_members pm
                    JOIN purpose p ON pm.purpose_id = p.id
                    ORDER BY p.name, pm.created_at DESC
                """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting purpose members: {e}")
            return []
        finally:
            cursor.close()

    def add_user_to_purpose(self, purpose_id, user_id, granted_by=None, expires_at=None):
        """Add a user to a purpose."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                INSERT INTO purpose_members (purpose_id, user_id, granted_by, expires_at)
                VALUES (%s, %s, %s, %s)
            """, (purpose_id, user_id, granted_by, expires_at))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding user {user_id} to purpose {purpose_id}: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def remove_user_from_purpose(self, purpose_id, user_id):
        """Remove a user from a purpose."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                DELETE FROM purpose_members
                WHERE purpose_id = %s AND user_id = %s
            """, (purpose_id, user_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error removing user {user_id} from purpose {purpose_id}: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def get_purposes_for_user(self, user_id):
        """Get all purposes for a user."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT pm.id, pm.purpose_id, p.name as purpose_name, 
                       pm.user_id, pm.granted_by, pm.expires_at,
                       pm.created_at, pm.updated_at
                FROM purpose_members pm
                JOIN purpose p ON pm.purpose_id = p.id
                WHERE pm.user_id = %s
                ORDER BY p.name
            """, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting purposes for user {user_id}: {e}")
            return []
        finally:
            cursor.close()
            
    # Policy Enforcement Methods
    
    def get_effective_policies(self, purpose_id=None, external_role_id=None, data_element_id=None, 
                               data_category_id=None, sensitivity_id=None, region_id=None):
        """
        Get effective policies based on the provided context.
        
        This method implements the core policy resolution logic:
        1. Find all matching context policy groups based on purpose, role, and region
        2. Sort by granularity_rank and manual_priority to find the most specific match
        3. Get policies from the matched policy group
        4. Filter policies by data element, category, or sensitivity if provided
        
        Returns a list of policy objects with their configurations.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Build the WHERE clause for context matching
            where_parts = []
            params = []
            
            if purpose_id is not None:
                where_parts.append("(cpg.purpose_id = %s OR cpg.purpose_id IS NULL)")
                params.append(purpose_id)
                
            if external_role_id is not None:
                where_parts.append("(cpg.external_role_id = %s OR cpg.external_role_id IS NULL)")
                params.append(external_role_id)
                
            if region_id is not None:
                where_parts.append("(cpg.region_id = %s OR cpg.region_id IS NULL)")
                params.append(region_id)
                
            # Add effective date filtering
            where_parts.append("(cpg.effective_from IS NULL OR cpg.effective_from <= NOW())")
            where_parts.append("(cpg.effective_to IS NULL OR cpg.effective_to >= NOW())")
            
            # Only include active policy groups
            where_parts.append("pg.is_active = TRUE")
            
            where_clause = " AND ".join(where_parts) if where_parts else "1=1"
            
            # Query to get matching context policy groups
            query = f"""
                SELECT cpg.id, cpg.policy_group_id, cpg.granularity_rank, cpg.manual_priority
                FROM context_policy_groups cpg
                JOIN policy_groups pg ON cpg.policy_group_id = pg.id
                WHERE {where_clause}
                ORDER BY cpg.manual_priority DESC, cpg.granularity_rank DESC
                LIMIT 1
            """
            
            cursor.execute(query, params)
            context_match = cursor.fetchone()
            
            if not context_match:
                return []  # No matching context found
                
            policy_group_id = context_match['policy_group_id']
            
            # Now get policies from the matched policy group
            policy_params = []
            policy_where_parts = []
            
            # Filter by data element, category, or sensitivity if provided
            if data_element_id is not None:
                policy_where_parts.append("(p.data_element_id = %s OR p.data_element_id IS NULL)")
                policy_params.append(data_element_id)
                
            if data_category_id is not None:
                policy_where_parts.append("(p.data_category_id = %s OR p.data_category_id IS NULL)")
                policy_params.append(data_category_id)
                
            if sensitivity_id is not None:
                policy_where_parts.append("(p.sensitivity_id = %s OR p.sensitivity_id IS NULL)")
                policy_params.append(sensitivity_id)
                
            # Add effective date filtering for policies
            policy_where_parts.append("(p.effective_from IS NULL OR p.effective_from <= NOW())")
            policy_where_parts.append("(p.effective_to IS NULL OR p.effective_to >= NOW())")
            
            policy_where_clause = " AND ".join(policy_where_parts) if policy_where_parts else "1=1"
            
            # Query to get policies from the policy group
            policy_query = f"""
                SELECT p.id, p.policy_type_id, pt.name as policy_type_name, 
                       p.data_element_id, de.name as data_element_name,
                       p.data_category_id, dc.name as data_category_name,
                       p.sensitivity_id, s.name as sensitivity_name,
                       p.policy_config, pgm.target_system
                FROM policy_group_members pgm
                JOIN policies p ON pgm.policy_id = p.id
                JOIN policy_types pt ON p.policy_type_id = pt.id
                LEFT JOIN data_element de ON p.data_element_id = de.id
                LEFT JOIN data_category dc ON p.data_category_id = dc.id
                LEFT JOIN sensitivity s ON p.sensitivity_id = s.id
                WHERE pgm.policy_group_id = %s AND {policy_where_clause}
            """
            
            policy_params.insert(0, policy_group_id)
            cursor.execute(policy_query, policy_params)
            policies = cursor.fetchall()
            
            return policies
        except Exception as e:
            print(f"Error getting effective policies: {e}")
            return []
        finally:
            cursor.close()

    def log_access_event(self, user_id, purpose_id=None, dataset_id=None, decision='allowed', query_fingerprint=None):
        """Log an access event for audit purposes."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                INSERT INTO access_events (user_id, dataset_id, purpose_id, decision, query_fingerprint)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, dataset_id, purpose_id, decision, query_fingerprint))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error logging access event: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_access_events(self, user_id=None, dataset_id=None, purpose_id=None, start_date=None, end_date=None):
        """Get access events with optional filtering."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Build the WHERE clause based on provided filters
            where_parts = []
            params = []
            
            if user_id is not None:
                where_parts.append("ae.user_id = %s")
                params.append(user_id)
                
            if dataset_id is not None:
                where_parts.append("ae.dataset_id = %s")
                params.append(dataset_id)
                
            if purpose_id is not None:
                where_parts.append("ae.purpose_id = %s")
                params.append(purpose_id)
                
            if start_date is not None:
                where_parts.append("ae.access_time >= %s")
                params.append(start_date)
                
            if end_date is not None:
                where_parts.append("ae.access_time <= %s")
                params.append(end_date)
                
            where_clause = " AND ".join(where_parts) if where_parts else "1=1"
            
            query = f"""
                SELECT ae.id, ae.user_id, ae.dataset_id, ae.purpose_id, p.name as purpose_name,
                       ae.decision, ae.query_fingerprint, ae.access_time
                FROM access_events ae
                LEFT JOIN purpose p ON ae.purpose_id = p.id
                WHERE {where_clause}
                ORDER BY ae.access_time DESC
            """
            
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting access events: {e}")
            return []
        finally:
            cursor.close()

    def check_user_purpose_access(self, user_id, purpose_id):
        """Check if a user has access to a purpose."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM purpose_members
                WHERE user_id = %s AND purpose_id = %s
                AND (expires_at IS NULL OR expires_at > NOW())
            """, (user_id, purpose_id))
            result = cursor.fetchone()
            return result['count'] > 0
        except Exception as e:
            print(f"Error checking user purpose access: {e}")
            return False
        finally:
            cursor.close()

    def evaluate_policy_for_access(self, user_id, purpose_id, data_element_id=None, 
                                  data_category_id=None, sensitivity_id=None, region_id=None):
        """
        Evaluate policies to determine if access should be allowed.
        
        This is a high-level method that:
        1. Checks if the user has access to the purpose
        2. Gets effective policies for the context
        3. Evaluates the policies to make an access decision
        
        Returns a tuple (allowed, reason, policies) where:
        - allowed is a boolean indicating if access is allowed
        - reason is a string explaining the decision
        - policies is a list of policies that were applied
        """
        # First check if user has access to the purpose
        if purpose_id and not self.check_user_purpose_access(user_id, purpose_id):
            return (False, "User does not have access to the specified purpose", [])
        
        # Get user's roles (this would be implemented in your authentication system)
        # For now, we'll assume external_role_id is passed directly
        external_role_id = None  # This would be determined based on user_id
        
        # Get effective policies
        policies = self.get_effective_policies(
            purpose_id=purpose_id,
            external_role_id=external_role_id,
            data_element_id=data_element_id,
            data_category_id=data_category_id,
            sensitivity_id=sensitivity_id,
            region_id=region_id
        )
        
        # Check for DENY policies first
        for policy in policies:
            if policy['policy_type_name'] == 'DENY':
                # Log the denied access
                self.log_access_event(
                    user_id=user_id,
                    purpose_id=purpose_id,
                    dataset_id=None,  # Would be set in a real implementation
                    decision='denied'
                )
                
                # Get reason from policy config
                config = json.loads(policy['policy_config']) if isinstance(policy['policy_config'], str) else policy['policy_config']
                reason = config.get('reason', 'Access denied by policy')
                
                return (False, reason, [policy])
        
        # If we get here, no DENY policies matched, so access is allowed
        # Log the allowed access
        self.log_access_event(
            user_id=user_id,
            purpose_id=purpose_id,
            dataset_id=None,  # Would be set in a real implementation
            decision='allowed'
        )
        
        return (True, "Access allowed", policies)
