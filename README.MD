# Investment Recommendations - A2UI POC

Application that demonstrates investment stock recommendations using Google's A2UI (Agent to UI) protocol. The system uses AI to generate investment recommendations and displays them through a web interface.

## Overview

This project consists of two main components:

- **Backend (Agent)**: A Python-based API that uses OpenAI's LLM to generate investment recommendations formatted according to the A2UI protocol
- **Frontend**: An Angular application that consumes the API and displays the investment recommendations

The backend generates structured UI components using the A2UI protocol, which allows for dynamic UI generation based on AI responses.

## Installation & Setup

### Prerequisites

- Python 3.12 or higher
- Node.js 18 or higher (LTS version recommended)
- npm or yarn
- OpenAI API key

### Backend (Agent) Setup

1. **Create a virtual environment and Install Python dependencies:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r agent/requirements.txt
```

2. **Configure OpenAI API Key:**
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Or export it as an environment variable:
```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

3. **Run the API server:**
```bash
python agent/api.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install Node.js dependencies:**
```bash
cd frontend
npm install
```

2. **Start the development server:**
```bash
npm start
```

The application will be available at `http://localhost:4200`

### Local Testing (Backend Only)

To test the backend without the frontend:

```bash
python agent/local_main.py
```

## License

This is a POC project for educational purposes.
