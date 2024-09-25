DROP DATABASE IF EXISTS My_Rag;
CREATE DATABASE My_Rag;
USE My_Rag;

DROP TABLE IF EXISTS ingested_documents;
CREATE TABLE ingested_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_name TEXT NOT NULL,
    document_text LONGTEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS embedded_contents;
CREATE TABLE embedded_contents(
	id INT AUTO_INCREMENT PRIMARY KEY,
    ingested_document_id INT,
    content_type TINYTEXT,
    tokenizer TINYTEXT,
    model TINYTEXT,
    normalizer TINYTEXT,
    binary_embedding BLOB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE embedded_contents
ADD CONSTRAINT fk_ingested_document
FOREIGN KEY (ingested_document_id)
REFERENCES ingested_documents(id)
ON DELETE CASCADE
ON UPDATE CASCADE;

DROP TABLE IF EXISTS indexed_contents;
CREATE TABLE indexed_contents(
	id INT AUTO_INCREMENT PRIMARY KEY,
    embedded_content_id INT,
    dimension INT,
    index_algorithm TINYTEXT,
    binary_indexing BLOB,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE indexed_contents
ADD CONSTRAINT fk_embedded_content
FOREIGN KEY (embedded_content_id)
REFERENCES embedded_contents(id)
ON DELETE CASCADE
ON UPDATE CASCADE;
