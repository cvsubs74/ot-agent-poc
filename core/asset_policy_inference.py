import pandas as pd

class AssetPolicyInference:
    """
    Inference engine to determine how policies are applied at the actual table column level
    for a given asset and purpose, including all policy types (security, usage, retention).
    """
    
    def __init__(self, catalog_repository, regulatory_metadata_repository, glossary_repository):
        """
        Initialize the AssetPolicyInference with required repositories.
        
        Args:
            catalog_repository: Repository for accessing catalog data
            regulatory_metadata_repository: Repository for accessing policy metadata
            glossary_repository: Repository for accessing glossary data
        """
        self.catalog_repository = catalog_repository
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository
    
    def get_applied_policies_for_asset_purpose(self, asset_id, purpose_id, policy_type='all', role_id='all'):
        """
        Get policies applied at the table column level for a given asset, purpose, policy type, and role.
        
        Args:
            asset_id: ID of the asset
            purpose_id: ID of the purpose or 'all' for all purposes
            policy_type: Type of policy to filter by ('security', 'usage', 'retention', or 'all')
            role_id: ID of the external role to filter by or 'all' for all roles
            
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
        assets = self.glossary_repository.get_assets()
        for asset in assets:
            if asset[0] == asset_id:
                asset_name = asset[1]
                break
        logger.info(f"Asset: {asset_name} (ID: {asset_id})")
        
        # Get all catalog entries for the asset
        catalog_entries = self.catalog_repository.get_catalog_entries_by_asset(asset_id)
        logger.info(f"Retrieved {len(catalog_entries)} catalog entries for asset")
        
        # Initialize results list
        results = []
        
        # Handle 'all' purposes case
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
                entries_processed = 0
                for entry in catalog_entries:
                    # Skip entries without a data element
                    if not entry.get('data_element_id'):
                        continue
                    
                    logger.debug(f"Processing entry: {entry.get('schema_name')}.{entry.get('table_name')}.{entry.get('column_name')}")
                    entries_processed += 1
                    
                    # Process policies for this entry and purpose based on policy type
                    if policy_type == 'all' or policy_type == 'security':
                        logger.debug(f"Processing security policies for {entry.get('column_name')}")
                        self._process_security_policies(entry, current_purpose_id, current_purpose_name, results, role_id)
                    if policy_type == 'all' or policy_type == 'usage':
                        logger.debug(f"Processing usage policies for {entry.get('column_name')}")
                        self._process_usage_policies(entry, current_purpose_id, current_purpose_name, results, role_id)
                    if policy_type == 'all' or policy_type == 'retention':
                        logger.debug(f"Processing retention policies for {entry.get('column_name')}")
                        self._process_retention_policies(entry, current_purpose_id, current_purpose_name, results, role_id)
                
                logger.info(f"Processed {entries_processed} entries for purpose {current_purpose_name}")
        else:
            logger.info(f"Processing specific purpose with ID: {purpose_id}")
            purpose_name = None
            purposes = self.glossary_repository.get_purposes()
            for purpose in purposes:
                if purpose["id"] == purpose_id:
                    purpose_name = purpose["name"]
                    break
            
            if not purpose_name:
                logger.warning(f"Purpose with ID {purpose_id} not found. Returning empty DataFrame.")
                return pd.DataFrame()
                
            logger.info(f"Processing purpose: {purpose_name} (ID: {purpose_id})")
                
            # Process each catalog entry for the specific purpose
            entries_processed = 0
            for entry in catalog_entries:
                # Skip entries without a data element
                if not entry.get('data_element_id'):
                    continue
                
                logger.debug(f"Processing entry: {entry.get('schema_name')}.{entry.get('table_name')}.{entry.get('column_name')}")
                entries_processed += 1
                
                # Get policy types for this data element and purpose based on selected policy type
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
            
        # We can't filter by role directly since role_id isn't in the security policies table
        # Instead, we'll check for role-specific overrides later
        
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
                
                # Add to results
                results.append({
                    'schema_name': entry.get('schema_name'),
                    'table_name': entry.get('table_name'),
                    'column_name': entry.get('column_name'),
                    'data_type': entry.get('data_type'),
                    'data_element_name': entry.get('data_element_name'),
                    'purpose_name': purpose_name,
                    'role_name': 'Default (No Override)',
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
            
        # We can't filter by role directly since role_id isn't in the usage policies table
        # Instead, we'll check for role-specific overrides later
        
        # If no usage policies found at all, return early
        if not policy_purpose_data_usages:
            return
            
        # Get policy overrides for this data element and purpose
        # We'll check for role-specific overrides if a role_id is specified
        if role_id != 'all':
            # Get the specific role
            roles = self.glossary_repository.get_external_roles()
            filtered_roles = [role for role in roles if role[0] == role_id]
            if not filtered_roles:
                logger.warning(f"[USAGE] Role ID {role_id} not found, no usage policies will be processed")
                return
            roles = filtered_roles
            logger.info(f"[USAGE] Filtering for role: {roles[0][1]} (ID: {role_id})")
        else:
            # Get all roles
            roles = self.glossary_repository.get_external_roles()
            logger.info(f"[USAGE] Processing all roles ({len(roles)} roles)")
        
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
                    'role_name': 'Default (No Override)',
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
        
        # Get all roles for filtering
        roles = self.glossary_repository.get_external_roles()
        
        # Filter by role_id if specified
        if role_id != 'all':
            logger.info(f"[RETENTION] Filtering by role ID: {role_id}")
            filtered_roles = [role for role in roles if role[0] == role_id]
            if not filtered_roles:
                logger.warning(f"[RETENTION] Role ID {role_id} not found, no retention policies will be processed")
                return
            roles = filtered_roles
        
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
                    'role_name': 'Default (No Override)',
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
        assets = self.glossary_repository.get_assets()
        for asset in assets:
            if asset[0] == asset_id:
                result["asset_name"] = asset[1]
                break
        
        # If no policies found, return the basic structure
        if df.empty:
            logger.info(f"No policies found for asset_id={asset_id}, purpose_id={purpose_id}, policy_type={policy_type}, role_id={role_id}")
            logger.info(f"===== POLICY JSON GENERATION COMPLETED =====")
            return result
        
        # Convert the DataFrame to a dictionary structure
        for _, row in df.iterrows():
            schema_name = row.get('schema_name')
            table_name = row.get('table_name')
            column_name = row.get('column_name')
            purpose_name = row.get('purpose_name')
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
            
            # Add policy based on its type
            if policy_type_name == 'security':
                result["tables"][table_key]["columns"][column_name]["purposes"][purpose_name]["security"] = {
                    "policy_name": row.get('policy_name'),
                    "encryption_required": row.get('encryption_required'),
                    "encryption_algorithm": row.get('encryption_algorithm'),
                    "masking_required": row.get('masking_required'),
                    "masking_format": row.get('masking_format')
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
        logger.info(f"===== POLICY JSON GENERATION COMPLETED =====")
        return result
        
        return result
