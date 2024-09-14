from requests import request

with open('./example_csv.csv', 'rb') as f:
    r = request(method="POST", url="http://localhost:8100/upload", files={'file': f})

print(r.content)