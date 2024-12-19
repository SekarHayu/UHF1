import requests

url = "https://api.tierkun.my.id/enter/209029"
body = {
                "capture": "ihoexw"
            }
response = requests.post(url, data=body)
print("url :", url)
print("Status code: ", response.status_code)
print("Response: ", response.json())
msg = response.json()
not_found = msg.get('error')