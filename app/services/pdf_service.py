from PyPDF2 import PdfReader, PdfWriter
import io
from pathlib import Path
from app.services.s3_service import upload_chunk
import logging

logger = logging.getLogger("PDF")

def process_pdf_chunks(path, chunk_size=50):
    reader = PdfReader(path)
    total_pages = len(reader.pages)
    name = Path(path).stem

    logger.info(f"Chunking PDF: {path} | {total_pages} pages")

    for start in range(0, total_pages, chunk_size):
        end = min(start + chunk_size, total_pages)

        writer = PdfWriter()
        for p in range(start, end):
            writer.add_page(reader.pages[p])

        buffer = io.BytesIO()
        writer.write(buffer)
        buffer.seek(0)

        object_key = f"{name}_{start+1}_to_{end}.pdf"
        upload_chunk(object_key, buffer)
