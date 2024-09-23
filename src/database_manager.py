import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
    
    # Method to connect to the database
    def connect(self):
        try:
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
    
    # Method to write document names to the database
    def save_documents(self, document_names):
        for doc in document_names:
            query = "INSERT INTO loaded_documents (filename) VALUES (%s)"
            try:
                self.cursor.execute(query, (doc,))
            except mysql.connector.Error as err:
                print(f"Error inserting {doc}: {err}")
        self.conn.commit()
        print(f"Documents saved successfully: {document_names}")
    
    # Method to read document names from the database
    def load_documents(self):
        query = "SELECT filename FROM loaded_documents"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        document_names = [row[0] for row in rows]
        print(f"Loaded documents: {document_names}")
        return document_names
