import pymysql.cursors
from enums.EntityType import EntityType
from enums.RelationshipType import RelationshipType

ALLOWED_RELATIONSHIPS = {
    RelationshipType.DATA_TRANSFER: [
        (EntityType.VENDOR, EntityType.ASSET),
        (EntityType.ENTITY, EntityType.ASSET),
        (EntityType.ASSET, EntityType.ASSET),
        (EntityType.VENDOR, EntityType.ENTITY),
        (EntityType.ENTITY, EntityType.ENTITY),
        (EntityType.ASSET, EntityType.VENDOR),
        (EntityType.ENTITY, EntityType.VENDOR),
        (EntityType.ASSET, EntityType.ENTITY),
        (EntityType.VENDOR, EntityType.VENDOR),
        (EntityType.PROCESSING_ACTIVITY, EntityType.ASSET),
        (EntityType.ASSET, EntityType.PROCESSING_ACTIVITY),
        (EntityType.PROCESSING_ACTIVITY, EntityType.VENDOR),
        (EntityType.PROCESSING_ACTIVITY, EntityType.ENTITY),
        (EntityType.PROJECT, EntityType.ASSET),
        (EntityType.PROJECT, EntityType.VENDOR),
        (EntityType.PROJECT, EntityType.ENTITY),
    ],
    RelationshipType.SALE_OF_DATA: [
        (EntityType.ASSET, EntityType.ASSET),
        (EntityType.VENDOR, EntityType.VENDOR),
        (EntityType.VENDOR, EntityType.ENTITY),
        (EntityType.ASSET, EntityType.ENTITY),
        (EntityType.ENTITY, EntityType.ENTITY),
        (EntityType.ENTITY, EntityType.VENDOR),
        (EntityType.ASSET, EntityType.VENDOR),
        (EntityType.PROCESSING_ACTIVITY, EntityType.ASSET),
        (EntityType.ASSET, EntityType.PROCESSING_ACTIVITY),
        (EntityType.PROJECT, EntityType.ASSET),
    ],
    RelationshipType.RELATED: [
        (source, target) for source in EntityType for target in EntityType
    ],
    RelationshipType.PRODUCT_OR_SERVICE_PROVIDER: [
        (EntityType.ENTITY, EntityType.ASSET),
        (EntityType.VENDOR, EntityType.ASSET),
        (EntityType.CONTRACT, EntityType.ENTITY),
        (EntityType.CONTRACT, EntityType.VENDOR),
        (EntityType.ENGAGEMENT, EntityType.ASSET),
        (EntityType.ENGAGEMENT, EntityType.VENDOR),
    ],
    RelationshipType.CONTROLLER: [
        (EntityType.ENTITY, EntityType.VENDOR),
        (EntityType.ENTITY, EntityType.ENTITY),
        (EntityType.VENDOR, EntityType.VENDOR),
        (EntityType.VENDOR, EntityType.ENTITY),
        (EntityType.CONTRACT, EntityType.VENDOR),
        (EntityType.CONTRACT, EntityType.ENTITY),
    ],
    RelationshipType.JOINT_CONTROLLER: [
        (EntityType.ENTITY, EntityType.ENTITY),
        (EntityType.VENDOR, EntityType.VENDOR),
        (EntityType.ENTITY, EntityType.VENDOR),
    ],
    RelationshipType.PROCESSOR: [
        (EntityType.ENTITY, EntityType.VENDOR),
        (EntityType.VENDOR, EntityType.ENTITY),
        (EntityType.VENDOR, EntityType.VENDOR),
        (EntityType.ENTITY, EntityType.ENTITY),
        (EntityType.PROCESSING_ACTIVITY, EntityType.VENDOR),
        (EntityType.PROCESSING_ACTIVITY, EntityType.ENTITY),
    ],
    RelationshipType.SUB_PROCESSOR: [
        (EntityType.VENDOR, EntityType.ENTITY),
        (EntityType.ENTITY, EntityType.VENDOR),
        (EntityType.ENTITY, EntityType.ENTITY),
        (EntityType.VENDOR, EntityType.VENDOR),
    ],
    RelationshipType.POLICY_GOVERNED: [
        (EntityType.POLICY, EntityType.ASSET),
        (EntityType.POLICY, EntityType.PROCESSING_ACTIVITY),
        (EntityType.POLICY, EntityType.ENTITY),
        (EntityType.POLICY, EntityType.VENDOR),
    ],
    RelationshipType.CONTROL_IMPLEMENTED: [
        (EntityType.CONTROL, EntityType.ASSET),
        (EntityType.CONTROL, EntityType.PROCESSING_ACTIVITY),
        (EntityType.CONTROL, EntityType.ENTITY),
    ],
    RelationshipType.RISK_ASSOCIATED: [
        (EntityType.RISK, EntityType.ASSET),
        (EntityType.RISK, EntityType.PROCESSING_ACTIVITY),
        (EntityType.RISK, EntityType.ENTITY),
        (EntityType.RISK, EntityType.VENDOR),
    ],
    RelationshipType.EVIDENCE_PROVIDED: [
        (EntityType.EVIDENCE_TASK, EntityType.CONTROL),
        (EntityType.EVIDENCE_TASK, EntityType.ASSET),
        (EntityType.EVIDENCE_TASK, EntityType.PROCESSING_ACTIVITY),
    ],
    RelationshipType.PROJECT_SUPPORTS: [
        (EntityType.PROJECT, EntityType.ASSET),
        (EntityType.PROJECT, EntityType.VENDOR),
        (EntityType.PROJECT, EntityType.ENTITY),
        (EntityType.PROJECT, EntityType.CONTRACT),
    ]
}


class ContextGraphRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_relationship_types_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `relationship_types` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def create_graphs_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `graphs` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def create_relationship_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `relationships` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            graph_id INT NOT NULL,
            source_entity_type VARCHAR(50) NOT NULL,
            source_entity_name VARCHAR(100) NOT NULL,
            target_entity_type VARCHAR(50) NOT NULL,
            target_entity_name VARCHAR(100) NOT NULL,
            relationship_type_id INT NOT NULL,
            UNIQUE (graph_id, source_entity_type, source_entity_name, target_entity_type, target_entity_name, relationship_type_id),
            FOREIGN KEY (relationship_type_id) REFERENCES relationship_types(id),
            FOREIGN KEY (graph_id) REFERENCES graphs(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def create_graph_questions_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `graph_questions` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            graph_id INT NOT NULL,
            question TEXT NOT NULL,
            asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (graph_id) REFERENCES graphs(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def populate_relationship_types(self):
        cursor = self.connection.cursor()
        try:
            for rel_type in RelationshipType:
                cursor.execute("""
                    INSERT IGNORE INTO relationship_types (name)
                    VALUES (%s)
                """, (rel_type.value,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error populating relationship types: {e}")
        finally:
            cursor.close()

    def add_graph(self, name, description=None):
        cursor = self.connection.cursor()
        try:
            add_graph_query = """
            INSERT INTO graphs (name, description)
            VALUES (%s, %s);
            """
            cursor.execute(add_graph_query, (name, description))
            self.connection.commit()
            graph_id = cursor.lastrowid
            print(f"Graph '{name}' added successfully with ID {graph_id}.")
            return graph_id
        except pymysql.err.IntegrityError:
            self.connection.rollback()
            print(f"Graph with name '{name}' already exists.")
            return None
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding graph: {e}")
            return None
        finally:
            cursor.close()

    def get_graph_id(self, name):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id FROM graphs WHERE name = %s
            """, (name,))
            result = cursor.fetchone()
            if result:
                return result['id']
            else:
                print(f"Graph '{name}' not found.")
                return None
        except Exception as e:
            print(f"Error retrieving graph ID: {e}")
            return None
        finally:
            cursor.close()

    def list_graphs(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, name, description, created_at FROM graphs
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error listing graphs: {e}")
            return []
        finally:
            cursor.close()

    def add_graph_question(self, graph_id, question):
        cursor = self.connection.cursor()
        try:
            add_question_query = """
            INSERT INTO graph_questions (graph_id, question)
            VALUES (%s, %s);
            """
            cursor.execute(add_question_query, (graph_id, question))
            self.connection.commit()
            question_id = cursor.lastrowid
            print(f"Question '{question}' added successfully with ID {question_id}.")
            return question_id
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding question: {e}")
            return None
        finally:
            cursor.close()

    def get_graph_questions(self, graph_id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, question, asked_at
                FROM graph_questions
                WHERE graph_id = %s
                ORDER BY asked_at DESC;
            """, (graph_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving questions for graph ID {graph_id}: {e}")
            return []
        finally:
            cursor.close()

    def add_relationship(self, graph_id, source_type, source_name, target_type, target_name, relationship_type):
        """
        Adds a relationship to a specific graph after validating the relationship type and entity types.
        """
        # Validate relationship type
        if relationship_type not in RelationshipType:
            print(f"Invalid relationship type: {relationship_type}")
            return

        # Validate source and target entity types
        allowed_combinations = ALLOWED_RELATIONSHIPS.get(relationship_type, [])
        if (source_type, target_type) not in allowed_combinations:
            print(
                f"Invalid source-target combination for relationship type '{relationship_type.value}': {source_type.value} -> {target_type.value}")
            return

        # Get relationship type ID
        relationship_type_id = self.get_relationship_type_id(relationship_type)
        if not relationship_type_id:
            print(f"Could not find ID for relationship type '{relationship_type.value}'.")
            return

        # Insert the relationship
        cursor = self.connection.cursor()
        try:
            add_relationship_query = """
            INSERT IGNORE INTO relationships 
            (graph_id, source_entity_type, source_entity_name, target_entity_type, target_entity_name, relationship_type_id)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(add_relationship_query, (
                graph_id,
                source_type.value["label"],
                source_name,
                target_type.value["label"],
                target_name,
                relationship_type_id
            ))
            self.connection.commit()
            print(f"Relationship '{relationship_type.value}' added successfully to graph ID {graph_id}.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding relationship: {e}")
        finally:
            cursor.close()

    def get_relationship_type_id(self, relationship_type):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id FROM relationship_types WHERE name = %s
            """, (relationship_type.value,))
            result = cursor.fetchone()
            if result:
                return result['id']
            else:
                raise ValueError(f"Relationship type '{relationship_type.value}' not found.")
        except Exception as e:
            print(f"Error retrieving relationship type ID: {e}")
            return None
        finally:
            cursor.close()

    def get_relationships_for_graph(self, graph_id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT rt.name AS relationship_type, 
                       r.source_entity_type, r.source_entity_name, 
                       r.target_entity_type, r.target_entity_name
                FROM relationships r
                JOIN relationship_types rt ON r.relationship_type_id = rt.id
                WHERE r.graph_id = %s;
            """, (graph_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving relationships for graph ID {graph_id}: {e}")
            return []
        finally:
            cursor.close()

    def delete_relationship(self, graph_id, source_type, source_name, target_type, target_name, relationship_type):
        cursor = self.connection.cursor()
        try:
            # Get relationship type ID
            relationship_type_id = self.get_relationship_type_id(relationship_type)
            if not relationship_type_id:
                print(f"Could not find ID for relationship type '{relationship_type.value}'.")
                return

            delete_relationship_query = """
            DELETE FROM relationships 
            WHERE graph_id = %s AND source_entity_type = %s AND source_entity_name = %s 
              AND target_entity_type = %s AND target_entity_name = %s 
              AND relationship_type_id = %s;
            """
            cursor.execute(delete_relationship_query, (
                graph_id,
                source_type.value,
                source_name,
                target_type.value,
                target_name,
                relationship_type_id
            ))
            self.connection.commit()
            print(f"Relationship '{relationship_type.value}' removed successfully from graph ID {graph_id}.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting relationship: {e}")
        finally:
            cursor.close()

    def get_relationship_path(self, graph_id, source_type, source_name, target_type, target_name):
        cursor = self.connection.cursor()
        try:
            # BFS to find the shortest path within the specific graph
            queue = [(source_type, source_name, [(source_type, source_name)])]
            visited = set()
            while queue:
                current_type, current_name, path = queue.pop(0)
                if (current_type, current_name) == (target_type, target_name):
                    return path
                if (current_type, current_name) in visited:
                    continue
                visited.add((current_type, current_name))
                relationships = self.get_relationships_for_graph(graph_id)
                for rel in relationships:
                    # Determine the direction of the relationship
                    if rel['source_entity_type'] == current_type.value and rel['source_entity_name'] == current_name:
                        next_entity = (
                            EntityType[rel['target_entity_type'].upper().replace(" ", "_")], rel['target_entity_name'])
                    else:
                        next_entity = (
                            EntityType[rel['source_entity_type'].upper().replace(" ", "_")], rel['source_entity_name'])
                    if next_entity not in visited:
                        queue.append((next_entity[0], next_entity[1], path + [next_entity]))
            return None  # No path found
        except Exception as e:
            print(f"Error finding relationship path: {e}")
            return None
        finally:
            cursor.close()

    def get_relationship_paths(self, graph_id, source_type, source_name, target_type, target_name, max_depth=5,
                               max_paths=10):
        """
        Determines if a path exists between two entities within a specific graph and returns the paths.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Recursive CTE to find all paths up to max_depth within the specific graph
            query = f"""
            WITH RECURSIVE path AS (
                SELECT
                    r.source_entity_type,
                    r.source_entity_name,
                    r.target_entity_type,
                    r.target_entity_name,
                    CONCAT(r.source_entity_type, ':', r.source_entity_name) AS path_trace,
                    1 AS depth
                FROM relationships r
                WHERE r.graph_id = %s
                  AND (
                      (r.source_entity_type = %s AND r.source_entity_name = %s)
                      OR
                      (r.target_entity_type = %s AND r.target_entity_name = %s)
                  )

                UNION ALL

                SELECT
                    r.source_entity_type,
                    r.source_entity_name,
                    r.target_entity_type,
                    r.target_entity_name,
                    CONCAT(p.path_trace, ' -> ', 
                        CASE 
                            WHEN r.source_entity_type = p.target_entity_type AND r.source_entity_name = p.target_entity_name THEN CONCAT(r.target_entity_type, ':', r.target_entity_name)
                            ELSE CONCAT(r.source_entity_type, ':', r.source_entity_name)
                        END
                    ) AS path_trace,
                    p.depth + 1 AS depth
                FROM relationships r
                JOIN path p ON (
                    r.graph_id = p.graph_id
                    AND (
                        r.source_entity_type = p.target_entity_type 
                        AND r.source_entity_name = p.target_entity_name
                    )
                )
                WHERE p.depth < %s
                  AND NOT FIND_IN_SET(CONCAT(r.source_entity_type, ':', r.source_entity_name), REPLACE(p.path_trace, ' -> ', ',')) 
                  AND NOT FIND_IN_SET(CONCAT(r.target_entity_type, ':', r.target_entity_name), REPLACE(p.path_trace, ' -> ', ','))
            )
            SELECT DISTINCT path_trace
            FROM path
            WHERE 
                (target_entity_type = %s AND target_entity_name = %s)
            LIMIT %s;
            """

            # Parameters for the query
            params = (
                graph_id,
                source_type.value, source_name,
                target_type.value, target_name,
                max_depth,
                target_type.value, target_name,
                max_paths
            )

            cursor.execute(query, params)
            results = cursor.fetchall()

            paths = []
            for record in results:
                path_str = record['path_trace']
                # Split the path string into entities
                entities = path_str.split(' -> ')
                path = []
                for entity in entities:
                    etype, ename = entity.split(':')
                    try:
                        etype_enum = EntityType[etype.upper().replace(" ", "_")]
                    except KeyError:
                        etype_enum = EntityType.ENTITY  # Default or handle unknown types
                    path.append((etype_enum, ename))
                paths.append(path)

            return paths

        except Exception as e:
            print(f"Error retrieving relationship paths: {e}")
            return []
        finally:
            cursor.close()

    def get_all_paths_to_target_type(self, graph_id, source_type, source_name, target_type, max_depth=5, max_paths=10):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Recursive CTE to find all paths up to max_depth within a specific graph
            query = f"""
            WITH RECURSIVE path AS (
                SELECT
                    r.source_entity_type,
                    r.source_entity_name,
                    r.target_entity_type,
                    r.target_entity_name,
                    CONCAT(r.source_entity_type, ':', r.source_entity_name) AS path_trace,
                    1 AS depth
                FROM relationships r
                WHERE r.graph_id = %s
                  AND r.source_entity_type = %s AND r.source_entity_name = %s

                UNION ALL

                SELECT
                    r.source_entity_type,
                    r.source_entity_name,
                    r.target_entity_type,
                    r.target_entity_name,
                    CONCAT(p.path_trace, ' -> ', 
                        CASE 
                            WHEN r.source_entity_type = p.target_entity_type AND r.source_entity_name = p.target_entity_name THEN CONCAT(r.target_entity_type, ':', r.target_entity_name)
                            ELSE CONCAT(r.source_entity_type, ':', r.source_entity_name)
                        END
                    ) AS path_trace,
                    p.depth + 1 AS depth
                FROM relationships r
                JOIN path p ON (
                    r.graph_id = p.graph_id
                    AND r.source_entity_type = p.target_entity_type 
                    AND r.source_entity_name = p.target_entity_name
                )
                WHERE p.depth < %s
                  AND NOT FIND_IN_SET(CONCAT(r.source_entity_type, ':', r.source_entity_name), REPLACE(p.path_trace, ' -> ', ',')) 
                  AND NOT FIND_IN_SET(CONCAT(r.target_entity_type, ':', r.target_entity_name), REPLACE(p.path_trace, ' -> ', ','))
            )
            SELECT DISTINCT path_trace
            FROM path
            WHERE 
                target_entity_type = %s
            LIMIT %s;
            """

            # Parameters for the query
            params = (
                graph_id,
                source_type.value, source_name,
                max_depth,
                target_type.value,
                max_paths
            )

            cursor.execute(query, params)
            results = cursor.fetchall()

            paths = []
            for record in results:
                path_str = record['path_trace']
                # Split the path string into entities
                entities = path_str.split(' -> ')
                path = []
                for entity in entities:
                    etype, ename = entity.split(':')
                    try:
                        # Adjust the mapping based on your EntityType enum definitions
                        etype_enum = EntityType[etype.upper().replace(" ", "_")]
                    except KeyError:
                        etype_enum = EntityType.ENTITY  # Default or handle unknown types
                    path.append((etype_enum, ename))
                paths.append(path)

            return paths

        except Exception as e:
            print(f"Error retrieving paths to target type: {e}")
            return []
        finally:
            cursor.close()

    def get_graph_details_by_id(self, graph_id):
        """
        Fetch all details of a graph by its ID, including relationships and related entities.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Fetch graph details
            cursor.execute("""
                SELECT id, name, description, created_at 
                FROM graphs 
                WHERE id = %s
            """, (graph_id,))
            graph_details = cursor.fetchone()

            if not graph_details:
                print(f"Graph with ID {graph_id} not found.")
                return None

            # Fetch relationships related to the graph
            cursor.execute("""
                SELECT rt.name AS relationship_type, 
                       r.source_entity_type, r.source_entity_name, 
                       r.target_entity_type, r.target_entity_name
                FROM relationships r
                JOIN relationship_types rt ON r.relationship_type_id = rt.id
                WHERE r.graph_id = %s;
            """, (graph_id,))
            relationships = cursor.fetchall()

            graph_details['relationships'] = relationships

            return graph_details

        except Exception as e:
            print(f"Error retrieving graph details: {e}")
            return None
        finally:
            cursor.close()

    def get_subgraph_for_entity(self, graph_id, entity):
        """
        Retrieves the subgraph of all entities linked directly or indirectly to the given entity.

        :param graph_id: The ID of the graph being explored.
        :param entity: The name of the entity to explore.
        :return: A dictionary with subgraph data containing entities and relationships.
        """
        try:
            # Fetch all relationships for the given graph
            relationships = self.get_relationships_for_graph(graph_id)
            if not relationships:
                print(f"No relationships found for graph with ID {graph_id}.")
                return None

            # Initialize sets for visited entities and relationships in the subgraph
            visited_entities = set()
            subgraph_entities = set()
            subgraph_relationships = []

            # Start BFS or DFS traversal from the given entity
            to_visit = [entity.strip()]  # Strip any leading/trailing spaces
            visited_entities.add(entity)

            while to_visit:
                current_entity = to_visit.pop(0)  # BFS: pop(0) or DFS: pop()

                for rel in relationships:
                    # Check if the current entity is involved in the relationship
                    if rel['source_entity_name'] == current_entity or rel['target_entity_name'] == current_entity:
                        # Add both entities of the relationship to the subgraph
                        subgraph_entities.add((rel['source_entity_type'], rel['source_entity_name']))
                        subgraph_entities.add((rel['target_entity_type'], rel['target_entity_name']))

                        # Add the relationship to the subgraph
                        subgraph_relationships.append({
                            "source_entity_type": rel["source_entity_type"],
                            "source_entity_name": rel["source_entity_name"],
                            "target_entity_type": rel["target_entity_type"],
                            "target_entity_name": rel["target_entity_name"],
                            "relationship_type": rel["relationship_type"]
                        })

                        # Queue up the other entity if it hasn't been visited yet
                        if rel['source_entity_name'] not in visited_entities:
                            to_visit.append(rel['source_entity_name'])
                            visited_entities.add(rel['source_entity_name'])
                        if rel['target_entity_name'] not in visited_entities:
                            to_visit.append(rel['target_entity_name'])
                            visited_entities.add(rel['target_entity_name'])

                # Prevent infinite loops in circular graphs
                if len(to_visit) > 10000:
                    print("Possible circular reference detected, stopping traversal.")
                    break

            # Convert the subgraph entities and relationships into the required JSON format
            entities_json = [{"type": etype, "name": ename} for etype, ename in subgraph_entities]
            relationships_json = [
                {
                    "source_entity_type": rel["source_entity_type"],
                    "source_entity_name": rel["source_entity_name"],
                    "target_entity_type": rel["target_entity_type"],
                    "target_entity_name": rel["target_entity_name"],
                    "relationship_type": rel["relationship_type"]
                }
                for rel in subgraph_relationships
            ]

            # Return the subgraph as a dictionary
            subgraph = {
                "entities": entities_json,
                "relationships": relationships_json
            }

            return subgraph

        except Exception as e:
            print(f"An error occurred while retrieving the subgraph: {str(e)}")
            return None


