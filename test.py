import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def read_rfid():
    reader = SimpleMFRC522()

    try:
        print("Positionnez votre carte RFID sur le lecteur...")
        id, text = reader.read()
        print("L'ID de la carte est : {}".format(id))
    finally:
        GPIO.cleanup()

# Appel de la fonction pour lire l'ID de la carte
read_rfid()
