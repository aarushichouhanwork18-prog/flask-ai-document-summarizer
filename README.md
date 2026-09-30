# Flask AI Document Summarizer

A Flask-based AI application that extracts text from PDFs and images, performs OCR on scanned documents, and generates concise summaries using Gemini AI.

## Features

- PDF text extraction using PyMuPDF
- OCR for scanned PDFs and images using Tesseract
- Supports PDF, JPG, JPEG, and PNG
- AI-powered summarization using Gemini
- Concise overview and key-point summaries
- Custom web interface
- Error handling for unsupported files

## Tech Stack

- Python
- Flask
- PyMuPDF
- Tesseract OCR
- Pillow
- Gemini AI
- HTML, CSS, JavaScript

## Project Structure

```text
flask_pdf_summarizer/
├── templates/
│   └── index.html
├── app.py
├── .env
└── .gitignore




Workflow
Upload PDF/Image
       ↓
Text Extraction / OCR
       ↓
Extracted Text
       ↓
Gemini AI
       ↓
Concise Summary
