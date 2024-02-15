# This is a sample Python script.
import logging

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, request, jsonify, send_from_directory

from Calculate_histogram import is_white

app = Flask(__name__)


@app.route('/api/is_white', methods=['POST'])
def is_jpeg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Check if the filename ends with .jpg or .jpeg
    if not file.filename.endswith(('.jpg', '.jpeg')):
        return jsonify({'is_jpeg': False}), 400

    try:
        # Try opening the file as a JPEG image
        value = is_white(file)
        logging.info("SUCCESSFUL")
        return jsonify({'is_white': value}), 200
    except (IOError, OSError):
        # If opening fails, it's not a valid JPEG
        logging.info("UNSUCCESSFUL")
        return jsonify({'is_jpeg': False}), 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
