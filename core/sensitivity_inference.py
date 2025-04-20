from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.GlossaryRepository import GlossaryRepository

class SensitivityInference:
    def __init__(self, regulatory_metadata_repository: RegulatoryMetadataRepository, glossary_repository: GlossaryRepository):
        """Initialize the SensitivityInference with required repositories.
        
        Args:
            regulatory_metadata_repository: Repository for regulatory metadata
            glossary_repository: Repository for glossary data
        """
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

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
        return self._infer_sensitivity(law, data_subject_type, data_value, data_type)

    def _infer_sensitivity(self, law: str, data_subject_type: str, data_value: str, data_type: str) -> str:
        """Internal method to infer sensitivity based on regulatory metadata.
        
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
