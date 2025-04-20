from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.GlossaryRepository import GlossaryRepository

class LegalBasisInference:
    def __init__(self, regulatory_metadata_repository: RegulatoryMetadataRepository, glossary_repository: GlossaryRepository):
        """Initialize the LegalBasisInference with required repositories.
        
        Args:
            regulatory_metadata_repository: Repository for regulatory metadata
            glossary_repository: Repository for glossary data
        """
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

    def get_legal_bases(self, law_name: str, jurisdiction_name: str, sensitivity_name: str, purpose_category: str = None) -> list:
        """Get recommended legal bases based on processing parameters.
        
        Args:
            law_name: Name of the applicable law
            jurisdiction_name: Name of the jurisdiction
            sensitivity_name: Name of the data sensitivity level
            purpose_category: Name of the purpose category (optional)
            
        Returns:
            List of recommended legal bases with their details
        """
        # First, try to get legal bases based on purpose category if available
        if purpose_category:
            # Get law ID
            law_id = None
            laws = self.glossary_repository.get_laws()
            for l in laws:
                if l["name"] == law_name:
                    law_id = l["id"]
                    break
            
            # Get purpose category ID
            purpose_category_id = None
            purpose_categories = self.glossary_repository.get_purpose_categories()
            for pc in purpose_categories:
                if pc["name"] == purpose_category:
                    purpose_category_id = pc["id"]
                    break
            
            if law_id and purpose_category_id:
                # Get legal bases recommended for this law and purpose category combination
                law_purpose_legal_bases = self.regulatory_metadata_repository.get_law_purpose_category_legal_bases(
                    law_id=law_id, purpose_category_id=purpose_category_id
                )
                
                if law_purpose_legal_bases:
                    # Get full legal basis information
                    all_legal_bases = self.glossary_repository.get_legal_bases()
                    
                    # Get the full legal basis objects and sort by preference order
                    recommended_legal_bases = []
                    for lb in all_legal_bases:
                        for lplb in law_purpose_legal_bases:
                            if lb["id"] == lplb["legal_basis_id"]:
                                lb["preference_order"] = lplb["preference_order"]
                                lb["recommendation_description"] = lplb["description"]
                                
                                # Get compliance requirements for this legal basis
                                requirements = self.regulatory_metadata_repository.get_legal_basis_requirements(lb["id"])
                                lb["compliance_requirements"] = [req["requirement"] for req in requirements] if requirements else []
                                
                                recommended_legal_bases.append(lb)
                    
                    # Sort by preference order (lower number = higher preference)
                    recommended_legal_bases.sort(key=lambda x: x.get("preference_order", 999))
                    
                    # Further refine based on sensitivity
                    self._refine_by_sensitivity(recommended_legal_bases, sensitivity_name)
                    
                    return recommended_legal_bases
    
        # Fall back to the original method if purpose category approach doesn't yield results
        # Get all legal bases for the selected law
        law_legal_bases = self.regulatory_metadata_repository.get_law_legal_bases()
        filtered_legal_bases = [item for item in law_legal_bases if item["law_name"] == law_name]
        
        if not filtered_legal_bases:
            return None
        
        # Get full legal basis information
        all_legal_bases = self.glossary_repository.get_legal_bases()
        
        # Extract just the legal basis names from the filtered results
        legal_basis_names = [item["legal_basis_name"] for item in filtered_legal_bases]
        
        # Get the full legal basis objects for the filtered names
        recommended_legal_bases = []
        for lb in all_legal_bases:
            if lb["name"] in legal_basis_names:
                # Get compliance requirements for this legal basis
                requirements = self.regulatory_metadata_repository.get_legal_basis_requirements(lb["id"])
                lb["compliance_requirements"] = [req["requirement"] for req in requirements] if requirements else []
                recommended_legal_bases.append(lb)
        
        # Sort legal bases based on sensitivity
        self._refine_by_sensitivity(recommended_legal_bases, sensitivity_name)
        
        return recommended_legal_bases

    def _refine_by_sensitivity(self, legal_bases: list, sensitivity: str) -> None:
        """Refine the legal basis recommendations based on data sensitivity.
        
        Args:
            legal_bases: List of legal bases to refine
            sensitivity: The sensitivity level (high, medium, low)
        """
        # For high sensitivity data, prioritize explicit consent and legal obligation
        if sensitivity.lower() == "high":
            legal_bases.sort(key=lambda lb: 
                ("consent" in lb["name"].lower(), "legal obligation" in lb["name"].lower()), 
                reverse=True)
        # For medium sensitivity, legitimate interests might be appropriate
        elif sensitivity.lower() == "medium":
            legal_bases.sort(key=lambda lb: 
                ("consent" in lb["name"].lower(), "contract" in lb["name"].lower(), 
                 "legitimate" in lb["name"].lower()), 
                reverse=True)
        # For low sensitivity, contract and legitimate interests are often suitable
        else:
            legal_bases.sort(key=lambda lb: 
                ("contract" in lb["name"].lower(), "legitimate" in lb["name"].lower(), 
                 "consent" in lb["name"].lower()), 
                reverse=True)
