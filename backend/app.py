from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from deepface import DeepFace
import numpy as np
import pickle
import os
import cv2
import gc  

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ACTORS_FOLDER = os.path.join(BASE_DIR, "actors")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

movies_data = {

    "Aamir Khan": [
        "3 Idiots",
        "Dangal",
        "Lagaan"
    ],

    "Aditi Rao": [
        "Heeramandi",
        "Padmaavat",
        "Murder 3"
    ],

    "Aditya Roy Kapoor": [
        "Aashiqui 2",
        "Malang",
        "Yeh Jawaani Hai Deewani"
    ],

    "aishwarya rai": [
        "Jodhaa Akbar",
        "Devdas",
        "Dhoom 2"
    ],

    "Ajay Devgn": [
        "Drishyam",
        "Singham",
        "Golmaal"
    ],

    "Akshay Kumar": [
        "Bhool Bhulaiyaa",
        "Hera Pheri",
        "Kesari"
    ],

    "alia bhatt": [
        "Raazi",
        "Gangubai Kathiawadi",
        "Dear Zindagi"
    ],

    "Ameesha Patel": [
        "Kaho Naa Pyaar Hai",
        "Gadar",
        "Humraaz"
    ],

    "amrita rao": [
        "Vivah",
        "Main Hoon Na",
        "Ishq Vishk"
    ],

    "ananya pandey": [
        "Dream Girl 2",
        "Kho Gaye Hum Kahan",
        "Student of the Year 2"
    ],

    "anushka sharma": [
        "PK",
        "Sultan",
        "Ae Dil Hai Mushkil"
    ],

    "Arjun Kapoor": [
        "2 States",
        "Ishaqzaade",
        "Ki & Ka"
    ],

    "Asin": [
        "Ghajini",
        "Ready",
        "Housefull 2"
    ],

    "ayesha takia": [
        "Wanted",
        "Dor",
        "Tarzan"
    ],

    "Ayushmann Khurrana": [
        "Andhadhun",
        "Dream Girl",
        "Bala"
    ],

    "Bipasha Basu": [
        "Raaz",
        "Jism",
        "Dhoom 2"
    ],

    "Deepika Padukone": [
        "Piku",
        "Pathaan",
        "Yeh Jawaani Hai Deewani"
    ],

    "Disha Patani": [
        "MS Dhoni",
        "Malang",
        "Ek Villain Returns"
    ],

    "Gauhar Khan": [
        "Rocket Singh",
        "Begum Jaan",
        "Ishaqzaade"
    ],

    "genelia": [
        "Jaane Tu Ya Jaane Na",
        "Tere Naal Love Ho Gaya",
        "Force"
    ],

    "Hrithik Roshan": [
        "Krrish",
        "War",
        "Zindagi Na Milegi Dobara"
    ],

    "Ibrahim Ali Khan": [
        "Nadaaniyan"
    ],

    "ileana": [
        "Barfi",
        "Rustom",
        "Main Tera Hero"
    ],

    "Ishaan Khatter": [
        "Dhadak",
        "Beyond The Clouds",
        "Pippa"
    ],

    "Jacqueline Fernandez": [
        "Kick",
        "Race 2",
        "Judwaa 2"
    ],

    "Juhi Chawla": [
        "Darr",
        "Yes Boss",
        "Hum Hain Rahi Pyar Ke"
    ],

    "kajol": [
        "DDLJ",
        "My Name Is Khan",
        "Kabhi Khushi Kabhie Gham"
    ],

    "kangana ranaut": [
        "Queen",
        "Fashion",
        "Tanu Weds Manu"
    ],

    "kareena kapoor": [
        "Jab We Met",
        "3 Idiots",
        "Bodyguard"
    ],

    "karishma kapoor": [
        "Raja Hindustani",
        "Dil To Pagal Hai",
        "Biwi No.1"
    ],

    "Kartik Aaryan": [
        "Bhool Bhulaiyaa 2",
        "Sonu Ke Titu Ki Sweety",
        "Satyaprem Ki Katha"
    ],

    "katrina kaif": [
        "Tiger Zinda Hai",
        "Zindagi Na Milegi Dobara",
        "Namastey London"
    ],

    "Kiara Advani": [
        "Shershaah",
        "Kabir Singh",
        "JugJugg Jeeyo"
    ],

    "kokona sen": [
        "Wake Up Sid",
        "Lipstick Under My Burkha",
        "A Death in the Gunj"
    ],

    "Kriti Sanon": [
        "Mimi",
        "Luka Chuppi",
        "Bareilly Ki Barfi"
    ],

    "madhuri dixit": [
        "Devdas",
        "Hum Aapke Hain Koun",
        "Dil To Pagal Hai"
    ],

    "nargis fakri": [
        "Rockstar",
        "Madras Cafe",
        "Main Tera Hero"
    ],

    "Nushrratt Bharuccha": [
        "Dream Girl",
        "Pyaar Ka Punchnama",
        "Chhorii"
    ],

    "Parineeti Chopra": [
        "Hasee Toh Phasee",
        "Ishaqzaade",
        "Kesari"
    ],

    "Preity Zinta": [
        "Kal Ho Naa Ho",
        "Veer-Zaara",
        "Koi Mil Gaya"
    ],

    "priyanka chopra": [
        "Don",
        "Barfi",
        "Fashion"
    ],

    "Priyanshu Chatterjee": [
        "Tum Bin",
        "Bhootnath",
        "Julie"
    ],

    "Rajkummar Rao": [
        "Stree",
        "Shahid",
        "Badhaai Do"
    ],

    "Rani Mukerji": [
        "Black",
        "Mardaani",
        "Hum Tum"
    ],

    "Ranveer Singh": [
        "Padmaavat",
        "83",
        "Gully Boy"
    ],

    "Saif Ali Khan": [
        "Love Aaj Kal",
        "Race",
        "Omkara"
    ],

    "Salman Khan": [
        "Sultan",
        "Bajrangi Bhaijaan",
        "Tiger 3"
    ],

    "Shahid Kapoor": [
        "Kabir Singh",
        "Jab We Met",
        "Haider"
    ],

    "shraddha kapoor": [
        "Aashiqui 2",
        "Stree",
        "Tu Jhoothi Main Makkaar"
    ],

    "Sridevi": [
        "English Vinglish",
        "Mr India",
        "Mom"
    ],

    "Siddhant Chaturvedi": [
        "Gully Boy",
        "Kho Gaye Hum Kahan",
        "Phone Bhoot"
    ],

    "Sidharth Malhotra": [
        "Shershaah",
        "Ek Villain",
        "Kapoor & Sons"
    ],

    "sonakshi sinha": [
        "Dabangg",
        "Lootera",
        "Rowdy Rathore"
    ],

    "sonali bendre": [
        "Sarfarosh",
        "Hum Saath Saath Hain",
        "Duplicate"
    ],

    "sonam kapoor": [
        "Neerja",
        "Khoobsurat",
        "Raanjhanaa"
    ],

    "Shah Rukh Khan": [
        "Jawan",
        "Pathaan",
        "Chennai Express"
    ],

    "Sunny Deol": [
        "Gadar",
        "Border",
        "Damini"
    ],

    "Sushant Singh Rajput": [
        "MS Dhoni",
        "Chhichhore",
        "Kai Po Che"
    ],

    "Taapsee Pannu": [
        "Pink",
        "Thappad",
        "Badla"
    ],

    "Tara Sutaria": [
        "Marjaavaan",
        "Heropanti 2",
        "Ek Villain Returns"
    ],

    "Tiger Shroff": [
        "War",
        "Baaghi",
        "Heropanti"
    ],

    "Urvashi Rautela": [
        "Sanam Re",
        "Great Grand Masti",
        "Hate Story 4"
    ],

    "Varun Dhawan": [
        "Badrinath Ki Dulhania",
        "October",
        "Judwaa 2"
    ],

    "Varun Sharma": [
        "Fukrey",
        "Chhichhore",
        "Roohi"
    ],

    "Vedang Raina": [
        "The Archies"
    ],

    "Vicky Kaushal": [
        "Uri",
        "Sardar Udham",
        "Raazi"
    ],

    "Vidya Balan": [
        "Kahaani",
        "The Dirty Picture",
        "Bhool Bhulaiyaa"
    ],

    "Yami Gautam": [
        "Article 370",
        "A Thursday",
        "Uri"
    ],

    "Zareen Khan": [
        "Veer",
        "Housefull 2",
        "Hate Story 3"
    ]
}

