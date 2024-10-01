-- Creazione del database
DROP DATABASE IF EXISTS My_Rag;
CREATE DATABASE My_Rag;
USE My_Rag;

-- Creazione della tabella 'ingested_documents'
DROP TABLE IF EXISTS ingested_documents;
CREATE TABLE ingested_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_name TEXT NOT NULL,
    document_text LONGTEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creazione della tabella 'embedded_contents' con chiave esterna verso 'ingested_documents'
DROP TABLE IF EXISTS embedded_contents;
CREATE TABLE embedded_contents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ingested_document_id INT,
    content_type TINYTEXT,
    tokenizer TINYTEXT,
    model TINYTEXT,
    normalizer TINYTEXT,
    binary_embedding LONGBLOB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ingested_document FOREIGN KEY (ingested_document_id)
        REFERENCES ingested_documents(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
