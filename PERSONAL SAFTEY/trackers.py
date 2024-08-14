import sys
import json
import os
import time
from datetime import datetime, timedelta
import pyaudio
import wave
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
                             QWidget, QMessageBox, QProgressBar, QListWidget, QTabWidget, QComboBox, QTextEdit,
                             QInputDialog, QDialog, QStyleFactory, QListWidgetItem)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QIcon, QFont, QDesktopServices
from PyQt5.QtWebEngineWidgets import QWebEngineView
import geocoder
from twilio.rest import Client
import folium
import schedule
import requests
import speech_recognition as sr
import pyttsx3
import phonenumbers
import webbrowser
import psutil  # For battery monitoring

class LocationTracker(QThread):
    location_update = pyqtSignal(list)

    def run(self):
        while True:
            location = geocoder.ip('me').latlng
            self.location_update.emit(location)
            time.sleep(300)  # Update every 5 minutes

class VoiceInteraction(QThread):
    finished = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.is_tts_running = False  # Track if TTS is currently running

    def run(self):
        self.voice_command()

    def text_to_speech(self, text):
        if not self.is_tts_running:
            self.is_tts_running = True
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.is_tts_running = False

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Sorry, I did not understand that."
            except sr.RequestError:
                return "Sorry, there was a problem with the request."

    def activate_sos(self):
        self.finished.emit("SOS Activated")

    def cancel_sos(self):
        self.finished.emit("SOS Cancelled")

    def safe_check_in(self):
        self.finished.emit("Checked in Safely")

    def update_location(self):
        self.finished.emit("Location Updated")

    def call_emergency_services(self):
        self.finished.emit("Calling Emergency Services")

    def find_nearby_safe_places(self):
        self.finished.emit("Finding Nearby Safe Places")

    def analyze_mood(self):
        self.finished.emit("Mood Analyzed")

    def voice_command(self):
        self.text_to_speech("Please speak your command")
        command = self.speech_to_text()

        if "sos" in command.lower():
            self.activate_sos()
        elif "cancel" in command.lower() and "sos" in command.lower():
            self.cancel_sos()
        elif "check in" in command.lower():
            self.safe_check_in()
        elif "location" in command.lower():
            self.update_location()
        elif "emergency" in command.lower() and "call" in command.lower():
            self.call_emergency_services()
        elif "nearby" in command.lower() and "safe" in command.lower():
            self.find_nearby_safe_places()
        elif "mood" in command.lower():
            self.text_to_speech("How are you feeling?")
            mood = self.speech_to_text()
            self.mood_input.setText(mood)  # Assuming self.mood_input is a UI element
            self.analyze_mood()
        else:
            self.text_to_speech("Command not recognized. Please try again.")
