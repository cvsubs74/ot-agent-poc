import pandas as pd
from core.sensitivity_inference import SensitivityInference
from repositories.GlossaryRepository import GlossaryRepository

class AssetPolicyInference:
    """
    Inference engine to determine how policies are applied at the actual table column level
    for a given asset and purpose, including all policy types (security, usage, retention).
    """
    
    def __init__(self, catalog_repository, regulatory_metadata_repository, glossary_repository, inventory_repository, policy_repository=None):
        """
        Initialize the AssetPolicyInference with required repositories.
        
        Args:
            catalog_repository: Repository for accessing catalog data
            regulatory_metadata_repository: Repository for accessing policy metadata
            glossary_repository: Repository for accessing glossary data
            inventory_repository: Repository for accessing inventory data
            policy_repository: Repository for accessing policy data (optional)
        """
        self.catalog_repository = catalog_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.inventory_repository = inventory_repository
        self.glossary_repository = glossary_repository
        self.policy_repository = policy_repository if policy_repository else glossary_repository
        self.sensitivity_inference = SensitivityInference(self.glossary_repository, regulatory_metadata_repository)
    
    def get_applied_policies_for_asset_purpose(self, asset_id, purpose_id, policy_type='all', role_id='all'):
        """
        Get policies applied at the table column level for a given asset, purpose, policy type, and role.
        
        Args:
            asset_id: ID of the asset
            purpose_id: ID of the purpose, 'all' for all purposes, or a list of purpose IDs
            policy_type: Type of policy to filter by ('security', 'usage', 'retention', or 'all'), or a list of policy types
            role_id: ID of the external role to filter by, 'all' for all roles, or a list of role IDs
            
        Returns:
            DataFrame containing filtered policies applied to the asset's columns
        """
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('AssetPolicyInference')
        
        logger.info(f"===== POLICY ANALYSIS STARTED =====")
        logger.info(f"Parameters: asset_id={asset_id}, purpose_id={purpose_id}, policy_type={policy_type}, role_id={role_id}")
        
        # Get asset name for reference
        asset_name = None
        assets = self.inventory_repository.get_assets()
        for asset in assets:
            try:
                # Try dictionary access first
                if asset['id'] == asset_id:
                    asset_name = asset['name']
                    break
            except (TypeError, KeyError):
                # Fall back to tuple access if dictionary access fails
                try:
                    if isinstance(asset, tuple) and len(asset) >= 2 and asset[0] == asset_id:
                        asset_name = asset[1]  # Assuming second element is name
                        break
                except Exception as e:
                    logger.warning(f"Error accessing asset data: {e}")
                    continue
        logger.info(f"Asset: {asset_name} (ID: {asset_id})")
        
        # Get all catalog entries for the asset
        catalog_entries = self.catalog_repository.get_catalog_entries_by_asset(asset_id)
        logger.info(f"Retrieved {len(catalog_entries)} catalog entries for asset")
        
        # Initialize results list
        results = []
        
        # Handle purpose_id parameter (could be 'all', a single ID, or a list of IDs)
        if isinstance(purpose_id, list):
            if 'all' in purpose_id:
                logger.info("Processing ALL purposes (from list containing 'all')")
                purpose_id = 'all'
            else:
                logger.info(f"Processing multiple purposes: {purpose_id}")
        
        # Handle policy_type parameter (could be 'all', a single type, or a list of types)
        if isinstance(policy_type, list):
            if 'all' in policy_type:
                logger.info("Processing ALL policy types (from list containing 'all')")
                policy_type = 'all'
            else:
                logger.info(f"Processing multiple policy types: {policy_type}")
        
        # Handle role_id parameter (could be 'all', a single ID, or a list of IDs)
        if isinstance(role_id, list):
            if 'all' in role_id:
                logger.info("Processing ALL roles (from list containing 'all')")
                role_id = 'all'
            else:
                logger.info(f"Processing multiple roles: {role_id}")
        
        # Handle purposes (either 'all', a single ID, or a list of IDs)
        if purpose_id == 'all':
            logger.info("Processing ALL purposes")
            # Get all purposes
            purposes = self.glossary_repository.get_purposes()
            logger.info(f"Retrieved {len(purposes)} purposes to process")
            
            # Process each purpose
            for purpose in purposes:
                current_purpose_id = purpose["id"]
                current_purpose_name = purpose["name"]
                logger.info(f"Processing purpose: {current_purpose_name} (ID: {current_purpose_id})")
                
                # Process each catalog entry for this purpose
                self._process_catalog_entries_for_purpose(catalog_entries, current_purpose_id, current_purpose_name, policy_type, role_id, results, logger)
        elif isinstance(purpose_id, list):
            # Process multiple specific purposes
            logger.info(f"Processing {len(purpose_id)} specific purposes")
            purposes = self.glossary_repository.get_purposes()
            filtered_purposes = [p for p in purposes if p["id"] in purpose_id]
            logger.info(f"Found {len(filtered_purposes)} matching purposes")
            
            # Process each purpose in the list
            for purpose in filtered_purposes:
                current_purpose_id = purpose["id"]
                current_purpose_name = purpose["name"]
                logger.info(f"Processing purpose: {current_purpose_name} (ID: {current_purpose_id})")
                
                # Process each catalog entry for this purpose
                self._process_catalog_entries_for_purpose(catalog_entries, current_purpose_id, current_purpose_name, policy_type, role_id, results, logger)
        else:
            # Process a single specific purpose
            current_purpose_id = purpose_id
            purposes = self.glossary_repository.get_purposes()
            purpose_obj = next((p for p in purposes if p["id"] == current_purpose_id), None)
            
            if purpose_obj:
                current_purpose_name = purpose_obj["name"]
                    
            if purpose_obj:
                logger.info(f"Processing single purpose: {current_purpose_name} (ID: {current_purpose_id})")
                
                # Process each catalog entry for this purpose
                self._process_catalog_entries_for_purpose(catalog_entries, current_purpose_id, current_purpose_name, policy_type, role_id, results, logger)
            else:
                logger.warning(f"Purpose with ID {current_purpose_id} not found")
        
        # Create a DataFrame from the results
        if results:
            df = pd.DataFrame(results)
            logger.info(f"Created DataFrame with {len(df)} rows")
            logger.info(f"===== POLICY ANALYSIS COMPLETED =====")
            return df
        else:
            logger.info("No policy results found")
            logger.info(f"===== POLICY ANALYSIS COMPLETED =====")
            return pd.DataFrame()
    
    def _process_catalog_entries_for_purpose(self, catalog_entries, purpose_id, purpose_name, policy_type, role_id, results, logger):
        """Helper method to process catalog entries for a specific purpose."""
        entries_processed = 0
        for entry in catalog_entries:
            # Skip entries without a data element
            if not entry.get('data_element_id'):
                continue
                
            logger.debug(f"Processing entry: {entry.get('schema_name')}.{entry.get('table_name')}.{entry.get('column_name')}")
            entries_processed += 1
            
            # Handle multiple policy types
            if isinstance(policy_type, list):
                for pt in policy_type:
                    if pt == 'security':
                        logger.debug(f"Processing security policies for {entry.get('column_name')}")
                        self._process_security_policies(entry, purpose_id, purpose_name, results, role_id)
                    elif pt == 'usage':
                        logger.debug(f"Processing usage policies for {entry.get('column_name')}")
                        self._process_usage_policies(entry, purpose_id, purpose_name, results, role_id)
                    elif pt == 'retention':
                        logger.debug(f"Processing retention policies for {entry.get('column_name')}")
                        self._process_retention_policies(entry, purpose_id, purpose_name, results, role_id)
            else:
                # Process policies for this entry and purpose based on policy type
                if policy_type == 'all' or policy_type == 'security':
                    logger.debug(f"Processing security policies for {entry.get('column_name')}")
                    self._process_security_policies(entry, purpose_id, purpose_name, results, role_id)
                if policy_type == 'all' or policy_type == 'usage':
                    logger.debug(f"Processing usage policies for {entry.get('column_name')}")
                    self._process_usage_policies(entry, purpose_id, purpose_name, results, role_id)
                if policy_type == 'all' or policy_type == 'retention':
                    logger.debug(f"Processing retention policies for {entry.get('column_name')}")
                    self._process_retention_policies(entry, purpose_id, purpose_name, results, role_id)
        
        logger.info(f"Processed {entries_processed} entries for purpose {purpose_name}")
    
    def _process_security_policies(self, entry, purpose_id, purpose_name, results, role_id):
        """Process security policies for a catalog entry and purpose."""
        import logging
        logger = logging.getLogger('AssetPolicyInference')
        
        # Get the data element ID from the entry
        data_element_id = entry.get('data_element_id')
        if not data_element_id:
            return
        
        data_element_name = entry.get('data_element_name')
        logger.info(f"[SECURITY] Processing security policies for data element {data_element_name}")
        
        # Get security policies for this data element and purpose
        security_policies = self.regulatory_metadata_repository.get_policy_purpose_data_security(
            purpose_id=purpose_id,
            data_element_id=data_element_id
        )
        
        if not security_policies:
            logger.info(f"[SECURITY] No security policies found for data element {data_element_name} and purpose {purpose_name}")
            return
        
        logger.info(f"[SECURITY] Found {len(security_policies)} security policies for data element {data_element_name}")
        
        # Get all roles
        roles = self.glossary_repository.get_external_roles()
        
        # Filter roles if needed
        if isinstance(role_id, list):
            if 'all' not in role_id:
                # Filter roles by the list of role IDs
                filtered_roles = [role for role in roles if role[0] in role_id]
                if not filtered_roles:
                    logger.warning(f"[SECURITY] No roles found matching IDs {role_id}, no security policies will be processed")
                    return
                roles = filtered_roles
                role_names = [role[1] for role in roles]
                logger.info(f"[SECURITY] Filtering for roles: {role_names} (IDs: {role_id})")
        elif role_id != 'all':
            # Filter by a single role ID
            filtered_roles = [role for role in roles if role[0] == role_id]
            if not filtered_roles:
                logger.warning(f"[SECURITY] Role ID {role_id} not found, no security policies will be processed")
                return
            roles = filtered_roles
            logger.info(f"[SECURITY] Filtering for role: {roles[0][1]} (ID: {role_id})")
        
        # Add security policies to results for each role
        for policy in security_policies:
            policy_id = policy.get('policy_id')
            
            # For each role, add a policy entry
            for role in roles:
                role_id_val = role[0]
                role_name_val = role[1]
                
                # Check for overrides for this role
                policy_purpose_data_element_id = self._get_policy_purpose_data_element_id(
                    policy.get('policy_name'),
                    purpose_id,
                    data_element_id
                )
                
                if policy_purpose_data_element_id:
                    overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_security(
                        policy_purpose_data_element_id=policy_purpose_data_element_id,
                        external_role_id=role_id_val
                    )
                    
                    # If we have overrides, use those values
                    if overrides:
                        override = overrides[0]
                        results.append({
                            'schema_name': entry.get('schema_name'),
                            'table_name': entry.get('table_name'),
                            'column_name': entry.get('column_name'),
                            'data_element_id': data_element_id,
                            'data_element_name': entry.get('data_element_name'),
                            'data_type': entry.get('data_type'),
                            'purpose_id': purpose_id,
                            'purpose_name': purpose_name,
                            'role_id': role_id_val,
                            'role_name': role_name_val,
                            'policy_id': policy_id,
                            'policy_name': policy.get('policy_name'),
                            'policy_type': 'Security',
                            'encryption_required': override.get('encryption_required'),
                            'encryption_algorithm': override.get('encryption_algorithm'),
                            'masking_required': override.get('masking_required'),
                            'masking_format': override.get('masking_format'),
                            'is_override': True
                        })
                        continue
                
                # No overrides, use the default policy
                results.append({
                    'schema_name': entry.get('schema_name'),
                    'table_name': entry.get('table_name'),
                    'column_name': entry.get('column_name'),
                    'data_element_id': data_element_id,
                    'data_element_name': entry.get('data_element_name'),
                    'data_type': entry.get('data_type'),
                    'purpose_id': purpose_id,
                    'purpose_name': purpose_name,
                    'role_id': role_id_val,
                    'role_name': role_name_val,
                    'policy_id': policy_id,
                    'policy_name': policy.get('policy_name'),
                    'policy_type': 'Security',
                    'encryption_required': policy.get('encryption_required'),
                    'encryption_algorithm': policy.get('encryption_algorithm'),
                    'masking_required': policy.get('masking_required'),
                    'masking_format': policy.get('masking_format'),
                    'is_override': False
                })
        
        # Convert results to DataFrame
        logger.info(f"Total policy results collected: {len(results)}")
        if results:
            df = pd.DataFrame(results)
            
            # Reorder columns for better display
            column_order = [
                'schema_name', 'table_name', 'column_name', 'data_type', 
                'data_element_name', 'purpose_name', 'role_name', 'policy_name',
                'policy_type', 'operation', 'allowed', 'restrictions',
                'retention_period', 'retention_basis',
                'encryption_required', 'encryption_algorithm', 
                'masking_required', 'masking_format', 'is_override'
            ]
            
            # Only include columns that exist in the DataFrame
            columns_to_use = [col for col in column_order if col in df.columns]
            df = df[columns_to_use]
            
            logger.info(f"Final DataFrame created with {len(df)} rows and {len(columns_to_use)} columns")
            logger.info("===== POLICY ANALYSIS COMPLETED =====")
            return df
        
        logger.info("No policy results found. Returning empty DataFrame.")
        logger.info("===== POLICY ANALYSIS COMPLETED =====")
        return pd.DataFrame()
    
    def _process_security_policies(self, entry, purpose_id, purpose_name, results, role_id='all'):
        """
        Process security policies for a catalog entry and add them to results.
        
        Args:
            entry: Catalog entry (table column)
            purpose_id: ID of the purpose
            purpose_name: Name of the purpose
            results: List to append results to
            role_id: ID of the external role to filter by or 'all' for all roles
        """
        import logging
        logger = logging.getLogger('AssetPolicyInference')
        
        column_name = entry.get('column_name')
        data_element_id = entry.get('data_element_id')
        data_element_name = entry.get('data_element_name')
        
        logger.info(f"[SECURITY] Processing security policies for column {column_name} (data element: {data_element_name})")
        logger.debug(f"[SECURITY] Parameters: purpose_id={purpose_id}, purpose_name={purpose_name}, role_id={role_id}")
        
        # Get policy purpose data security for this data element
        policy_purpose_data_securities = self.regulatory_metadata_repository.get_policy_purpose_data_security(
            data_element_id=data_element_id,
            purpose_id=purpose_id
        )
        
        # Check if there are any security policies for this data element and purpose
        if not policy_purpose_data_securities:
            logger.info(f"[SECURITY] No security policies found for data element {data_element_name} and purpose {purpose_name}")
            return
            
        logger.info(f"[SECURITY] Found {len(policy_purpose_data_securities)} security policies for data element {data_element_name}")
            
        # If no security policies found at all, return early
        if not policy_purpose_data_securities:
            return
        
        # Get policy overrides for this data element and purpose
        # We'll check for role-specific overrides if a role_id is specified
        if role_id != 'all':
            # Get the specific role
            roles = self.glossary_repository.get_external_roles()
            filtered_roles = [role for role in roles if role[0] == role_id]
            if not filtered_roles:
                logger.warning(f"[SECURITY] Role ID {role_id} not found, no security policies will be processed")
                return
            roles = filtered_roles
            logger.info(f"[SECURITY] Filtering for role: {roles[0][1]} (ID: {role_id})")
        else:
            # Get all roles
            roles = self.glossary_repository.get_external_roles()
            logger.info(f"[SECURITY] Processing all roles ({len(roles)} roles)")
        
        # Track if we have any overrides for this data element
        has_overrides = False
        
        # Check each role for overrides
        for role in roles:
            current_role_id = role[0]
            role_name = role[1]
            
            logger.debug(f"[SECURITY] Checking role: {role_name} (ID: {current_role_id})")
            
            # For each policy purpose data security entry
            for security in policy_purpose_data_securities:
                # Get the policy purpose data element ID
                policy_purpose_data_element_id = self._get_policy_purpose_data_element_id(
                    security.get('policy_name'),
                    purpose_id,
                    entry.get('data_element_id')
                )
                
                if not policy_purpose_data_element_id:
                    continue
                
                # Check for overrides
                overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_security(
                    policy_purpose_data_element_id=policy_purpose_data_element_id,
                    external_role_id=current_role_id
                )
                
                logger.debug(f"[SECURITY] Checking overrides for role {role_name} (ID: {current_role_id})")
                
                # If we have overrides, use those values
                if overrides:
                    has_overrides = True
                    override = overrides[0]
                    
                    # Handle Default Role Assignment purpose for encryption settings
                    encryption_required = override.get('encryption_required')
                    encryption_algorithm = override.get('encryption_algorithm')
                    
                    # If this is not the Default Role Assignment purpose, get encryption settings from there
                    if purpose_name != "Default Role Assignment":
                        default_purpose_id = self._get_purpose_id_by_name("Default Role Assignment")
                        if default_purpose_id:
                            default_securities = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                                data_element_id=entry.get('data_element_id'),
                                purpose_id=default_purpose_id
                            )
                            
                            if default_securities:
                                encryption_required = default_securities[0].get('encryption_required')
                                encryption_algorithm = default_securities[0].get('encryption_algorithm')
                    
                    # Add to results
                    results.append({
                        'schema_name': entry.get('schema_name'),
                        'table_name': entry.get('table_name'),
                        'column_name': entry.get('column_name'),
                        'data_type': entry.get('data_type'),
                        'data_element_name': entry.get('data_element_name'),
                        'purpose_name': purpose_name,
                        'role_name': role_name,
                        'role_id': current_role_id,
                        'policy_name': security.get('policy_name'),
                        'policy_type': 'Security',
                        'encryption_required': encryption_required,
                        'encryption_algorithm': encryption_algorithm,
                        'masking_required': override.get('masking_required'),
                        'masking_format': override.get('masking_format'),
                        'is_override': True
                    })
        
        # If no overrides were found, add the default policy for each security policy
        if not has_overrides:
            for security in policy_purpose_data_securities:
                # Handle Default Role Assignment purpose for encryption settings
                encryption_required = security.get('encryption_required')
                encryption_algorithm = security.get('encryption_algorithm')
                
                # If this is not the Default Role Assignment purpose, get encryption settings from there
                if purpose_name != "Default Role Assignment":
                    default_purpose_id = self._get_purpose_id_by_name("Default Role Assignment")
                    if default_purpose_id:
                        default_securities = self.regulatory_metadata_repository.get_policy_purpose_data_security(
                            data_element_id=entry.get('data_element_id'),
                            purpose_id=default_purpose_id
                        )
                        
                        if default_securities:
                            encryption_required = default_securities[0].get('encryption_required')
                            encryption_algorithm = default_securities[0].get('encryption_algorithm')
                
                # Get all external roles from the glossary repository
                external_roles = self.glossary_repository.get_external_roles()
                
                # Filter roles if role_id is specified
                if role_id != 'all':
                    # Convert role_id to a list if it's not already
                    role_id_list = role_id if isinstance(role_id, list) else [role_id]
                    
                    # Filter out 'all' from the list if present
                    if 'all' in role_id_list:
                        logger.info(f"[SECURITY] 'all' found in role_id list, using all roles")
                    else:
                        # Filter roles by ID
                        logger.info(f"[SECURITY] Filtering roles by ID: {role_id_list}")
                        external_roles = [role for role in external_roles if role[0] in role_id_list]
                        logger.info(f"[SECURITY] Found {len(external_roles)} matching roles")
                
                if external_roles:
                    # Add an entry for each role
                    for role in external_roles:
                        role_id_val = role[0]  # external_role_id
                        role_name_val = role[1]  # role_name
                        
                        logger.info(f"[SECURITY] Adding policy for purpose {purpose_name} with role {role_name_val}")
                        
                        # Add to results
                        results.append({
                            'schema_name': entry.get('schema_name'),
                            'table_name': entry.get('table_name'),
                            'column_name': entry.get('column_name'),
                            'data_type': entry.get('data_type'),
                            'data_element_name': entry.get('data_element_name'),
                            'purpose_name': purpose_name,
                            'role_name': role_name_val,
                            'role_id': role_id_val,  # Add role_id to the results for easier filtering
                            'policy_name': security.get('policy_name'),
                            'policy_type': 'Security',
                            'encryption_required': encryption_required,
                            'encryption_algorithm': encryption_algorithm,
                            'masking_required': security.get('masking_required'),
                            'masking_format': security.get('masking_format'),
                            'is_override': False
                        })
                else:
                    # If no roles are found, use a placeholder
                    logger.warning(f"[SECURITY] No roles found in the system. Using placeholder.")
                    
                    # Add to results with a placeholder role
                    results.append({
                        'schema_name': entry.get('schema_name'),
                        'table_name': entry.get('table_name'),
                        'column_name': entry.get('column_name'),
                        'data_type': entry.get('data_type'),
                        'data_element_name': entry.get('data_element_name'),
                        'purpose_name': purpose_name,
                        'role_name': f"Unassigned ({purpose_name})",
                        'policy_name': security.get('policy_name'),
                        'policy_type': 'Security',
                        'encryption_required': encryption_required,
                        'encryption_algorithm': encryption_algorithm,
                        'masking_required': security.get('masking_required'),
                        'masking_format': security.get('masking_format'),
                        'is_override': False
                    })
    
    def _process_usage_policies(self, entry, purpose_id, purpose_name, results, role_id='all'):
        """
        Process usage policies for a catalog entry and add them to results.
        
        Args:
            entry: Catalog entry (table column)
            purpose_id: ID of the purpose
            purpose_name: Name of the purpose
            results: List to append results to
            role_id: ID of the external role to filter by or 'all' for all roles
        """
        import logging
        logger = logging.getLogger('AssetPolicyInference')
        
        column_name = entry.get('column_name')
        data_element_id = entry.get('data_element_id')
        data_element_name = entry.get('data_element_name')
        
        logger.info(f"[USAGE] Processing usage policies for column {column_name} (data element: {data_element_name})")
        logger.debug(f"[USAGE] Parameters: purpose_id={purpose_id}, purpose_name={purpose_name}, role_id={role_id}")
        
        # Get policy purpose data usage for this data element
        policy_purpose_data_usages = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
            data_element_id=data_element_id,
            purpose_id=purpose_id
        )
        
        # Check if there are any usage policies for this data element and purpose
        if not policy_purpose_data_usages:
            logger.info(f"[USAGE] No usage policies found for data element {data_element_name} and purpose {purpose_name}")
            return
        
        logger.info(f"[USAGE] Found {len(policy_purpose_data_usages)} usage policies for data element {data_element_name}")
            
        # We'll filter by role after processing the policies
        
        # If no usage policies found at all, return early
        if not policy_purpose_data_usages:
            return
            
        # Get all external roles from the glossary repository
        roles = self.glossary_repository.get_external_roles()
        
        # Filter roles if role_id is specified
        if role_id != 'all':
            # Convert role_id to a list if it's not already
            role_id_list = role_id if isinstance(role_id, list) else [role_id]
            
            # Filter out 'all' from the list if present
            if 'all' in role_id_list:
                logger.info(f"[USAGE] 'all' found in role_id list, using all roles")
            else:
                # Filter roles by ID
                logger.info(f"[USAGE] Filtering roles by ID: {role_id_list}")
                roles = [role for role in roles if role[0] in role_id_list]
                logger.info(f"[USAGE] Found {len(roles)} matching roles")
                
                if not roles:
                    logger.warning(f"[USAGE] No roles found matching {role_id_list}, no usage policies will be processed")
                    return
        
        # Track if we have any overrides for this data element
        has_overrides = {}  # Track by operation
        
        # Check each role for overrides
        for role in roles:
            current_role_id = role[0]
            role_name = role[1]
            
            logger.debug(f"[USAGE] Checking role: {role_name} (ID: {current_role_id})")
            
            # For each policy purpose data usage entry
            for usage in policy_purpose_data_usages:
                # Get the policy purpose data element ID
                policy_purpose_data_element_id = self._get_policy_purpose_data_element_id(
                    usage.get('policy_name'),
                    purpose_id,
                    entry.get('data_element_id')
                )
                
                if not policy_purpose_data_element_id:
                    continue
                
                # Check for overrides for each operation
                operation = usage.get('operation')
                
                # Check for overrides
                overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_usages(
                    policy_purpose_data_element_id=policy_purpose_data_element_id,
                    external_role_id=current_role_id
                )
                
                logger.debug(f"[USAGE] Checking overrides for role {role_name} (ID: {current_role_id})")
                
                # Filter overrides by operation
                operation_overrides = [o for o in overrides if o.get('operation') == operation]
                
                # If we have overrides for this operation, use those values
                if operation_overrides:
                    if operation not in has_overrides:
                        has_overrides[operation] = True
                    
                    override = operation_overrides[0]
                    
                    # Add to results
                    results.append({
                        'schema_name': entry.get('schema_name'),
                        'table_name': entry.get('table_name'),
                        'column_name': entry.get('column_name'),
                        'data_type': entry.get('data_type'),
                        'data_element_name': entry.get('data_element_name'),
                        'purpose_name': purpose_name,
                        'role_name': role_name,
                        'role_id': current_role_id,
                        'policy_name': usage.get('policy_name'),
                        'policy_type': 'Usage',
                        'operation': operation,
                        'allowed': override.get('allowed'),
                        'restrictions': override.get('restrictions'),
                        'is_override': True
                    })
        
        # For operations without overrides, add the default policy
        for usage in policy_purpose_data_usages:
            operation = usage.get('operation')
            if operation not in has_overrides:
                # Add to results
                results.append({
                    'schema_name': entry.get('schema_name'),
                    'table_name': entry.get('table_name'),
                    'column_name': entry.get('column_name'),
                    'data_type': entry.get('data_type'),
                    'data_element_name': entry.get('data_element_name'),
                    'purpose_name': purpose_name,
                    'role_name': 'Default Role',
                    'role_id': 'default',
                    'policy_name': usage.get('policy_name'),
                    'policy_type': 'Usage',
                    'operation': operation,
                    'allowed': usage.get('allowed'),
                    'restrictions': usage.get('restrictions'),
                    'is_override': False
                })
    
    def _process_retention_policies(self, entry, purpose_id, purpose_name, results, role_id='all'):
        """
        Process retention policies for a catalog entry and add them to results.
        
        Args:
            entry: Catalog entry (table column)
            purpose_id: ID of the purpose
            purpose_name: Name of the purpose
            results: List to append results to
            role_id: ID of the external role to filter by or 'all' for all roles
        """
        import logging
        logger = logging.getLogger('AssetPolicyInference')
        
        logger.info(f"[RETENTION] Processing retention policies for {entry.get('schema_name')}.{entry.get('table_name')}.{entry.get('column_name')}")
        logger.info(f"[RETENTION] Purpose: {purpose_name} (ID: {purpose_id}), Role ID: {role_id}")
        
        # Get all retention policies for this data element and purpose
        policy_purpose_data_retentions = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
            data_element_id=entry.get('data_element_id'),
            purpose_id=purpose_id
        )
        
        logger.info(f"[RETENTION] Found {len(policy_purpose_data_retentions)} retention policies for data element {entry.get('data_element_name')}")
        
        # If no retention policies found, return
        if not policy_purpose_data_retentions:
            logger.info(f"[RETENTION] No retention policies found for data element {entry.get('data_element_name')}")
            return
        
        # Get all external roles from the glossary repository
        roles = self.glossary_repository.get_external_roles()
        
        # Filter roles if role_id is specified
        if role_id != 'all':
            # Convert role_id to a list if it's not already
            role_id_list = role_id if isinstance(role_id, list) else [role_id]
            
            # Filter out 'all' from the list if present
            if 'all' in role_id_list:
                logger.info(f"[RETENTION] 'all' found in role_id list, using all roles")
            else:
                # Filter roles by ID
                logger.info(f"[RETENTION] Filtering roles by ID: {role_id_list}")
                roles = [role for role in roles if role[0] in role_id_list]
                logger.info(f"[RETENTION] Found {len(roles)} matching roles")
                
                if not roles:
                    logger.warning(f"[RETENTION] No roles found matching {role_id_list}, no retention policies will be processed")
                    return
        
        # Track if we have any overrides for this data element
        has_overrides = False
        
        # Check each role for overrides
        for role in roles:
            current_role_id = role[0]
            role_name = role[1]
            
            logger.debug(f"[RETENTION] Checking role: {role_name} (ID: {current_role_id})")
            
            # For each policy purpose data retention entry
            for retention in policy_purpose_data_retentions:
                # Get the policy purpose data element ID
                policy_purpose_data_element_id = self._get_policy_purpose_data_element_id(
                    retention.get('policy_name'),
                    purpose_id,
                    entry.get('data_element_id')
                )
                
                if not policy_purpose_data_element_id:
                    logger.debug(f"[RETENTION] No policy_purpose_data_element_id found for policy {retention.get('policy_name')}")
                    continue
                
                # Check for overrides
                overrides = self.regulatory_metadata_repository.get_policy_override_role_purpose_data_retentions(
                    policy_purpose_data_element_id=policy_purpose_data_element_id,
                    external_role_id=current_role_id
                )
                
                # If we have overrides, use those values
                if overrides:
                    has_overrides = True
                    override = overrides[0]
                    
                    logger.info(f"[RETENTION] Found override for role {role_name} and policy {retention.get('policy_name')}")
                    
                    # Add to results
                    results.append({
                        'schema_name': entry.get('schema_name'),
                        'table_name': entry.get('table_name'),
                        'column_name': entry.get('column_name'),
                        'data_type': entry.get('data_type'),
                        'data_element_name': entry.get('data_element_name'),
                        'purpose_name': purpose_name,
                        'role_name': role_name,
                        'role_id': current_role_id,
                        'policy_name': retention.get('policy_name'),
                        'policy_type': 'Retention',
                        'retention_period': override.get('retention_period'),
                        'retention_basis': override.get('retention_basis'),
                        'is_override': True
                    })
                    logger.debug(f"[RETENTION] Added override retention policy for role {role_name}")
        
        # If no overrides were found, add the default policy for each retention policy
        if not has_overrides:
            logger.info(f"[RETENTION] No overrides found, using default retention policies")
            for retention in policy_purpose_data_retentions:
                # Add to results
                results.append({
                    'schema_name': entry.get('schema_name'),
                    'table_name': entry.get('table_name'),
                    'column_name': entry.get('column_name'),
                    'data_type': entry.get('data_type'),
                    'data_element_name': entry.get('data_element_name'),
                    'purpose_name': purpose_name,
                    'role_name': 'Default Role',
                    'role_id': 'default',
                    'policy_name': retention.get('policy_name'),
                    'policy_type': 'Retention',
                    'retention_period': retention.get('retention_period'),
                    'retention_basis': retention.get('retention_basis'),
                    'is_override': False
                })
                logger.debug(f"[RETENTION] Added default retention policy for policy {retention.get('policy_name')}")
    
    def _get_policy_purpose_data_element_id(self, policy_name, purpose_id, data_element_id):
        """
        Get the policy_purpose_data_element_id for a given policy, purpose, and data element.
        
        Args:
            policy_name: Name of the policy
            purpose_id: ID of the purpose
            data_element_id: ID of the data element
            
        Returns:
            ID of the policy_purpose_data_element entry, or None if not found
        """
        cursor = self.regulatory_metadata_repository.connection.cursor()
        try:
            query = """
            SELECT ppde.id
            FROM policy_purpose_data_element ppde
            JOIN policy p ON ppde.policy_id = p.id
            WHERE p.name = %s AND ppde.purpose_id = %s AND ppde.data_element_id = %s
            """
            cursor.execute(query, (policy_name, purpose_id, data_element_id))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting policy_purpose_data_element_id: {e}")
            return None
        finally:
            cursor.close()
    
    def _get_purpose_id_by_name(self, purpose_name):
        """
        Get the purpose ID for a given purpose name.
        
        Args:
            purpose_name: Name of the purpose
            
        Returns:
            ID of the purpose, or None if not found
        """
        purposes = self.glossary_repository.get_purposes()
        for purpose in purposes:
            if purpose['name'] == purpose_name:
                return purpose['id']
        return None
    
    def format_boolean_as_checkbox(self, df):
        """
        Format boolean columns in the DataFrame as checkboxes.
        
        Args:
            df: DataFrame to format
            
        Returns:
            Formatted DataFrame
        """
        # Create a copy to avoid modifying the original
        formatted_df = df.copy()
        
        # Format boolean columns
        boolean_columns = ['encryption_required', 'masking_required', 'is_override', 'allowed']
        for col in boolean_columns:
            if col in formatted_df.columns:
                formatted_df[col] = formatted_df[col].apply(
                    lambda val: "✅" if val is True else "❌" if val is False else val
                )
        
        return formatted_df
        
    def analyze_policies_for_asset(self, asset_id, purpose_id=None, policy_type='all', role_id='all'):
        """
        Analyze policies for an asset and return a structured JSON representation.
        This method uses the same data source as get_applied_policies_for_asset_purpose to ensure consistency.
        
        Args:
            asset_id: ID of the asset to analyze policies for
            purpose_id: ID of the purpose to filter by, or 'all' for all purposes, or a list of purpose IDs
            policy_type: Type of policy to filter by ('security', 'usage', 'retention', or 'all'), or a list of policy types
            role_id: ID of the external role to filter by, or 'all' for all roles, or a list of role IDs
            
        Returns:
            Dictionary containing policies grouped by table/column and purpose
        """
        # Call the column-based JSON generation method
        return self.generate_column_based_policy_json(asset_id, purpose_id, policy_type, role_id)

    def get_data_element_by_id(self, data_element_id):
        """
        Get data element details by ID.
        
        Args:
            data_element_id: The ID of the data element
            
        Returns:
            Dictionary containing data element details or None if not found
        """
        # Get all data elements from the glossary repository
        data_elements = self.glossary_repository.get_data_elements()
        
        # Find the data element with the matching ID
        for element in data_elements:
            if element.get('id') == data_element_id:
                return element
                
        return None
    
    def get_sensitivity_based_policies_for_asset(self, asset_id):
        """
        Get sensitivity-based policies for all data elements in an asset.
        
        Args:
            asset_id: ID of the asset
            
        Returns:
            DataFrame containing sensitivity-based policies for the asset's data elements
        """
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('AssetPolicyInference')
        
        logger.info(f"===== SENSITIVITY-BASED POLICY ANALYSIS STARTED =====")
        logger.info(f"Parameters: asset_id={asset_id}")
        print(f"===== SENSITIVITY-BASED POLICY ANALYSIS STARTED =====")
        print(f"Parameters: asset_id={asset_id}")
        
        # Get asset name for reference
        asset_name = None
        assets = self.inventory_repository.get_assets()
        for asset in assets:
            try:
                # Try dictionary access first
                if asset['id'] == asset_id:
                    asset_name = asset['name']
                    break
            except (TypeError, KeyError):
                # Fall back to tuple access if dictionary access fails
                try:
                    if isinstance(asset, tuple) and len(asset) >= 2 and asset[0] == asset_id:
                        asset_name = asset[1]  # Assuming second element is name
                        break
                except Exception as e:
                    logger.warning(f"Error accessing asset data: {e}")
                    continue
        logger.info(f"Asset: {asset_name} (ID: {asset_id})")
        
        # Get all catalog entries for the asset
        catalog_entries = self.catalog_repository.get_catalog_entries_by_asset(asset_id)
        logger.info(f"Retrieved {len(catalog_entries)} catalog entries for asset")
        
        # Initialize results list
        results = []
        
        # Process each catalog entry
        for entry in catalog_entries:
            # Skip entries without data elements
            if not entry.get('data_element_id'):
                logger.info(f"Skipping entry without data element ID")
                continue
                
            data_element_id = entry.get('data_element_id')
            logger.info(f"Processing data element ID: {data_element_id}")
            print(f"Processing data element ID: {data_element_id}")
            
            data_element = self.get_data_element_by_id(data_element_id)
            
            if not data_element:
                logger.info(f"Data element not found for ID: {data_element_id}")
                continue
                
            logger.info(f"Found data element: {data_element.get('name')}")
            print(f"Found data element: {data_element.get('name')}")
            
            # Get sensitivity-based policies for this data element
            sensitivity_result = self.infer_policies_by_data_element_sensitivity(data_element_id)
            
            # Skip if no sensitivity or policies found
            if not sensitivity_result['sensitivity'] or not sensitivity_result['policies']:
                logger.info(f"No sensitivity or policies found for data element: {data_element.get('name')}")
                continue
                
            sensitivity_name = sensitivity_result['sensitivity'].get('name', 'Unknown')
            logger.info(f"Sensitivity: {sensitivity_name}")
            print(f"Sensitivity: {sensitivity_name}")
            
            # Log the number of policies found
            logger.info(f"Found {len(sensitivity_result['policies'])} policies for data element: {data_element.get('name')}")
            print(f"Found {len(sensitivity_result['policies'])} policies for data element: {data_element.get('name')}")
            
            # Log the first policy's keys to see what fields are available
            if sensitivity_result['policies']:
                first_policy = sensitivity_result['policies'][0]
                logger.info(f"First policy keys: {list(first_policy.keys())}")
                print(f"First policy keys: {list(first_policy.keys())}")
            
            # Add each policy to results
            for policy in sensitivity_result['policies']:
                result = {
                    'schema_name': entry.get('schema_name', ''),
                    'table_name': entry.get('table_name', ''),
                    'column_name': entry.get('column_name', ''),
                    'data_type': entry.get('data_type', ''),
                    'data_element_name': data_element.get('name', ''),
                    'sensitivity': sensitivity_name,
                    'policy_name': policy.get('name', ''),
                    'policy_type': policy.get('policy_type', '')
                }
                
                # Add security policy details
                logger.info(f"Checking for security policy details in policy: {policy.get('name')}")
                print(f"Checking for security policy details in policy: {policy.get('name')}")
                if 'requires_encryption' in policy:
                    logger.info(f"Found security details: encryption={policy.get('requires_encryption')}, masking={policy.get('requires_masking')}")
                    print(f"Found security details: encryption={policy.get('requires_encryption')}, masking={policy.get('requires_masking')}")
                    result['encryption_required'] = policy.get('requires_encryption', False)
                    result['encryption_algorithm'] = policy.get('encryption_algorithm', '')
                    result['masking_required'] = policy.get('requires_masking', False)
                    result['masking_format'] = policy.get('masking_format', '')
                    result['access_control_required'] = policy.get('requires_access_control', False)
                    result['access_control_type'] = policy.get('access_control_type', '')
                else:
                    logger.info(f"No security details found in policy")
                    print(f"No security details found in policy")
                
                # Add usage policy details
                logger.info(f"Checking for usage policy details")
                print(f"Checking for usage policy details")
                if 'usage_operations' in policy:
                    logger.info(f"Found usage details: operations={policy.get('usage_operations')}, allowed={policy.get('usage_allowed')}")
                    print(f"Found usage details: operations={policy.get('usage_operations')}, allowed={policy.get('usage_allowed')}")
                    result['usage_operations'] = policy.get('usage_operations', '')
                    result['usage_allowed'] = policy.get('usage_allowed', '')
                else:
                    logger.info(f"No usage details found in policy")
                    print(f"No usage details found in policy")
                
                # Add retention policy details
                logger.info(f"Checking for retention policy details")
                print(f"Checking for retention policy details")
                if 'retention_period' in policy:
                    logger.info(f"Found retention details: period={policy.get('retention_period')}, basis={policy.get('retention_basis')}")
                    print(f"Found retention details: period={policy.get('retention_period')}, basis={policy.get('retention_basis')}")
                    result['retention_period'] = policy.get('retention_period', '')
                    result['retention_basis'] = policy.get('retention_basis', '')
                else:
                    logger.info(f"No retention details found in policy")
                    print(f"No retention details found in policy")
                
                results.append(result)
        
        # Create a DataFrame from the results
        if results:
            df = pd.DataFrame(results)
            logger.info(f"Created DataFrame with {len(df)} rows")
            logger.info(f"===== SENSITIVITY-BASED POLICY ANALYSIS COMPLETED =====")
            return df
        else:
            logger.info("No sensitivity-based policies found")
            logger.info(f"===== SENSITIVITY-BASED POLICY ANALYSIS COMPLETED =====")
            return pd.DataFrame()
    
    def infer_policies_by_data_element_sensitivity(self, data_element_id):
        """
        Infer policies for a data element based on its sensitivity level.
        
        Args:
            data_element_id: The ID of the data element
            
        Returns:
            Dictionary containing inferred policies and sensitivity information
        """
        # Get the data element details
        data_element = self.get_data_element_by_id(data_element_id)
        if not data_element:
            return {
                "data_element_id": data_element_id,
                "sensitivity": None,
                "policies": []
            }
        
        # Use sensitivity inference to get the sensitivity
        sensitivities = self.sensitivity_inference.infer_data_element_sensitivities([data_element])
        if data_element['name'] not in sensitivities:
            return {
                "data_element_id": data_element_id,
                "sensitivity": None,
                "policies": []
            }
        
        sensitivity_info = sensitivities[data_element['name']]
        sensitivity_name = sensitivity_info['sensitivity']
        
        # If sensitivity is unknown, return empty result
        if sensitivity_name == 'Unknown':
            return {
                "data_element_id": data_element_id,
                "sensitivity": {
                    "name": "Unknown",
                    "source": sensitivity_info['source']
                },
                "policies": []
            }
        
        # Get sensitivity details
        sensitivity = self.regulatory_metadata_repository.get_sensitivity_by_name(sensitivity_name)
        if not sensitivity:
            return {
                "data_element_id": data_element_id,
                "sensitivity": {
                    "name": sensitivity_name,
                    "source": sensitivity_info['source']
                },
                "policies": []
            }
        
        # Add source information to sensitivity
        sensitivity["source"] = sensitivity_info['source']
        
        # Get basic policies for this sensitivity
        basic_policies = self.regulatory_metadata_repository.get_policies_by_sensitivity(sensitivity["id"])
        
        # Enhance policies with security, usage, and retention details
        enhanced_policies = []
        for policy in basic_policies:
            policy_id = policy['id']
            enhanced_policy = dict(policy)
            
            # Get security policies for this data element
            security_policies = self.regulatory_metadata_repository.get_policy_data_element_security(
                policy_id=policy_id, data_element_id=data_element_id)
            
            # Get usage policies for this data element
            usage_policies = self.regulatory_metadata_repository.get_policy_data_element_usage(
                policy_id=policy_id, data_element_id=data_element_id)
            
            # Get retention policies for this data element
            retention_policies = self.regulatory_metadata_repository.get_policy_data_element_retention(
                policy_id=policy_id, data_element_id=data_element_id)
            
            # Add security details
            if security_policies:
                enhanced_policy['requires_encryption'] = any(p['requires_encryption'] for p in security_policies)
                encryption_algos = [p['encryption_algorithm'] for p in security_policies if p['encryption_algorithm']]
                enhanced_policy['encryption_algorithm'] = encryption_algos[0] if encryption_algos else None
                
                enhanced_policy['requires_masking'] = any(p['requires_masking'] for p in security_policies)
                masking_formats = [p['masking_format'] for p in security_policies if p['masking_format']]
                enhanced_policy['masking_format'] = masking_formats[0] if masking_formats else None
                
                enhanced_policy['requires_access_control'] = any(p['requires_access_control'] for p in security_policies)
                access_types = [p['access_control_type'] for p in security_policies if p['access_control_type']]
                enhanced_policy['access_control_type'] = access_types[0] if access_types else None
            
            # Add usage details
            if usage_policies:
                operations = [p['operation'] for p in usage_policies]
                allowed = [p['allowed'] for p in usage_policies]
                enhanced_policy['usage_operations'] = ', '.join(operations)
                enhanced_policy['usage_allowed'] = 'Yes' if all(allowed) else 'No' if not any(allowed) else 'Partial'
            
            # Add retention details
            if retention_policies:
                retention_periods = [p['retention_period'] for p in retention_policies if p['retention_period']]
                enhanced_policy['retention_period'] = retention_periods[0] if retention_periods else None
                
                retention_bases = [p['retention_basis'] for p in retention_policies if p['retention_basis']]
                enhanced_policy['retention_basis'] = retention_bases[0] if retention_bases else None
            
            enhanced_policies.append(enhanced_policy)
        
        return {
            "data_element_id": data_element_id,
            "sensitivity": sensitivity,
            "policies": enhanced_policies
        }
        
    def infer_policies_by_jurisdiction_data_subject_type_data_element(self, data_element_id, jurisdiction_id, data_subject_type_id):
        """
        Infer policies for a data element based on jurisdiction, data subject type, and sensitivity level.
        
        Args:
            data_element_id: The ID of the data element
            jurisdiction_id: The ID of the jurisdiction
            data_subject_type_id: The ID of the data subject type
            
        Returns:
            Dictionary containing inferred policies and sensitivity information
        """
        # Get the data element details
        data_element = self.get_data_element_by_id(data_element_id)
        if not data_element:
            return {
                "data_element_id": data_element_id,
                "jurisdiction_id": jurisdiction_id,
                "data_subject_type_id": data_subject_type_id,
                "sensitivity": None,
                "policies": []
            }
        
        # Use sensitivity inference to get the sensitivity based on jurisdiction and data subject type
        data_elements = [data_element]
        sensitivities = self.sensitivity_inference.infer_jurisdiction_data_subject_type_data_element_sensitivities(
            data_elements, jurisdiction_id, data_subject_type_id
        )
        
        if data_element['name'] not in sensitivities:
            return {
                "data_element_id": data_element_id,
                "jurisdiction_id": jurisdiction_id,
                "data_subject_type_id": data_subject_type_id,
                "sensitivity": None,
                "policies": []
            }
        
        sensitivity_info = sensitivities[data_element['name']]
        sensitivity_name = sensitivity_info['sensitivity']
        
        # If sensitivity is unknown, return empty result
        if sensitivity_name == 'Unknown':
            return {
                "data_element_id": data_element_id,
                "jurisdiction_id": jurisdiction_id,
                "data_subject_type_id": data_subject_type_id,
                "sensitivity": {
                    "name": "Unknown",
                    "source": sensitivity_info['source']
                },
                "policies": []
            }
        
        # Get sensitivity details
        sensitivity = self.regulatory_metadata_repository.get_sensitivity_by_name(sensitivity_name)
        if not sensitivity:
            return {
                "data_element_id": data_element_id,
                "jurisdiction_id": jurisdiction_id,
                "data_subject_type_id": data_subject_type_id,
                "sensitivity": {
                    "name": sensitivity_name,
                    "source": sensitivity_info['source']
                },
                "policies": []
            }
        
        # Add source information to sensitivity
        sensitivity["source"] = sensitivity_info['source']
        sensitivity["jurisdiction_id"] = jurisdiction_id
        sensitivity["data_subject_type_id"] = data_subject_type_id
        
        # Get basic policies for this sensitivity
        basic_policies = self.regulatory_metadata_repository.get_policies_by_sensitivity(sensitivity["id"])
        
        # Enhance policies with security, usage, and retention details
        enhanced_policies = []
        for policy in basic_policies:
            policy_id = policy['id']
            enhanced_policy = dict(policy)
            
            # Get security policies for this data element
            security_policies = self.regulatory_metadata_repository.get_policy_data_element_security(
                policy_id=policy_id, data_element_id=data_element_id)
            
            # Get usage policies for this data element
            usage_policies = self.regulatory_metadata_repository.get_policy_data_element_usage(
                policy_id=policy_id, data_element_id=data_element_id)
            
            # Get retention policies for this data element
            retention_policies = self.regulatory_metadata_repository.get_policy_data_element_retention(
                policy_id=policy_id, data_element_id=data_element_id)
            
            # Add security details
            if security_policies:
                enhanced_policy['requires_encryption'] = any(p['requires_encryption'] for p in security_policies)
                encryption_algos = [p['encryption_algorithm'] for p in security_policies if p['encryption_algorithm']]
                enhanced_policy['encryption_algorithm'] = encryption_algos[0] if encryption_algos else None
                
                enhanced_policy['requires_masking'] = any(p['requires_masking'] for p in security_policies)
                masking_formats = [p['masking_format'] for p in security_policies if p['masking_format']]
                enhanced_policy['masking_format'] = masking_formats[0] if masking_formats else None
                
                enhanced_policy['requires_access_control'] = any(p['requires_access_control'] for p in security_policies)
                access_types = [p['access_control_type'] for p in security_policies if p['access_control_type']]
                enhanced_policy['access_control_type'] = access_types[0] if access_types else None
            
            # Add usage details
            if usage_policies:
                operations = [p['operation'] for p in usage_policies]
                allowed = [p['allowed'] for p in usage_policies]
                enhanced_policy['usage_operations'] = ', '.join(operations)
                enhanced_policy['usage_allowed'] = 'Yes' if all(allowed) else 'No' if not any(allowed) else 'Partial'
            
            # Add retention details
            if retention_policies:
                retention_periods = [p['retention_period'] for p in retention_policies if p['retention_period']]
                enhanced_policy['retention_period'] = retention_periods[0] if retention_periods else None
                
                retention_bases = [p['retention_basis'] for p in retention_policies if p['retention_basis']]
                enhanced_policy['retention_basis'] = retention_bases[0] if retention_bases else None
            
            enhanced_policies.append(enhanced_policy)
        
        return {
            "data_element_id": data_element_id,
            "jurisdiction_id": jurisdiction_id,
            "data_subject_type_id": data_subject_type_id,
            "sensitivity": sensitivity,
            "policies": enhanced_policies
        }
    
    def get_policies_by_jurisdiction_data_subject_type_data_elements_sensitivity(self, data_element_ids, jurisdiction_id=None, data_subject_type_id=None):
        """
        Get sensitivity-based policies for a list of data elements, optionally filtered by jurisdiction and data subject type.
        
        Args:
            data_element_ids: List of data element IDs
            jurisdiction_id: Optional ID of the jurisdiction to consider
            data_subject_type_id: Optional ID of the data subject type to consider
            
        Returns:
            DataFrame containing sensitivity-based policies for the data elements
        """
        import logging
        import pandas as pd
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('AssetPolicyInference')
        
        logger.info(f"===== SENSITIVITY-BASED POLICY ANALYSIS FOR DATA ELEMENTS STARTED =====")
        logger.info(f"Parameters: data_element_ids={data_element_ids}, jurisdiction_id={jurisdiction_id}, data_subject_type_id={data_subject_type_id}")
        
        # Initialize results list
        results = []
        
        # Process each data element
        for data_element_id in data_element_ids:
            logger.info(f"Processing data element ID: {data_element_id}")
            
            data_element = self.get_data_element_by_id(data_element_id)
            
            if not data_element:
                logger.info(f"Data element not found for ID: {data_element_id}")
                continue
                
            logger.info(f"Found data element: {data_element.get('name')}")
            
            # Get sensitivity-based policies for this data element
            if jurisdiction_id and data_subject_type_id:
                # Use the jurisdiction and data subject type specific method
                sensitivity_result = self.infer_policies_by_jurisdiction_data_subject_type_data_element(
                    data_element_id, jurisdiction_id, data_subject_type_id
                )
                logger.info(f"Using jurisdiction and data subject type specific inference")
            else:
                # Use the standard method without jurisdiction and data subject type
                sensitivity_result = self.infer_policies_by_data_element_sensitivity(data_element_id)
                logger.info(f"Using standard sensitivity inference")
            
            # Skip if no sensitivity or policies found
            if not sensitivity_result['sensitivity'] or not sensitivity_result['policies']:
                logger.info(f"No sensitivity or policies found for data element: {data_element.get('name')}")
                continue
                
            sensitivity_name = sensitivity_result['sensitivity'].get('name', 'Unknown')
            logger.info(f"Sensitivity: {sensitivity_name}")
            
            # Add each policy to results
            for policy in sensitivity_result['policies']:
                result = {
                    'data_element_name': data_element.get('name', ''),
                    'sensitivity': sensitivity_name,
                    'policy_name': policy.get('name', ''),
                    'policy_type': policy.get('policy_type', '')
                }
                
                # Add jurisdiction and data subject type if provided
                if jurisdiction_id:
                    jurisdiction = self.glossary_repository.get_jurisdiction_by_id(jurisdiction_id)
                    result['jurisdiction_name'] = jurisdiction.get('name', '') if jurisdiction else ''
                    result['jurisdiction_id'] = jurisdiction_id
                
                if data_subject_type_id:
                    data_subject_type = self.glossary_repository.get_data_subject_type_by_id(data_subject_type_id)
                    result['data_subject_type_name'] = data_subject_type.get('name', '') if data_subject_type else ''
                    result['data_subject_type_id'] = data_subject_type_id
                
                # Add security policy details
                if 'requires_encryption' in policy:
                    result['encryption_required'] = policy.get('requires_encryption', False)
                    result['encryption_algorithm'] = policy.get('encryption_algorithm', '')
                    result['masking_required'] = policy.get('requires_masking', False)
                    result['masking_format'] = policy.get('masking_format', '')
                    result['access_control_required'] = policy.get('requires_access_control', False)
                    result['access_control_type'] = policy.get('access_control_type', '')
                
                # Add usage policy details
                if 'usage_operations' in policy:
                    result['usage_operations'] = policy.get('usage_operations', '')
                    result['usage_allowed'] = policy.get('usage_allowed', '')
                
                # Add retention policy details
                if 'retention_period' in policy:
                    result['retention_period'] = policy.get('retention_period', '')
                    result['retention_basis'] = policy.get('retention_basis', '')
                
                results.append(result)
        
        # Create a DataFrame from the results
        if results:
            df = pd.DataFrame(results)
            logger.info(f"Created DataFrame with {len(df)} rows")
            logger.info(f"===== SENSITIVITY-BASED POLICY ANALYSIS FOR DATA ELEMENTS COMPLETED =====")
            return df
        else:
            logger.info("No sensitivity-based policies found")
            logger.info(f"===== SENSITIVITY-BASED POLICY ANALYSIS FOR DATA ELEMENTS COMPLETED =====")
            return pd.DataFrame()
    
    # Keep the old method for backward compatibility, but have it call the new method
    def get_policies_by_data_elements_sensitivity(self, data_element_ids):
        """
        Get sensitivity-based policies for a list of data elements.
        This method is maintained for backward compatibility and calls the new method.
        
        Args:
            data_element_ids: List of data element IDs
            
        Returns:
            DataFrame containing sensitivity-based policies for the data elements
        """
        return self.get_policies_by_jurisdiction_data_subject_type_data_elements_sensitivity(data_element_ids)
            
    def get_policies_by_data_elements_purpose(self, data_element_ids, purpose_id, policy_type='all', role_id='all'):
        """
        Get purpose-based policies for a list of data elements.
        
        Args:
            data_element_ids: List of data element IDs
            purpose_id: ID of the purpose, 'all' for all purposes, or a list of purpose IDs
            policy_type: Type of policy to filter by ('security', 'usage', 'retention', or 'all'), or a list of policy types
            role_id: ID of the external role to filter by, 'all' for all roles, or a list of role IDs
            
        Returns:
            DataFrame containing filtered policies applied to the data elements
        """
        import logging
        import pandas as pd
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('AssetPolicyInference')
        
        logger.info(f"===== PURPOSE-BASED POLICY ANALYSIS FOR DATA ELEMENTS STARTED =====")
        logger.info(f"Parameters: data_element_ids={data_element_ids}, purpose_id={purpose_id}, policy_type={policy_type}, role_id={role_id}")
        
        # Initialize results list
        results = []
        
        # Handle purpose_id parameter (could be 'all', a single ID, or a list of IDs)
        if isinstance(purpose_id, list):
            if 'all' in purpose_id:
                logger.info("Processing ALL purposes (from list containing 'all')")
                purpose_id = 'all'
            else:
                logger.info(f"Processing multiple purposes: {purpose_id}")
        
        # Handle policy_type parameter (could be 'all', a single type, or a list of types)
        if isinstance(policy_type, list):
            if 'all' in policy_type:
                logger.info("Processing ALL policy types (from list containing 'all')")
                policy_type = 'all'
            else:
                logger.info(f"Processing multiple policy types: {policy_type}")
        
        # Handle role_id parameter (could be 'all', a single ID, or a list of IDs)
        if isinstance(role_id, list):
            if 'all' in role_id:
                logger.info("Processing ALL roles (from list containing 'all')")
                role_id = 'all'
            else:
                logger.info(f"Processing multiple roles: {role_id}")
        
        # Process each data element
        for data_element_id in data_element_ids:
            data_element = self.get_data_element_by_id(data_element_id)
            if not data_element:
                logger.info(f"Data element not found for ID: {data_element_id}")
                continue
                
            logger.info(f"Processing data element: {data_element.get('name')} (ID: {data_element_id})")
            
            # Handle purposes (either 'all', a single ID, or a list of IDs)
            if purpose_id == 'all':
                logger.info("Processing ALL purposes")
                # Get all purposes
                purposes = self.glossary_repository.get_purposes()
                logger.info(f"Retrieved {len(purposes)} purposes to process")
                
                # Process each purpose for this data element
                for purpose in purposes:
                    current_purpose_id = purpose["id"]
                    current_purpose_name = purpose["name"]
                    logger.info(f"Processing purpose: {current_purpose_name} (ID: {current_purpose_id})")
                    
                    # Process each policy type
                    self._process_purpose_data_element(data_element, current_purpose_id, current_purpose_name, policy_type, role_id, results, logger)
            elif isinstance(purpose_id, list):
                # Process multiple specific purposes
                logger.info(f"Processing {len(purpose_id)} specific purposes")
                purposes = self.glossary_repository.get_purposes()
                filtered_purposes = [p for p in purposes if p["id"] in purpose_id]
                logger.info(f"Found {len(filtered_purposes)} matching purposes")
                
                # Process each purpose in the list for this data element
                for purpose in filtered_purposes:
                    current_purpose_id = purpose["id"]
                    current_purpose_name = purpose["name"]
                    logger.info(f"Processing purpose: {current_purpose_name} (ID: {current_purpose_id})")
                    
                    # Process each policy type
                    self._process_purpose_data_element(data_element, current_purpose_id, current_purpose_name, policy_type, role_id, results, logger)
            else:
                # Process a single specific purpose
                current_purpose_id = purpose_id
                purposes = self.glossary_repository.get_purposes()
                purpose_obj = next((p for p in purposes if p["id"] == current_purpose_id), None)
                if not purpose_obj:
                    logger.warning(f"Purpose not found for ID: {current_purpose_id}")
                    continue
                    
                current_purpose_name = purpose_obj["name"]
                logger.info(f"Processing purpose: {current_purpose_name} (ID: {current_purpose_id})")
                
                # Process each policy type
                self._process_purpose_data_element(data_element, current_purpose_id, current_purpose_name, policy_type, role_id, results, logger)
        
        # Create a DataFrame from the results
        if results:
            df = pd.DataFrame(results)
            logger.info(f"Created DataFrame with {len(df)} rows")
            logger.info(f"===== PURPOSE-BASED POLICY ANALYSIS FOR DATA ELEMENTS COMPLETED =====")
            return df
        else:
            logger.info("No purpose-based policies found")
            logger.info(f"===== PURPOSE-BASED POLICY ANALYSIS FOR DATA ELEMENTS COMPLETED =====")
            return pd.DataFrame()
    
    def _process_purpose_data_element(self, data_element, purpose_id, purpose_name, policy_type, role_id, results, logger):
        """
        Helper method to process a data element for a specific purpose.
        """
        # Process security policies
        if policy_type == 'all' or policy_type == 'security' or (isinstance(policy_type, list) and 'security' in policy_type):
            logger.info(f"Processing security policies for data element: {data_element.get('name')} and purpose: {purpose_name}")
            self._process_security_policies_for_data_element(data_element, purpose_id, purpose_name, results, role_id)
        
        # Process usage policies
        if policy_type == 'all' or policy_type == 'usage' or (isinstance(policy_type, list) and 'usage' in policy_type):
            logger.info(f"Processing usage policies for data element: {data_element.get('name')} and purpose: {purpose_name}")
            self._process_usage_policies_for_data_element(data_element, purpose_id, purpose_name, results, role_id)
        
        # Process retention policies
        if policy_type == 'all' or policy_type == 'retention' or (isinstance(policy_type, list) and 'retention' in policy_type):
            logger.info(f"Processing retention policies for data element: {data_element.get('name')} and purpose: {purpose_name}")
            self._process_retention_policies_for_data_element(data_element, purpose_id, purpose_name, results, role_id)
    
    def _process_security_policies_for_data_element(self, data_element, purpose_id, purpose_name, results, role_id='all'):
        """
        Process security policies for a data element and add them to results.
        """
        # Get policy-purpose-data-element entries for this purpose
        ppde_entries = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
            purpose_id=purpose_id)
        
        # Filter entries for the current data element
        data_element_id = data_element['id']
        filtered_entries = [entry for entry in ppde_entries if entry.get('data_element_id') == data_element_id]
        
        for ppde in filtered_entries:
            # Get security policy details for this policy
            policy_id = ppde.get('policy_id')
            if not policy_id:
                continue
                
            security_details = self.regulatory_metadata_repository.get_policy_security_details(policy_id)
            if not security_details:
                continue
                
            # Skip if no security policy details
            if not security_details.get('encryption_required') and not security_details.get('masking_required'):
                continue
                
            # Get policy details
            policy = self.glossary_repository.get_policy_by_id(ppde['policy_id'])
            if not policy:
                continue
                
            # Check role filter
            if role_id != 'all':
                # Get roles for this purpose
                purpose_roles = self.policy_repository.get_purpose_roles_by_purpose(purpose_id)
                purpose_role_ids = [pr[0] for pr in purpose_roles]
                
                # Skip if role filter doesn't match
                if isinstance(role_id, list):
                    if not any(r in purpose_role_ids for r in role_id):
                        continue
                elif role_id not in purpose_role_ids:
                    continue
            
            # Get role information
            role_name = None
            role_id_value = None
            if purpose_id:
                purpose_roles = self.policy_repository.get_purpose_roles_by_purpose(purpose_id)
                if purpose_roles:
                    role_id_value = purpose_roles[0][0]  # Use the first role associated with this purpose
                    role_name = purpose_roles[0][1]  # Assuming the second element is the role name
            
            # Add to results
            results.append({
                'data_element_name': data_element.get('name', ''),
                'purpose_name': purpose_name,
                'policy_name': policy.get('name', ''),
                'policy_type': 'security',
                'role_name': role_name,
                'encryption_required': security_details.get('encryption_required', False),
                'encryption_algorithm': security_details.get('encryption_algorithm', ''),
                'masking_required': security_details.get('masking_required', False),
                'masking_format': security_details.get('masking_format', '')
            })
    
    def _process_usage_policies_for_data_element(self, data_element, purpose_id, purpose_name, results, role_id='all'):
        """
        Process usage policies for a data element and add them to results.
        """
        # Get policy-purpose-data-element entries for this purpose
        ppde_entries = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
            purpose_id=purpose_id)
        
        # Filter entries for the current data element
        data_element_id = data_element['id']
        filtered_entries = [entry for entry in ppde_entries if entry.get('data_element_id') == data_element_id]
        
        for ppde in filtered_entries:
            # Get usage policies for this policy and data element
            policy_id = ppde.get('policy_id')
            if not policy_id:
                continue
                
            usage_policies = self.regulatory_metadata_repository.get_policy_purpose_data_usages(
                policy_id=policy_id, purpose_id=purpose_id, data_element_id=data_element_id)
            
            if not usage_policies:
                continue
                
            # Get policy details
            policy = self.glossary_repository.get_policy_by_id(ppde['policy_id'])
            if not policy:
                continue
                
            # Check role filter
            if role_id != 'all':
                # Get roles for this purpose
                purpose_roles = self.policy_repository.get_purpose_roles_by_purpose(purpose_id)
                purpose_role_ids = [pr[0] for pr in purpose_roles]
                
                # Skip if role filter doesn't match
                if isinstance(role_id, list):
                    if not any(r in purpose_role_ids for r in role_id):
                        continue
                elif role_id not in purpose_role_ids:
                    continue
            
            # Get role information
            role_name = None
            role_id_value = None
            if purpose_id:
                purpose_roles = self.policy_repository.get_purpose_roles_by_purpose(purpose_id)
                if purpose_roles:
                    role_id_value = purpose_roles[0][0]  # Use the first role associated with this purpose
                    role_name = purpose_roles[0][1]  # Assuming the second element is the role name
            
            # Add each usage policy to results
            for usage in usage_policies:
                results.append({
                    'data_element_name': data_element.get('name', ''),
                    'purpose_name': purpose_name,
                    'policy_name': policy.get('name', ''),
                    'policy_type': 'usage',
                    'role_name': role_name,
                    'operation': usage.get('operation', ''),
                    'allowed': usage.get('allowed', False),
                    'restrictions': usage.get('restrictions', '')
                })
    
    def _process_retention_policies_for_data_element(self, data_element, purpose_id, purpose_name, results, role_id='all'):
        """
        Process retention policies for a data element and add them to results.
        """
        # Get policy-purpose-data-element entries for this purpose
        ppde_entries = self.regulatory_metadata_repository.get_policy_purpose_data_elements(
            purpose_id=purpose_id)
        
        # Filter entries for the current data element
        data_element_id = data_element['id']
        filtered_entries = [entry for entry in ppde_entries if entry.get('data_element_id') == data_element_id]
        
        for ppde in filtered_entries:
            # Get retention policies for this policy and data element
            policy_id = ppde.get('policy_id')
            if not policy_id:
                continue
                
            retention_policies = self.regulatory_metadata_repository.get_policy_purpose_data_retentions(
                policy_id=policy_id, purpose_id=purpose_id, data_element_id=data_element_id)
            
            if not retention_policies:
                continue
                
            # Get policy details
            policy = self.glossary_repository.get_policy_by_id(ppde['policy_id'])
            if not policy:
                continue
                
            # Check role filter
            if role_id != 'all':
                # Get roles for this purpose
                purpose_roles = self.policy_repository.get_purpose_roles_by_purpose(purpose_id)
                purpose_role_ids = [pr[0] for pr in purpose_roles]
                
                # Skip if role filter doesn't match
                if isinstance(role_id, list):
                    if not any(r in purpose_role_ids for r in role_id):
                        continue
                elif role_id not in purpose_role_ids:
                    continue
            
            # Get role information
            role_name = None
            role_id_value = None
            if purpose_id:
                purpose_roles = self.policy_repository.get_purpose_roles_by_purpose(purpose_id)
                if purpose_roles:
                    role_id_value = purpose_roles[0][0]  # Use the first role associated with this purpose
                    role_name = purpose_roles[0][1]  # Assuming the second element is the role name
            
            # Add each retention policy to results
            for retention in retention_policies:
                results.append({
                    'data_element_name': data_element.get('name', ''),
                    'purpose_name': purpose_name,
                    'policy_name': policy.get('name', ''),
                    'policy_type': 'retention',
                    'role_name': role_name,
                    'retention_period': retention.get('retention_period', ''),
                    'retention_basis': retention.get('retention_basis', '')
                })

    
    def compare_purpose_and_sensitivity_policies(self, data_element_id):
        """
        Compare policies inferred from purpose-based approach vs. sensitivity-based approach.
        
        Args:
            data_element_id: The ID of the data element
            
        Returns:
            Dictionary containing both sets of policies and gap analysis
        """
        # Get policies from purpose-based approach
        purpose_policies = self.regulatory_metadata_repository.get_purpose_based_policies_for_data_element(data_element_id)
        
        # Get policies from sensitivity-based approach
        sensitivity_result = self.infer_policies_by_data_element_sensitivity(data_element_id)
        sensitivity_policies = sensitivity_result["policies"]
        
        # Identify gaps (policies in one approach but not the other)
        purpose_policy_ids = set(p["id"] for p in purpose_policies)
        sensitivity_policy_ids = set(p["id"] for p in sensitivity_policies)
        
        missing_in_purpose = [p for p in sensitivity_policies if p["id"] not in purpose_policy_ids]
        missing_in_sensitivity = [p for p in purpose_policies if p["id"] not in sensitivity_policy_ids]
        
        return {
            "data_element_id": data_element_id,
            "data_element_name": self.get_data_element_by_id(data_element_id)['name'] if self.get_data_element_by_id(data_element_id) else None,
            "sensitivity": sensitivity_result["sensitivity"],
            "purpose_policies": purpose_policies,
            "sensitivity_policies": sensitivity_policies,
            "gap_analysis": {
                "missing_in_purpose_approach": missing_in_purpose,
                "missing_in_sensitivity_approach": missing_in_sensitivity,
                "has_gaps": len(missing_in_purpose) > 0 or len(missing_in_sensitivity) > 0
            }
        }
        
    def generate_column_based_policy_json(self, asset_id, purpose_id=None, policy_type='all', role_id='all'):
        """
        Generate a column-based JSON structure for policy analysis.
        Policies are organized by table/column first, with roles and purposes nested under each column.
        
        Args:
            asset_id: ID of the asset to analyze policies for
            purpose_id: ID of the purpose to filter by, or 'all' for all purposes, or a list of purpose IDs
            policy_type: Type of policy to filter by ('security', 'usage', 'retention', or 'all'), or a list of policy types
            role_id: ID of the external role to filter by, or 'all' for all roles, or a list of role IDs
            
        Returns:
            Dictionary containing policies organized by table/column, role, and purpose
        """
        # This method is a complete rewrite to ensure all columns are processed correctly
        import logging
        logger = logging.getLogger('AssetPolicyInference')
        
        logger.info(f"===== POLICY JSON GENERATION STARTED =====")
        logger.info(f"Parameters: asset_id={asset_id}, purpose_id={purpose_id}, policy_type={policy_type}, role_id={role_id}")
        
        # First get the policy analysis results using the same method as the policy analysis display
        # This ensures consistency between the policy analysis display and the JSON generation
        df = self.get_applied_policies_for_asset_purpose(
            asset_id=asset_id,
            purpose_id=purpose_id,
            policy_type=policy_type,
            role_id=role_id
        )
        
        # Initialize the result dictionary
        result = {
            "asset_id": asset_id,
            "tables": {}
        }
        
        # Get asset name
        assets = self.inventory_repository.get_assets()
        for asset in assets:
            if asset['id'] == asset_id:
                result["asset_name"] = asset['name']
                break
        
        # If no policies found, return the basic structure
        if df.empty:
            logger.info(f"No policies found for asset_id={asset_id}, purpose_id={purpose_id}, policy_type={policy_type}, role_id={role_id}")
            logger.info(f"===== POLICY JSON GENERATION COMPLETED =====")
            return result
        
        # Get all catalog entries for the asset to ensure we include all columns
        catalog_entries = self.catalog_repository.get_catalog_entries_by_asset(asset_id)
        logger.info(f"Retrieved {len(catalog_entries)} catalog entries for asset")
        
        # First, create a complete structure with all columns from catalog entries
        # This ensures we include all columns, even if they don't have policies
        for entry in catalog_entries:
            schema_name = entry.get('schema_name')
            table_name = entry.get('table_name')
            column_name = entry.get('column_name')
            data_element_id = entry.get('data_element_id')
            data_element_name = entry.get('data_element_name')
            data_type = entry.get('data_type')
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Initialize table if not exists
            if table_key not in result["tables"]:
                result["tables"][table_key] = {
                    "schema": schema_name,
                    "table": table_name,
                    "columns": {}
                }
            
            # Initialize column if not exists for this table
            if column_name not in result["tables"][table_key]["columns"]:
                result["tables"][table_key]["columns"][column_name] = {
                    "data_element_id": data_element_id,
                    "data_element_name": data_element_name,
                    "data_type": data_type,
                    "roles": {}
                }
        
        # Now process the DataFrame to add policy information
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
                    "retention_basis": row.get('retention_basis')
                })
            
            logger.info(f"===== POLICY JSON GENERATION COMPLETED =====")
            return result
        
    def generate_policy_json_by_table_column(self, asset_id, purpose_id=None, policy_type='all', role_id='all'):
        """
        Generate JSON that specifies policies by table/column and purpose.
        
        Args:
            asset_id: ID of the asset to generate JSON for
            purpose_id: ID of the purpose to filter by, or 'all' for all purposes (default)
            policy_type: Type of policy to filter by ('security', 'usage', 'retention', or 'all')
            role_id: ID of the external role to filter by, or 'all' for all roles (default)
            
        Returns:
            Dictionary containing policies grouped by table/column and purpose
        """
        import logging
        logger = logging.getLogger('AssetPolicyInference')
        
        logger.info(f"===== POLICY JSON GENERATION STARTED =====")
        logger.info(f"Parameters: asset_id={asset_id}, purpose_id={purpose_id}, policy_type={policy_type}, role_id={role_id}")
        
        # Get the policy analysis results first
        df = self.get_applied_policies_for_asset_purpose(
            asset_id=asset_id,
            purpose_id=purpose_id,
            policy_type=policy_type,
            role_id=role_id
        )
        
        # Initialize the result dictionary
        result = {
            "asset_id": asset_id,
            "tables": {}
        }
        
        # Get asset name
        assets = self.inventory_repository.get_assets()
        for asset in assets:
            if asset['id'] == asset_id:
                result["asset_name"] = asset['name']
                break
        
        # If no policies found, return the basic structure
        if df.empty:
            logger.info(f"No policies found for asset_id={asset_id}, purpose_id={purpose_id}, policy_type={policy_type}, role_id={role_id}")
            logger.info(f"===== POLICY JSON GENERATION COMPLETED =====")
            return result
        
        # Get all roles for mapping
        roles = self.glossary_repository.get_external_roles()
        role_map = {role[0]: role[1] for role in roles}
        
        # Convert the DataFrame to a dictionary structure
        for _, row in df.iterrows():
            schema_name = row.get('schema_name')
            table_name = row.get('table_name')
            column_name = row.get('column_name')
            purpose_name = row.get('purpose_name')
            purpose_id_value = row.get('purpose_id')
            policy_type_name = row.get('policy_type').lower()
            
            # Create table key (schema.table)
            table_key = f"{schema_name}.{table_name}"
            
            # Initialize table if not exists
            if table_key not in result["tables"]:
                result["tables"][table_key] = {
                    "columns": {}
                }
            
            # Initialize column if not exists
            if column_name not in result["tables"][table_key]["columns"]:
                result["tables"][table_key]["columns"][column_name] = {
                    "data_element_id": row.get('data_element_id'),
                    "data_element_name": row.get('data_element_name'),
                    "data_type": row.get('data_type'),
                    "purposes": {}
                }
            
            # Initialize purpose if not exists
            if purpose_name not in result["tables"][table_key]["columns"][column_name]["purposes"]:
                result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name] = {}
                
                # Determine the appropriate role for this purpose
                # First try to get the role from the row if available
                role_id_value = row.get('role_id')
                role_name_value = row.get('role_name')
                
                # If not available in the row, look up the default role for this purpose
                if not role_id_value or not role_name_value:
                    # Get the default role for this purpose from the repository
                    purpose_roles = self.policy_repository.get_purpose_roles_by_purpose(purpose_id_value) if purpose_id_value else []
                    if purpose_roles:
                        role_id_value = purpose_roles[0][0]  # Use the first role associated with this purpose
                        role_name_value = role_map.get(role_id_value, "Unknown Role")
                    else:
                        # If no specific role found, use a default role
                        logger.info(f"No specific role found for purpose {purpose_name}, using default role")
                        role_id_value = "default_role"
                        role_name_value = "Default Role"
                
                # Always add role information to the purpose
                result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]["role"] = {
                    "id": role_id_value or "default_role",
                    "name": role_name_value or "Default Role"
                }
                
                # Log the role information being added
                logger.info(f"Added role information for purpose {purpose_name}: {role_name_value} (ID: {role_id_value})")
            
            # Add policy based on its type
            if policy_type_name == 'security':
                result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]["security"] = {
                    "policy_name": row.get('policy_name'),
                    "encryption_required": row.get('encryption_required'),
                    "encryption_algorithm": row.get('encryption_algorithm'),
                    "masking_required": row.get('masking_required'),
                    "masking_format": row.get('masking_format'),
                    "is_override": row.get('is_override', False)
                }
            elif policy_type_name == 'usage':
                # Initialize usage array if not exists
                if "usage" not in result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]["usage"] = []
                
                result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]["usage"].append({
                    "policy_name": row.get('policy_name'),
                    "operation": row.get('operation'),
                    "allowed": row.get('allowed'),
                    "restrictions": row.get('restrictions')
                })
            elif policy_type_name == 'retention':
                # Initialize retention array if not exists
                if "retention" not in result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]:
                    result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]["retention"] = []
                
                result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]["retention"].append({
                    "policy_name": row.get('policy_name'),
                    "retention_period": row.get('retention_period'),
                    "retention_basis": row.get('retention_basis')
                })
        
        logger.info(f"Generated JSON with {len(result['tables'])} tables")
        # Debug: Log the final structure
        logger.info(f"Generated JSON with {len(result['tables'])} tables")
        for table_key, table_data in result['tables'].items():
            logger.info(f"Table {table_key} has {len(table_data['columns'])} columns")
            for column_name, column_data in table_data['columns'].items():
                logger.info(f"Column {column_name} has {len(column_data['roles'])} roles")
        
        logger.info(f"===== POLICY JSON GENERATION COMPLETED =====")
        return result
