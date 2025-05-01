# Health Diagnosis Assistant

A Flask web application that uses AI to analyze medical images and provide preliminary health insights.

## Features

- Modern, responsive UI with drag-and-drop image upload
- Image analysis using Google's Gemini Pro Vision AI
- Provides possible diagnosis, home remedies, and critical warning signs
- Secure image handling with temporary storage

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open the application in your web browser (default: http://localhost:5000)
2. Upload an image of your medical concern using the drag-and-drop interface
3. Click "Analyze Image" to receive AI-generated insights

## Important Notice

This application is for informational purposes only and should not be considered as professional medical advice. Always consult with a qualified healthcare provider for proper diagnosis and treatment.

## Security

- Images are temporarily stored and immediately deleted after analysis
- File size limit: 16MB
- Accepted file formats: PNG, JPG, GIF