# Face2FameAI 

A web app where users can discover movies based on their celebrity lookalike.



##  About

Face2FameAI is an AI-powered celebrity lookalike web application built using React, Flask, and DeepFace.

Users can upload their photo and the app:

- Detects their celebrity lookalike
- Shows the matched celebrity image
- Recommends popular movies of that celebrity



##  Features

- Face recognition using DeepFace
- Celebrity similarity matching
- Movie recommendations
- Responsive modern UI
- React frontend
- Flask backend
- Fast embedding-based face comparison



##  Tech Stack

### Frontend
- React.js
- React Router
- CSS3

### Backend
- Flask
- DeepFace
- TensorFlow
- NumPy



##  How It Works

1. User uploads an image
2. Flask backend receives image
3. DeepFace generates face embeddings
4. Embeddings are compared with celebrity embeddings
5. Closest celebrity match is returned
6. Recommended movies are displayed



##  Project Structure

```text
face2fameai/
│
├── backend/
│   ├── app.py
│   ├── embeddings.pkl
│   ├── actors/
│   └── uploads/
│
├── frontend/
│   ├── src/
│   ├── Home.js
│   ├── Result.js
│   └── Result.css
│
└── README.md
```



##  Installation

### Backend Setup

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

Run backend:

```bash
python app.py
```


### Frontend Setup

```bash
cd frontend

npm install

npm start
```


##  Future Improvements

- Top 3 celebrity matches
- Movie posters
- Trailers
- AI confidence percentage
- User authentication
- Cloud deployment



##  Author

Built by me

GitHub:
https://github.com/aafianaz2027
