# Consent-Based User Activity Monitoring System

## Overview

This project is a consent-based user activity monitoring system designed to collect and visualize user interaction data in an ethical and secure manner.

The system captures keyboard and mouse activity, stores detailed logs locally, and sends aggregated, non-sensitive metrics to a centralized server. A web-based dashboard displays this data in real time using interactive graphs.

This project demonstrates concepts similar to Security Information and Event Management (SIEM) systems.

---

## Features

* User consent before monitoring starts
* Keyboard activity tracking
* Mouse click tracking
* Automatic screenshot capture
* Local log storage (Logfile.txt)
* REST API for sending data to server
* Device-wise and date-wise log storage
* Live dashboard with graphs (Chart.js)
* Auto-refresh dashboard (real-time updates)
* Multi-device support

---

## System Architecture

Client (Python)
↓
Local Logging (Detailed Data)
↓
Filtered Metrics (Keys, Clicks)
↓
Flask Backend API
↓
JSON Storage (Device-wise, Date-wise)
↓
Web Dashboard (Chart.js Visualization)

---

## Technologies Used

* Frontend: HTML, CSS, Chart.js
* Backend: Flask (Python)
* Client: Python (pynput, requests, pyautogui)
* Data Storage: JSON (file-based)
* Deployment: Render (Cloud Hosting)

---

## Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

### 2. Install Dependencies

Server:

```bash
pip install flask gunicorn
```

Client:

```bash
pip install pynput requests pyautogui
```

---

### 3. Run Server

```bash
python server.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

### 4. Run Client

```bash
python Keylogger.py
```

---

## Dashboard

* Displays device-wise activity
* Shows total key presses and mouse clicks
* Graph visualization using Chart.js
* Auto-refresh every 5 seconds

---

## Project Structure

```
project/

├── server.py
├── Keylogger.py
├── devices/
│   └── DEVICE_NAME/
│       └── YYYY-MM-DD.json
├── requirements.txt
└── README.md
```

---

## Ethical Considerations

* This system is fully consent-based
* No data is collected without user approval
* Sensitive data (raw keystrokes) is stored locally only
* Only aggregated metrics are sent to the server
* Designed strictly for educational and demonstration purposes

---

## Deployment

The project can be deployed using:

* Render (recommended)
* Railway

After deployment, update the client API URL:

```python
requests.post("https://your-app.onrender.com/api/log", json=data)
```

---

## Future Enhancements

* Real-time updates using WebSockets
* Time-series graphs
* User authentication system
* Database integration (MongoDB or Firebase)
* Mobile-responsive dashboard
* Alert system for abnormal activity

---

## Learning Outcomes

* Client-server architecture
* REST API development
* Real-time data visualization
* Ethical cybersecurity practices
* Monitoring and logging systems

---

## Conclusion

This project provides a practical implementation of a monitoring system with a strong focus on ethics, transparency, and real-time analytics, making it suitable for academic and professional demonstrations.
