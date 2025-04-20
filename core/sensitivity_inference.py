from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.GlossaryRepository import GlossaryRepository

class SensitivityInference:
    def __init__(self, glossary_repository: GlossaryRepository, regulatory_metadata_repository: RegulatoryMetadataRepository):
        """Initialize the SensitivityInference with required repositories.
        
        Args:
            glossary_repository: Repository for glossary data
            regulatory_metadata_repository: Repository for regulatory metadata
        """
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

    def infer_data_element_sensitivities(self, data_elements):
        """Infer sensitivity levels for a list of data elements.
        
        Args:
            data_elements: List of data element dictionaries with 'id', 'name', and 'description' keys
            
        Returns:
            Dictionary mapping data element names to sensitivity levels and sources
        """
        # Initialize result dictionary
        sensitivities = {}
        
        # Get all data elements from the database to map names to IDs if needed
        all_data_elements = self.glossary_repository.get_data_elements()
        name_to_id_map = {de['name']: de['id'] for de in all_data_elements}
        
        # Process each data element
        for data_element in data_elements:
            # If we have an ID, use it directly
            if 'id' in data_element and data_element['id']:
                data_element_id = data_element['id']
            # Otherwise, try to find the ID by name
            elif data_element['name'] in name_to_id_map:
                data_element_id = name_to_id_map[data_element['name']]
            else:
                # Skip if we can't find the data element
                continue
            
            # Use the infer_sensitivity method to get the sensitivity
            sensitivity_result = self._infer_sensitivity(data_element_id=data_element_id)
            
            if sensitivity_result:
                sensitivities[data_element['name']] = {
                    'sensitivity': sensitivity_result['sensitivity_name'],
                    'source': sensitivity_result['source']
                }
            else:
                # If no sensitivity found, mark as 'Unknown'
                sensitivities[data_element['name']] = {
                    'sensitivity': 'Unknown',
                    'source': 'No sensitivity mapping found'
                }
        
        return sensitivities  

    def _infer_sensitivity(self, data_element_id=None, data_category_id=None, data_subject_type_id=None, law_id=None, jurisdiction_id=None):
        """Infer sensitivity level based on provided parameters.
        
        This method determines the sensitivity level using different approaches based on the parameters provided:
        1. If data_element_id and data_subject_type_id are provided, it checks direct data element sensitivity mappings
        2. If data_category_id and data_subject_type_id are provided, it checks data category sensitivity mappings
        3. If law_id is also provided, it checks law-specific sensitivity mappings
        4. If only data_element_id is provided, it tries to find any sensitivity mapping for that element
        5. If only data_category_id is provided, it tries to find any sensitivity mapping for that category
        
        Args:
            data_element_id: ID of the data element (optional)
            data_category_id: ID of the data category (optional)
            data_subject_type_id: ID of the data subject type (optional)
            law_id: ID of the law (optional)
            jurisdiction_id: ID of the jurisdiction (optional, used to find applicable laws)
            
        Returns:
            Dictionary with sensitivity_id, sensitivity_name, and source information
            or None if no sensitivity could be determined
        """
        # Initialize result
        result = None
        
        # Case 1: Direct lookup with data element, data subject type, and law
        if data_element_id and data_subject_type_id and law_id:
            # Get all law data subject type data element sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
            
            # Filter for the specific 
            matching = [s for s in all_sensitivities if 
                       s['law_id'] == law_id and 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_element_id'] == data_element_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Law-specific data element sensitivity'
                }
                return result
        
        # Case 2: Direct lookup with data category, data subject type, and law
        if data_category_id and data_subject_type_id and law_id:
            # Get all law data subject type data category sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
            
            # Filter for the specific combination
            matching = [s for s in all_sensitivities if 
                       s['law_id'] == law_id and 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_category_id'] == data_category_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Law-specific data category sensitivity'
                }
                return result
        
        # Case 3: Direct lookup with data element and data subject type (no specific law)
        if data_element_id and data_subject_type_id:
            # Get all data subject type data element sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
            
            # Filter for the specific combination
            matching = [s for s in all_sensitivities if 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_element_id'] == data_element_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Data element sensitivity'
                }
                return result
        
        # Case 4: Direct lookup with data category and data subject type (no specific law)
        if data_category_id and data_subject_type_id:
            # Get all data subject type data category sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
            
            # Filter for the specific combination
            matching = [s for s in all_sensitivities if 
                       s['data_subject_type_id'] == data_subject_type_id and 
                       s['data_category_id'] == data_category_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'source': 'Data category sensitivity'
                }
                return result
        
        # Case 5: Find applicable laws based on jurisdiction and check their sensitivities
        if jurisdiction_id and (data_element_id or data_category_id) and data_subject_type_id:
            # Get all law jurisdictions
            law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
            
            # Filter for the specific jurisdiction
            applicable_laws = []
            for lj in law_jurisdictions:
                if lj['jurisdiction_id'] == jurisdiction_id:
                    applicable_laws.append({
                        'id': lj['law_id'],
                        'name': lj['law_name']
                    })
            
            for law in applicable_laws:
                # Try with data element first
                if data_element_id:
                    # Recursive call with the specific law
                    law_result = self._infer_sensitivity(
                        data_element_id=data_element_id,
                        data_subject_type_id=data_subject_type_id,
                        law_id=law['id']
                    )
                    
                    if law_result:
                        law_result['source'] = f'Jurisdiction-derived law ({law["name"]}) data element sensitivity'
                        return law_result
                
                # Then try with data category
                if data_category_id:
                    # Recursive call with the specific law
                    law_result = self.infer_sensitivity(
                        data_category_id=data_category_id,
                        data_subject_type_id=data_subject_type_id,
                        law_id=law['id']
                    )
                    
                    if law_result:
                        law_result['source'] = f'Jurisdiction-derived law ({law["name"]}) data category sensitivity'
                        return law_result
        
        # Case 6: If we only have data_element_id, try to find any sensitivity mapping
        if data_element_id and not result:
            # Get all data subject type data element sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
            
            # Filter for the specific data element
            matching = [s for s in all_sensitivities if s['data_element_id'] == data_element_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'data_subject_type_id': matching[0]['data_subject_type_id'],
                    'data_subject_type_name': matching[0]['data_subject_type_name'],
                    'source': 'Any available data element sensitivity'
                }
                return result
            
            # If not found directly, try through data category
            data_category_mappings = self.regulatory_metadata_repository.get_data_category_data_elements()
            data_category_ids = [dcde['data_category_id'] for dcde in data_category_mappings 
                               if dcde['data_element_id'] == data_element_id]
            
            if data_category_ids:
                # Try each data category
                for dc_id in data_category_ids:
                    # Recursive call with the data category
                    dc_result = self._infer_sensitivity(data_category_id=dc_id)
                    if dc_result:
                        dc_result['source'] = 'Data element derived from data category sensitivity'
                        return dc_result
        
        # Case 7: If we only have data_category_id, try to find any sensitivity mapping
        if data_category_id and not result:
            # Get all data subject type data category sensitivities
            all_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
            
            # Filter for the specific data category
            matching = [s for s in all_sensitivities if s['data_category_id'] == data_category_id]
            
            if matching:
                result = {
                    'sensitivity_id': matching[0]['sensitivity_id'],
                    'sensitivity_name': matching[0]['sensitivity_name'],
                    'data_subject_type_id': matching[0]['data_subject_type_id'],
                    'data_subject_type_name': matching[0]['data_subject_type_name'],
                    'source': 'Any available data category sensitivity'
                }
                return result
        
        # If no sensitivity found, return None
        return None              

    def infer_sensitivity(self, law: str, data_subject_type: str, data_value: str, data_type: str) -> str:
        """Infer sensitivity based on regulatory metadata.
        
        Args:
            law: The name of the selected law
            data_subject_type: The name of the data subject type
            data_value: The name of the data element or category
            data_type: Either "Data Element" or "Data Category"
            
        Returns:
            The inferred sensitivity level or None if not found
        """
        # Hierarchical sensitivity inference strategy:
        # 1. First check law-specific mappings with data subject type (most specific)
        # 2. Then check general mappings with data subject type
        # 3. If data element, check if it belongs to a data category with known sensitivity
        # 4. Finally, check for any default sensitivity for the data element/category
        
        if data_type == "Data Element":
            # 1. Check law-specific data element sensitivity with data subject type
            de_law_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_element_sensitivities()
            for item in de_law_sensitivities:
                if (item["law_name"] == law and 
                    item["data_subject_type_name"] == data_subject_type and 
                    item["data_element_name"] == data_value):
                    return item["sensitivity_name"]
            
            # 2. Check general data element sensitivity with data subject type
            de_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_element_sensitivities()
            for item in de_sensitivities:
                if (item["data_subject_type_name"] == data_subject_type and 
                    item["data_element_name"] == data_value):
                    return item["sensitivity_name"]
            
            # 3. Check if the data element belongs to a data category with known sensitivity
            # First, get the data categories for this data element
            data_categories = self.regulatory_metadata_repository.get_data_category_data_elements()
            element_categories = []
            for mapping in data_categories:
                if mapping["data_element_name"] == data_value:
                    element_categories.append(mapping["data_category_name"])
            
            # Then check sensitivities for these categories
            if element_categories:
                # Check law-specific category sensitivities
                dc_law_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
                for category in element_categories:
                    for item in dc_law_sensitivities:
                        if (item["law_name"] == law and 
                            item["data_subject_type_name"] == data_subject_type and 
                            item["data_category_name"] == category):
                            return item["sensitivity_name"]
                
                # Check general category sensitivities
                dc_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
                for category in element_categories:
                    for item in dc_sensitivities:
                        if (item["data_subject_type_name"] == data_subject_type and 
                            item["data_category_name"] == category):
                            return item["sensitivity_name"]
            
            # 4. Look for default sensitivity for this data element
            all_data_elements = self.glossary_repository.get_data_elements()
            for element in all_data_elements:
                if element["name"] == data_value and "sensitivity" in element and element["sensitivity"]:
                    return element["sensitivity"]
                    
        else:  # Data Category
            # 1. Check law-specific data category sensitivity with data subject type
            dc_law_sensitivities = self.regulatory_metadata_repository.get_law_data_subject_type_data_category_sensitivities()
            for item in dc_law_sensitivities:
                if (item["law_name"] == law and 
                    item["data_subject_type_name"] == data_subject_type and 
                    item["data_category_name"] == data_value):
                    return item["sensitivity_name"]
            
            # 2. Check general data category sensitivity with data subject type
            dc_sensitivities = self.regulatory_metadata_repository.get_data_subject_type_data_category_sensitivities()
            for item in dc_sensitivities:
                if (item["data_subject_type_name"] == data_subject_type and 
                    item["data_category_name"] == data_value):
                    return item["sensitivity_name"]
            
            # 3. Look for default sensitivity for this data category
            all_data_categories = self.glossary_repository.get_data_categories()
            for category in all_data_categories:
                if category["name"] == data_value and "sensitivity" in category and category["sensitivity"]:
                    return category["sensitivity"]
        
        # If no sensitivity found after all checks, return None
        return None
