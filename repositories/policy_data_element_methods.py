"""
This file contains methods to be added to the RegulatoryMetadataRepository class
for handling policy data element tables.
"""

# Add these methods to RegulatoryMetadataRepository class

def get_policy_data_element_usage(self, policy_id=None, data_element_id=None):
    """Retrieve policy data element usage rules with optional filters.
    
    Args:
        policy_id: Optional policy ID to filter by
        data_element_id: Optional data element ID to filter by
        
    Returns:
        List of dictionaries containing policy data element usage rules
    """
    cursor = self.connection.cursor()
    try:
        query = """
        SELECT p.name as policy_name, de.name as data_element_name,
               u.operation, u.allowed, u.restrictions
        FROM policy_data_element_usage u
        JOIN policy p ON u.policy_id = p.id
        JOIN data_element de ON u.data_element_id = de.id
        WHERE 1=1
        """
        params = []
        if policy_id:
            query += " AND u.policy_id = %s"
            params.append(policy_id)
        if data_element_id:
            query += " AND u.data_element_id = %s"
            params.append(data_element_id)
            
        cursor.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append({
                "policy_name": row[0],
                "data_element_name": row[1],
                "operation": row[2],
                "allowed": row[3],
                "restrictions": row[4]
            })
        return results
    except Exception as e:
        print(f"Error getting policy data element usage: {e}")
        return []
    finally:
        cursor.close()

def get_policy_data_element_retention(self, policy_id=None, data_element_id=None):
    """Retrieve policy data element retention rules with optional filters.
    
    Args:
        policy_id: Optional policy ID to filter by
        data_element_id: Optional data element ID to filter by
        
    Returns:
        List of dictionaries containing policy data element retention rules
    """
    cursor = self.connection.cursor()
    try:
        query = """
        SELECT p.name as policy_name, de.name as data_element_name,
               r.retention_period, r.retention_basis, r.exceptions
        FROM policy_data_element_retention r
        JOIN policy p ON r.policy_id = p.id
        JOIN data_element de ON r.data_element_id = de.id
        WHERE 1=1
        """
        params = []
        if policy_id:
            query += " AND r.policy_id = %s"
            params.append(policy_id)
        if data_element_id:
            query += " AND r.data_element_id = %s"
            params.append(data_element_id)
            
        cursor.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append({
                "policy_name": row[0],
                "data_element_name": row[1],
                "retention_period": row[2],
                "retention_basis": row[3],
                "exceptions": row[4]
            })
        return results
    except Exception as e:
        print(f"Error getting policy data element retention: {e}")
        return []
    finally:
        cursor.close()

def get_policy_data_element_security(self, policy_id=None, data_element_id=None):
    """Retrieve policy data element security rules with optional filters.
    
    Args:
        policy_id: Optional policy ID to filter by
        data_element_id: Optional data element ID to filter by
        
    Returns:
        List of dictionaries containing policy data element security rules
    """
    cursor = self.connection.cursor()
    try:
        query = """
        SELECT p.name as policy_name, de.name as data_element_name,
               s.requires_encryption, s.encryption_algorithm, 
               s.requires_masking, s.masking_format,
               s.requires_access_control, s.access_control_type
        FROM policy_data_element_security s
        JOIN policy p ON s.policy_id = p.id
        JOIN data_element de ON s.data_element_id = de.id
        WHERE 1=1
        """
        params = []
        if policy_id:
            query += " AND s.policy_id = %s"
            params.append(policy_id)
        if data_element_id:
            query += " AND s.data_element_id = %s"
            params.append(data_element_id)
            
        cursor.execute(query, params)
        results = []
        for row in cursor.fetchall():
            results.append({
                "policy_name": row[0],
                "data_element_name": row[1],
                "requires_encryption": row[2],
                "encryption_algorithm": row[3],
                "requires_masking": row[4],
                "masking_format": row[5],
                "requires_access_control": row[6],
                "access_control_type": row[7]
            })
        return results
    except Exception as e:
        print(f"Error getting policy data element security: {e}")
        return []
    finally:
        cursor.close()
