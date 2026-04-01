# ✍️ BeeBot: Your AI Writing Companion

BeeBot is a premium, minimalist AI writing workspace designed for effortless drafting, professional editing, and stylistic refinement. Built with a focus on high-performance streaming and executive-level typography, it serves as an elite assistant for writers, editors, and communication strategists.

![Screenshot](https://via.placeholder.com/1200x600/6366f1/ffffff?text=BeeBot+Writing+Assistant)

## ✨ Features

- **🚀 Real-Time Streaming**: Instant, token-by-token response generation with zero initial latency.
- **🧬 On-The-Fly Filtering**: Intelligent background reasoning (think tags) is stripped live, keeping your workspace clean and professional.
- **🖋️ Premium Typography**: A custom design system using **Inter** (weights 400-800) for UI/Content and **JetBrains Mono** for technical elements.
- **🛠️ Specialized Writing Modes**: Optimized for:
  - Professional Email Drafting
  - Essay Polishing & Structural Improvement
  - Creative Storytelling & Narrative Flow
  - Headline & Content Generation
- **📋 One-Click Export**: Rapid copy buttons for entire responses or individual code snippets.
- **📱 Responsive Minimalist UI**: A distraction-free, single-pane focus mode that adapts to your workflow.

## 🛠️ Technology Stack

- **Frontend**: Next.js, React, Lucide Icons, React-Markdown.
- **Backend**: FastAPI (Python), Httpx, Pydantic.
- **AI Model**: Sarvam-M (Optimized for long-form, high-quality generation).
- **Communication**: Server-Sent Events (SSE) for seamless streaming.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- Node.js 18+
- Sarvam AI API Key

### 2. Backend Setup
```bash
# Navigate to project root
cd aichatapp

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env and add your API key
echo "SARVAM_API_KEY=your_key_here" > backend/.env

# Start the server
python3 -m uvicorn backend.app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Open the App
Visit [http://localhost:3000](http://localhost:3000) to start writing!

## 📜 License
MIT License. Created by [Kiran](https://github.com/korrakiran).
