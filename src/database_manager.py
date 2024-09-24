import mysql.connector

class DatabaseManager:
    # Class constructor
    def __init__(self):
        self.host = "localhost" 
        self.user = "root" 
        self.password = "1234Ale!" 
        self.database = "My_Rag"
        self.conn = None
        self.cursor = None
    
    # Method to connect to the database
    def connect(self):
        try:
            # Connect to the database
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print("\n-> Connected to database successfully!")
        except mysql.connector.Error as err:
            print(f"\n-> Error: {err}")
    
    # Method to close the database connection
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("\n-> Connection closed.")

    # Method to write document names and contents to the database
    def save_documents(self, document_names, document_contents):
        query = """
            INSERT INTO ingested_documents (filename, content)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE content = VALUES(content)
        """
        
        # Create a list of tuples with (document_name, document_content)
        data = [(document_names[i], document_contents[i]) for i in range(len(document_names))]
        
        try:
            # Execute a batch insert/update in a single call
            self.cursor.executemany(query, data)
            self.conn.commit()  # Commit changes to the database
            print(f"\n-> Documents and contents saved successfully!")
        except mysql.connector.Error as err:
            print(f"\n-> Error saving documents and contents: {err}")

    # New method to save embeddings to the database
    def save_embeddings(self, ingested_titles, binary_embeddings):
        
        documents_ids = self.__get_document_ids(ingested_titles)

        query = """
            INSERT INTO embedded_documents (loaded_document_id, content_type, tokenizer, model, normalizer, binary_embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Prepare data for batch insert
        data = [
            (
                documents_ids[i],           # loaded_document_id
                "full_content",             # Type of content
                "all-MiniLM-L6-v2",         # Name of the tokenizer
                "sentence-transformers",    # Name of the model
                "L2-normalization",         # Normalization used
                binary_embeddings[i]        # Binary embedding
            )
            for i in range(len(documents_ids))
        ]

        try:
            self.cursor.executemany(query, data)
            self.conn.commit()
            print(f"\n-> Binary Embeddings saved successfully!")
        except mysql.connector.Error as err:
            print(f"\n-> Error saving Binary Embeddings: {err}")
            self.conn.rollback()
        finally:
            self.cursor.close()
    
    # Method to read documents names from the database
    def load_documents_names(self):
        # SQL query to select all filenames from the loaded_documents table
        query = "SELECT filename FROM ingested_documents"
        
        # Execute the query to retrieve the filenames
        self.cursor.execute(query)
        
        # Fetch all rows from the query result
        rows = self.cursor.fetchall()
        
        # Extract the filenames from the rows and store them in a list
        documents_names = [row[0] for row in rows]
        
        # Return the list of document names
        return documents_names

    # Method to load the content of multiple documents based on their filenames in one query
    def load_documents_contents(self, documents_names):
        # If the document_names list is empty, return an empty list
        if not documents_names:
            return []
        
        # Create the SQL query using the IN clause to search for multiple filenames
        format_strings = ','.join(['%s'] * len(documents_names))  # Create placeholders for the query
        query = f"SELECT content FROM ingested_documents WHERE filename IN ({format_strings})"
        
        # Execute the query with the list of document names
        self.cursor.execute(query, documents_names)
        
        # Fetch all the rows from the result
        rows = self.cursor.fetchall()
        
        # Extract only the content from each row and return it
        contents = [row[0] for row in rows]
        
        return contents
    
    def __get_document_ids(self, document_names):
        # If the document_names list is empty, return an empty list
        if not document_names:
            return []

        # Create the SQL query using the IN clause to search for multiple document names
        format_strings = ','.join(['%s'] * len(document_names))  # Create placeholders for the query
        query = f"SELECT id FROM ingested_documents WHERE filename IN ({format_strings})"
        
        try:
            # Execute the query with the list of document names
            self.cursor.execute(query, document_names)
            
            # Fetch all document IDs from the result
            rows = self.cursor.fetchall()
            
            # Extract only the IDs from the results
            document_ids = [row[0] for row in rows]
            
            return document_ids

        except mysql.connector.Error as err:
            print(f"Error retrieving document IDs: {err}")
            return []
