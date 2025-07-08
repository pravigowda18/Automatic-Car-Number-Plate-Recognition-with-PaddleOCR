import os
import cv2
from flask import Flask, render_template, request, Response, jsonify
from ultralytics import YOLO
from car_plate import gen_frames_with_text
import car_plate


app = Flask(__name__)
# model = YOLO('best.pt')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames_with_text(0),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_owner_details', methods=['GET'])
def get_owner_details():
    if car_plate.matched_record:
        return jsonify(car_plate.matched_record), 200
    return jsonify({"message": "No match found"}), 404

@app.route('/start_stream', methods=['POST'])
def start_stream():
    car_plate.streaming = True
    return "Streaming started", 200


@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    car_plate.streaming = False
    return "Streaming stopped", 200


if __name__ == '__main__':
    app.run(debug=True)