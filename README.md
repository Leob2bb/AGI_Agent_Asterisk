# ✨ DreamInsight 🧠

<p align="center">
  <img src="https://github.com/user-attachments/assets/31b25270-fa6f-46cd-9f75-d6dc0b8d7a08" alt="DreamInsights Banner" width="20%" />
</p>

<p align="center">
  
  🚀 <a href="https://dreamsinsight.netlify.app/">Live Demo → dreamsinsight.netlify.app</a>
</p>

---

## 📖 Project Overview
### 🔍 What Are Your Dreams Telling You?
**DreamInsight** is a dream interpretation platform that analyzes user-submitted dream journals to provide psychological insights and personalized feedback.


## 📌 Key Features of DreamInsight

### 🔑 Login System
- Users can register and log in securely.
<p align="center">
  <img src="https://github.com/user-attachments/assets/4a7cf87f-6dcb-4841-9d8f-4fce25428e6e" width="280"/>
  <img src="https://github.com/user-attachments/assets/0fc7b3a8-ede7-4d77-9239-dc8868f8796f" width="330"/>
</p>

### 📓 Dream Input System
- Users can upload dream journals via text or file.
- All dream entries can be viewed and managed within the platform.
<p align="center">
  <img src="https://github.com/user-attachments/assets/a2ad2474-81ea-4743-9ea4-377a30509979" width="280"/>
  <img src="https://github.com/user-attachments/assets/4f28c24f-cf5e-4a28-9922-6e7111698bef" width="370"/>
</p>

### 🧬 Personalized Psychological Feedback
- The system automatically analyzes psychological patterns within the dreams and provides tailored feedback.
<p align="center">
  <img src="https://github.com/user-attachments/assets/c3065782-d64e-4487-86fa-6c204342f8a6" width="350"/>
</p>

### 🧵 Interactive History-based Conversations
- Users can continue conversations with the AI chatbot based on previous dream analysis results.
<p align="center">
  <img src="https://github.com/user-attachments/assets/63f5e8d2-754d-4130-9286-244cce370af3" width="350"/>
</p>

## 🪛 Technical Highlights of DreamInsight

- 🔍 **RAG-based Dream Interpretation System**  
  Retrieves relevant academic papers from Qdrant using user dream data and generates interpretation with LLM.  
  → Retrieval-Augmented Generation structure

- 📄 **Automated PDF Dream Embedding Pipeline**  
  Converts uploaded dream PDFs into text, chunks the text, embeds it using Upstage API, and stores it in Qdrant.  
  → PDF → Text → Chunk → Vector → Qdrant

- 💬 **Emotion & Symbol/Intent Analysis via API**  
  Integrates external APIs to tag emotional tone and extract symbolic elements from dreams.  
  → Emotion tagging + Symbolic keyword extraction used as reasoning for interpretation

- 🤖 **LLM-Based Interpretation Module**  
  Combines emotion/symbol data and retrieved paper vectors to generate interpretations using psychological theories (CBT, Freud, Jung, etc.)

- 💾 **Qdrant-based Vector Storage with Metadata**  
  All vectors include metadata such as `title`, `source`, and `chunk_id` to support grouping and post-processing.  
  → Enables emotional analysis, summarization, and comparison

- 🗂 **Interpretation History DB & Version Control**  
  All generated results are stored per user with like/dislike feedback. Conversations can continue and evolve with user questions.

- 👍 **User Feedback System**  
  Users provide simple like/dislike responses through the UI, which are saved to the DB and used to improve future interpretations.

## 🧪 DreamInsight System Architecture

1. User dream input  
2. Data storage and preprocessing (backend)  
3. Emotion/symbol analysis and vector embedding  
4. LLM-based interpretation generation  
5. History-based interaction and response feedback


## ⚙️ Tech Stack
| Area | Technology |
|------|------------|
| Frontend | React |
| Backend | Flask |
| Vector Database | QdrantVectorStore |
| Embedding | Upstage Embedding API |
| RAG | LangChain |
| Others | SQLite, Document Parser, Solar Pro LLM |

## 🚀 Live Demo
https://dreamsinsight.netlify.app/


## 📬 Contact
- Email: Minkyu Kim - leo437782@yonsei.ac.kr
