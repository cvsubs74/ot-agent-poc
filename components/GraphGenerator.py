import json
import logging
import uuid
from enums.EntityType import EntityType
from enums.RelationshipType import RelationshipType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ContextGraphGenerator:
    def __init__(self, context_graph_repo):
        """
        Initializes the ContextGraphGenerator with a DatabaseManager instance.
        """
        self.context_graph_repo = context_graph_repo
        self.entities = {}  # Stores entity names and their types
        self.relationships = []  # Stores relationships between entities
        logger.info("ContextGraphGenerator initialized.")

    def add_entity(self, entity_type: EntityType, entity_name: str):
        """
        Adds an entity to the internal memory (does not commit to the database).

        :param entity_type: The type of the entity (EntityType).
        :param entity_name: The unique name of the entity (string).
        """
        self.entities[entity_name] = entity_type
        logger.debug(f"Added entity: {entity_type.value} - {entity_name}")

    def add_relationship(self, source_name: str, target_name: str, relationship_type: RelationshipType):
        """
        Adds a relationship between two entities to the internal memory (does not commit to the database).

        :param source_name: Name of the source entity (string).
        :param target_name: Name of the target entity (string).
        :param relationship_type: Type of the relationship (RelationshipType).
        """
        if source_name not in self.entities or target_name not in self.entities:
            logger.error(f"One or both entities not found: {source_name}, {target_name}")
            return False

        source_type = self.entities[source_name]
        target_type = self.entities[target_name]

        # Store the relationship in memory
        self.relationships.append({
            'source_name': source_name,
            'source_type': source_type,
            'target_name': target_name,
            'target_type': target_type,
            'relationship_type': relationship_type
        })
        logger.debug(f"Added relationship: {relationship_type.value} between {source_name} and {target_name}")
        return True

    def create_graph_from_json(self, graph_data: dict):
        """
        Creates a graph from a JSON object containing entities and relationships.

        :param graph_data: JSON object containing entities and relationships.
        :return: True if the graph creation is successful, False otherwise.
        """
        try:
            description = graph_data.get('description', '')

            # Step 1: Append a unique suffix (UUID) to the graph name to ensure uniqueness
            unique_suffix = str(uuid.uuid4())[:8]  # Generate a unique suffix (8 characters from UUID)
            graph_name = f"{graph_data.get('graph_name')}_{unique_suffix}"

            # Step 2: Check if the graph with the modified name already exists (highly unlikely, but for safety)
            existing_graph_id = self.context_graph_repo.get_graph_id(graph_name)
            if existing_graph_id:
                logger.info(
                    f"Graph with name '{graph_name}' already exists with ID {existing_graph_id}. Skipping creation.")
                return graph_name, False

            # Step 3: Add the graph with the unique name
            graph_id = self.context_graph_repo.add_graph(graph_name, description)
            if not graph_id:
                logger.error(f"Failed to create graph '{graph_name}'.")
                return graph_name, False

            # Step 4: Add entities from the JSON (with attributes)
            entities = graph_data.get('entities', [])
            for entity in entities:
                entity_name = entity['name']
                entity_type_str = entity['type']
                entity_attributes = entity.get('attributes', {})  # Capture the attributes from JSON

                # Convert the entity type string to the corresponding enum
                entity_type = EntityType.from_value(entity_type_str)

                # Ensure entity attributes are properly converted to JSON before storing
                entity_attributes_json = json.dumps(entity_attributes)

                # Persist entity with attributes to the database, now with graph_id
                self.add_entity(entity_type, entity_name)
                entity_name_prefixed = f"G{graph_id}_{entity_name}"
                self.context_graph_repo.add_entity(entity_name_prefixed, entity_type_str, entity_attributes_json, graph_id)
                logger.info(
                    f"Entity '{entity_name}' of type '{entity_type_str}' added with attributes {entity_attributes}.")

            # Step 5: Add relationships from the JSON
            relationships = graph_data.get('relationships', [])
            for relationship in relationships:
                source_name = relationship['source']
                target_name = relationship['target']
                relationship_type_str = relationship['relationship']
                try:
                    # Try to convert the relationship type string to an enum value
                    relationship_type = RelationshipType.from_value(relationship_type_str)
                    # If successful, add the relationship
                    self.add_relationship(source_name, target_name, relationship_type)
                    logger.info(
                        f"Relationship '{relationship_type_str}' added between '{source_name}' and '{target_name}'.")

                except ValueError:
                    # If an invalid relationship type is encountered, skip this relationship
                    logger.error(
                        f"Skipping invalid relationship type: {relationship_type_str} between {source_name} and {target_name}")

            # Step 6: Commit the relationships to the database
            for rel in self.relationships:
                source_name_prefixed = f"G{graph_id}_{rel['source_name']}"
                target_name_prefixed = f"G{graph_id}_{rel['target_name']}"
                self.context_graph_repo.add_relationship(
                    graph_id=graph_id,
                    source_type=rel['source_type'],
                    source_name=source_name_prefixed,
                    target_type=rel['target_type'],
                    target_name=target_name_prefixed,
                    relationship_type=rel['relationship_type']
                )
                logger.info(
                    f"Relationship '{rel['relationship_type'].value}' added between '{source_name_prefixed}' and '{target_name_prefixed}'.")

            # Clear memory after graph creation
            self.entities.clear()
            self.relationships.clear()

            logger.info(f"Graph '{graph_name}' created successfully with ID {graph_id}.")
            return graph_id, graph_name, True

        except Exception as e:
            logger.error(f"Error during graph creation from JSON: {e}")
            return None, None, False

    def reset(self):
        """
        Resets the internal entity and relationship storage without committing to the database.
        """
        self.entities.clear()
        self.relationships.clear()
        logger.info("ContextGraphGenerator reset: Entities and relationships cleared.")

    def list_graphs(self) -> list:
        """
        Retrieves a list of all existing graphs.

        :return: List of graphs, where each graph is a dict with keys 'id', 'name', 'description', 'created_at'.
        """
        try:
            graphs = self.context_graph_repo.list_graphs()
            logger.info(f"Retrieved {len(graphs)} graphs.")
            return graphs
        except Exception as e:
            logger.error(f"Failed to list graphs: {e}")
            return []

    def get_relationship_paths(
            self,
            graph_id: int,
            source_type: EntityType,
            source_name: str,
            target_type: EntityType,
            target_name: str,
            max_depth: int = 5,
            max_paths: int = 10
    ) -> list:
        """
        Retrieves all paths from a specific source entity to a specific target entity within a specific graph.

        :param graph_id: The ID of the graph (int).
        :param source_type: The type of the source entity (EntityType).
        :param source_name: The name of the source entity (string).
        :param target_type: The type of the target entity (EntityType).
        :param target_name: The name of the target entity (string).
        :param max_depth: The maximum depth to traverse (int).
        :param max_paths: The maximum number of paths to return (int).
        :return: A list of paths, where each path is a list of tuples (EntityType, entity_name).
        """
        return self.context_graph_repo.get_relationship_paths(
            graph_id=graph_id,
            source_type=source_type,
            source_name=source_name,
            target_type=target_type,
            target_name=target_name,
            max_depth=max_depth,
            max_paths=max_paths
        )

    def get_all_paths_to_target_type(
            self,
            graph_id: int,
            source_type: EntityType,
            source_name: str,
            target_type: EntityType,
            max_depth: int = 5,
            max_paths: int = 10
    ) -> list:
        """
        Retrieves all paths from a specific source entity to any entity of the target type within a specific graph.

        :param graph_id: The ID of the graph (int).
        :param source_type: The type of the source entity (EntityType).
        :param source_name: The name of the source entity (string).
        :param target_type: The target type to match (EntityType).
        :param max_depth: The maximum depth to traverse (int).
        :param max_paths: The maximum number of paths to return (int).
        :return: A list of paths, where each path is a list of tuples (EntityType, entity_name).
        """
        return self.context_graph_repo.get_all_paths_to_target_type(
            graph_id=graph_id,
            source_type=source_type,
            source_name=source_name,
            target_type=target_type,
            max_depth=max_depth,
            max_paths=max_paths
        )



