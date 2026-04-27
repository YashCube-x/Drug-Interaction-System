# Backend Setup Guide

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

**On Windows (PowerShell):**
```bash
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Setting Up OpenRouter API (Optional but Recommended)

The system can work in two modes:

#### **Mode 1: With LLM (Recommended)**
For better drug extraction and AI-powered explanations:

1. **Get a Free API Key**
   - Go to [https://openrouter.ai](https://openrouter.ai)
   - Sign up for a free account
   - Navigate to Dashboard → Create API Key
   - Copy your API key

2. **Add to `.env` file**
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   OPENROUTER_MODEL=gpt-4o-mini
   ```

#### **Mode 2: Demo Mode (Works Without API Key)**
The system will automatically work in demo mode if:
- No API key is provided, OR
- API key is invalid

In demo mode:
- Uses pattern matching for drug extraction
- Returns template responses for drug interactions
- Database lookups still work normally
- Perfect for testing and development!

## Running the Server

```bash
python main.py
```

Expected output:
```
INFO:     Started server process [28000]
INFO:     Uvicorn running on http://0.0.0.0:1001
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The API will be available at:
- **Local**: `http://localhost:1001`
- **Network**: `http://your-ip:1001`

## Testing the API

### Using curl:
```bash
curl -X POST http://localhost:1001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I take aspirin and warfarin daily"}'
```

### Using Python:
```python
import requests

response = requests.post(
    "http://localhost:1001/analyze",
    json={"text": "I take aspirin and warfarin daily"}
)
print(response.json())
```

## API Endpoints

### POST /analyze

**Request:**
```json
{
  "text": "I take medication1 and medication2 daily"
}
```

**Response:**
```json
{
  "normalized_drugs": ["medication1", "medication2"],
  "pairs": [["medication1", "medication2"]],
  "results": [
    {
      "pair": ["medication1", "medication2"],
      "interaction": "...",
      "type": "pharmacokinetic",
      "severity": "high",
      "explanation": "...",
      "source": "database",
      "confidence": "high",
      "disclaimer": "..."
    }
  ]
}
```

## Troubleshooting

### Error: "User not found" (401 Unauthorized)
- Your API key is invalid or expired
- The system will automatically switch to demo mode
- Get a new key at [https://openrouter.ai](https://openrouter.ai)

### Error: "ModuleNotFoundError"
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

### Port 1001 Already in Use
- Change port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=YOUR_PORT)`

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── llm.py              # LLM integration (OpenRouter)
├── utils.py            # Drug normalization & validation
├── cache.py            # Caching logic
├── generate_report.py  # Report generation
├── requirements.txt    # Python dependencies
├── .env                # Configuration (API keys)
├── .env.example        # Example configuration
├── SETUP.md            # This file
└── data/
    └── interactions.csv # Drug interaction database
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | No | (empty) | Your OpenRouter API key |
| `OPENROUTER_MODEL` | No | `gpt-4o-mini` | LLM model to use |

## Next Steps

1. Start the backend server: `python main.py`
2. In another terminal, start the frontend: `cd ../frontend && npm run dev`
3. Open [http://localhost:3000](http://localhost:3000) or [http://localhost:3001](http://localhost:3001) in your browser

## Support

- Backend API runs on: `http://localhost:1001`
- Frontend runs on: `http://localhost:3000` (or next available port)
- CORS is enabled for localhost connections
