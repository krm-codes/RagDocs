# RAGDocs

This is a Python application. Follow the steps below to set it up after cloning the repository.

## Installation

### 1. Clone the repository

```sh
git clone 
cd <repository-name>
```

### 2. Create and activate a virtual environment (optional but recommended)

#### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

## Running the Application

```sh
streamlit run app.py
```

## Environment Variables

The app requires environment variables, create a `.env` file in the root directory and add your variables:

```sh
OPENAI_API_KEY=your_key
OLLAMA_BASE_URL=http://localhost:11434
```

## Deactivating the Virtual Environment

To deactivate the virtual environment, run:

```sh
deactivate
```

## Notes

- Make sure you have Python installed.
- If you encounter issues, ensure you have the necessary permissions or try running commands with `python3` instead of `python`.

```
