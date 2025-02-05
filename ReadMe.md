# Sustainability Credit Exchange (SCE)

## 🌍 Overview
Sustainability Credit Exchange (SCE) is a **full-stack platform** designed to enable businesses and individuals to **buy, sell, and track** environmental credits, including **Carbon Credits, Renewable Energy Credits (RECs), and Plastic Credits**. The platform promotes sustainability by integrating financial incentives into eco-friendly actions.

---

# 📌 Backend Repository (Django & DRF)

## 🛠️ Tech Stack
- Django & Django REST Framework (DRF)
- PostgreSQL (or Azure SQL)
- Celery & Redis (for background tasks)
- Azure App Service (for backend deployment)

## 🚀 Getting Started
### **1️⃣ Clone the Repository**
```sh
git clone git remote add origin https://github.com/Ncoder23/SCE-Backend.git
cd SCE-Backend
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up Database**
- Configure **PostgreSQL** settings in `.env`.
- Apply migrations:
```sh
python manage.py migrate
```

### **4️⃣ Start the Backend Server**
```sh
python manage.py runserver
```

## 📖 API Documentation
- **User Authentication** (Signup/Login)
- **Credit Marketplace** (Browse & Purchase)
- **Transaction History**
- **Admin Controls**

API documentation is available via **Swagger UI**.

## ✅ Contributing
Feel free to fork the repo, create a feature branch, and submit a pull request.
