from requests import request

r = request(method="GET", url="http://localhost:8100/download", headers={'filename': 'example_csv.csv'})

with open("downloaded" + r.headers.get('filename'), 'w') as file:
    file.write(r.content.decode("utf-8"))