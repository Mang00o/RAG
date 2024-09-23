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
        print(f"Documents saved successfully")
    
    # Method to read document names from the database
    def load_documents(self):
        query = "SELECT filename FROM loaded_documents"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        document_names = [row[0] for row in rows]
        print(f"Documents loaded successfully")
        return document_names
    
    def save_content(self, document_name, content):
        query = "UPDATE loaded_documents SET content = %s WHERE filename = %s"
        try:
            self.cursor.execute(query, (content, document_name))
            self.conn.commit()  # Salva i cambiamenti nel database
            print(f"Content for {document_name} saved successfully!")
        except mysql.connector.Error as err:
            print(f"Error saving content for {document_name}: {err}")

    def load_content(self, document_name):
        query = "SELECT content FROM loaded_documents WHERE filename = %s"
        self.cursor.execute(query, (document_name,))
        result = self.cursor.fetchone()  # Ritorna una singola riga
        if result:
            return result[0]  # Il contenuto è il primo (e unico) elemento della riga
        else:
            print(f"No content found for {document_name}")
            return None
