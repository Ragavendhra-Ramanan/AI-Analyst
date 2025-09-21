# AI Analyst - Investment Analysis Platform

AI Analyst is a sophisticated investment analysis platform that processes investor pitch documents and generates comprehensive investment analysis reports. The platform offers two main capabilities:

1. **Deal Note Generation** - Analyzes uploaded pitch documents and creates detailed investment memos
2. **Benchmark Analysis** - Compares companies against sector competitors using stored data

## 🚀 Features

- **PDF Processing**: Extract and analyze content from investor pitch decks
- **AI-Powered Analysis**: 12-section comprehensive investment analysis using Google Gemini
- **Competitive Benchmarking**: Compare companies against sector peers
- **Visualization**: Generate charts, heatmaps, and comparative analysis
- **PDF Report Generation**: Create professional investment reports
- **RESTful API**: FastAPI-based backend with Streamlit frontend

## 🏗️ Architecture

- **Backend**: FastAPI with Python 3.11+
- **Frontend**: Streamlit web interface
- **AI Services**: Google Vertex AI, Gemini, Vision API
- **Database**: Firestore for structured data storage
- **Storage**: Google Cloud Storage for file management
- **Visualization**: Matplotlib, Plotly, Seaborn

## 📋 Prerequisites

1. **Python 3.11 or higher**
2. **Google Cloud Platform account** with the following APIs enabled:
   - Vertex AI API
   - Vision API
   - Firestore API
   - Cloud Storage API
3. **Environment Variables** (see Configuration section)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ragavendhra-Ramanan/AI-Analyst.git
cd AI-Analyst
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

Or install individual dependencies:
```bash
pip install fastapi uvicorn streamlit google-cloud-aiplatform google-cloud-vision google-cloud-firestore google-cloud-storage google-generativeai pymupdf reportlab python-multipart python-dotenv langchain langchain-google-vertexai pillow matplotlib seaborn plotly pandas numpy
```

## 🔧 Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
# Google Cloud Configuration
PROJECT_ID=your-gcp-project-id
REGION=region
GCS_BUCKET=your-storage-bucket-name

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key

# Optional: Override default settings
FIRESTORE_COLLECTION=structured_investor_memos
```

### 2. Google Cloud Authentication

Set up Google Cloud credentials:

```bash
# Option 1: Service Account Key
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"

# Option 2: gcloud CLI authentication
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Create Required Buckets

```bash
# Create GCS bucket for file storage
gsutil mb gs://your-storage-bucket-name

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable storage.googleapis.com
```

## 🚀 Usage

### Option 1: Run Individual Services

#### Start the Backend API Server

```bash
cd backend/app
python main.py
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

#### Start the Frontend Interface

```bash
streamlit run frontend/app_interface.py
```

The Streamlit app will be available at `http://localhost:8501`

### Option 2: Run with UV (Recommended)

If you have `uv` installed:

```bash
# Start backend
uv run python backend/app/main.py

# In another terminal, start frontend
uv run streamlit run frontend/app_interface.py
```

## 📡 API Endpoints

### Core Endpoints

1. **Upload & Process Documents**
   ```
   POST /api/upload/
   ```
   Upload pitch documents (PDF) for RAG processing

2. **Generate Deal Note**
   ```
   POST /api/generate_memo/
   ```
   Generate comprehensive investment memo

3. **Benchmark Analysis**
   ```
   POST /api/benchmark/
   ```
   Create benchmark analysis report

### Example API Usage

```python
import requests

# Upload a PDF
files = {"file": open("pitch_deck.pdf", "rb")}
response = requests.post("http://localhost:8000/api/upload/", files=files)

# Generate deal note
response = requests.post("http://localhost:8000/api/generate_memo/")

# Download PDF
with open("deal_note.pdf", "wb") as f:
    f.write(response.content)
```

## 🖥️ Frontend Interface

The Streamlit interface provides an intuitive way to:

1. **Upload Files**: Support for PDF pitch decks
2. **Start Processing**: Automatic document analysis
3. **Generate Reports**: Create investment memos and benchmark analyses
4. **Download Results**: Get PDF reports directly

### Using the Interface

1. Open `http://localhost:8501` in your browser
2. Upload a PDF pitch deck
3. Click "Upload & Start Processing"
4. Once processing is complete, click "Generate Memo"
5. Download the generated investment report

## 🔍 Analysis Capabilities

### Deal Note Analysis (12 Sections)

1. **Team Overview** - Leadership and founding team analysis
2. **Problem Statement** - Market problems and pain points
3. **Solution** - Product/service solution and value proposition
4. **Differentiation** - Competitive advantages and unique factors
5. **Market Opportunity** - TAM/SAM analysis and market sizing
6. **Business Model** - Revenue streams and monetization strategy
7. **Traction** - Growth metrics and key milestones
8. **Product Architecture** - Technical infrastructure and capabilities
9. **Go-to-Market Strategy** - Sales and marketing approach
10. **Funding Details** - Investment rounds and financial status
11. **Risks & Mitigations** - Risk analysis and mitigation strategies
12. **Exit Potentials** - Exit opportunities and strategic options

