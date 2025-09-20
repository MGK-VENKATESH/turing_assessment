# Industrial & Machine Safety QA System

A question-answering system for industrial and machine safety documents that provides extractive answers with citations from PDF sources. The system uses hybrid retrieval combining vector embeddings and keyword scoring for improved accuracy.

## 📋 Overview

This project implements an intelligent QA system that:
- Processes industrial safety PDF documents
- Provides short, extractive answers with source citations
- Uses hybrid retrieval (vector similarity + keyword matching)
- Includes confidence thresholding to avoid low-quality answers
- Offers both baseline and enhanced reranking modes

## 🏗️ Project Structure

```
turing_assessment/
├── answerer.py              # Core logic: ingestion, chunking, embeddings, retrieval
├── api.py                   # FastAPI endpoint: POST /ask
├── evaluate.py              # Evaluation script with 8-question test suite
├── 8_questions.json         # Sample evaluation questions
├── sources.json             # PDF metadata (titles and URLs)
├── industrial-safety-pdfs/  # Collection of 20 PDF documents
├── results_table.md         # Generated evaluation results
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── venv/                   # Virtual environment (excluded from Git)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MGK-VENKATESH/turing_assessment.git
   cd turing_assessment
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify data files**
   - Ensure `industrial-safety-pdfs/` directory contains PDF files
   - Verify `sources.json` exists in project root

## 💻 Usage

### Starting the API Server

```bash
uvicorn api:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`

### Making Queries

#### Using cURL

**Simple safety question:**
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What are the main mechanical hazards associated with industrial machinery?",
    "k": 5,
    "mode": "hybrid"
  }'
```

**Complex maintenance question:**
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "What safety measures should be applied during robot maintenance?",
    "k": 5,
    "mode": "hybrid"
  }'
```

#### API Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | The question to ask |
| `k` | integer | 5 | Number of document chunks to retrieve |
| `mode` | string | "hybrid" | Retrieval mode: "baseline" or "hybrid" |

#### Response Format

```json
{
  "question": "What are the main mechanical hazards?",
  "answer": "The main mechanical hazards include crushing, cutting, shearing...",
  "source": "Machine Safety Guidelines - Section 2.1",
  "confidence": 0.87,
  "mode": "hybrid"
}
```

### Running Evaluation

Execute the comprehensive test suite:

```bash
python evaluate.py
```

This generates `results_table.md` comparing baseline vs. hybrid performance across 8 test questions.

## 🔧 Technical Features

### Core Components

- **Document Processing**: Automated PDF ingestion and paragraph-level chunking
- **Embeddings**: CPU-based vector embeddings using `all-MiniLM-L6-v2`
- **Hybrid Retrieval**: Combines semantic similarity with keyword matching
- **Confidence Scoring**: Threshold-based answer quality assessment
- **Extractive Answers**: Direct text extraction with source attribution

### Retrieval Modes

1. **Baseline Mode**: Pure vector similarity search
2. **Hybrid Mode**: Enhanced with keyword scoring and reranking

### Quality Assurance

- Fixed random seeds for reproducible results
- Comprehensive evaluation framework
- Source citation for all answers
- Confidence-based answer filtering

## 📊 Evaluation Results

The system is evaluated on 8 diverse safety questions covering:
- Mechanical hazards identification
- Safety protocols and procedures
- Maintenance best practices
- Risk assessment methodologies

Results are automatically generated in `results_table.md` showing:
- Answer accuracy comparison
- Source attribution quality
- Confidence score analysis
- Performance improvements with hybrid mode

## 🎯 Key Learnings

1. **Chunking Strategy**: Paragraph-level document splitting significantly improves retrieval precision
2. **Hybrid Approach**: Combining vector similarity with keyword matching enhances answer relevance
3. **CPU Efficiency**: Local embeddings eliminate API dependencies while maintaining performance
4. **Evaluation Framework**: Systematic testing enables measurable improvements
5. **Extractive Benefits**: Direct text extraction ensures factual accuracy and traceability

## 🔒 System Requirements

- **CPU-only processing**: No GPU requirements
- **Local embeddings**: No external API dependencies
- **Memory**: ~2GB RAM recommended for document processing
- **Storage**: ~100MB for documents and embeddings

## 📝 License

This project is developed for educational and research purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or issues, please open a GitHub issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- System information

---

**Note**: Large files including `venv/` and processed embeddings are excluded from version control to maintain repository efficiency.
