# Document Summarizer

A Streamlit application that uses LangChain and OpenAI's GPT-4o-mini to provide detailed summaries of documents and web articles.

## Features

- Upload documents in various formats (PDF, DOCX, TXT, CSV, XLSX)
- Summarize web content by providing a URL
- Generate comprehensive, well-structured summaries
- Download summaries for later reference

## Project Structure

```
document-summarizer/
├── app.py                  # Main application file
├── file_processors.py      # File processing functions
├── url_processor.py        # URL processing functions
├── summarizer.py           # Text summarization functionality
├── ui_components.py        # UI components and styling
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
```

## Installation

This project is recommended to run on Python 3.11.

### Setting Up Python 3.11 with UV

[UV](https://github.com/astral-sh/uv) is a fast Python package installer and environment manager that can also help manage Python versions.

1. **Install UV** (if you don't have it already):

   ```bash
   # Install with curl (macOS/Linux)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install with PowerShell (Windows)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Install with pip
   pip install uv
   ```

2. **Install Python 3.11 using uv**:

   You can install Python 3.11 using the following command:

   ```bash
   uv python install 3.11
   ```

   Once Python 3.11 is installed, run the following command to use it for the project:
   ```bash
   uv python pin 3.11
   ```

3. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/document-summarizer.git
   cd document-summarizer
   ```

4. **Create and activate a virtual environment with UV targeting Python 3.11**:

   ```bash
   # Create virtual environment with Python 3.11
   uv venv --python=3.11

   # On macOS/Linux
   source .venv/bin/activate

   # On Windows
   .\.venv\Scripts\activate
   ```

   Verify Python version:
   ```bash
   python --version  # Should output Python 3.11.x
   ```

5. **Install dependencies using UV**:

   ```bash
   uv pip install -r requirements.txt
   ```

   UV is significantly faster than pip for installing packages, so this should complete quickly.

### Option 2: Using Traditional Pip with Python 3.11

1. **Install Python 3.11** from [python.org](https://www.python.org/downloads/release/python-3115/) or using your system's package manager.

2. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/document-summarizer.git
   cd document-summarizer
   ```

3. **Create and activate a virtual environment**:

   ```bash
   # On macOS/Linux
   python3.11 -m venv venv
   source venv/bin/activate

   # On Windows
   py -3.11 -m venv venv
   .\venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app**:

   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and go to the displayed URL (typically http://localhost:8501)

3. **Using the app**:
   - Select either "Upload File" or "Enter URL" tab
   - Provide your document or URL
   - Enter your OpenAI API key
   - Click "Generate Summary"
   - View and download your summary

## OpenAI API Key

You'll need an OpenAI API key to use this application:

1. If you don't have an OpenAI account, sign up at [platform.openai.com](https://platform.openai.com/)
2. Generate an API key in your OpenAI dashboard
3. Enter this API key in the application when prompted

## How it works

1. The app extracts text from your document or URL
2. For longer documents, the text is split into manageable chunks
3. GPT-4o-mini processes each chunk and creates a summary
4. For multi-chunk documents, individual summaries are combined into a coherent final summary

## Dependencies

- streamlit: Web application framework
- langchain: Framework for LLM applications
- PyPDF2: PDF processing
- python-docx: DOCX processing
- pandas: Data processing (for spreadsheets)
- openpyxl: Excel file support

## Development

### Adding support for new file types

To add support for new file types, modify the `file_processors.py` file and add a new extraction function.

### Implementing different summarization strategies

To implement different summarization strategies, modify the `summarizer.py` file.

## Troubleshooting

### Python Version Issues

If you encounter errors related to Python version compatibility:

1. Verify your Python version:
   ```bash
   python --version
   ```

2. If it's not 3.11.x, recreate your virtual environment targeting Python 3.11:
   ```bash
   # With uv
   uv venv --python=3.11 --force
   ```

### Package Installation Issues

If you encounter issues installing packages:

1. Make sure your virtual environment is activated
2. Try updating UV to the latest version:
   ```bash
   pip install --upgrade uv
   ```
3. Install packages individually if there are conflicts:
   ```bash
   uv pip install streamlit langchain langchain-openai
   ```

## Privacy Note

Your OpenAI API key is used only for making requests to OpenAI and is not stored or logged anywhere.