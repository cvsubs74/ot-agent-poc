import os
import json
import vertexai
from vertexai.generative_models import GenerativeModel

class IdentifierMatcher:
    """
    A class for identifying matching columns for user identifiers using VertexAI.
    This helps with row-level security by finding columns that can be used for consent-based filtering.
    """
    
    def __init__(self):
        """
        Initialize the IdentifierMatcher with VertexAI configuration.
        """
        # Initialize VertexAI
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["GC_CRED"]
        vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["LOCATION"])
        self.model = GenerativeModel(os.environ["MODEL"])
    
    def find_identifier_columns(self, table_columns, consent_identifiers):
        """
        Use VertexAI to find columns in a table that can be used for row filtering based on consent identifiers.
        
        Args:
            table_columns: Dictionary of column names with their data element names and types
            consent_identifiers: Dictionary of consent profile identifiers we want to match against
            
        Returns:
            Dictionary mapping consent identifier types to matching column names
        """
        # Create a prompt for the VertexAI model
        prompt = self._create_matching_prompt(table_columns, consent_identifiers)
        
        # Get response from VertexAI
        response = self.model.generate_content(prompt)
        
        # Parse the response to extract the identifier column mappings
        return self._parse_response(response.text, consent_identifiers)
    
    def _create_matching_prompt(self, table_columns, consent_identifiers):
        """
        Create a prompt for VertexAI to match table columns with consent identifiers.
        
        Args:
            table_columns: Dictionary of column names with their data element names and types
            consent_identifiers: Dictionary of consent profile identifiers we want to match against
            
        Returns:
            String prompt for the VertexAI model
        """
        # Format table columns for the prompt
        columns_json = json.dumps(table_columns, indent=2)
        
        # Format consent identifiers for the prompt
        identifiers_json = json.dumps(consent_identifiers, indent=2)
        
        # Create the prompt
        prompt = f"""
        You are an expert in data mapping and identity resolution. Your task is to find the best matching columns 
        in a database table that correspond to user identifiers needed for consent-based row filtering.

        Here are the available columns in the table, with their data element names and types:
        {columns_json}

        Here are the consent identifiers we need to match, with descriptions and examples:
        {identifiers_json}

        For each consent identifier, find the best matching column in the table. Consider:
        1. Exact or close matches between column names and identifier examples
        2. Semantic similarity between data element names and identifier descriptions
        3. Data type compatibility (e.g., email should be a string type)
        4. Avoid matching address, location, or other clearly non-identifier columns

        Return a JSON object with this structure:
        {{
          "identifier_type_1": "matching_column_name_1",
          "identifier_type_2": "matching_column_name_2",
          ...
        }}

        Only include matches that you're confident about (score > 0.5). If you can't find a good match for an identifier, don't include it in the result.
        """
        
        return prompt
    
    def _parse_response(self, response_text, consent_identifiers):
        """
        Parse the response from VertexAI to extract the identifier column mappings.
        
        Args:
            response_text: Text response from VertexAI
            consent_identifiers: Dictionary of consent profile identifiers for validation
            
        Returns:
            Dictionary mapping consent identifier types to matching column names
        """
        # Extract JSON from the response
        try:
            # Find JSON in the response (it might be surrounded by markdown code blocks or other text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                mappings = json.loads(json_str)
                
                # Validate that all keys in the mappings are valid consent identifiers
                valid_mappings = {k: v for k, v in mappings.items() if k in consent_identifiers}
                
                return valid_mappings
            else:
                # Fallback to empty mappings if no JSON found
                return {}
                
        except (json.JSONDecodeError, ValueError):
            # Fallback to empty mappings if parsing fails
            return {}
