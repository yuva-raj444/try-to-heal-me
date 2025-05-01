import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('models/gemini-2.0-flash-lite')

def analyze_medical_image(image_path):
    try:
        img = Image.open(image_path)
        prompt = """Analyze this medical image and provide:
        1. A possible diagnosis of the visible condition (1-2 points)
        2. Safe home remedies (if applicable) (6-7 detailed points)
        3. Critical warning signs that would require immediate medical attention (exactly 3 most important points)
        
        For home remedies, include detailed steps and specific recommendations for wound care, pain management, and recovery.
        For warning signs, focus only on the most critical symptoms that require immediate medical attention.
        
        Please format the response clearly with these sections.
        Important: Format each point with a bullet point (•) at the start of the line.
        End with a brief medical disclaimer."""
        
        response = model.generate_content([prompt, img])
        text = response.text
        
        # Format sections with bullet points and clean up markdown
        sections = text.split('\n')
        formatted_sections = []
        
        for line in sections:
            line = line.strip()
            # Remove markdown symbols
            line = line.replace('**', '').replace('*', '')
            # Clean up any multiple spaces
            line = ' '.join(line.split())
            
            if line:
                if line.startswith(('1.', '2.', '3.')):
                    formatted_sections.append('\n' + line)
                else:
                    if not line.startswith('•'):
                        line = '• ' + line
                    formatted_sections.append(line)
        
        return '\n'.join(formatted_sections)
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save file temporarily
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Analyze image
        analysis = analyze_medical_image(filepath)
        
        # Clean up
        os.remove(filepath)
        
        return render_template('results.html', analysis=analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)