from flask import Blueprint, request, jsonify, render_template
import logging

from app.services.pdf_service import process_pdf_chunks
from app.services.ingestion_service import start_ingestion, wait_for_ingestion
from app.services.retrieval_service import retrieve_context
from app.services.context_service import build_context
from app.services.llm_service import get_llm_answer

kb_blueprint = Blueprint("kb", __name__)
logger = logging.getLogger("ROUTES")


# -------------------------
# UI ROUTE (HTML)
# -------------------------
@kb_blueprint.route("/", methods=["GET"])
def index_page():
    """
    Serve main UI page (index.html).
    """
    return render_template("index.html")


# -------------------------
# 1) UPLOAD + CHUNK PDF
# -------------------------
@kb_blueprint.route("/upload", methods=["POST"])
def upload_pdf():
    """
    Uploads a PDF, saves to disk, then chunks and uploads to S3.
    Expects:
      - multipart/form-data
      - file: <PDF>
      - chunk_size: <int>
    """
    if "file" not in request.files:
        return jsonify({"error": "Missing file in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    chunk_size = request.form.get("chunk_size", default="50")

    try:
        chunk_size = int(chunk_size)
    except ValueError:
        return jsonify({"error": "chunk_size must be an integer"}), 400

    save_path = f"uploads/{file.filename}"
    file.save(save_path)
    logger.info(f"File saved: {save_path}")

    try:
        process_pdf_chunks(save_path, chunk_size=chunk_size)
    except Exception as e:
        logger.exception("Chunking failed")
        return jsonify({"error": f"Chunking failed: {str(e)}"}), 500

    return jsonify({"message": f"Uploaded and chunked '{file.filename}' successfully."})


# -------------------------
# 2) START INGESTION (sync wait)
# -------------------------
@kb_blueprint.route("/ingest", methods=["POST"])
def ingest():
    """
    Starts ingestion of S3 content into Bedrock KB.
    Waits synchronously until status is COMPLETE or FAILED.
    """
    try:
        job_id = start_ingestion()
        status = wait_for_ingestion(job_id)
        return jsonify({
            "job_id": job_id,
            "status": status
        })
    except Exception as e:
        logger.exception("Ingestion failed")
        return jsonify({"error": f"Ingestion error: {str(e)}"}), 500


# -------------------------
# 3) QUERY KB + ANSWER WITH LLM
# -------------------------
@kb_blueprint.route("/query", methods=["POST"])
def query_kb():
    """
    Expects JSON:
      {
        "query": "some question",
        "top_k": 3
      }
    """
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    query_text = data["query"]
    top_k = data.get("top_k", 3)

    try:
        retrievals = retrieve_context(query_text, top_k=top_k)
        context = build_context(retrievals)
        answer = get_llm_answer(query_text, context)

        return jsonify({
            "query": query_text,
            "answer": answer,
            "context": context,
            "retrievals": retrievals
        })

    except Exception as e:
        logger.exception("Query failed")
        return jsonify({"error": f"Query error: {str(e)}"}), 500
