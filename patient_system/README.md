# 🏥 AI Patient Record Management System  

This is a **Django-based Patient Record Management System** with API support.  
It allows storing patient data in a database and retrieving it easily through API endpoints.  

---

## 🚀 Features
- Add, update, and delete patient records  
- View all patients in the system  
- Search and fetch a patient’s record via API  
- Django admin panel for managing records  

---

## 👨‍💻 Tech Stack
- Python 3.10+
- Git
- Django 5.x
- Django REST Framework (DRF)
- SQLite (default database)

---

## 📦 Setup Instructions  

Follow these steps to run this project on your laptop:  

### 1. Clone the Repository  
```bash
git clone <https://github.com/Usman-NisarUETTaxila/LLM_app.git>
cd patient_record_system
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate it
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Integrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Admin Login)
```bash
python manage.py migrate
```

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Now open in browser (API Endpoints)
- **Admin Panel** → http://127.0.0.1:8000/admin/
- **Get All Patients (List)** → http://127.0.0.1:8000/api/patients/  (GET)
- **Add New Patient** → http://127.0.0.1:8000/api/patients/  (POST)
- **Get Patient by ID** → http://127.0.0.1:8000/api/patients/<id>/  (GET)
- **Update Patient by ID** → http://127.0.0.1:8000/api/patients/<id>/  (PUT/PATCH)
- **Delete Patient by ID** → http://127.0.0.1:8000/api/patients/<id>/  (DELETE)

---

## 📂 Project Structure
```bash
patient_record_system/
│
├── patient_system/        # Main Django project folder
├── patients/              # App containing patient models, views, serializers
├── manage.py              # Django management script
├── requirements.txt       # List of dependencies
└── README.md              # Documentation (this file)
```

---

## Author
### Khawaja Hasnain
