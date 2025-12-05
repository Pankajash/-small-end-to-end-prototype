Pickabook – Story Illustration Personaliser

This project is a small end-to-end prototype that demonstrates how a child’s face photo can be turned into a personalised storybook-style illustration. The goal was to build something simple, functional, and easy to deploy — without any heavy ML models — just the working pipeline.

The prototype consists of:

A very lightweight FastAPI backend (deployed on Railway)

A simple React-in-HTML frontend (deployed on Vercel)

A mocked personalisation step that returns a sample illustration (Base64)

A clean UI to upload a child’s photo and preview the result

This is meant for demo and learning purposes, not production.

🌐 Live Demo

Frontend (Vercel):
👉 https://small-end-to-end-prototype.vercel.app

Backend (Railway):
👉 https://small-end-to-end-prototype-production.up.railway.app

🧰 Tech Stack

Frontend

React (via CDN)

HTML + CSS only

Hosted on Vercel

Backend

FastAPI (Python)

Uvicorn

Railway deployment

Other

Base64 image handling

Basic fetch API calls

📸 Screenshots

(Add your own screenshots in a /screenshots folder and link them here.)

Example:

![Demo Screenshot](screenshots/demo.png)

📝 Features

Upload any child’s face photo

Sends the image to a FastAPI backend

Backend returns a Base64 “personalised” illustration (mocked pipeline)

Clean, minimal, responsive frontend

Fully deployed end-to-end

Good for interviews, demo presentations, or technical assignments

🏗️ Architecture Overview
Frontend (Vercel) → POST request → Backend (Railway/FastAPI) 
                                   ↓
                              Mock AI Pipeline
                                   ↓
                             Returns Base64 Image
                                   ↓
                           UI displays illustration


A very simple flow, intentionally built for clarity.

📁 Folder Structure
/
├── backend/
│   ├── main.py
│   ├── mock_generator.py
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
└── README.md

🚀 Running the Project Locally
1. Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload


Backend will start at:
http://localhost:8000

2. Frontend

No build tools. No frameworks. Just open the file:

frontend/index.html


(Optional) Run a local server for smoother testing:

cd frontend
python -m http.server 3000


Frontend will run at:
http://localhost:3000

📡 API (Backend)
POST /api/personalize

Request:

Form-data

Field: photo (image file)

Response:

{
  "image_base64": "<base64 PNG>"
}


You can test with cURL:

curl -X POST -F "photo=@child.jpg" http://localhost:8000/api/personalize

🧩 Notes / Things to Improve

Replace the mock with a real Instant-ID or diffusion pipeline

Add face detection for crop alignment

Add loading skeletons

Add history of generated images

Multi-character support for group photos

Storybook page rendering

Move frontend to a proper React project (optional)

👤 Author

Pankaj Kumar
GitHub: https://github.com/Pankajash
