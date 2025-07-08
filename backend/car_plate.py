from ultralytics import YOLO
import cv2
from paddleocr import PaddleOCR
import json

streaming = False
matched_record = None

# Load model and OCR
model = YOLO("best.pt")
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)

# Load vehicle details from JSON
def load_plate_data():
    with open('plates.json', 'r') as file:
        return json.load(file)

plate_data = load_plate_data()

def match_plate(plate_text):
    plate_text_cleaned = plate_text.strip().replace(" ", "").upper()
    for record in plate_data:
        if record["license_number"].replace(" ", "").upper() == plate_text_cleaned:
            return record
    return None



# OCR helper
def paddle(img, bbox):
    x1, y1, x2, y2 = bbox
    x1, y1, x2, y2 = max(0, x1), max(0, y1), min(img.shape[1], x2), min(img.shape[0], y2)
    cropped_img = img[y1:y2, x1:x2]
    cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
    result = ocr.predict(input=cropped_img_rgb)

    texts = []
    for res in result:
        texts.extend(res['rec_texts'])  # assuming 'rec_texts' is a list
    return texts

# Stream video frames and text with OCR
def gen_frames_with_text(path):
    global streaming, matched_record
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {path}")
        return

    while streaming:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)
        result = results[0]

        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                # Run OCR
                texts = paddle(frame, [x1, y1, x2, y2])
                text_str = ", ".join(texts).strip()

                # Match plate
                if text_str:
                    # for text in text_str:
                    #     print(text)
                    matched_record = match_plate(text_str)
                    print(f"Matched Record: {matched_record}")

                # Draw bbox and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 225, 225), 2)
                label = f'{conf:.2f} | {text_str}'
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                # Optionally: also print or yield the text separately
                print(f"Detected Text: {text_str}")

        # Encode and yield annotated frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        

    cap.release()
