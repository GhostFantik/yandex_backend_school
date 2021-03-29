from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from workshop.app import app
import pytest

client = TestClient(app)


@pytest.mark.order(1)
def test_create_couriers_wrong_type(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'footeeer',
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:00", "09:00-11:00"],
            }
        ]
    })
    response = client.post('/couriers', json=json)
    assert response.status_code == 400
    assert response.json()['validation_error']['couriers'][0]['id'] == 1


@pytest.mark.order(2)
def test_create_couriers_wrong_time_format(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'foot',
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:00000", "09:00-11000:00"],
            }
        ]
    })
    response = client.post('/couriers', json=json)
    assert response.status_code == 400
    assert response.json()['validation_error']['couriers'][0]['id'] == 1


@pytest.mark.order(3)
def test_create_couriers_extra_some_field(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'foot',
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:00", "09:00-11:00"],
                'some_extra_field': 'some data'
            }
        ]
    })
    response = client.post('/couriers', json=json)
    assert response.status_code == 400
    assert response.json()['validation_error']['couriers'][0]['id'] == 1


@pytest.mark.order(4)
def test_create_couriers_without_some_field(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'courier_id': 1,
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:00", "09:00-11:00"]
            }
        ]
    })
    response = client.post('/couriers', json=json)
    assert response.status_code == 400
    assert response.json()['validation_error']['couriers'][0]['id'] == 1


@pytest.mark.order(5)
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
    response = client.post('/couriers', json=json)
    assert response.status_code == 201
    assert response.json() == jsonable_encoder({'couriers': [{'id': 1}, {'id': 2}]})


@pytest.mark.order(6)
def test_create_same_couriers(temp_db):
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
    response = client.post('/couriers', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == 'courier_id = 1 already exist'


@pytest.mark.order(7)
def test_patch_courier_with_extra_field(temp_db):
    json = jsonable_encoder({
        'regionees': [10, 20]
    })
    response = client.patch('/couriers/1', json=json)
    assert response.status_code == 400



