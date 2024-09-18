# RAG

Implementazione RAG (Retrieval-Augmented Generation) per il tirocinio.

## Tecnologie

Il progetto utilizza le seguenti tecnologie:

- **Python**: Linguaggio principale per l'implementazione.
- **Ollama**: Utilizzato per la gestione e l'interazione con i modelli locali.

## Installazione

Queste istruzioni ti guideranno attraverso la configurazione dell'ambiente di sviluppo per poter lavorare al progetto.

### Prerequisiti

Assicurati di avere installato:
- **Python 3.8 o superiore**
- **pip** (il gestore di pacchetti Python)
- **Olama**
- **Documenti** caricati nella cartella /Documents

### Clonare il progetto

```bash
git clone https://github.com/tuo-repo/progetto.git
cd progetto
```

### Creare ambiente virtuale

```bash
python -m venv venv
```

#### Attivazione Su macOS/Linux:

```bash
source venv/bin/activate
```

#### Attivazione Windows:

```bash
venv\Scripts\activate
```

### Installare le dipendeze

```bash
pip install -r requirements.txt
```

### Eseguire il progetto

```bash
python .\src\main.py
```

### In caso di aggiunta di librerie eseguire

```bash
pip freeze > requirements.txt
```


## Evoluzione

Ecco link utili per approfondire future evoluzioni:

- [Python/Flash on DDEV](https://ddev.readthedocs.io/en/stable/users/quickstart/#pythonflask-experimental)
- [TryChroma](https://www.trychroma.com/)
- [LangChain](https://js.langchain.com/v0.1/docs/modules/data_connection/)
