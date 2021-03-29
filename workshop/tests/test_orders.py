from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from workshop.app import app
import pytest
import datetime

client = TestClient(app)


def increase_time_on_minutes(assign_time: str, minutes: int) -> str:
    ct = datetime.datetime.strptime(assign_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    ct += datetime.timedelta(minutes=minutes)
    return ct.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


@pytest.mark.order(9)
def test_create_orders_wrong_time(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'order_id': 1,
                'weight': 7,
                'region': 12,
                'delivery_hours': ['09:00-18000:00']

            }
        ]
    })
    response = client.post('/orders', json=json)
    assert response.status_code == 400
    assert response.json()['validation_error']['orders'][0]['id'] == 1


@pytest.mark.order(10)
def test_create_orders_extra_some_field(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'order_id': 1,
                'weight': 7,
                'region': 12,
                'delivery_hours': ['09:00-18:00'],
                'some_extra_field': 'some data'

            }
        ]
    })
    response = client.post('/orders', json=json)
    assert response.status_code == 400
    assert response.json()['validation_error']['orders'][0]['id'] == 1


@pytest.mark.order(11)
def test_create_orders_without_some_field(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'order_id': 1,
                'weight': 7,
                'delivery_hours': ['09:00-18:00'],

            }
        ]
    })
    response = client.post('/orders', json=json)
    assert response.status_code == 400
    assert response.json()['validation_error']['orders'][0]['id'] == 1


@pytest.mark.order(12)
def test_create_orders(temp_db):
    json = jsonable_encoder({
        'data': [
            {
                'order_id': 1,
                'weight': 7,
                'region': 12,
                'delivery_hours': ['09:00-18:00'],

            },
            {
                'order_id': 2,
                'weight': 15,
                'region': 12,
                'delivery_hours': ['09:00-18:00']
            },
            {
                'order_id': 3,
                'weight': 7,
                'region': 5,
                'delivery_hours': [
                    '09:00-12:00',
                    '16:00-21:30'
                ]
            }
        ]
    })
    response = client.post('/orders', json=json)
    assert response.status_code == 201
    assert response.json() == jsonable_encoder({'orders': [
        {'id': 1},
        {'id': 2},
        {'id': 3}
    ]})


@pytest.mark.order(13)
def test_assign_orders_not_exist_courier(temp_db):
    json = jsonable_encoder({
        'courier_id': 3
    })
    response = client.post('/orders/assign', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == 'courier_id does not exist!'

assign_time_1: str
assign_time_2: str

@pytest.mark.order(14)
def test_assign_orders(temp_db):
    json = jsonable_encoder({
        'courier_id': 1
    })
    response = client.post('/orders/assign', json=json)
    assert response.status_code == 200
    assert response.json()['orders'] == jsonable_encoder([{'id': 1}])
    global assign_time_1
    assign_time_1 = response.json()['assign_time']


@pytest.mark.order(15)
def test_assign_order_another_courier(temp_db):
    json = jsonable_encoder({
        'courier_id': 2
    })
    response = client.post('/orders/assign', json=json)
    assert response.status_code == 200
    assert response.json()['orders'] == jsonable_encoder([{'id': 2}, {'id': 3}])
    global assign_time_2
    assign_time_2 = response.json()['assign_time']


@pytest.mark.order(16)
def test_patch_courier(temp_db):
    json = jsonable_encoder({
        'regions': [12, 50]
    })
    response = client.patch('/couriers/2', json=json)
    assert response.status_code == 200
    assert response.json() == jsonable_encoder({
                'courier_id': 2,
                'courier_type': 'car',
                'regions': [12, 50],
                'working_hours': ["13:00-14:00", "18:00-21:00"]
            })


@pytest.mark.order(17)
def test_assign_order_after_patch(temp_db):
    json = jsonable_encoder({
        'courier_id': 2
    })
    response = client.post('/orders/assign', json=json)
    assert response.status_code == 200
    assert response.json()['orders'] == jsonable_encoder([{'id': 2}])
    assert assign_time_2 == response.json()['assign_time']


@pytest.mark.order(18)
def test_complete_order_without_courier(temp_db):
    ct = increase_time_on_minutes(assign_time_2, 1)
    json = jsonable_encoder({
        'courier_id': 2,
        'order_id': 3,
        'complete_time': ct
    })
    response = client.post('/orders/complete', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == 'This order does not have some courier'


@pytest.mark.order(19)
def test_complete_order_not_owner(temp_db):
    ct = increase_time_on_minutes(assign_time_1, 1)
    json = jsonable_encoder({
        'courier_id': 1,
        'order_id': 2,
        'complete_time': ct
    })
    response = client.post('/orders/complete', json=json)
    assert response.status_code == 400
    assert response.json()['detail'] == 'This courier does not own this order'


@pytest.mark.order(20)
def test_complete_order(temp_db):
    ct = increase_time_on_minutes(assign_time_2, 1)
    json = jsonable_encoder({
        'courier_id': 2,
        'order_id': 2,
        'complete_time': ct
    })
    response = client.post('/orders/complete', json=json)
    assert response.status_code == 200
    assert response.json() == jsonable_encoder({'order_id': 2})


@pytest.mark.order(21)
def test_get_courier_not_exist(temp_db):
    response = client.get('/couriers/3')
    assert response.status_code == 400
    assert response.json()['detail'] == 'courier_id does not exist!'


@pytest.mark.order(22)
def test_get_courier_not_completed_order(temp_db):
    response = client.get('/couriers/1')
    assert response.status_code == 200
    assert response.json()['rating'] is None
    assert response.json()['earnings'] == 0


@pytest.mark.order(23)
def test_get_couriers(temp_db):
    response = client.get('/couriers/2')
    assert response.status_code == 200
    assert response.json()['rating'] == 4.916666666666666
    assert response.json()['earnings'] == 4500
