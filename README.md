# 🌎 Environmental Friendliness Calculator
Welcome to the Environmental Barcode Scanner project! This tool combines computer vision, environmental analysis, AI, and Flask to assess the environmental friendliness of products based on their ingredients. With just a scan of a barcode, you'll uncover a product's impact on the planet! 🌱

## 🛠 Features
- **Barcode Scanning:** Utilize your phone's camera or webcam to scan barcodes in real time.
- **Environmental Scoring:** Evaluate the environmental impact of a product's ingredients with AI-powered scoring.
- **Flask Integration:** Seamlessly serve results through a user-friendly web interface.
- **Database Support:** Store and retrieve product information for future reference.

## 🧰 Requirements
**- Python 3.8+**
**- Libraries:**
  - cv2 (OpenCV) 📷
  - pyzbar (Barcode decoding)
  - dotenv (API key management)
  - Flask (Web server)
  - OpenAI (AI-powered ingredient evaluation)
**- External APIs:**
  - **GOUPC:** For fetching product data.
  - **OpenRouter:** For AI-based ingredient scoring.

## 🚀 Installation
**1. Clone the repository:**
```
git clone https://github.com/yourusername/environmental-barcode-scanner.git
cd environmental-barcode-scanner
```
**2. Install dependencies.**
```
pip install -r requirements.txt
```
**3. Set up environment variables:**
- create a .env file
```
API_KEY=your_openrouter_api_key
GOUPC_API_KEY=your_goupc_api_key
```
**4. Run the Flask app.**

## 📋 Usage
1. Navigate to the ```/main``` endpoint in your browser to access the homepage.
2. Select Camera to scan a product's barcode.
3. Once scanned, view the Environmental Score and product details.

## 📜 Code Highlights
# Barcode Scanning
```
cap = cv2.VideoCapture("http://192.168.1.151:4747/video")
while cap.isOpened():
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    detectedBarcode = decode(frame)
    # Process detected barcodes...
```
# Environment Scoring with AI
```
client.chat.completions.create(
    model="meta-llama/llama-3.2-11b-vision-instruct:free",
    messages=[
        {"role": "user", "content": "Provide a score from 0-100 for this ingredient's environmental friendliness."},
        {"role": "user", "content": ingredient}
    ]
)
```
## 🌟 Future Improvements
- Mobile App Support 📱
- Expanded Ingredient Database 🧪
- Detailed Score Breakdown 📊
