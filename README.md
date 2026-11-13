# TravelMate — Travel & Tourism RAG Chatbot

A Retrieval-Augmented Generation chatbot that answers questions about Telangana tourism using a local document knowledge base.

## Features
- Loads PDF, TXT and Markdown documents
- Splits source text into overlapping chunks
- Generates Gemini embeddings
- Stores vectors and metadata in ChromaDB
- Retrieves the most relevant chunks for each question
- Uses Gemini to generate answers grounded in retrieved context
- Streamlit chat interface with retrieved-source display

## RAG architecture
Document Loading → Text Splitting → Gemini Embeddings → ChromaDB Vector Database → Retriever (Top-K) → Gemini LLM → Final Response

## Setup (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file by copying `.env.example`, then add your Google AI Studio API key:

```env
GOOGLE_API_KEY=your_actual_key
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=gemini-embedding-001
```

Never commit `.env` or API keys to GitHub.

## Add knowledge documents
Put trusted tourism PDFs, TXT or Markdown files inside `data/`. A starter Telangana tourism guide is included. For reliable information, use official sources and record their URLs in the documents.

## Run

```bash
streamlit run app.py
```

The first run creates embeddings and persists the vector database in `chroma_db/`. Use **Rebuild knowledge base** after changing source documents.

## Test questions
- What are the main attractions in Hyderabad?
- What is Charminar known for?
- What are some heritage attractions in Warangal?
- Which places are mentioned as nature attractions?
- Does the knowledge base provide current ticket prices?

## Limitations
- Answers are limited to the ingested documents.
- Opening times, prices, transport and availability can change; verify them with official tourism sources.
- This is an educational prototype, not a live booking service.

## Data sources
- Telangana Tourism: https://tourism.telangana.gov.in/
- Telangana Tourism — Hyderabad: https://www.tourism.telangana.gov.in/destinations/hyderabad
- Telangana Tourism — Warangal: https://www.tourism.telangana.gov.in/destinations/warangal
- Incredible India — Telangana: https://www.incredibleindia.gov.in/en/telangana
- Telangana State Portal — Tourism: https://www.telangana.gov.in/telangana-tourism/
