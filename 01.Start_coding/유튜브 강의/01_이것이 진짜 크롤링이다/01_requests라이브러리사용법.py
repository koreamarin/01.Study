import requests

response = requests.get("https://sellerlife.co.kr/keyword")

print(response.status_code)