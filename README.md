# 🤖 Multi-Provider PDF RAG Chatbot

A production-ready, high-performance RAG (Retrieval-Augmented Generation) Chatbot that allows you to chat with your PDF documents using multiple AI providers including **OpenAI**, **Claude**, **Gemini**, and **OpenRouter**.

## 🌟 Features
- **Multi-Provider Support**: Switch between OpenAI, Claude (Anthropic), Gemini (Google), and OpenRouter seamlessly.
- **Free Model Optimized**: Pre-configured with high-quality free models from OpenRouter (Qwen & Nemotron).
- **Intelligent RAG**: Keyword-based retrieval for high-accuracy context selection from PDF documents.
- **Premium UI**: Modern Streamlit interface with a clean, responsive design and persistence indicators.
- **Full Privacy**: PDF text is processed locally and context is sent securely to your selected AI provider.

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/pdf-rag-chatbot.git
   cd pdf-rag-chatbot
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   OPENROUTER_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   OPENAI_API_KEY=your_key
   ANTHROPIC_API_KEY=your_key
   ```

## 🚀 Running the App
Launch the Streamlit dashboard:
```bash
streamlit run app.py
```

## 📂 Project Structure
- `app.py`: Main Streamlit application and RAG orchestrator.
- `requirements.txt`: Python dependencies.
- `.env.template`: Template for required API keys.
- `.gitignore`: Standard exclusions for Python and Streamlit.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
MIT License - see the LICENSE file for details.
