from repositories.RegulatoryMetadataRepository import RegulatoryMetadataRepository
from repositories.GlossaryRepository import GlossaryRepository

class LawInference:
    def __init__(self, regulatory_metadata_repository: RegulatoryMetadataRepository, glossary_repository: GlossaryRepository):
        """Initialize the LawInference with required repositories.
        
        Args:
            regulatory_metadata_repository: Repository for regulatory metadata
            glossary_repository: Repository for glossary data
        """
        self.regulatory_metadata_repository = regulatory_metadata_repository
        self.glossary_repository = glossary_repository

    def get_applicable_laws(self, jurisdiction_name: str) -> list:
        """Get all laws applicable to a specific jurisdiction.
        
        Args:
            jurisdiction_name: Name of the jurisdiction to check
            
        Returns:
            List of applicable laws with their details
        """
        # Get all law-jurisdiction mappings
        law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
        
        # Find all laws that apply to the selected jurisdiction
        applicable_laws = []
        for lj in law_jurisdictions:
            if lj["jurisdiction_name"] == jurisdiction_name:
                applicable_laws.append(lj["law_name"])
        
        # Get detailed information for each applicable law
        detailed_laws = []
        if applicable_laws:
            all_laws = self.glossary_repository.get_laws()
            for law_name in applicable_laws:
                law_details = next((law for law in all_laws if law["name"] == law_name), None)
                if law_details:
                    detailed_laws.append({
                        "name": law_details["name"],
                        "full_name": law_details.get("full_name", "Not available"),
                        "description": law_details.get("description", "No description available"),
                        "effective_date": law_details.get("effective_date", "Not specified")
                    })
        
        return detailed_laws

    def get_jurisdictions(self) -> list:
        """Get all unique jurisdictions from the law jurisdiction mappings.
        
        Returns:
            Sorted list of unique jurisdiction names
        """
        law_jurisdictions = self.regulatory_metadata_repository.get_law_jurisdictions()
        return sorted(list(set([lj["jurisdiction_name"] for lj in law_jurisdictions])))

    def get_decision_tree_nodes(self) -> list:
        """Get nodes for the law inference decision tree.
        
        Returns:
            List of node dictionaries for visualization
        """
        return [
            {"id": "jurisdiction", "label": "Jurisdiction Selection", "color": "#3498db", "shape": "ellipse", "size": 30},
            {"id": "mapping", "label": "Law Jurisdiction Mapping", "color": "#f39c12", "shape": "box", "size": 25},
            {"id": "laws", "label": "Applicable Laws", "color": "#27ae60", "shape": "box", "size": 25},
            {"id": "details", "label": "Law Details", "color": "#9b59b6", "shape": "box", "size": 25}
        ]

    def get_decision_tree_edges(self) -> list:
        """Get edges for the law inference decision tree.
        
        Returns:
            List of edge dictionaries for visualization
        """
        return [
            {"source": "jurisdiction", "target": "mapping", "label": "Lookup"},
            {"source": "mapping", "target": "laws", "label": "Identify"},
            {"source": "laws", "target": "details", "label": "Retrieve"}
        ]
