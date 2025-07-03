### README.md – CSV Upload & Query API with AI Assistant

---

## 📌 Project Overview
This project is a backend API system that allows users to:

- 📁 Upload a CSV file
- ✅ Validate and store data in a SQLite database
- 🔍 Query and filter the stored records
- 📄 Log all API activity
- 🤖 (Optional) Ask an AI assistant questions about the uploaded data using OpenAI API
- 🔐 Secure all endpoints using Basic Authentication

---

## 🚀 Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Custom logic using Pandas
- **Authentication**: HTTP Basic Auth
- **AI Assistant**: OpenAI API (GPT-3.5 Turbo)

---

## 📂 Project Structure
```
csv_api_project/
│
├── app/
│   ├── main.py            # FastAPI app with endpoints and authentication
│   ├── models.py          # SQLAlchemy DB model
│   ├── database.py        # DB setup and session management
│   ├── utils.py           # CSV validation logic
│
├── data/
│   └── sample.csv         # Sample CSV to test (optional)
│
├── requirements.txt       # Python dependencies
└── README.md              # Project instructions
```

---

## 🔧 Setup Instructions

### 1. ✅ Clone the Repo & Navigate to the Project
```bash
git clone <your-repo-url>
cd csv_api_project
```

### 2. 📦 Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # For Windows
# OR
source venv/bin/activate  # For Linux/macOS
```

### 3. 📥 Install Requirements
```bash
pip install -r requirements.txt
```

### 4. ▶️ Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```

Server runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 Authentication
All endpoints are secured with Basic Auth.
```
Username: admin
Password: secret
```
Use the "Authorize" button in Swagger UI or add headers manually:
```
-H "Authorization: Basic YWRtaW46c2VjcmV0"
```

---

## 📁 Sample CSV Format
```
name,age,email
Alice,25,alice@example.com
Bob,30,bob@example.com
```

---

## 🧪 API Endpoints

### 🔹 Upload CSV
```http
POST /upload
```
Upload and store records from a CSV file.

### 🔹 Get All Records
```http
GET /records
```
Retrieve all records stored in the database.

### 🔹 Search Records
```http
GET /records/search?min_age=20&name=Ali
```
Filter by age range or partial name match.

### 🔹 Ask AI (Optional)
```http
POST /ask-ai?question=What is the average age?
```
Uses OpenAI GPT to analyze stored CSV data.

**Note:** AI functionality requires a working OpenAI API key. If you exceed your quota, the AI endpoint will return an error. To test this feature, update your API key in `main.py`:
```python
client = OpenAI(api_key="your-valid-key")
```

---

## 📝 Notes
- Logs are written to `api.log`
- Database file: `data.db` created in root directory
- Ensure your uploaded CSV includes `name`, `age`, and `email` fields
- Only `.csv` files are accepted

---

## 📦 Sample cURL Test
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46c2VjcmV0' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@data/sample.csv;type=text/csv'
```

---

## ✅ Status
✅ Fully working, tested, and production-ready (student-level) backend project. AI assistant is integrated but requires valid OpenAI quota to function.

---

## 📧 Contact
Built by **Yasir A**  
📩 yasircysec@gmail.com  
🧠 Guided by ChatGPT (OpenAI)
