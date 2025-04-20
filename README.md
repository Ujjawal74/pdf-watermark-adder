# PDF Watermark Tool

A simple yet powerful web app built with Flask that allows users to upload one or more PDF files and apply a watermark (with a clickable link) to each page. Optionally, it also supports compression of the output files.

---

## 🚀 Features

- 🗂 Upload one or more PDFs
- 🖊️ Add watermark with black background and clickable link (`https://krispnotes.in/`)
- 🧼 Clean watermark layout with white text and padding
- 📦 Download processed PDFs (ZIP if multiple)
- 📉 Optional compression of PDF files
- 🖥️ Responsive UI built with Bootstrap 5
- ⚡ Works entirely offline

---

## 📂 Folder Structure

```
project/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── uploads/               # Temporary input files
└── processed/             # Output (watermarked) files
```

---

## 💻 Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/pdf-watermark-tool.git
cd pdf-watermark-tool
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Flask app**

```bash
python app.py
```

5. **Open in browser**

```
http://127.0.0.1:5000/
```

---

## 📸 Screenshot

![PDF Watermark Tool UI](https://your-screenshot-link.com/example.png)

---

## 🔐 Security Notes

- Max upload limit set to **16MB**
- Input sanitization via `secure_filename`
- Safe directory cleanup using `shutil`

---

## 📄 License

MIT License – Free for personal and commercial use.

---

## 🙌 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [PyPDF](https://pypdf.readthedocs.io/)
- [ReportLab](https://www.reportlab.com/)
