import pymysql.cursors

class KnowledgeRepository:
    def __init__(self, connection):
        """Initialize the KnowledgeRepository with a database connection."""
        self.connection = connection
        
    def setup_tables(self):
        """Create all the necessary tables for the knowledge base if they don't exist."""
        # Skip table creation in test mode
        if self.connection is None:
            return
            
        self.create_knowledge_base_table()
        
    def create_knowledge_base_table(self):
        """Create the Knowledge Base table."""
        cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `knowledge_base` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `category` VARCHAR(100) NOT NULL,
            `subcategory` VARCHAR(100),
            `question` TEXT NOT NULL,
            `answer` TEXT NOT NULL,
            `tags` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX `idx_category` (`category`),
            INDEX `idx_subcategory` (`subcategory`),
            FULLTEXT INDEX `idx_question_answer` (`question`, `answer`)
        );
        """
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()
        
    def get_all_knowledge_items(self):
        """Get all knowledge base items."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM knowledge_base ORDER BY category, subcategory;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving knowledge base items: {e}")
            return []
        finally:
            cursor.close()
            
    def get_knowledge_items_by_category(self, category):
        """Get knowledge base items by category."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM knowledge_base WHERE category = %s ORDER BY subcategory;", (category,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving knowledge base items by category: {e}")
            return []
        finally:
            cursor.close()
            
    def get_knowledge_items_by_subcategory(self, subcategory):
        """Get knowledge base items by subcategory."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM knowledge_base WHERE subcategory = %s;", (subcategory,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving knowledge base items by subcategory: {e}")
            return []
        finally:
            cursor.close()
            
    def search_knowledge_base(self, query):
        """Search the knowledge base using full-text search."""
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        try:
            # Use MySQL's MATCH AGAINST for full-text search
            search_query = """
            SELECT *, MATCH(question, answer) AGAINST(%s IN NATURAL LANGUAGE MODE) AS relevance
            FROM knowledge_base
            WHERE MATCH(question, answer) AGAINST(%s IN NATURAL LANGUAGE MODE)
            ORDER BY relevance DESC;
            """
            cursor.execute(search_query, (query, query))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching knowledge base: {e}")
            return []
        finally:
            cursor.close()
            
    def add_knowledge_item(self, category, question, answer, subcategory=None, tags=None):
        """Add a new knowledge base item."""
        cursor = self.connection.cursor()
        try:
            insert_query = """
            INSERT INTO knowledge_base (category, subcategory, question, answer, tags)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (category, subcategory, question, answer, tags))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding knowledge base item: {e}")
            return None
        finally:
            cursor.close()
            
    def update_knowledge_item(self, item_id, category=None, subcategory=None, question=None, answer=None, tags=None):
        """Update an existing knowledge base item."""
        cursor = self.connection.cursor()
        try:
            # Build the update query dynamically based on provided parameters
            update_parts = []
            params = []
            
            if category is not None:
                update_parts.append("category = %s")
                params.append(category)
                
            if subcategory is not None:
                update_parts.append("subcategory = %s")
                params.append(subcategory)
                
            if question is not None:
                update_parts.append("question = %s")
                params.append(question)
                
            if answer is not None:
                update_parts.append("answer = %s")
                params.append(answer)
                
            if tags is not None:
                update_parts.append("tags = %s")
                params.append(tags)
                
            if not update_parts:
                return False  # Nothing to update
                
            update_query = f"UPDATE knowledge_base SET {', '.join(update_parts)} WHERE id = %s;"
            params.append(item_id)
            
            cursor.execute(update_query, params)
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating knowledge base item: {e}")
            return False
        finally:
            cursor.close()
            
    def delete_knowledge_item(self, item_id):
        """Delete a knowledge base item."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM knowledge_base WHERE id = %s;", (item_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting knowledge base item: {e}")
            return False
        finally:
            cursor.close()
            
    def seed_knowledge_base(self):
        """Seed the knowledge base with initial FAQ data."""
        # Check if we already have data
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM knowledge_base;")
            count = cursor.fetchone()[0]
            if count > 0:
                print("Knowledge base already seeded.")
                return
                
            # Add seed data from the seed_data.sql file
            print("Seeding knowledge base...")
        except Exception as e:
            print(f"Error checking knowledge base: {e}")
        finally:
            cursor.close()
