# Medical Document Processing System

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange)

An AI-powered system for automated extraction of medical information from documents and mapping to HCC (Hierarchical Condition Category) codes for insurance processing.

## Features

- **Multi-format OCR**: Extracts text from PDFs, JPGs, and PNGs using Tesseract with OpenCV preprocessing
- **Clinical NLP**: Identifies diagnoses, medications, and lab results using spaCy and 200+ custom patterns
- **HCC Code Mapping**: Converts medical terms to standardized insurance codes with confidence scoring
- **Web Interface**: Responsive Flask-based UI with drag-and-drop upload
- **Data Export**: Results export to CSV/Excel for integration with other systems

## System Architecture

```plaintext
medical-doc-processor/
├── app/                      # Flask application
│   ├── controllers/          # Route handlers
│   ├── services/             # Business logic
│   ├── static/               # CSS/JS assets
│   └── templates/            # HTML templates
├── config/                   # Configuration files
├── modules/                  # Core processing
│   ├── ocr_processor.py      # Text extraction
│   ├── nlp_processor.py      # Medical term recognition
│   └── hcc_mapper.py         # Code mapping engine
├── tests/                    # Unit and integration tests
├── data/                     # Sample medical documents
└── requirements.txt          # Python dependencies


## Prerequisites

### Core Requirements
- Python 3.9+ ([Download](https://www.python.org/downloads/))
- Tesseract OCR 5.0

### For Production Deployment
- MongoDB 5.0+ ([Installation Guide](https://www.mongodb.com/docs/manual/installation/))
- Redis 6.2+ ([Installation Guide](https://redis.io/docs/getting-started/installation/))

### Installation Commands
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 tesseract-ocr mongodb redis-server

# MacOS (Homebrew)
brew install python tesseract mongodb-community redis

# Verify installations
python3 --version
tesseract --version
mongod --version
redis-server --version
