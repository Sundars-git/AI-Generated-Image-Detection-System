import requests
import io
import numpy as np
from PIL import Image

# Create dummy image
img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype='uint8'))
buff = io.BytesIO()
img.save(buff, format="JPEG")
buff.seek(0)
# Reset buffer for request
buff.seek(0)

url = "http://127.0.0.1:8000/predict"
# files dict: {field_name: (filename, file_object, content_type)}
files = {"file": ("test.jpg", buff, "image/jpeg")}

print("Sending request to API...")
try:
    response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print(f"AI Probability: {data.get('ai_probability')}")
        print(f"Real Probability: {data.get('real_probability')}")
        if data.get("heatmap_image"):
            print("Heatmap image received (Base64).")
        else:
            print("No heatmap image received.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except requests.exceptions.ConnectionError:
    print("Connection refused. Is the backend running?")
