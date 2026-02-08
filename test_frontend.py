import requests

url = "http://localhost:3000"
try:
    response = requests.get(url)
    if response.status_code == 200:
        print("Frontend is up and running!")
        if "<title>AI Image Detector</title>" in response.text:
            print("Title check: Passed")
        else:
            print("Title check: Failed (Title not found)")
    else:
        print(f"Frontend returned status: {response.status_code}")
except Exception as e:
    print(f"Frontend check failed: {e}")
