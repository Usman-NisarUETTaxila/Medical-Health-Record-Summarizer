import requests 
endpoint = "http://localhost:8000/patient-app/api/patients/"
response = requests.get(url=endpoint)
print(response.status_code)
print(response.text)