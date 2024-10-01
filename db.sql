-- Creazione del database
DROP DATABASE IF EXISTS My_Rag;
CREATE DATABASE My_Rag;
USE My_Rag;

-- Creazione della tabella 'ingested_documents'
DROP TABLE IF EXISTS ingested_pdfs;
CREATE TABLE ingested_pdfs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pdf_name TEXT NOT NULL,
    pdf_text LONGTEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
