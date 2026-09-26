# Personnel Tracking System

AI-powered personnel tracking system designed to monitor the latest known
location of employees using multiple cameras.

The system combines object detection, multi-object tracking, face recognition,
and a local dashboard to identify employees and determine their latest detected
location.

## Features

- Person detection with YOLO
- Multi-object tracking with ByteTrack
- Face recognition with InsightFace
- Employee identification
- Multi-camera support
- Webcam support
- Smartphone/IP camera support
- SQLite database
- Detection history
- Latest employee location
- Unknown person detection
- Unknown-person alerts
- Local web dashboard
- Camera management through database configuration


## Architecture

```text
Camera
   |
   v
Camera Manager
   |
   v
YOLO + ByteTrack
   |
   v
Face Recognition
   |
   +-------------------+
   |                   |
Known Employee      Unknown Person
   |                   |
   v                   v
Detection Service   Alert Service
   |                   |
   +---------+---------+
             |
             v
          SQLite
             |
             v
      Location Service
             |
             v
       Flask Dashboard


## Project Structure

personnel_tracking/
│
├── app/
│   ├── database/
│   ├── models/
│   ├── services/
│   └── web/
│
├── dashboard/
│   ├── templates/
│   └── static/
│
├── dataset/
│   └── faces/
│
├── tests/
│
├── vision/
│   ├── camera.py
│   ├── camera_stream.py
│   ├── detector.py
│   ├── face_database.py
│   ├── face_recognition.py
│   ├── identity.py
│   ├── pipeline.py
│   ├── track_identity.py
│   └── ...
│
├── run_dashboard.py
├── requirements.txt
├── .gitignore
└── README.md

