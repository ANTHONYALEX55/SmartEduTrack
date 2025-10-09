import requests
import json
data = [
    {

    "student_id" :5,
    "date" : "2025-10-06",
    "status" : "ABSENT"
},
{

    "student_id" :7,
    "date" : "2025-10-06",
    "status" : "ABSENT"
},
{

    "student_id" :8,
    "date" : "2025-10-06",
    "status" : "ABSENT"
}
]



url = "http://127.0.0.1:8000/api/students/attendance/mark/"
json_data = json.dumps(data)
response = requests.post(url, json=json_data)
print(response.json())
print(response.status_code)

print('cicd done')