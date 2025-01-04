# Book Management API

Una API RESTful para gestionar información de libros utilizando Django REST Framework y MongoDB.

---

## **Requisitos Previos**

1. **Python**: Asegúrate de tener Python 3.12 o superior instalado en tu sistema.
2. **MongoDB**: Debes tener un servidor MongoDB en ejecución (puede ser local o remoto).
3. **Git**: Asegúrate de tener Git instalado para clonar el repositorio.
4. **Entorno Virtual (opcional pero recomendado)**: Usaremos `venv` para manejar las dependencias.

---

## **Instrucciones para Inicializar el Proyecto**

### **1. Clonar el Repositorio**

```bash
git clone https://github.com/<tu-usuario>/<nombre-del-repositorio>.git
cd <nombre-del-repositorio>
```

### **2. Crear un Entorno Virtual**

En la raíz del proyecto, crea y activa un entorno virtual:

#### **Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
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

### **3. Instalar las Dependencias**

Ejecuta el siguiente comando para instalar todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```

---

### **4. Configurar la Base de Datos**

Asegúrate de que MongoDB esté ejecutándose en `mongodb://localhost:27017/`. Si usas una configuración personalizada, edita las conexiones a MongoDB en el archivo `views.py` del proyecto.

---

### **5. Migraciones**

Ejecuta las migraciones de Django:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **6. Crear un Superusuario**

Crea un superusuario para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para ingresar un nombre de usuario, correo electrónico y contraseña.

---

### **7. Cargar Datos de Prueba (Opcional)**

Si configuraste un script para insertar datos iniciales en MongoDB, ejecútalo ahora.

---

## **Encender el Proyecto**

Ejecuta el siguiente comando para iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor estará disponible en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## **Probar la API**

### **1. Registrar un Usuario**
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

### **2. Obtener un Token de Autenticación**
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
Respuesta esperada:
```json
{
  "token": "your-auth-token"
}
```

Usa este token en las solicitudes protegidas:
```
Authorization: Token your-auth-token
```

### **3. Listar Libros**
```bash
GET /api/books/
```

### **4. Crear un Libro**
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

## **Ejecutar Pruebas**

Para ejecutar las pruebas unitarias:

```bash
python manage.py test
```

---