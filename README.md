# Email Twin (Gmail AI Assistant)

A Google Workspace Add-on that generates personalized email responses using AI. The assistant learns your writing style and incorporates context from both email threads and PDF attachments to create natural, contextually-aware responses.

## Features

- 🎯 Learns and mimics your personal writing style
- 📧 Analyzes full email thread context
- 📎 Processes PDF attachments for relevant information
- ⚡ Real-time response generation
- 🔒 Secure and privacy-focused

## Tech Stack

- **Frontend**: Google Apps Script (Gmail Add-on)
- **Backend**: Python FastAPI deployed on Google Cloud Run
- **LLM**: OpenAI GPT-4o-mini
- **Vector Store**: LangChain + Chroma for PDF context retrieval
