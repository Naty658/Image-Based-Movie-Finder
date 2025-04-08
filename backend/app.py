from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
from collections import Counter

app = Flask(__name__)
CORS(app)

IMGBB_API_KEY = 'fed55b46b1c65b3a1b7ac2d66ec03276'

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    res = requests.post(
        f'https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}',
        files={'image': (file.filename, file.stream)}
    )

    json_data = res.json()
    print(json_data)

    if 'data' not in json_data:
        return "Upload failed: " + str(json_data), 400

    image_url = json_data['data']['url']
    return image_url, 200, {'Content-Type': 'text/plain'}

@app.route('/save-text', methods=['POST'])
def save_text():
    data = request.get_json()
    text = data.get('text', '')

    # Save screen result
    with open("bing_results.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # Lowercase text once
    text_lower = text.lower()

    # Load movie list
    with open("movies.txt", "r", encoding="utf-8") as f:
        movies = [line.strip() for line in f]

    counter = Counter()
    for title in set(movies):
        title_lower = title.lower()
        pattern = re.compile(r'(^|\n)' + re.escape(title_lower) + r'\b')
        matches = pattern.finditer(text_lower)
        if sum(1 for _ in matches) >= 3:
            counter[title] = 1

    matched = list(counter.keys())

    # Save matched results
    with open("matched_movies.txt", "w", encoding="utf-8") as f:
        for m in matched:
            f.write(m + "\n")

    print("✅ Matched movies (3+ times, start only):", matched)
    return jsonify({"matched": matched}), 200

if __name__ == '__main__':
    app.run(port=5000)
