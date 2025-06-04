# PDF Question-Answering Pipeline

## Features
- Upload and process multiple PDFs
- Chunk documents and generate embeddings
- Store and search embeddings with Milvus
- Semantic QA using LangChain + OpenAI/HuggingFace

## Setup
1. Clone this repo and enter the directory.
2. Copy `.env.example` to `.env` and fill in your OpenAI API key.
3. Start Milvus:
   ```sh
   docker-compose up -d
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Place your PDFs in the `pdfs/` directory.
6. Run the pipeline:
   - As script: `python pdf_qa.py`
   - As notebook: Open `pdf_qa.ipynb` in Jupyter

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `MILVUS_HOST`: Milvus host (default: localhost)
- `MILVUS_PORT`: Milvus port (default: 19530)

## Milvus
- Self-hosted via Docker Compose (see `docker-compose.yml`)
- Access Milvus at `localhost:19530`

## References
- [LangChain Docs](https://python.langchain.com/)
- [Milvus Docs](https://milvus.io/docs/)
- [OpenAI API](https://platform.openai.com/docs/api-reference/embeddings)
