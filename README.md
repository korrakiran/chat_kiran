# BeeBot - Premium AI Chat App

A full-stack AI chat application inspired by ChatGPT, featuring real-time streaming, multimodal processing (OCR/PDF), and persistent memory.

## Tech Stack
- **Backend:** FastAPI (Python) - *Vercel Deployment Compatibility Added*
- **Frontend:** Next.js (React) + Lucide Icons
- **Database:** Hosted PostgreSQL (e.g., **Neon.tech** or **Supabase**) - *Recommended for Vercel*
- **AI Engine:** Sarvam AI (sarvam-105b)
- **OCR:** Tesseract + PyMuPDF

## Project Structure
```text
/
├── backend/            # FastAPI - Backend functions
├── frontend/           # Next.js - Client application
└── README.md
```

## Getting Started

### 1. Database
Instead of Docker, use a hosted database like **Neon.tech** or **Supabase**. Get your `DATABASE_URL` from their dashboards.

### 2. Backend Setup
1. Navigate to `/backend`.
2. Add your `SARVAM_API_KEY` and `DATABASE_URL` to a `.env` file.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start locally:
```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup
1. Navigate to `/frontend`.
2. Update the API URL in your components or environment if needed.
3. Run the development server:
```bash
npm run dev
```

## Vercel Deployment
The project is structure-ready for Vercel:
1. **Frontend**: Deploy with `npm run build`.
2. **Backend**: Add `vercel.json` as provided, connect to your hosted PostgreSQL via environment variables.

## Key Features
- **SSE Streaming:** Real-time token progressive rendering.
- **Multimodal Uploads:** Drag-and-drop Images/PDFs for automated context extraction.
- **Memory Layer:** User preferences and past conversation context injected into prompts.
- **Modern UI:** Glassmorphic design with a premium feel and smooth animations.

## Environment Variables (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/aichatapp
GOOGLE_CLIENT_ID=your_id
GOOGLE_CLIENT_SECRET=your_secret
SARVAM_API_KEY=your_key
JWT_SECRET=your_jwt_secret
```
