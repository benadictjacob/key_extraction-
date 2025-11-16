# 🌾 Enterprise Agriculture IoT Data Management and Automation System

## Project Overview

This system is a robust, multi-component data management and automation solution designed for enterprise-level, live IoT-based agriculture. It provides real-time data ingestion, secure storage, and advanced analytics for automated farm operations, ensuring optimal crop yield and resource efficiency.

A key distinguishing feature of this platform is the integration of a **cutting-edge, proprietary cryptographic algorithm** for enhanced data security and integrity, making it ideal for managing sensitive agricultural enterprise data.

## ✨ Key Features

### Security & Data Integrity

* **Novel Cryptography:** Implements a newly discovered cryptographic algorithm to secure IoT data transmission and storage, offering unparalleled security and computational efficiency.

* **RFID-Based Access Control:** Features integrated authentication using RFID tags for physical site access and automated system interaction.

* **Granular User Permissions:** A comprehensive, user-based access control system managed through Django, allowing for fine-grained permissions and action flow control across the platform's features.

### Architecture & Data Flow

* **Flask Middleware:** A dedicated, lightweight Flask server acts as the central middleware, handling high-throughput, real-time data ingestion from distributed IoT sensors and ensuring secure preprocessing before data persistence.

* **Django Data Monitoring & Analytics:** A powerful Django application provides the primary user interface for data monitoring, analysis, and system administration.

### Monitoring & Analytics Dashboard

* **Real-Time Dashboard:** A dynamic, centralized dashboard for visualizing key environmental metrics (temperature, humidity, soil conditions, etc.) and automation system status.

* **Data Analytics:** Tools for historical data analysis, trend identification, and generating predictive insights to optimize farm management strategies.

## 🧱 Architectural Components

The system is structured into three primary tiers:

| Component | Technology | Role | 
 | ----- | ----- | ----- | 
| **Edge Devices** | IoT Sensors/Actuators | Collects environmental data (soil, climate) and executes automation commands. | 
| **Data Ingestion** | **Python / Flask** | Acts as the lightweight, non-blocking background server for receiving, decrypting/encrypting, and queuing all raw IoT sensor data. | 
| **Application Layer** | **Python / Django** | Handles persistent data storage, runs the cryptographic algorithm services, manages the web interface (dashboard, analytics, security), and controls user access. | 

## ⚙️ Setup and Deployment

### Prerequisites

Before deploying the application, ensure you have the following installed:

* Python 3.9+

* Git

* Virtual Environment Tool (`venv` or `conda`)

### 1. Repository Clone

```
git clone 
cd sentinel-agri


```

### 2. Environment Setup

Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows


```

### 3. Install Dependencies

Install all required Python packages for both Flask and Django:

```
pip install -r requirements.txt


```

*(NOTE: You will need to create a `requirements.txt` file listing `Django`, `Flask`, and any necessary database/cryptography packages.)*

### 4. Database Migrations

Set up the Django database schema (required for the monitoring dashboard and user security):

```
python manage.py makemigrations
python manage.py migrate


```

### 5. Running the System

Since this is a multi-process system, you must run the Flask middleware and the Django server simultaneously.

#### A. Start Flask Middleware (Data Ingestion)

The Flask application is typically run on a different port and handles API endpoints for sensor data POSTs.

```
# Assuming your Flask app entry point is 'middleware.py'
python middleware.py & 


```

#### B. Start Django Application (Monitoring & Analytics)

The Django server hosts the main web application and dashboard.

```
python manage.py runserver


```

### 6. Access Application

Access the main monitoring dashboard via your browser:



## 🔒 Cryptographic Implementation Details

The core security of this system relies on the custom cryptographic algorithm.

* **Algorithm Name:** (Insert Algorithm Name Here, e.g., AES-Custom-256)

* **Location:** The core logic is implemented in the `biometric_auth/cryptography/` module (or similar location).

* **Use Case:** Applied to all incoming sensor payloads (via Flask) and enforced on sensitive data fields within the Django models.

## 👥 Access Control

The system implements a layered security model:

1. **RFID Access:** Physical system and site access is managed by matching RFID IDs against the database.

2. **User Authentication:** Standard Django user authentication for dashboard access.

3. **Permissions Flow:** Custom decorators and middleware enforce specific feature permissions (`view_dashboard`, `modify_automation_rules`, `manage_users`) based on the authenticated user's role.

## 🤝 Contribution

We welcome contributions to this project. Please follow these guidelines:

1. Fork the repository.

2. Create a new feature branch (`git checkout -b feature/new-analytic-tool`).

3. Commit your changes (`git commit -m 'feat: Added new analytic tool'`).

4. Push to the branch (`git push origin feature/new-analytic-tool`).

5. Open a Pull Request.
6. vedio_implementation_demo:https://youtu.be/Bz3NGBNqJG8
            
