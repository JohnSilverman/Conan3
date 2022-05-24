from fastapi.testclient import TestClient
import random

from main import app

client = TestClient(app)

def test_post_subjects():
    response = client.post("/subjects",
                           json = {
                               "subject_name": "test_subject" + str(random.random()),
                               "random_rate": 0.3,
                               "overlap_rate": 0.3,
                               "status" : "ready",
                               "task": "TextClassification"
                           })
    print("post response", response.json())
    subject_id = response.json()['id']
    assert response.status_code == 200
    assert response.json()['status'] == "ready"


def test_modify_subjects():
    status_token = "modified" + str(int(random.random() * 1000))
    response = client.put("/subjects",
                           json={
                               "id": 1,
                               "subject_name": "test_subject" + str(random.random()),
                               "random_rate": 0.3,
                               "overlap_rate": 0.3,
                               "status" : status_token,
                               "task": "TextClassification"
                           })

    print("modify response", response.json())

    assert response.status_code == 200
    assert response.json()['status'] == status_token

def test_get_subjects():
    response = client.get("/subjects")
    assert response.status_code == 200