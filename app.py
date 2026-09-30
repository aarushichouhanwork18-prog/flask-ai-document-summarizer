from flask import Flask, render_template, request, jsonify

import pymupdf
import pytesseract
from PIL import Image

from google import genai
from dotenv import load_dotenv

import os
import io


# Load variables from .env
load_dotenv()


# Create Flask app
app = Flask(__name__)


# Tesseract OCR location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Upload and process document
@app.route("/upload", methods=["POST"])
def upload_file():

    # Get uploaded file
    file = request.files.get("file")

    if not file:
        return jsonify({
            "message": "No file uploaded."
        }), 400

    # Get filename
    filename = file.filename

    # Read file
    file_bytes = file.read()

    # Store extracted text
    extracted_text = ""

    # Check file type
    file_extension = os.path.splitext(filename)[1].lower()


    # ------------------------------------------------
    # PDF PROCESSING
    # ------------------------------------------------

    if file_extension == ".pdf":

        # Open PDF
        pdf = pymupdf.open(
            stream=file_bytes,
            filetype="pdf"
        )

        # Process each page
        for page in pdf:

            # Try extracting normal text
            text = page.get_text()

            if text.strip():

                # Text-based PDF
                extracted_text += text + "\n"

            else:

                # Scanned/image-based PDF
                pix = page.get_pixmap()

                image_bytes = pix.tobytes("png")

                image = Image.open(
                    io.BytesIO(image_bytes)
                )

                # OCR
                ocr_text = pytesseract.image_to_string(image)

                extracted_text += ocr_text + "\n"

        pdf.close()


    # ------------------------------------------------
    # IMAGE PROCESSING
    # ------------------------------------------------

    elif file_extension in [".jpg", ".jpeg", ".png"]:

        # Open image
        image = Image.open(
            io.BytesIO(file_bytes)
        )

        # OCR
        extracted_text = pytesseract.image_to_string(image)


    # ------------------------------------------------
    # UNSUPPORTED FILE
    # ------------------------------------------------

    else:

        return jsonify({
            "message": "Unsupported file type. Please upload a PDF, JPG, JPEG, or PNG file."
        }), 400


    # Remove unnecessary spaces
    extracted_text = extracted_text.strip()


    # Check if text was extracted
    if not extracted_text:

        return jsonify({
            "filename": filename,
            "message": "No text could be extracted from this file."
        })


    # ------------------------------------------------
    # GEMINI SUMMARY
    # ------------------------------------------------

    prompt = f"""
Analyze the following document and create a very concise summary.

Follow this EXACT format:

Overview:
Write only 2-3 short sentences explaining the main idea.

Key Points:
- Write one short line for the first important point.
- Write one short line for the second important point.
- Write one short line for the third important point.
- Write one short line for the fourth important point.

Rules:
- Maximum 4 key points.
- Each key point must be ONE short line.
- Keep the overview concise.
- Include only the most important information.
- Do not add extra sections.
- Do not repeat information.
- Do not write long explanations.

Document:

{extracted_text}
"""


    # Send text to Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )


    # Get summary
    summary = response.text


    # Return result
    return jsonify({
        "filename": filename,
        "extracted_text": extracted_text,
        "summary": summary
    })


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)