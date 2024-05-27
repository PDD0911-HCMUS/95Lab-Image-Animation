from flask import Flask, request
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS, cross_origin
import os
from demo import create_animation
import time
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['CORS_HEADERS'] = 'Content-Type'
upload_folder = 'upload'

@app.route('/animation/<filename>')
def serve_image(filename):
    return send_from_directory('Datasets/VisualGenome/VG_100K', filename)

@app.route('/animation', methods=['POST'])
@cross_origin()
def animation():
    # Kiểm tra xem có file trong request không
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file:
        # Lưu file
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)
        mode = request.form.get('mode')
        start_time = time.time()
        video_name = create_animation(source_image=filepath,mode=mode)
        end_time = time.time() - start_time

    return jsonify(
            {
                'ressult': video_name,
                'mode': mode,
                'time': end_time,
                'status': 200
            }
        )

if __name__ == '__main__':
    app.run(debug=True)