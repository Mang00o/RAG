import subprocess

class Generating:

    def __init__(self, pdf_texts, pdf_filenames):
        # Store PDF texts and filenames
        self.pdf_texts = pdf_texts
        self.pdf_filenames = pdf_filenames

    def generate_response_with_ollama(self, query, documents):
        # Build the prompt to send to Ollama
        docs_text = " ".join([self.pdf_texts[self.pdf_filenames.index(doc)] for doc, _ in documents])[:1000]  # Take only the first 1000 characters
        
        # Construct the prompt for Ollama
        prompt = f"Question: {query}\n\nDocuments:\n{docs_text}"
        
        # Run the `ollama run codellama` command inside WSL with UTF-8 encoding
        process = subprocess.Popen(['wsl', 'ollama', 'run', 'codellama'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        
        # Send the prompt and retrieve the response
        stdout, stderr = process.communicate(input=prompt)
        
        if stderr:
            print(f"Error: {stderr}")
        
        return stdout.strip()  # Return Ollama's response
