import os
import json
import base64
from pathlib import Path
from datetime import datetime
import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from openai import OpenAI
from pypdf import PdfReader
import fitz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Create upload folder
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Initialize Groq client (Strictly Groq Only)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

# New Llama 4 Scout Model
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
ADMIN_TEMPLATE_KEY = os.getenv("ADMIN_TEMPLATE", "invoice")

# Predefined templates
TEMPLATES = {
    "invoice": {
        "name": "Tax Invoice Extraction",
        "prompt": """Extract the following information from the document as a structured JSON object:
- invoice_number
- date
- seller_name
- seller_gstin
- buyer_name
- buyer_gstin
- items (array of: description, quantity, rate, amount)
- tax_details (cgst, sgst, igst)
- total_amount
- currency""",
    }
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_file_to_base64(file_path):
    with open(file_path, "rb") as file:
        return base64.standard_b64encode(file.read()).decode("utf-8")

def get_media_type(filename):
    ext = filename.rsplit(".", 1)[1].lower()
    media_types = {
        "pdf": "application/pdf",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }
    return media_types.get(ext, "application/octet-stream")

def extract_pdf_text(file_path):
    try:
        reader = PdfReader(file_path)
        text_chunks = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_chunks.append(page_text.strip())
        return "\n\n".join(text_chunks).strip()
    except Exception:
        return ""

def render_pdf_pages_to_images(file_path, max_pages=3):
    image_payloads = []
    try:
        document = fitz.open(file_path)
        page_count = min(len(document), max_pages)
        for page_index in range(page_count):
            page = document[page_index]
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            image_bytes = pixmap.tobytes("png")
            encoded = base64.b64encode(image_bytes).decode("utf-8")
            image_payloads.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{encoded}"}
            })
        document.close()
    except Exception:
        return []
    return image_payloads

def process_with_llm(file_path, filename, prompt_text):
    try:
        media_type = get_media_type(filename)
        file_data = encode_file_to_base64(file_path)
       
        # Construct message content for Llama 4 Scout (multimodal)
        if filename.lower().endswith(".pdf"):
            extracted_text = extract_pdf_text(file_path)
            if extracted_text:
                content = f"Extract the following data as JSON: {prompt_text}\n\nDocument Text:\n{extracted_text}"
                messages = [{"role": "user", "content": content}]
            else:
                # Use vision for PDFs without text
                pdf_images = render_pdf_pages_to_images(file_path)
                content = [{"type": "text", "text": prompt_text}, *pdf_images]
                messages = [{"role": "user", "content": content}]
        else:
            # Use vision for images
            image_data_url = f"data:{media_type};base64,{file_data}"
            content = [
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {"url": image_data_url}}
            ]
            messages = [{"role": "user", "content": content}]

        print(f"--- Calling Groq with Model: {MODEL_NAME} ---")
        print(f"--- Prompt: {prompt_text} ---")

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=4000,
            response_format={"type": "json_object"}
        )

        response_text = completion.choices[0].message.content or ""
        print(f"--- Raw Response: {response_text} ---")
        
        # Robust JSON extraction
        try:
            return {"structured": json.loads(response_text)}
        except json.JSONDecodeError:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                return {"structured": json.loads(response_text[json_start:json_end])}
            raise Exception("No valid JSON found in response")
       
    except Exception as e:
        raise Exception(f"Groq Inference Error: {str(e)}")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ready", "model": MODEL_NAME})

@app.route("/api/extract", methods=["POST"])
def extract_data():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file"}), 400
       
        file = request.files["file"]
        prompt_text = TEMPLATES.get(ADMIN_TEMPLATE_KEY, TEMPLATES["invoice"])["prompt"]
       
        if file.filename == "" or not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file format"}), 400
       
        filename = secure_filename(file.filename)
        filepath = UPLOAD_FOLDER / (datetime.now().strftime("%Y%m%d_%H%M%S_") + filename)
        file.save(str(filepath))
       
        extraction = process_with_llm(str(filepath), filename, prompt_text)
       
        return jsonify({
            "success": True,
            "filename": filename,
            "extraction": extraction,
        }), 200
       
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
