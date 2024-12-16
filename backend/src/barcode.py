import cv2 
from pyzbar.pyzbar import decode
from dotenv import load_dotenv
from dotenv import find_dotenv
import re
from openai import OpenAI
import os
import subprocess
import json

# Load API keys
load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.environ['API_KEY']
GOUPC_API_KEY = os.environ['GOUPC_API_KEY']

storedBarcodes = []

average = 0

def startCam():
    global storedBarcodes

    # Clear stored barcodes array
    storedBarcodes = []

    # use cam on phone
    cap = cv2.VideoCapture("http://192.168.1.151:4747/video")

    while cap.isOpened():
        success,frame = cap.read()
        
        # Get mirror image
        frame  = cv2.flip(frame,1)

        # Detect and decode barcode 
        detectedBarcode = decode(frame)
        
        # Codes in barcode 
        for barcode in detectedBarcode:
            # If barcode is not blank 
            if barcode.data != "" and barcode.data not in storedBarcodes:
                storedBarcodes.append(re.findall(r'\d+', str(barcode.data)))
                print(storedBarcodes)
        cv2.imshow('Scan Barcode' , frame)
        
        # Close webcam once barcode scanned
        if len(storedBarcodes) == 1:
            cap.release()
            cv2.destroyAllWindows()
            break
            
        if cv2.waitKey(1) == ord('q'):
            break

# -------------------------------------------------------------

productNameAndDesc = []

def getData():
    global productNameAndDesc
    productNameAndDesc = []
    
    response = subprocess.check_output(['curl', '-s', f"https://go-upc.com/api/v1/code/{storedBarcodes[0][0]}?key={GOUPC_API_KEY}&format=true"])
    jsonResponse = json.loads(response.decode('utf-8'))

    cleaned = []

    for key in jsonResponse['product']:
        cleaned.append(jsonResponse['product'][key])
    
    productNameAndDesc.append(cleaned[0])
    productNameAndDesc.append(cleaned[1])
    
    productIngredients = [] 

    if isinstance(cleaned[8], dict):
        for item in cleaned[8]:
            productIngredients.append(cleaned[8]['text'].split(','))
    else:
        print("PRODUCT INGREDIENTS CANNOT BE ACCESSED")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=f"{OPENROUTER_API_KEY}"
    )

    scores = []

    def getScore(ingredient):
        completion = client.chat.completions.create(
        model="meta-llama/llama-3.2-11b-vision-instruct:free",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "You are a environmental assisant that deems ingredients of a given item environmentally friendly or not. You will not be coding.\
                    Given an ingredient, look into its background and see if its environmentally safe or not. Give this ingredient a score from 0-100, with 0\
                        being not environmentally friendly, and 100 being environmentally friendly. Keep in mind that Water scores 100.\
                            Just output the numerical 0-100 score ONCE please (without explanation)."
                },
                {
                "type": "text",
                "text": f"{ingredient}r"
                },  
            ]
            }
        ]
        )

        numbers = ""

        for char in completion.choices[0].message.content:
            if char.isdigit():
                numbers += char

        scores.append(int(numbers))

    if len(productIngredients) >= 1:
        for ingredient in productIngredients[0]:
            getScore(ingredient)
    if len(scores) < 1:
        average = "ERROR: PRODUCT INGREDIENTS NOT FOUND"
    else:
        average = round(sum(scores) / len(scores), 1)
    return average

if __name__ == "__main__":
    startCam()
    
