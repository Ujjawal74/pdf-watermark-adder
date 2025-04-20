import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import black, white
from io import BytesIO
import zipfile
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

def clear_directory(directory):
    """Safely clear a directory"""
    try:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
    except Exception as e:
        print(f'Error clearing directory {directory}: {e}')

def ensure_directory(directory):
    """Ensure a directory exists, create if it doesn't"""
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        print(f'Error creating directory {directory}: {e}')

# Initialize directories on startup
ensure_directory(app.config['UPLOAD_FOLDER'])
ensure_directory(app.config['PROCESSED_FOLDER'])

def add_watermark(input_pdf_path, output_pdf_path, compress=False):
    watermark_text = "https://krispnotes.in/"
    
    try:
        # Read the input PDF
        with open(input_pdf_path, "rb") as input_file:
            input_pdf = PdfReader(input_file)
            output_pdf = PdfWriter()
            
            # Get the first page to determine size
            first_page = input_pdf.pages[0]
            page_width = float(first_page.mediabox[2])
            page_height = float(first_page.mediabox[3])
            
            for page_num in range(len(input_pdf.pages)):
                page = input_pdf.pages[page_num]
                
                # Create a watermark PDF
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                
                # Calculate text width and height
                text_width = can.stringWidth(watermark_text, "Helvetica-Bold", 12)
                text_height = 12
                
                # Add black background rectangle
                can.setFillColor(black)
                can.rect(0, page_height - text_height - 10, text_width + 20, text_height + 10, fill=1, stroke=0)
                
                # Add white text with link
                can.setFillColor(white)
                can.setFont("Helvetica-Bold", 12)
                can.drawString(10, page_height - text_height - 5, watermark_text)
                
                # Add the link
                can.linkURL("https://krispnotes.in/", 
                           (10, page_height - text_height - 5, 10 + text_width, page_height - 5), 
                           relative=1)
                
                can.save()
                
                # Move to the beginning of the StringIO buffer
                packet.seek(0)
                watermark_pdf = PdfReader(packet)
                watermark_page = watermark_pdf.pages[0]
                
                # Merge the watermark with the page
                page.merge_page(watermark_page)
                
                # Add to output
                output_pdf.add_page(page)
            
            # Apply compression if requested (after all pages are added)
            if compress:
                for page in output_pdf.pages:
                    page.compress_content_streams()
            
            # Write the output PDF
            with open(output_pdf_path, "wb") as output_file:
                output_pdf.write(output_file)
    except Exception as e:
        print(f'Error processing PDF: {e}')
        raise

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Clear previous files
            clear_directory(app.config['UPLOAD_FOLDER'])
            clear_directory(app.config['PROCESSED_FOLDER'])
            
            # Check if files were uploaded
            if 'pdf_files' not in request.files:
                flash('No files selected', 'error')
                return redirect(request.url)
            
            files = request.files.getlist('pdf_files')
            if len(files) == 0 or files[0].filename == '':
                flash('No files selected', 'error')
                return redirect(request.url)
            
            compress = 'compress' in request.form
            
            # Process each file
            processed_files = []
            for file in files:
                if file and file.filename.lower().endswith('.pdf'):
                    filename = secure_filename(file.filename)
                    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    output_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
                    
                    # Ensure the upload directory exists
                    ensure_directory(os.path.dirname(input_path))
                    
                    file.save(input_path)
                    add_watermark(input_path, output_path, compress)
                    processed_files.append(output_path)
            
            if not processed_files:
                flash('No valid PDF files uploaded', 'error')
                return redirect(request.url)
            
            # Prepare download
            if len(processed_files) == 1:
                return send_file(
                    processed_files[0],
                    as_attachment=True,
                    download_name='watermarked_' + os.path.basename(processed_files[0]),
                    mimetype='application/pdf'
                )
            else:
                zip_filename = os.path.join(app.config['PROCESSED_FOLDER'], 'watermarked_pdfs.zip')
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for file in processed_files:
                        zipf.write(file, os.path.basename(file))
                
                return send_file(
                    zip_filename,
                    as_attachment=True,
                    download_name='watermarked_pdfs.zip',
                    mimetype='application/zip'
                )
        
        except Exception as e:
            print(f'Error processing request: {e}')
            flash('An error occurred while processing your files', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)