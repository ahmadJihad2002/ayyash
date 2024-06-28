import subprocess

print("THIS MY TAKE A WHILE DEPENDING ON YOUR SYSTEM AND INTERNET SPEED\n\nPLEASE WAIT..\n\n")
try:
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
except KeyboardInterrupt:
    print("DOWNLOAD STOPPED")
    exit(0)

try:
    # importing prebuilt modules
    import pyttsx3
    from keras_preprocessing.sequence import pad_sequences
    import numpy as np
    from keras.models import load_model
    from pickle import load
    import speech_recognition as sr
    import sys
    import datetime
    from dotenv import load_dotenv
    from newsapi import NewsApiClient
    import re
    import requests
    from wolframalpha import Client
    import webbrowser
    import wikipedia
    import speedtest
    from youtubesearchpython import VideosSearch
    import smtplib
    import io
    import warnings
    from PIL import Image
    from stability_sdk import client
    import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
    import math
    import psutil
    import time
    from random import randint
    import AppOpener
    from pynput.keyboard import Key, Controller


except ImportError:
    print("MODULES NOT INSTALLED!")
    exit(0)
except KeyboardInterrupt:
    print("INTERRUPTED WHILE IMPORTING MODULES")

print("\n\nSETUP SUCCESSFUL")
