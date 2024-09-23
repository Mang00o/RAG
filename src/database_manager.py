import mysql.connector

class DatabaseManager:
    # Class constructor
    def __init__(self):
        self.host = "localhost", 
        self.user = "root", 
        self.password = "1234Ale!", 
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
            print("Connected to database successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    # Method to close the database connection
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection closed.")
    
    # Method to write documents names to the database
    def save_documents_names(self, documents_names):
        # SQL query to insert document names into the loaded_documents table
        query = "INSERT INTO loaded_documents (filename) VALUES (%s)"
        
        # Create a list of tuples, each containing a single document_name
        data = [(doc,) for doc in documents_names]
        
        try:
            # Execute the query for all documents in a single call
            self.cursor.executemany(query, data)
            self.conn.commit()  # Commit the changes to the database
            print(f"Documents saved successfully")
        except mysql.connector.Error as err:
            print(f"Error saving documents: {err}")
    
    # Method to read documents names from the database
    def load_documents_names(self):
        # SQL query to select all filenames from the loaded_documents table
        query = "SELECT filename FROM loaded_documents"
        
        # Execute the query to retrieve the filenames
        self.cursor.execute(query)
        
        # Fetch all rows from the query result
        rows = self.cursor.fetchall()
        
        # Extract the filenames from the rows and store them in a list
        documents_names = [row[0] for row in rows]
        
        # Return the list of document names
        return documents_names

    # Method to write documents contents to the database
    def save_documents_contents(self, document_names, document_contents):
        query = "UPDATE loaded_documents SET content = %s WHERE filename = %s"
        
        # Create a list of tuples containing (content, document_name)
        data = [(document_contents[i], document_names[i]) for i in range(len(document_names))]
        
        try:
            # Query all documents in a single call
            self.cursor.executemany(query, data)
            self.conn.commit()  # Save changes to database
            print(f"Contents saved successfully!")
        except mysql.connector.Error as err:
            print(f"Error saving contents: {err}")

    # Method to load the content of multiple documents based on their filenames in one query
    def load_documents_content(self, documents_names):
        # If the document_names list is empty, return an empty list
        if not documents_names:
            return []
        
        # Create the SQL query using the IN clause to search for multiple filenames
        format_strings = ','.join(['%s'] * len(documents_names))  # Create placeholders for the query
        query = f"SELECT filename, content FROM loaded_documents WHERE filename IN ({format_strings})"
        
        # Execute the query with the list of document names
        self.cursor.execute(query, documents_names)
        
        # Fetch all the rows from the result
        rows = self.cursor.fetchall()
        
        # Create a dictionary to map filenames to content
        content_dict = {row[0]: row[1] for row in rows}
        
        # Return the content in the same order as the document_names list
        contents = [content_dict.get(name, None) for name in documents_names]
        
        return contents


