import pytest
from web_report_monaco_2018_racing.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_report_page(client):
    response = client.get("/report")
    assert response.status_code == 200
    assert b"Race Report" in response.data


def test_report_drivers_page(client):
    response = client.get("/report/drivers")
    assert response.status_code == 200
    assert b"Drivers List" in response.data


def test_driver_info_page_not_found(client):
    response = client.get("/report/drivers/?driver_id=XYZ")
    assert response.status_code == 404
    assert b"was not found" in response.data


def test_driver_info_page_found(client):
    response = client.get("/report/drivers/?driver_id=SVF")
    assert response.status_code == 200
    assert b"Sebastian Vettel" in response.data