### Benchmark Analysis Features

- **Competitive Positioning**: Compare against sector peers
- **Financial Metrics Analysis**: Revenue, CAC, LTV, margins
- **Visualization Suite**: Radar charts, heatmaps, bubble charts
- **Sector Benchmarks**: Industry-specific performance metrics
- **AI-Powered Insights**: Competitive advantages and recommendations

## 🗂️ Project Structure

```
AI-Analyst/
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── pyproject.toml
├── uv.lock
├── backend/
│   ├── extracted_prompt_template.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── generate_deal_note_pdf.py
│   │   ├── main.py               # FastAPI application
│   │   ├── vertex_config.py
│   │   ├── processors/           # File processors
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   └── pdf_processor.py
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── comprehensive_deal_note_prompt.py
│   │   │   └── multimodal_extraction_prompt.py
│   │   ├── router/               # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── generate_benchmark.py
│   │   │   ├── generate_deal_note.py
│   │   │   └── rag_file_upload.py
│   │   ├── services/             # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── gemini_api.py
│   │   │   ├── benchmark_creation/  # Benchmarking services
│   │   │   │   ├── __init__.py
│   │   │   │   ├── firestore_service.py
│   │   │   │   ├── gcp_service.py
│   │   │   │   ├── gemini_service.py
│   │   │   │   └── vision_service.py
│   │   │   ├── rag_agent/           # RAG and analysis agents
│   │   │   │   ├── __init__.py
│   │   │   │   ├── deal_note_agent_analyser.py
│   │   │   │   ├── deal_note_agent.py
│   │   │   │   ├── execute_deal_note_agent.py
│   │   │   │   ├── rag_config/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── rag_llm.py
│   │   │   │   │   ├── rag_models_config.py
│   │   │   │   │   └── rag_registry.py
│   │   │   │   └── tools/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── base_tool.py
│   │   │   │       ├── business_model_tool.py
│   │   │   │       ├── differentiation_tool.py
│   │   │   │       ├── exit_potential_tool.py
│   │   │   │       ├── funding_details_tool.py
│   │   │   │       ├── market_opportunity_tool.py
│   │   │   │       ├── market_strategy_tool.py
│   │   │   │       ├── problem_solution_tool.py
│   │   │   │       ├── problem_statement_tool.py
│   │   │   │       ├── product_architecture_tool.py
│   │   │   │       ├── risk_mitigation_tool.py
│   │   │   │       ├── team_overview_tool.py
│   │   │   │       └── traction_tool.py
│   │   │   └── vector_indexing/     # Document processing
│   │   │       ├── __init__.py
│   │   │       ├── chunking.py
│   │   │       ├── create_corpus.py
│   │   │       └── upload_to_gcs.py
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   └── store_raw_pitch.py
│   │   └── utils/                   # Utility functions
│   │       ├── __init__.py
│   │       ├── gcs_utils.py
│   │       └── helpers.py
│   ├── config/                      # Configuration management
│   │   ├── __init__.py
│   │   ├── gemini_config.py
│   │   └── settings.py
│   ├── data/                        # Data processing modules
│   │   ├── __init__.py
│   │   ├── analyzers.py
│   │   └── processors.py
│   ├── flows/                       # Workflow orchestration
│   │   └── orchestrators.py
│   └── visualizations/              # Chart and report generation
│       ├── charts.py
│       ├── comparisons.py
│       └── reports.py
└── frontend/
    └── app_interface.py            # Streamlit interface
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -e .
   
   # Check Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Google Cloud Authentication**
   ```bash
   # Verify authentication
   gcloud auth list
   gcloud config list project
   
   # Re-authenticate if needed
   gcloud auth application-default login
   ```

3. **Missing APIs**
   ```bash
   # Enable required Google Cloud APIs
   gcloud services enable aiplatform.googleapis.com vision.googleapis.com firestore.googleapis.com storage.googleapis.com
   ```

4. **Port Conflicts**
   ```bash
   # Use different ports if needed
   uvicorn main:app --host 0.0.0.0 --port 8001
   streamlit run frontend/app_interface.py --server.port 8502
   ```

### Error Messages

- **"Benchmarking services not available"**: Check Google Cloud credentials and API enablement
- **"Vision API not available"**: Ensure Vision API is enabled and credentials are configured
- **"Firestore not available"**: Check Firestore API enablement and database creation

## 🔗 Additional Resources

- [Google Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Firestore Documentation](https://cloud.google.com/firestore/docs)