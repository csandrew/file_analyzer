# 📁 File Analyzer

A powerful document analysis tool that extracts information from various file types including PDFs, images, Word documents, Excel spreadsheets, and text files.

## 🚀 Features

- **Upload any file** - PDF, Images, Word, Excel, CSV, Text files
- **Instant analysis** - Get detailed information about your files
- **Drag & drop interface** - Easy file upload
- **Multiple file support** - Analyze various document formats
- **RESTful API** - Built with Django REST Framework
- **Modern UI** - React + Vite frontend

## 🛠️ Tech Stack

### Backend
- Django 5.0
- Django REST Framework
- SQLite (development) / PostgreSQL (production)
- PyPDF2, python-docx, pandas, Pillow

### Frontend
- React 19
- Vite
- Axios
- React Dropzone

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

## 🔧 Installation

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/file-analyzer.git
cd file-analyzer
\`\`\`

### 2. Backend setup
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
\`\`\`

### 3. Frontend setup
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

### 4. Open your browser
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## 📁 Project Structure

\`\`\`
FILE_ANALYSER/
├── backend/
│   ├── analysis/          # Analysis services
│   ├── documents/         # Document models & views
│   ├── document_analyzer/ # Django project settings
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Styling
│   │   └── main.jsx
│   └── package.json
└── README.md
\`\`\`

## 🎯 API Endpoints

- `POST /api/documents/upload/` - Upload a file
- `GET /api/documents/list/` - List all documents
- `GET /api/documents/{id}/` - Get document details

## 📊 Supported File Types

- **PDF** - Pages, metadata, encryption status
- **Images** - Dimensions, format, color mode
- **Word Documents** - Paragraphs, tables, sections
- **Excel Files** - Sheets, rows, columns
- **Text Files** - Word count, line count, character count
- **CSV** - Rows, columns, column names

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this project for learning or production!

## 👨‍💻 Author

Your Name

---

Built with 🐍 Django and ⚛️ React
