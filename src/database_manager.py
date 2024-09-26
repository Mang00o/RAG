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
    def save_documents_ingestions(self, document_names, document_contents):
        if not document_names:
            return  # Exit if lists are empty
        
        query = """
            INSERT INTO ingested_documents (document_name, document_text)
            VALUES (%s, %s)
        """

        # Create a list of tuples with (document_name, document_content)
        data = [
            (
                document_names[i], 
                document_contents[i]
            ) 
            for i in range(len(document_names))
        ]
        
        self.__write_to_db(query, data, "Documents and contents")

    # Method to save embeddings to the database
    def save_contents_embeddings(self, ingested_documents_names, binary_contents_embeddings):
        if not ingested_documents_names:
            print("\n-> No embeddings to save.")
            return  # Exit if lists are empty
        
        query = """
            INSERT INTO embedded_contents (ingested_document_id, content_type, tokenizer, model, normalizer, binary_embedding)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        documents_ids = self.__get_ingested_documents_ids(ingested_documents_names)

        # Prepare data for batch insert
        data = [
            (
                documents_ids[i],           # loaded_document_id
                "full_content",             # Type of content
                "all-MiniLM-L6-v2",         # Name of the tokenizer
                "sentence-transformers",    # Name of the model
                "L2-normalization",         # Normalization used
                binary_contents_embeddings[i]        # Binary embedding
            )
            for i in range(len(documents_ids))
        ]

        self.__write_to_db(query, data, "Binary Embedding")

    # Method to save indexings to the database
    def save_indexings(self, document_names, binary_indexings):
        query = """
            INSERT INTO indexed_contents (embedded_content_id, dimension, index_algorithm, binary_indexing)
            VALUES (%s, %s, %s, %s)
        """

        contents_ids = self.__get_embedded_contents_ids(document_names)

        data = [
            (
                contents_ids[i],        # loaded_document_id
                384,                    # indexing dimension
                "IndexFlatL2",          # Indexing algorith used
                binary_indexings[i]     # Binary Indexing
            )
            for i in range(len(contents_ids))
        ]

        self.__write_to_db(query, data, "Binary Indexing")
    
    def __write_to_db(self, query, data, object_description):
        try:
            # Execute a batch insert/update in a single call
            self.cursor.executemany(query, data)
            self.conn.commit()  # Commit changes to the database
            print(f"\n-> {object_description} saved successfully!")
        except mysql.connector.Error as err:
            print(f"\n-> Error saving {object_description}: {err}")
            self.conn.rollback()  # Rollback in case of error

    def __get_ingested_documents_ids(self, document_names):
        # If the document_names list is empty, return an empty list
        if not document_names:
            return []

        # Create the SQL query using the IN clause to search for multiple document names
        format_strings = ','.join(['%s'] * len(document_names))  # Create placeholders for the query
        query = f"SELECT id FROM ingested_documents WHERE document_name IN ({format_strings})"
        
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
        
    def __get_embedded_contents_ids(self, document_names):
        # Create the SQL query using the IN clause to search for multiple document names
        format_strings = ','.join(['%s'] * len(document_names))  # Create placeholders for the query

        query = f"""
            SELECT id 
            FROM embedded_contents 
            WHERE ingested_document_id IN (
                SELECT id 
                FROM ingested_documents 
                WHERE document_name IN ({format_strings})
            )
        """
        
        try:
            # Execute the query with the list of document names
            self.cursor.execute(query, document_names)
            # Fetch all content IDs from the result
            rows = self.cursor.fetchall()
            # Extract only the IDs from the results
            contents_ids = [row[0] for row in rows]
            
            return contents_ids

        except mysql.connector.Error as err:
            print(f"Error retrieving content IDs: {err}")
            return []

    # Method to read documents names from the database
    def load_documents_names(self):
        # SQL query to select all filenames from the loaded_documents table
        query = "SELECT document_name FROM ingested_documents"
        
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
        
        documents_ids = self.__get_ingested_documents_ids(documents_names)

        # Create the SQL query using the IN clause to search for multiple filenames
        format_strings = ','.join(['%s'] * len(documents_ids))  # Create placeholders for the query
        query = f"SELECT document_text FROM ingested_documents WHERE document_name IN ({format_strings})"
        
        # Execute the query with the list of document names
        self.cursor.execute(query, documents_names)
        
        # Fetch all the rows from the result
        rows = self.cursor.fetchall()
        
        # Extract only the content from each row and return it
        contents = [row[0] for row in rows]
        
        return contents
    
    # Method to retrieve all binary indices from the database
    def load_all_indices(self):
        query = "SELECT binary_indexing FROM indexed_contents"
        
        try:
            # Execute the query
            self.cursor.execute(query)
            
            # Fetch all the rows from the query result
            rows = self.cursor.fetchall()
            
            # Extract the binary indexing from each row
            indices = [row[0] for row in rows]
            
            return indices

        except mysql.connector.Error as err:
            print(f"Error retrieving indices: {err}")
            return []

