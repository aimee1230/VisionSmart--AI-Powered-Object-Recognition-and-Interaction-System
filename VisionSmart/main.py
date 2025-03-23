import sys
import cv2
import pyttsx3
import numpy as np
import torch
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
                             QWidget, QTextBrowser, QGridLayout, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer
from detection import detect_objects

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

class GameUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gamified Object Detection")
        self.setGeometry(100, 100, 900, 600)
        self.score = 0  # Score system

        # Main Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Score Label
        self.score_label = QLabel(f"Score: {self.score}")
        self.layout.addWidget(self.score_label)

        # Start Page Label
        self.label = QLabel("🎮 Welcome to VisionSmart: A Real-Time Object Detection Game!\nClick Start to Begin.")
        self.layout.addWidget(self.label)

        # Start Button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_detection)
        self.layout.addWidget(self.start_button)

        # Camera Feed Label
        self.camera_label = QLabel()
        self.layout.addWidget(self.camera_label)

        # Grid Layout for Detected Objects
        self.object_grid = QGridLayout()
        self.layout.addLayout(self.object_grid)

        self.central_widget.setLayout(self.layout)

        # Timer for Real-Time Updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = None  # Webcam Capture

    def start_detection(self):
        """Start webcam and begin real-time object detection"""
        self.label.setText("Detecting objects...")
        self.start_button.setDisabled(True)
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)  # Refresh every 30ms

    def update_frame(self):
        """Continuously capture frames and perform object detection"""
        ret, frame = self.cap.read()
        if not ret:
            return

        annotated_frame, detected_objects = detect_objects(frame)
        self.display_detected_objects(detected_objects)

        # Convert OpenCV frame to Qt format
        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qt_img = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qt_img))

    def display_detected_objects(self, detected_objects):
        """Update the grid layout with detected objects and clickable links"""
        for i in reversed(range(self.object_grid.count())):  # Clear previous widgets
            self.object_grid.itemAt(i).widget().deleteLater()

        row = 0
        for obj in detected_objects:
            if "Buy Here:" in obj:
                object_name = detected_objects[row - 1]  # Previous item is the object name
                buy_button = QPushButton(f"🛒 Buy {object_name}")
                buy_button.clicked.connect(lambda _, url=obj.split("Buy Here: ")[1]: self.open_link(url))
                self.object_grid.addWidget(buy_button, row, 1)
            else:
                obj_label = QLabel(f"🔍 {obj}")
                self.object_grid.addWidget(obj_label, row, 0)
            row += 1

    def open_link(self, url):
        """Open Amazon link in browser and increase score"""
        webbrowser.open(url)
        self.score += 10  # Increase score
        self.score_label.setText(f"Score: {self.score}")

    def closeEvent(self, event):
        if self.cap is not None:
            self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameUI()
    window.show()
    sys.exit(app.exec())
