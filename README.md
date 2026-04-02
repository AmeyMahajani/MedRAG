## MedRAG

Production-style Flask RAG assistant with a minimal frontend.

### Project structure

```text
.
|-- app.py
|-- requirements.txt
|-- .env.example
|-- src/
|   `-- medrag/
|       |-- __init__.py
|       |-- services/
|       |   |-- __init__.py
|       |   |-- embeddings.py
|       |   |-- prompt.py
|       |   `-- rag.py
|       `-- web/
|           |-- routes.py
|           |-- static/
|           |   `-- style.css
|           `-- templates/
|               `-- chat.html
`-- tests/
	`-- test_flow.py
```

### Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create env file:

```bash
cp .env.example .env
```

4. Add your keys in `.env`.

### Run

```bash
python app.py
```

Open `http://127.0.0.1:8080`.

### Test flow

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The tests run in `MEDRAG_FAKE_MODE=true`, so they validate full HTTP flow without external API calls.
