from flask import Flask, request, jsonify
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = '/app/input'
OUTPUT_FOLDER = '/app/output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <h1>Video to Image Converter</h1>
    <form action="/convert" method="post" enctype="multipart/form-data">
        <input type="file" name="video">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/convert', methods=['POST'])
def convert_video_to_images():
    if 'video' not in request.files:
        return "No video file found in the request", 400
    
    video_file = request.files['video']
    video_id = str(uuid.uuid4())
    input_video_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
    output_image_path = os.path.join(OUTPUT_FOLDER, video_id, "frame_%03d.jpg")
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    
    video_file.save(input_video_path)
    
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_video_path, "-vf", "fps=1/5", output_image_path],
            check=True
        )
        return jsonify({"message": "Video converted successfully", "video_id": video_id}), 200
    except subprocess.CalledProcessError as e:
        return f"Error during conversion: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
