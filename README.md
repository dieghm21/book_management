
# Book Management API

A RESTful API to manage book information using Django REST Framework and MongoDB.

---

## **Prerequisites**

1. **Python**: Ensure that Python 3.12 or higher is installed on your system.
2. **MongoDB**: You should have a MongoDB server running (it can be local or remote).
3. **Git**: Ensure that Git is installed to clone the repository.
4. **Virtual Environment (optional but recommended)**: We will use `venv` to manage dependencies.

---

## **Project Setup Instructions**

### **1. Clone the Repository**

```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

### **2. Create a Virtual Environment**

At the root of the project, create and activate a virtual environment:

#### **Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\ctivate
```

#### **Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

#### **Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### **3. Install Dependencies**

Run the following command to install all the required dependencies:

```bash
pip install -r requirements.txt
```

---

### **4. Configure the Database**

Make sure MongoDB is running at `mongodb://localhost:27017/`. If you are using a custom configuration, edit the MongoDB connection settings in the `views.py` file of the project.

---

### **5. Migrations**

Run the Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **6. Create a Superuser**

Create a superuser to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter a username, email, and password.

---

### **7. Load Test Data (Optional)**

If you have configured a script to insert initial data into MongoDB, run it now.

---

## **Start the Project**

Run the following command to start the development server:

```bash
python manage.py runserver
```

The server will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## **Test the API**

### **1. Register a User**
```bash
POST /api/register/
```
Body (JSON):
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```

### **2. Obtain an Authentication Token**
```bash
POST /api/login/
```
Body (JSON):
```json
{
  "username": "testuser",
  "password": "testpassword"
}
```
Expected response:
```json
{
  "token": "your-auth-token"
}
```

Use this token for protected requests:
```
Authorization: Token your-auth-token
```

### **3. List Books**
```bash
GET /api/books/
```

### **4. Create a Book**
```bash
POST /api/books/
```
Body (JSON):
```json
{
  "title": "Book Title",
  "author": "Author Name",
  "published_date": "2023-01-01",
  "genre": "Fiction",
  "price": 19.99
}
```

---

## **Run Tests**

To run the unit tests:

```bash
python manage.py test
```

---
