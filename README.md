# Intelligent Parser 🚀

A high-performance document extraction platform powered by **Groq's Llama 4 Scout**. This application allows users to upload PDFs or images and instantly extract structured JSON data with extreme accuracy.

## 🌟 Key Features
- **Llama 4 Scout Integration**: Leveraging the latest multimodal 17B-16E model for superior document understanding.
- **Hybrid PDF Processing**: Automatically switches between text extraction and high-resolution vision rendering for optimal results.
- **Premium UI/UX**: Dark-themed, responsive dashboard with glassmorphism and smooth animations.
- **Strict Validation**: Enforced 10MB file limit and specific format constraints (PDF, JPG, PNG, WEBP).
- **Dynamic Mapping**: Automatically renders extracted JSON fields into a clean, human-readable results grid.

## 🛠 Tech Stack
- **Frontend**: React (Vite), Vanilla CSS (Custom Design System).
- **Backend**: Flask, OpenAI SDK (Groq Endpoint), PyMuPDF (PDF Processing).
- **Model**: `meta-llama/llama-4-scout-17b-16e-instruct`

## 🚀 Getting Started

### Backend Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment:
   Create a `.env` file in the root and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
3. Start the server:
   ```bash
   python src/backendCode.py
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Run the dev server:
   ```bash
   npm run dev
   ```

---

## 🔮 Future Roadmap (The "Chatbot" Evolution)

We aim to evolve this platform from a static extractor into an **Active Document Assistant**.

### 1. Document Chatbot (Chat-with-Doc)
- **Interactive QA**: Allow users to ask natural language questions about the uploaded document (e.g., "What is the total tax amount?" or "Is there a discount mentioned?").
- **Visual Grounding**: The AI will be able to point to specific areas of the image/PDF where it found the answer.

### 2. Multi-Page Context
- Support for complex, 50+ page documents using RAG (Retrieval-Augmented Generation) combined with Llama 4's 128K context window.

### 3. Historical Dashboard
- A database integration (PostgreSQL/Supabase) to save past extractions, allowing users to search and export history to Excel/CSV.

### 4. Template Learning
- User-defined custom extraction templates for specialized industry documents (medical reports, legal contracts, etc.).

---

## 📄 License
MIT License - Created with 💜 using Groq.
