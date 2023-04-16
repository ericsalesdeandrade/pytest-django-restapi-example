import pytest


@pytest.mark.django_db
def test_create_task(api_client):
    payload = {
        "title": "Wash Clothes",
        "content": "Wash clothes in the washing machine",
    }

    response = api_client.post('/api/tasks/', data=payload, format='json')
    print(response.data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_tasks(api_client):
    response = api_client.get('/api/tasks/', format='json')
    print(response.data)
    assert response.status_code == 200
