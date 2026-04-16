# 🏛️ Bharat Legal AI — Multilingual Indian Law Assistant

A multilingual AI-powered legal assistant that answers questions about **Indian laws and the Indian Constitution** using **voice or text queries** and provides **audio responses** in **10 Indian languages**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?logo=fastapi)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?logo=google)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)

---

## ✨ Features

### 🤖 AI-Powered Legal Responses
- **Retrieval-Augmented Generation (RAG)**: NLP pipeline retrieves relevant legal content, then Gemini AI generates context-aware responses
- **35+ legal entries** covering Indian Constitution, IPC, CrPC, Civil, Family, Labor, Consumer, and Cyber laws
- **Citations and references** to specific articles, sections, and acts

### 🌐 10 Indian Languages Supported
| Code | Language | Native |
|------|----------|--------|
| `en` | English | English |
| `hi` | Hindi | हिन्दी |
| `te` | Telugu | తెలుగు |
| `ta` | Tamil | தமிழ் |
| `kn` | Kannada | ಕನ್ನಡ |
| `ml` | Malayalam | മലയാളം |
| `bn` | Bengali | বাংলা |
| `mr` | Marathi | मराठी |
| `pa` | Punjabi | ਪੰਜਾਬੀ |
| `gu` | Gujarati | ગુજરાતી |

### 🎤 Speech-to-Text (Voice Input)
- **Web Speech API** integration for browser-based voice input
- Supports voice input in **all 10 Indian languages**
- Real-time transcription with animated waveform visualization
- Auto-sends voice queries after speech ends

### 🔊 Text-to-Speech (Audio Response)
- **gTTS (Google TTS)** for natural multilingual audio responses
- Server-side audio generation returned as base64 MP3
- Browser TTS fallback when server TTS is unavailable
- Listen button on every bot response

### 💬 Premium Chat Interface
- Glassmorphic dark theme with Indian tricolor (🇮🇳) accents
- Animated aurora background with floating blobs
- Quick-access topic suggestion chips
- Message actions: Listen (audio), Copy
- Voice recording with animated waveform
- Emergency helplines sidebar
- Fully responsive (mobile-first)

---

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)          Python Backend (FastAPI)
┌────────────────────┐          ┌─────────────────────────┐
│ Web Speech API     │──STT──→  │ POST /api/chat          │
│ (voice input)      │          │   ├─ Translation Service │
│                    │          │   ├─ NLP Pipeline (TF-IDF)│
│ Chat Interface     │──text──→ │   ├─ Gemini AI           │
│                    │          │   └─ Response Translation │
│ Audio Playback     │←─TTS──  │ POST /api/tts            │
│ (base64 MP3)       │          │   └─ gTTS Engine         │
│                    │          │ POST /api/translate       │
│ Language Selector  │          │ GET  /api/health          │
└────────────────────┘          └─────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/indian-legal-bot.git
cd indian-legal-bot

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Run Locally

```bash
python run.py
```

Open **http://localhost:8000/** in your browser.

### API Documentation

Visit **http://localhost:8000/docs** for interactive Swagger docs.

---

## 🌍 Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Set `GEMINI_API_KEY` in Vercel Environment Variables (Settings → Environment Variables).

---

## 📁 Project Structure

```
indian-legal-bot/
├── api/                          # Python backend
│   ├── __init__.py
│   ├── index.py                  # FastAPI app & endpoints
│   ├── legal_knowledge.py        # Legal knowledge base (35+ entries)
│   ├── nlp_pipeline.py           # TF-IDF retrieval pipeline
│   ├── ai_service.py             # Gemini AI response generation
│   ├── translation_service.py    # 10-language translation service
│   └── tts_service.py            # Text-to-Speech generation
├── public/                       # Frontend
│   ├── index.html                # Premium chat interface
│   ├── style.css                 # Glassmorphic design system
│   └── app.js                    # Client-side application (STT/TTS)
├── run.py                        # Local dev server script
├── requirements.txt              # Python dependencies
├── vercel.json                   # Vercel deployment config
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Submit a legal query and receive an AI response |
| `POST` | `/api/tts` | Convert text to speech (base64 MP3) |
| `POST` | `/api/translate` | Translate text between languages |
| `GET` | `/api/health` | Service health check |
| `GET` | `/api/languages` | List supported languages |

### Example: Chat Request
```json
POST /api/chat
{
  "query": "What is Article 21?",
  "language": "en"
}
```

### Example: Hindi Voice Query (TTS)
```json
POST /api/tts
{
  "text": "अनुच्छेद 21 आपके जीवन के अधिकार की रक्षा करता है।",
  "language": "hi"
}
```

---

## 📖 Legal Topics Covered

| Domain | Coverage |
|--------|----------|
| **Constitution** | Articles 14, 15, 19, 21, 21A, 22, 25, 32, 44, 370 |
| **Criminal (IPC)** | Sections 302, 304A, 307, 354, 376, 379, 420, 498A |
| **Procedures (CrPC)** | Sections 41, 125, 154, 436, 437, 438; FIR filing, Bail process |
| **Civil Law** | Contract Act, Property Rights, Civil Suit procedure |
| **Family Law** | Hindu Marriage Act, Divorce, Domestic Violence Act |
| **Labor Law** | Minimum Wages, EPF/ESI, POSH Act |
| **Consumer** | Consumer Protection Act 2019, Complaint filing |
| **Cyber Law** | IT Act 2000, Cyber crime reporting |
| **Rights** | RTI Act 2005 |

---

## ⚖️ Legal Disclaimer

This AI assistant provides **general legal information only** and should **not** be considered as legal advice. Always consult with qualified legal professionals for specific legal matters.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
