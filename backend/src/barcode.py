import cv2 
from pyzbar.pyzbar import decode
from dotenv import load_dotenv
from dotenv import find_dotenv
import re
from openai import OpenAI
import os
import subprocess
import json
import google.generativeai as genai

# Load API keys
load_dotenv(find_dotenv())
AIMLAPI_API_KEY = os.environ['API_KEY']
GOUPC_API_KEY = os.environ['GOUPC_API_KEY']

storedBarcodes = []

average = 0

def startCam():
    global storedBarcodes

    # Clear stored barcodes array
    storedBarcodes = []

    # use cam on phone; alternatively, you can replace with '0' to use native webcam
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
productImageLink = ''

def getData():
    global productNameAndDesc
    global productImageLink

    # Clear previous entries
    productNameAndDesc = []
    productImageLink = ''

    response = subprocess.check_output(['curl', '-s', f"https://go-upc.com/api/v1/code/{storedBarcodes[0][0]}?key={GOUPC_API_KEY}&format=true"])
    jsonResponse = json.loads(response.decode('utf-8'))

    cleaned = []
    
    for key in jsonResponse['product']:
        cleaned.append(jsonResponse['product'][key])
        if 'imageUrl' in jsonResponse['product'].keys() and len(productImageLink) < 1:
            productImageLink += jsonResponse['product']['imageUrl']

    productNameAndDesc.append(cleaned[0])
    productNameAndDesc.append(cleaned[1])

    productIngredients = [] 

    if isinstance(cleaned[8], dict):
        for item in cleaned[8]:
            productIngredients.append(cleaned[8]['text'].split(','))
    else:
        print("PRODUCT INGREDIENTS CANNOT BE ACCESSED")

    genai.configure(api_key=f"{AIMLAPI_API_KEY}")
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    scores = []

    def getScore(ingredientList):
        response = model.generate_content(f"Give a 0-100 rating for each of these ingredients based on its environmental friendliness: {ingredientList}. Do not include reasoning, just output the numbers in a comma seperated list in [] format")

        # Clean response
        response_text = response.text.strip("[]")  
        numbers = response_text.split(",")  

        scores = []

        for number in numbers:
            cleaned_number = ''.join(number.split()) 
            if cleaned_number.isdigit():
                scores.append(int(cleaned_number))

        return scores

    if len(productIngredients) >= 1:    
        for num in getScore(productIngredients):
            scores.append(int(num))
    
    if len(scores) < 1:
        average = "ERROR: PRODUCT INGREDIENTS NOT FOUND"
    else:
        average = round(sum(scores) / len(scores), 1)

    return average

if __name__ == "__main__":
    startCam()
    getData()
    
