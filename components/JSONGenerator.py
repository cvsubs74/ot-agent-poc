import pandas as pd
import random
import string

class JSONGenerator:
    """
    A class for generating structured JSON from policy analysis DataFrames.
    This class handles the conversion of policy data into structured JSON formats
    for use in various components of the application.
    """
    
    def __init__(self, glossary_repository, catalog_repository):
        """
        Initialize the JSONGenerator with required repositories.
        
        Args:
            glossary_repository: Repository for accessing glossary data (assets, data elements)
            catalog_repository: Repository for accessing catalog entries
        """
        self.glossary_repository = glossary_repository
        self.catalog_repository = catalog_repository
    
    def build_column_based_json_from_df(self, df, asset_id):
        """
        Build a column-based JSON structure from the policy analysis DataFrame.
        The structure is organized by table/column first, with roles and purposes nested under each column.
        Includes ALL columns from each table, not just the classified ones with policies.
        
        Args:
            df: DataFrame containing policy analysis results
            asset_id: ID of the asset
            
        Returns:
            Dictionary containing policies organized by table/column, role, and purpose
        """
        # Initialize the result dictionary
        result = {
            "asset_id": asset_id,
            "tables": {}
        }
        
        # Get asset name
        assets = self.glossary_repository.get_assets()
        for asset in assets:
            if asset[0] == asset_id:
                result["asset_name"] = asset[1]
                break
        
        # Track unique purposes for each table to add to row filtering
        table_purposes = {}
        
        # Get all catalog entries for this asset to include ALL columns
        all_columns = self.catalog_repository.get_catalog_entries_by_asset(asset_id)
        
        # First, create the structure with ALL columns from the catalog
        for col in all_columns:
            schema_name = col.get('schema_name')
            table_name = col.get('table_name')
            column_name = col.get('column_name')
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Initialize table if not exists
            if table_key not in result["tables"]:
                result["tables"][table_key] = {
                    "schema": schema_name,
                    "table": table_name,
                    "columns": {}
                }
            
            # Add column to the table (even if it has no policies)
            if column_name not in result["tables"][table_key]["columns"]:
                result["tables"][table_key]["columns"][column_name] = {
                    "data_element_id": col.get('data_element_id'),
                    "data_element_name": col.get('data_element_name'),
                    "data_type": col.get('data_type'),
                    "roles": {}
                }
        
        # If no policies found, return the structure with all columns but no policies
        if df.empty:
            return result
        
        # Now add policy information to the columns that have policies
        for _, row in df.iterrows():
            schema_name = row.get('schema_name')
            table_name = row.get('table_name')
            column_name = row.get('column_name')
            purpose_name = row.get('purpose_name')
            role_name = row.get('role_name')
            role_id_val = row.get('role_id', 'default')
            policy_type_name = row.get('policy_type').lower()
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Track purposes for row filtering
            if table_key not in table_purposes:
                table_purposes[table_key] = set()
            table_purposes[table_key].add(purpose_name)
            
            # Initialize role if not exists for this column
            if role_name not in result["tables"][table_key]["columns"][column_name]["roles"]:
                result["tables"][table_key]["columns"][column_name]["roles"][role_name] = {
                    "role_id": role_id_val,
                    "purposes": {}
                }
            
            # Initialize purpose if not exists for this role and column
            if purpose_name not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"]:
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name] = {}
            
            # Add policy based on its type
            if policy_type_name == 'security':
                if "security" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["security"] = {
                        "policy_name": row.get('policy_name'),
                        "encryption_required": row.get('encryption_required'),
                        "encryption_algorithm": row.get('encryption_algorithm'),
                        "masking_required": row.get('masking_required'),
                        "masking_format": row.get('masking_format'),
                        "is_override": row.get('is_override', False)
                    }
            elif policy_type_name == 'usage':
                if "usage" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["usage"] = []
                
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["usage"].append({
                    "policy_name": row.get('policy_name'),
                    "operation": row.get('operation'),
                    "allowed": row.get('allowed'),
                    "restrictions": row.get('restrictions')
                })
            elif policy_type_name == 'retention':
                if "retention" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["retention"] = []
                
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["retention"].append({
                    "policy_name": row.get('policy_name'),
                    "retention_period": row.get('retention_period'),
                    "retention_condition": row.get('retention_condition'),
                    "is_override": row.get('is_override', False)
                })
        
        # Add row filtering information to tables
        for table_key, purposes in table_purposes.items():
            if table_key in result["tables"]:
                # Get identifier columns for this table (email and user_id if available)
                identifier_columns = {}
                for col_name, col_info in result["tables"][table_key]["columns"].items():
                    data_element_name = col_info.get("data_element_name", "").lower() if col_info.get("data_element_name") else ""
                    if "email" in data_element_name:
                        identifier_columns["email"] = col_name
                    elif "user" in data_element_name and "id" in data_element_name:
                        identifier_columns["user_id"] = col_name
                
                # Only add row filtering if we have identifier columns
                if identifier_columns:
                    result["tables"][table_key]["row_filtering"] = {
                        "identifier_columns": identifier_columns,
                        "purposes": list(purposes)
                    }
        
        return result
    
    def build_json_for_access_request(self, df, asset_id, selected_tables, selected_purposes, purpose_options):
        """
        Build a JSON structure for the access request based on the filtered policy analysis.
        This method is specifically designed for data access requests where only selected tables
        and purposes are included in the JSON.
        
        Args:
            df: DataFrame containing filtered policy analysis results
            asset_id: ID of the asset
            selected_tables: List of selected tables
            selected_purposes: List of selected purpose IDs
            purpose_options: Dictionary mapping purpose IDs to names
            
        Returns:
            Dictionary containing policies organized for the access request
        """
        # Initialize the result dictionary
        result = {
            "asset_id": asset_id,
            "tables": {},
            "role_name": f"DATA_ACCESS_{self._generate_random_suffix()}",
            "purposes": [purpose_options[p_id] for p_id in selected_purposes],
            "purpose_ids": selected_purposes
        }
        
        # Get asset name
        assets = self.glossary_repository.get_assets()
        for asset in assets:
            if asset[0] == asset_id:
                result["asset_name"] = asset[1]
                break
        
        # Get all catalog entries for this asset to include ALL columns
        all_columns = self.catalog_repository.get_catalog_entries_by_asset(asset_id)
        
        # Filter catalog entries to only include selected tables
        filtered_columns = [
            col for col in all_columns 
            if f"{col['schema_name']}.{col['table_name']}" in selected_tables
        ]
        
        # Track unique purposes for each table to add to row filtering
        table_purposes = {}
        
        # Create a dictionary of all selected tables and their columns
        for col in filtered_columns:
            schema_name = col.get('schema_name')
            table_name = col.get('table_name')
            column_name = col.get('column_name')
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Initialize table if not exists
            if table_key not in result["tables"]:
                result["tables"][table_key] = {
                    "schema": schema_name,
                    "table": table_name,
                    "columns": {}
                }
            
            # Add column to the table (even if it has no policies)
            if column_name not in result["tables"][table_key]["columns"]:
                result["tables"][table_key]["columns"][column_name] = {
                    "data_element_id": col.get('data_element_id'),
                    "data_element_name": col.get('data_element_name'),
                    "data_type": col.get('data_type'),
                    "roles": {}
                }
        
        # Now add policy information to the columns that have policies
        for _, row in df.iterrows():
            schema_name = row.get('schema_name')
            table_name = row.get('table_name')
            column_name = row.get('column_name')
            purpose_name = row.get('purpose_name')
            role_name = row.get('role_name')
            role_id_val = row.get('role_id', 'default')
            policy_type_name = row.get('policy_type').lower()
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Skip if this table is not in our selected tables
            if table_key not in selected_tables:
                continue
            
            # Track purposes for row filtering
            if table_key not in table_purposes:
                table_purposes[table_key] = set()
            table_purposes[table_key].add(purpose_name)
                
            # Initialize role if not exists for this column
            if role_name not in result["tables"][table_key]["columns"][column_name]["roles"]:
                result["tables"][table_key]["columns"][column_name]["roles"][role_name] = {
                    "role_id": role_id_val,
                    "purposes": {}
                }
            
            # Initialize purpose if not exists for this role and column
            if purpose_name not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"]:
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name] = {}
            
            # Add policy based on its type
            if policy_type_name == 'security':
                if "security" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["security"] = {
                        "policy_name": row.get('policy_name'),
                        "encryption_required": row.get('encryption_required'),
                        "encryption_algorithm": row.get('encryption_algorithm'),
                        "masking_required": row.get('masking_required'),
                        "masking_format": row.get('masking_format'),
                        "is_override": row.get('is_override', False)
                    }
            elif policy_type_name == 'usage':
                if "usage" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["usage"] = []
                
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["usage"].append({
                    "policy_name": row.get('policy_name'),
                    "operation": row.get('operation'),
                    "allowed": row.get('allowed'),
                    "restrictions": row.get('restrictions')
                })
            elif policy_type_name == 'retention':
                if "retention" not in result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["retention"] = []
                
                result["tables"][table_key]["columns"][column_name]["roles"][role_name]["purposes"][purpose_name]["retention"].append({
                    "policy_name": row.get('policy_name'),
                    "retention_period": row.get('retention_period'),
                    "retention_condition": row.get('retention_condition'),
                    "is_override": row.get('is_override', False)
                })
        
        # Add row filtering information to tables
        for table_key, purposes in table_purposes.items():
            if table_key in result["tables"]:
                # Get identifier columns for this table (email and user_id if available)
                identifier_columns = {}
                for col_name, col_info in result["tables"][table_key]["columns"].items():
                    data_element_name = col_info.get("data_element_name", "").lower() if col_info.get("data_element_name") else ""
                    if "email" in data_element_name:
                        identifier_columns["email"] = col_name
                    elif "user" in data_element_name and "id" in data_element_name:
                        identifier_columns["user_id"] = col_name
                
                # Only add row filtering if we have identifier columns
                if identifier_columns:
                    result["tables"][table_key]["row_filtering"] = {
                        "identifier_columns": identifier_columns,
                        "purposes": list(purposes)
                    }
        
        return result
    
    def _generate_random_suffix(self, length=4):
        """Generate a random alphanumeric suffix for the role name."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
