import pymysql.cursors
from enums.EntityType import EntityType
from enums.RelationshipType import RelationshipType

# Predefined attributes for each entity type
ENTITY_TYPE_ATTRIBUTES = {
    'Vendor': {
        'vendor_type': 'VARCHAR(50)',
        'country': 'VARCHAR(100)',
        'status': 'VARCHAR(50)'
    },
    'Asset': {
        'asset_type': 'VARCHAR(50)',
        'location': 'VARCHAR(255)',
        'criticality': 'ENUM("low", "medium", "high")'
    },
    'Entity': {
        'entity_type': 'VARCHAR(50)',
        'date_created': 'DATE',
        'status': 'VARCHAR(50)'
    },
    'Processing Activity': {
        'process_owner': 'VARCHAR(100)',
        'activity_type': 'VARCHAR(50)',
        'purpose': 'VARCHAR(255)'
    },
    'Contract': {
        'start_date': 'DATE',
        'end_date': 'DATE',
        'status': 'VARCHAR(50)'
    },
    'Engagement': {
        'engagement_type': 'VARCHAR(50)',
        'start_date': 'DATE',
        'end_date': 'DATE'
    },
    'Policy': {
        'policy_type': 'VARCHAR(50)',
        'effective_date': 'DATE',
        'expiration_date': 'DATE'
    },
    'Exception': {
        'exception_type': 'VARCHAR(50)',
        'created_date': 'DATE',
        'status': 'VARCHAR(50)'
    },
    'Control': {
        'control_type': 'VARCHAR(50)',
        'status': 'VARCHAR(50)',
        'implementation_date': 'DATE'
    },
    'Evidence Task': {
        'assigned_to': 'VARCHAR(100)',
        'due_date': 'DATE',
        'status': 'VARCHAR(50)'
    },
    'Risk': {
        'risk_type': 'VARCHAR(50)',
        'severity': 'ENUM("low", "medium", "high")',
        'mitigation_plan': 'VARCHAR(255)'
    },
    'Project': {
        'project_manager': 'VARCHAR(100)',
        'start_date': 'DATE',
        'end_date': 'DATE'
    },
    'AI Model': {
        'model_version': 'VARCHAR(50)',
        'training_data': 'VARCHAR(255)',
        'accuracy': 'DECIMAL(5,2)'
    },
    'Dataset': {
        'source_system': 'VARCHAR(255)',
        'row_count': 'INT',
        'last_updated': 'DATE'
    }
}

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

    def create_context_grammar_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `context_grammar` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rule_name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            active BOOLEAN DEFAULT TRUE,
            is_default BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def create_entity_types_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `entity_types` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `label` VARCHAR(100) UNIQUE NOT NULL
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def create_actions_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `actions` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `entity_type_id` INT NOT NULL,
            `action_name` VARCHAR(100) NOT NULL,
            `api_endpoint` VARCHAR(255) NOT NULL,
            `description` TEXT,
            `active` BOOLEAN DEFAULT TRUE,
            UNIQUE (`entity_type_id`, `action_name`),
            FOREIGN KEY (`entity_type_id`) REFERENCES `entity_types`(`id`) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def create_entities_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `entities` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(255) NOT NULL,
            `type` VARCHAR(100) NOT NULL,  # Added type column
            `attributes` JSON NOT NULL,
            `graph_id` INT,
            FOREIGN KEY (graph_id) REFERENCES graphs(id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def add_entity(self, name, entity_type, attributes, graph_id):
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO entities (name, type, attributes, graph_id)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (name, entity_type, attributes, graph_id))
            self.connection.commit()
            print(f"Entity '{name}' of type '{entity_type}' added successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding entity '{name}' of type '{entity_type}': {e}")
        finally:
            cursor.close()

    def list_entities(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT `id`, `name`, `attributes` FROM `entities`;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error listing entities: {e}")
            return []
        finally:
            cursor.close()

    def get_entity_by_name(self, name):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT `id`, `name`, `attributes` FROM `entities` WHERE `name` = %s;", (name,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving entity by name '{name}': {e}")
            return None
        finally:
            cursor.close()

    def add_context_grammar_rule(self, rule_name, description):
        cursor = self.connection.cursor()
        try:
            add_rule_query = """
            INSERT INTO context_grammar (rule_name, description)
            VALUES (%s, %s);
            """
            cursor.execute(add_rule_query, (rule_name, description))
            self.connection.commit()
            print(f"Context grammar rule '{rule_name}' added successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding context grammar rule: {e}")
        finally:
            cursor.close()

    def list_context_grammar_rules(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, rule_name, description, active
                FROM context_grammar
                WHERE is_default = 0;  
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching context grammar rules: {e}")
            return []
        finally:
            cursor.close()

    def get_enabled_rules(self):
        """Fetch all rules that are enabled (active) and not marked as default."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT id, rule_name, description
                FROM context_grammar
                WHERE active = 1;
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching enabled context grammar rules: {e}")
            return []
        finally:
            cursor.close()

    def update_context_grammar_rule(self, rule_id, active):
        cursor = self.connection.cursor()
        try:
            update_rule_query = """
            UPDATE context_grammar
            SET active = %s
            WHERE id = %s;
            """
            cursor.execute(update_rule_query, (active, rule_id))
            self.connection.commit()
            print(f"Context grammar rule with ID {rule_id} updated successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating context grammar rule: {e}")
        finally:
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
                source_type.value,
                source_name,
                target_type.value,
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
        Fetch all details of a graph by its ID, including relationships and related entities with their attributes.
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

            # Fetch entities and their attributes related to the graph
            cursor.execute("""
                SELECT e.name, e.type, e.attributes 
                FROM entities e
                WHERE e.graph_id = %s;
            """, (graph_id,))
            entities = cursor.fetchall()

            # Add entities with their attributes to the graph details
            graph_details['entities'] = entities

            return graph_details

        except Exception as e:
            print(f"Error retrieving graph details: {e}")
            return None
        finally:
            cursor.close()

    def get_subgraph_for_entity(self, graph_id, entity):
        """
        Retrieves the subgraph of all entities linked directly or indirectly to the given entity,
        including their attributes.

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

            # Fetch attributes for each entity in the subgraph
            entities_list = []
            for etype, ename in subgraph_entities:
                entity_data = self.get_entity_attributes(ename, graph_id)
                if entity_data:
                    entities_list.append({
                        "name": ename,
                        "type": etype,
                        "attributes": entity_data['attributes']  # Ensure attributes are captured as JSON
                    })

            # Convert relationships into the required JSON format
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

            # Return the subgraph as a dictionary, containing entities and relationships
            subgraph = {
                "entities": entities_list,  # All entities with name, type, and attributes
                "relationships": relationships_json
            }

            return subgraph

        except Exception as e:
            print(f"An error occurred while retrieving the subgraph: {str(e)}")
            return None

    def get_entity_attributes(self, entity_name, graph_id):
        """
        Fetches the attributes of a specific entity from the entities table.

        :param entity_name: The name of the entity.
        :param graph_id: The ID of the graph to which the entity belongs.
        :return: A dictionary with the entity's name and attributes, or None if not found.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
            SELECT name, attributes 
            FROM entities 
            WHERE name = %s AND graph_id = %s;
            """
            cursor.execute(query, (entity_name, graph_id))
            result = cursor.fetchone()

            if result:
                return result
            else:
                print(f"No attributes found for entity '{entity_name}' in graph ID {graph_id}.")
                return None
        except Exception as e:
            print(f"Error fetching attributes for entity '{entity_name}': {e}")
            return None
        finally:
            cursor.close()

    def add_entity_type(self, label):
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO entity_types (label)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE label = label;
            """
            cursor.execute(insert_query, (label,))
            self.connection.commit()
            print(f"Entity type '{label}' added successfully.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding entity type '{label}': {e}")
        finally:
            cursor.close()

    def list_entity_types(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Fetch id, label from the entity_types table
            cursor.execute("SELECT `id`, `label` FROM `entity_types`;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error listing entity types: {e}")
            return []
        finally:
            cursor.close()

    def get_entity_type_id(self, label):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT `id` FROM `entity_types` WHERE `label` = %s;", (label,))
            result = cursor.fetchone()
            if result:
                return result['id']
            else:
                print(f"Entity type '{label}' not found.")
                return None
        except Exception as e:
            print(f"Error retrieving entity type ID for '{label}': {e}")
            return None
        finally:
            cursor.close()

    def add_entity_action(self, entity_type_label, action_name, api_endpoint, description, active=True):
        """
        Add a new entity action to the database.

        :param entity_type_label: Label of the entity type (e.g., 'Vendor', 'Asset').
        :param action_name: Name of the action.
        :param api_endpoint: API endpoint associated with the action.
        :param description: Description of the action.
        :param active: Boolean indicating if the action is active.
        """
        cursor = self.connection.cursor()
        try:
            insert_query = """
                INSERT INTO actions (entity_type_id, action_name, api_endpoint, description, active)
                VALUES (
                    (SELECT id FROM entity_types WHERE label = %s),
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON DUPLICATE KEY UPDATE 
                    api_endpoint = VALUES(api_endpoint),
                    description = VALUES(description),
                    active = VALUES(active);
            """
            cursor.execute(insert_query, (entity_type_label, action_name, api_endpoint, description, active))
            self.connection.commit()
            print(f"Entity action '{action_name}' added/updated successfully for entity type '{entity_type_label}'.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding/updating entity action '{action_name}' for entity type '{entity_type_label}': {e}")
        finally:
            cursor.close()

    def list_entity_actions_by_entity_type(self, entity_type_label):
        """
        Retrieve all entity actions for a specific entity type.

        :param entity_type_label: Label of the entity type (e.g., 'Vendor', 'Asset').
        :return: List of actions associated with the entity type.
        """
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT a.id, a.action_name, a.api_endpoint, a.description, a.active
                FROM actions a
                JOIN entity_types et ON a.entity_type_id = et.id
                WHERE et.label = %s
                ORDER BY a.action_name;
            """, (entity_type_label,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching actions for entity type '{entity_type_label}': {e}")
            return []
        finally:
            cursor.close()

    def update_entity_action_status(self, action_id, active):
        """
        Update the active status of an entity action.

        :param action_id: ID of the action to update.
        :param active: Boolean indicating the new status.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                UPDATE actions
                SET active = %s
                WHERE id = %s;
            """, (active, action_id))
            self.connection.commit()
            print(f"Entity action ID '{action_id}' updated to {'active' if active else 'inactive'}.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating entity action ID '{action_id}': {e}")
        finally:
            cursor.close()

    def update_action(self, entity_type_label, action_name, api_endpoint=None, description=None):
        entity_type_id = self.get_entity_type_id(entity_type_label)
        if not entity_type_id:
            print(f"Cannot update action. Entity type '{entity_type_label}' does not exist.")
            return

        cursor = self.connection.cursor()
        try:
            if api_endpoint and description:
                update_query = """
                UPDATE `actions`
                SET `api_endpoint` = %s, `description` = %s
                WHERE `entity_type_id` = %s AND `action_name` = %s;
                """
                cursor.execute(update_query, (api_endpoint, description, entity_type_id, action_name))
            elif api_endpoint:
                update_query = """
                UPDATE `actions`
                SET `api_endpoint` = %s
                WHERE `entity_type_id` = %s AND `action_name` = %s;
                """
                cursor.execute(update_query, (api_endpoint, entity_type_id, action_name))
            elif description:
                update_query = """
                UPDATE `actions`
                SET `description` = %s
                WHERE `entity_type_id` = %s AND `action_name` = %s;
                """
                cursor.execute(update_query, (description, entity_type_id, action_name))
            else:
                print("No fields to update.")
                return

            if cursor.rowcount == 0:
                print(f"No action named '{action_name}' found for entity type '{entity_type_label}'.")
            else:
                self.connection.commit()
                print(f"Action '{action_name}' updated successfully for entity type '{entity_type_label}'.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating action '{action_name}' for entity type '{entity_type_label}': {e}")
        finally:
            cursor.close()

    def delete_action(self, entity_type_label, action_name):
        entity_type_id = self.get_entity_type_id(entity_type_label)
        if not entity_type_id:
            print(f"Cannot delete action. Entity type '{entity_type_label}' does not exist.")
            return

        cursor = self.connection.cursor()
        try:
            delete_query = """
            DELETE FROM `actions`
            WHERE `entity_type_id` = %s AND `action_name` = %s;
            """
            cursor.execute(delete_query, (entity_type_id, action_name))
            self.connection.commit()
            if cursor.rowcount == 0:
                print(f"No action named '{action_name}' found for entity type '{entity_type_label}'.")
            else:
                print(f"Action '{action_name}' deleted successfully from entity type '{entity_type_label}'.")
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting action '{action_name}' from entity type '{entity_type_label}': {e}")
        finally:
            cursor.close()

    def get_all_actions(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("""
                SELECT et.label AS entity_type, a.action_name, a.api_endpoint, a.description
                FROM actions a
                JOIN entity_types et ON a.entity_type_id = et.id;
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving all actions: {e}")
            return []
        finally:
            cursor.close()
