# Drug-Drug Interaction Analyzer

A full-stack AI-powered system that detects potential drug-drug interactions from free-text input.

## Architecture

```
User Input (free text)
       │
       ▼
  FastAPI Backend
       │
       ├── LLM extracts drug names (OpenRouter API)
       ├── Normalize (lowercase, synonyms, fuzzy match)
       ├── Validate (deduplicate, ensure ≥ 2 drugs)
       ├── Generate pairs (nC2)
       ├── Check in-memory cache
       ├── Lookup in CSV dataset
       │     ├── FOUND → LLM simplifies description (confidence: HIGH)
       │     └── NOT FOUND → LLM generates explanation (confidence: LOW + disclaimer)
       ├── Rank by severity > confidence
       └── Return JSON results
               │
               ▼
      Next.js Frontend (Tailwind CSS)
```

## Project Structure

```
drug-interaction-system/
├── backend/
│   ├── main.py              # FastAPI app + /analyze endpoint
│   ├── llm.py               # OpenRouter LLM calls
│   ├── utils.py             # Normalization, validation, pair gen, DB lookup
│   ├── cache.py             # In-memory cache
│   ├── data/
│   │   └── interactions.csv # Drug interaction dataset
│   ├── requirements.txt
│   └── .env                 # OPENROUTER_API_KEY
│
├── frontend/
│   └── src/app/
│       ├── page.js          # Main page
│       ├── layout.js        # Root layout
│       ├── globals.css      # Global styles
│       └── components/
│           ├── InputBox.js   # Text input + analyze button
│           └── ResultCard.js # Interaction result card
│
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai/) API key

### 1. Backend Setup

```bash
cd drug-interaction-system/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Edit .env and replace "your_openrouter_api_key_here" with your actual key
notepad .env

# Run the server
python main.py
```

The backend will start at `http://localhost:8000`.  
API docs available at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd drug-interaction-system/frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

The frontend will start at `http://localhost:3000`.

### 3. Usage

1. Open `http://localhost:3000` in your browser
2. Type a sentence mentioning at least 2 drugs, e.g.:  
   *"I'm taking Warfarin and Aspirin daily"*
3. Click **Analyze Interactions**
4. View results with severity levels, explanations, and confidence scores

## API Reference

### POST `/analyze`

**Request:**
```json
{
  "text": "I am taking Warfarin and Aspirin"
}
```

**Response:**
```json
{
  "detected_drugs": ["Warfarin", "Aspirin"],
  "normalized_drugs": ["warfarin", "aspirin"],
  "pairs": [["warfarin", "aspirin"]],
  "results": [
    {
      "pair": ["warfarin", "aspirin"],
      "interaction": "Aspirin increases the anticoagulant effect of Warfarin",
      "type": "pharmacodynamic",
      "severity": "high",
      "explanation": "...",
      "confidence": "high",
      "source": "database",
      "disclaimer": null
    }
  ]
}
```

## Environment Variables

| Variable             | Description              | Required |
| -------------------- | ------------------------ | -------- |
| `OPENROUTER_API_KEY` | Your OpenRouter API key  | ✅        |

## Tech Stack

- **Backend:** Python, FastAPI, Pandas, RapidFuzz, OpenAI SDK (OpenRouter)
- **Frontend:** Next.js 15, Tailwind CSS, Axios
- **LLM:** Meta Llama 3.1 8B (via OpenRouter, free tier)
