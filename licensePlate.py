from ultralytics import YOLO
import cv2
from paddleocr import PaddleOCR

# Load YOLO model
model = YOLO("run/detect/weights/best.pt")

# Initialize PaddleOCR with new API settings
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

# OCR function using latest API
def paddle(img, bbox):
    x1, y1, x2, y2 = bbox
    x1, y1, x2, y2 = max(0, x1), max(0, y1), min(img.shape[1], x2), min(img.shape[0], y2)
    cropped_img = img[y1:y2, x1:x2]

    cropped_img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)

    result = ocr.predict(input=cropped_img_rgb)

    for res in result:
        txt = res['rec_texts']
        
    return txt

# Detection + OCR on video
def pred(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print(f"Error: Cannot open video file {path}")
        return

    while True:
        success, frame = cap.read()
        if not success:
            print("End of video stream or cannot read frame.")
            break

        results = model(frame)
        result = results[0]

        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                conf = float(box.conf[0])

                # Run OCR on detected region
                text = paddle(frame, [x1, y1, x2, y2])
                print(text)

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 225, 225), 2)

                # Draw label
                label = f'{conf:.2f} | {text}' if text else f'{conf:.2f}'
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("License Plate", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run with webcam (0) or path to video
pred(0)
