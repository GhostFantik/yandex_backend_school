from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from workshop.app import app
import pytest

client = TestClient(app)


@pytest.mark.run(order=1)
def test_create_couriers(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'foot',
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:00", "09:00-11:00"]
            },
            {
                "courier_id": 2,
                "courier_type": "car",
                "regions": [
                    5,
                    12,
                    50
                ],
                "working_hours": [
                    "13:00-14:00",
                    "18:00-21:00"
                ]
            }
        ]
    })
    response = client.post('/couriers/', json=json)
    assert response.status_code == 201
    assert response.json() == jsonable_encoder({'couriers': [{'id': 1}, {'id': 2}]})
