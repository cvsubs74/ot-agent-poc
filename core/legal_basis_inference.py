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

    def get_legal_bases(self, law_name: str, jurisdiction_name: str, sensitivity_name: str, purpose_category: str) -> list:
        """Get recommended legal bases based on processing parameters.
        
        Args:
            law_name: Name of the applicable law
            jurisdiction_name: Name of the jurisdiction
            sensitivity_name: Name of the data sensitivity level
            purpose_category: Name of the purpose category
            
        Returns:
            List of recommended legal bases with their details
        """
        # Get all legal bases from the repository
        legal_bases = self.glossary_repository.get_legal_bases()
        
        # Filter legal bases based on law and jurisdiction
        applicable_bases = []
        for lb in legal_bases:
            # Check if this legal basis applies to the selected law
            if lb.get("law_name") == law_name:
                # Check if it applies to the selected jurisdiction
                if lb.get("jurisdiction_name") == jurisdiction_name or not jurisdiction_name:
                    applicable_bases.append(lb)
        
        # Sort legal bases by preference order (lower number = higher preference)
        applicable_bases.sort(key=lambda x: x.get("preference_order", 100))
        
        # Add compliance requirements for each legal basis
        for lb in applicable_bases:
            # Get compliance requirements from regulatory metadata
            requirements = self.regulatory_metadata_repository.get_legal_basis_requirements(
                law_name,
                jurisdiction_name,
                lb["name"]
            )
            lb["compliance_requirements"] = requirements
        
        # Refine recommendations based on sensitivity
        self._refine_by_sensitivity(applicable_bases, sensitivity_name)
        
        return applicable_bases

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
