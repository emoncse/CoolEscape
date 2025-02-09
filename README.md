# 🚀 CoolEscape  

CoolEscape is a Django-based web application designed to help users:  

🌟 **Find the Coolest Districts** – Identify the lowest-temperature districts in Bangladesh.  
🌟 **Compare Weather for Travel** – Check and compare weather conditions between two locations for a specific date.  
🌟 **Secure Access** – Uses JWT authentication for enhanced security.  
🌟 **API Documentation** – Built with Django Rest Framework (DRF) and drf-spectacular for easy API documentation.  

---

## 📌 Table of Contents  
- [Installation](#installation)  
- [Docker Setup](#docker-setup)  
- [API Endpoints](#api-endpoints)  
- [Swagger API Documentation](#swagger-api-documentation)  
- [Using Postman](#using-postman)  

---

## 🛠 Installation  

### **Prerequisites**  
Ensure you have the following installed:  
- Python `3.12.8`  
- Django `5.1.6`  
- Virtualenv  

### **Steps**  

1️⃣ **Clone the repository:**  
```sh
git clone https://github.com/emoncse/CoolEscape.git
cd CoolEscape
```

2️⃣ **Create and activate a virtual environment:**  
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3️⃣ **Install dependencies:**  
```sh
pip install -r requirements.txt
```

** Special Note: **
```
aiohttp 
````
4️⃣ **Apply database migrations:**  
```sh
python manage.py makemigrations
python manage.py migrate
```

5️⃣ **Collect static files:**  
```sh
python manage.py collectstatic
```

6️⃣ **Create a superuser (for admin access):**  
```sh
python manage.py createsuperuser
```

7️⃣ **Run the development server:**  
```sh
python manage.py runserver
```

8️⃣ **Access the application:**  
Open your browser and go to:  
👉 `http://127.0.0.1:8000`  

---

## 🐋 Docker Setup  

### **Prerequisites**  
Make sure you have:  
- Docker  
- Docker Compose  
- Git  

### **Steps**  

1️⃣ **Clone the repository:**  
```sh
git clone https://github.com/emoncse/CoolEscape.git
```

2️⃣ **Navigate to the project directory:**  
```sh
cd CoolEscape
```

3️⃣ **Build and run the Docker container:**  
```sh
docker compose up --build
```

4️⃣ **Run in detached mode (background):**  
```sh
docker compose up -d
```

---

## 🔌 API Endpoints  

### **Authentication**  
- 🔑 **Obtain Token:** `POST /api/token/`  
- 🔄 **Refresh Token:** `POST /api/token/refresh/`  

### **Coolest Districts API**  
- ❄️ **Get the coolest districts:** `GET /v1/coolest-districts/`  

### **Travel Advice API**  
- ✈️ **Get travel advice:** `GET /v1/travel-destination/`  

---

## 📚 Swagger API Documentation  

CoolEscape provides an interactive API documentation powered by **Swagger**.  

📌 **Swagger URL:**  
👉 `http://127.0.0.1:8000/api/docs/`  

### **API Examples**  

📌 **Obtain Token:**  
```http
POST /api/token/
```
**Body:**  
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

📌 **Access Protected Endpoints:**  
```http
GET /v1/coolest-districts/
```
**Headers:**  
```text
Authorization: Bearer <your_access_token>
```

📌 **Refresh Token:**  
```http
POST /api/token/refresh/
```
**Body:**  
```json
{
    "refresh": "<your_refresh_token>"
}
```

---

## 🛠 Using Postman  

1️⃣ **Obtain Token**  
- **URL:** `http://127.0.0.1:8000/api/token/`  
- **Method:** `POST`  
- **Body:**  
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```

2️⃣ **Access Protected Endpoints**  
- **URL:** `http://127.0.0.1:8000/v1/*/`  
- **Method:** `GET`  
- **Headers:**  
  ```
  Authorization: Bearer <access_token>
  ```

3️⃣ **Refresh Token**  
- **URL:** `http://127.0.0.1:8000/api/token/refresh/`  
- **Method:** `POST`  
- **Body:**  
  ```json
  {
      "refresh": "<refresh_token>"
  }
  ```

---

### Special Note: aiohttp library the Game Changer

**Why Use aiohttp?**

* The aiohttp library is an asynchronous HTTP client/server framework that enables non-blocking network operations. It is particularly useful when handling multiple API calls concurrently.

#### Benefits of aiohttp:

* Asynchronous Networking – Allows non-blocking HTTP requests, making API interactions faster.

* Performance Boost – Handles multiple API requests simultaneously, reducing wait times.

* Streaming Support – Efficient for large data transfers.

* Built-in Connection Pooling – Reuses existing connections to optimize performance.



---
## ⚠️ Note  

🚀 **The API is currently open for public use.** However, we can restrict access by enabling the `IsAuthenticated` permission class. The necessary code is already included but commented out in the project.  

---

