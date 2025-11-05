# 🚗 Automatic Car Number Plate Recognition with PaddleOCR

## 📖 Overview
This project is an **AI-powered License Plate Recognition System** that automatically detects car number plates from live video or camera input and recognizes the plate characters using **YOLOv8** and **PaddleOCR**.

Once the plate number is recognized, it checks for a match in a sample **JSON file (`plates.json`)** containing owner details.  
If a match is found, the system displays the owner’s information in real time via a web interface built with **Flask**.

---

## ⚙️ Key Features
- 🎯 **Automatic Number Plate Detection** using YOLOv8  
- 🧠 **Text Recognition** using PaddleOCR  
- 🔍 **Owner Data Matching** from `plates.json`  
- 🌐 **Web Interface** powered by Flask  
- 🖼️ **Real-time Video Stream Processing** with OpenCV  
- 🧩 **Easily Extendable** — Add more plate-owner pairs to JSON

---

## 🧰 Tech Stack
| Component | Technology Used |
|------------|------------------|
| **Backend** | Flask |
| **Detection Model** | YOLOv8 (Ultralytics) |
| **OCR Engine** | PaddleOCR |
| **Computer Vision** | OpenCV |
| **Data Format** | JSON |
| **Frontend** | HTML + Tailwind CSS |

---

## 📂 Project Structure
Automatic-Car-Number-Plate-Recognition-with-PaddleOCR/
- │
- ├── backend/
- │ ├── templates/
- │ │ └── index.html # Web interface
- │ └── app.py # Flask backend
- │
- ├── car_plate.py # Detection, OCR & data matching logic
- ├── best.pt # YOLOv8 trained model
- ├── plates.json # Demo JSON with owner data
- ├── output/ # (Optional) Output frames
- ├── run/detect/ # YOLO detection folder
- ├── licensePlate.py # Auxiliary script
- ├── LicensePlateReco.ipynb # Jupyter notebook version
- ├── requirements.txt # Dependencies
- ├── tailwind.config.js # Tailwind config
- └── .gitignore


---

## 🚀 Installation & Setup

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/pravigowda18/Automatic-Car-Number-Plate-Recognition-with-PaddleOCR.git
cd Automatic-Car-Number-Plate-Recognition-with-PaddleOCR 
```
---
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the Flask Server
```bash
cd backend
python app.py
```
Then open your browser and visit:
👉 http://127.0.0.1:5000

### 🧠 How It Works

1. The YOLOv8 model (best.pt) detects license plates in each frame.
2. Detected plate regions are passed to PaddleOCR, which extracts text from the cropped region.
3. The recognized plate text is compared against entries in plates.json.
4. If a match is found, owner details are displayed on the web interface.
5. Users can start or stop live video streaming through Flask endpoints


### 📡 API Endpoints
   | Endpoint             | Method | Description                           |
| -------------------- | ------ | ------------------------------------- |
| `/`                  | GET    | Renders the homepage (index.html)     |
| `/video_feed`        | GET    | Streams live detection video frames   |
| `/get_owner_details` | GET    | Returns matched owner details in JSON |
| `/start_stream`      | POST   | Starts the camera stream              |
| `/stop_stream`       | POST   | Stops the camera stream               |

### 📜 Example JSON Format
plates.json
```json
{
    "license_number": "GJ03ER0563",
    "owner": "John Doe",
    "address": "123 Maple Street, Springfield, IL",
    "make": "Toyota",
    "model": "Camry",
    "year": 2018,
    "color": "Blue",
    "registration_date": "2022-04-15",
    "expiration_date": "2025-04-15"
  },
```

### 🔮 Future Enhancements

- ☁️ Integrate with a real-time database instead of JSON
- 📱 Add a dashboard for viewing recognition history
- 🔐 Implement authentication for admin access
- 🧩 Add cloud deployment (AWS, Render, or Hugging Face Spaces)

### 🧑‍💻 Author
## Praveen S
- 📧 Email: pravisb0002@gmail.com
- 💼 LinkedIn: linkedin.com/in/praveens182002
- 🌐 Portfolio: pravigowda18.github.io/pravigowda18/
- 📦 GitHub Repo: Automatic Car Number Plate Recognition with PaddleOCR
