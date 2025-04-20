from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.GlossaryRepository import GlossaryRepository

class BreachNotificationInference:
    def __init__(self, regulatory_metadata_repository: RegulatoryMetadataRepository, glossary_repository: GlossaryRepository):
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

    def get_breach_notification_guidance(self, law_name: str) -> dict:
        """Get breach notification guidance for a specific law.
        
        Args:
            law_name (str): The name of the selected law
            
        Returns:
            dict: The breach notification guidance or None if not found
        """
        # Get the law ID from the name
        laws = self.glossary_repository.get_laws()
        law_id = None
        for law in laws:
            if law["name"] == law_name:
                law_id = law["id"]
                break
        
        if not law_id:
            return None
        
        # Get breach notification guidance for the law
        guidances = self.regulatory_metadata_repository.get_law_incident_breach_guidances(law_id)
        
        if not guidances:
            return None
        
        # Return the first guidance for the law (typically there's only one per law)
        return guidances[0]
