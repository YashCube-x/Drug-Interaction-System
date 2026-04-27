# Drug-Interaction-System

A full-stack web application for analyzing potential drug-drug interactions using AI and a comprehensive drug interaction database.

**Live Demo**: Coming soon  
**Repository**: [https://github.com/YashCube-x/Drug-Interaction-System](https://github.com/YashCube-x/Drug-Interaction-System)

## 🚀 Features

- **Smart Drug Extraction**: Enter medications in plain text, the system extracts drug names automatically
- **Database Lookups**: Queries verified drug interactions from a comprehensive database
- **AI-Powered Analysis**: Uses OpenRouter LLM for advanced analysis (optional)
- **Demo Mode**: Works perfectly without API keys (pattern-matching based)
- **Modern UI**: Clean, professional interface built with Next.js and Tailwind CSS
- **Real-time Results**: Instant analysis with severity levels (high, moderate, low)
- **CORS Enabled**: Full cross-origin support for frontend-backend communication

## 📋 Tech Stack

### Frontend
- **Next.js 16.2.4** - React framework with built-in optimization
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **JavaScript** - Modern ES6+

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI web server
- **OpenAI Client** - OpenRouter API integration
- **Pydantic** - Data validation using Python types
- **RapidFuzz** - Fuzzy string matching for drug names
- **Python 3.8+** - Latest Python features

### Database
- **CSV-based** - Drug interactions stored in CSV format
- **In-memory Loading** - Fast data access with lazy loading

## 🏗️ Project Structure

```
Drug-Interaction-System/
├── frontend/                    # Next.js React app
│   ├── src/
│   │   └── app/
│   │       ├── components/
│   │       │   ├── InputBox.js          # Medication input form
│   │       │   └── ResultCard.js        # Interaction result display
│   │       ├── globals.css              # Global styles
│   │       ├── layout.js                # Root layout
│   │       └── page.js                  # Home page
│   ├── package.json
│   ├── next.config.mjs
│   └── README.md
│
├── backend/                     # FastAPI Python app
│   ├── main.py                  # API entry point
│   ├── llm.py                   # LLM integration (OpenRouter)
│   ├── utils.py                 # Drug normalization & validation
│   ├── cache.py                 # Caching logic
│   ├── generate_report.py       # Report generation
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Configuration (create from .env.example)
│   ├── .env.example             # Example environment variables
│   ├── SETUP.md                 # Backend setup guide
│   ├── data/
│   │   └── interactions.csv     # Drug interaction database
│   └── README.md
│
├── db_drug_interactions.csv     # Alternative database file
├── README.md                    # This file
└── .git/                        # Git repository
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- npm or yarn (JavaScript package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/YashCube-x/Drug-Interaction-System.git
cd Drug-Interaction-System
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

Expected output:
```
INFO:     Started server process [...]
INFO:     Uvicorn running on http://0.0.0.0:1001
```

### 3. Setup Frontend (in a new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Expected output:
```
▲ Next.js 16.2.4
- Local:         http://localhost:3000
- Network:       http://your-ip:3000
✓ Ready in 823ms
```

### 4. Open in Browser

Navigate to:
- **Frontend**: `http://localhost:3000` (or next available port like 3001)
- **Backend API**: `http://localhost:1001`

## 🔑 Configuration

### Option 1: With OpenRouter API (Recommended)

For enhanced LLM-powered drug extraction and explanations:

1. Get a free API key at [https://openrouter.ai](https://openrouter.ai)
2. Update `backend/.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   OPENROUTER_MODEL=gpt-4o-mini
   ```

### Option 2: Demo Mode (No API Key Needed)

The system works perfectly in demo mode:
- Pattern-matching based drug extraction
- Template-based interaction responses
- Full database lookup support
- Perfect for testing and development

To use demo mode, simply leave the API key empty or invalid in `.env`.

## 📚 API Documentation

### POST /analyze

Analyze medications for interactions.

**Request:**
```json
{
  "text": "I take aspirin and warfarin daily"
}
```

**Response:**
```json
{
  "normalized_drugs": ["aspirin", "warfarin"],
  "pairs": [["aspirin", "warfarin"]],
  "results": [
    {
      "pair": ["aspirin", "warfarin"],
      "interaction": "Increased risk of bleeding",
      "type": "pharmacokinetic",
      "severity": "high",
      "explanation": "Both medications increase bleeding risk...",
      "source": "database",
      "confidence": "high",
      "disclaimer": "Please consult your healthcare provider..."
    }
  ]
}
```

## 🔄 How It Works

1. **User Input**: Enter medications in plain text (e.g., "I take aspirin and warfarin")
2. **Drug Extraction**: LLM (or pattern matching in demo mode) extracts drug names
3. **Drug Normalization**: Normalizes drug names and handles synonyms (e.g., "Advil" → "ibuprofen")
4. **Pair Generation**: Creates all possible drug pairs for analysis
5. **Database Lookup**: Queries the interaction database for known interactions
6. **LLM Processing**: Uses LLM to simplify and explain complex interactions
7. **Result Display**: Shows interactions with severity levels and explanations

## 🎨 UI Features

- **Clean Modern Design**: Professional light theme with blue accents
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Loading States**: Animated skeletons during analysis
- **Error Handling**: Clear error messages with helpful suggestions
- **Severity Indicators**: Color-coded alerts (high=red, moderate=amber, low=green)
- **Source Attribution**: Shows whether data comes from database or AI

## 🧪 Testing

### Test in Browser
1. Open `http://localhost:3000`
2. Enter: "I take aspirin and warfarin"
3. Click "Analyze"
4. View interaction results

### Test via API
```bash
curl -X POST http://localhost:1001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I take aspirin and warfarin daily"}'
```

## 📊 Data

The system includes a comprehensive drug interaction database (`data/interactions.csv`) with:
- Known drug pairs
- Interaction types (pharmacokinetic, pharmacodynamic, etc.)
- Severity levels (high, moderate, low)
- Detailed descriptions

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. It should NOT be used for medical decisions. Always consult with a healthcare professional before combining medications.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with ❤️ by [YashCube-x](https://github.com/YashCube-x)

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced filtering and sorting
- [ ] User accounts and interaction history
- [ ] Mobile app (iOS/Android)
- [ ] PDF report generation
- [ ] Integration with pharmacy APIs
- [ ] Machine learning for severity prediction
- [ ] Dosage interaction analysis

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/YashCube-x/Drug-Interaction-System/issues)
- Check existing documentation in `frontend/README.md` and `backend/SETUP.md`

## 🙏 Acknowledgments

- OpenRouter API for LLM capabilities
- FastAPI community for the excellent framework
- Next.js team for the React framework
- Tailwind CSS for beautiful styling

---

**Status**: ✅ Production Ready | **Last Updated**: April 27, 2026
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