EMBEDDINGS_PATH = os.path.join(BASE_DIR, "embeddings.pkl")

with open(EMBEDDINGS_PATH, "rb") as f:
    actor_embeddings = pickle.load(f)

@app.route("/")
def home():
    return "Face2FameAI Backend Running"

@app.route("/actors/<filename>")
def get_actor_image(filename):
    return send_from_directory("actors", filename)

@app.route("/upload", methods=["POST"])
def upload():
    file_path = None
    try:
        print("UPLOAD HIT")

        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        file = request.files["image"]
        
        file_path = os.path.join(UPLOAD_FOLDER, "temp_upload.jpg")
        file.save(file_path)

        img = cv2.imread(file_path)
        if img is not None:

            h, w = img.shape[:2]
            max_size = 640
            if max(h, w) > max_size:
                scale = max_size / max(h, w)
                img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
                cv2.imwrite(file_path, img) # Overwrite with the small version
        
        print("File saved and resized:", file_path)

        result = DeepFace.analyze(
            img_path=file_path,
            actions=['emotion'], 
            detector_backend='opencv', 
            enforce_detection=False
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        print("ERROR IN UPLOAD:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        try:
            from tensorflow.keras import backend as K
            K.clear_session() 
        except Exception:
            pass
        
        gc.collect() 

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
