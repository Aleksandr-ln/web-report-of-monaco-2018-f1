import re

import pytest
from bs4 import BeautifulSoup
from web_report_monaco_2018_racing.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def extract_lap_times(soup, column_index=3):
    return [
        row.find_all("td")[column_index].text.strip()
        for row in soup.find("table").find_all("tr")[1:]
        if re.match(
            r"\d+:\d{2}\.\d{3}", row.find_all("td")[column_index].text.strip()
        )
    ]


def convert_to_seconds(lap_times):
    return [
        float(t.split(":")[0]) * 60 + float(t.split(":")[1]) for t in lap_times
    ]


def test_report_page_content(client):
    response = client.get("/report")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    assert soup.find("h1").text == "Race Report"
    assert len(soup.find_all("tr")) >= 15


def test_report_drivers_page(client):
    response = client.get("/report/drivers")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    assert soup.find("h1") and "Drivers List" in soup.find("h1").text
    assert len(soup.find_all("tr")) > 0


def test_driver_info_page_content(client):
    response = client.get("/report/drivers/?driver_id=SVF")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    assert "Sebastian Vettel" in soup.text
    assert "FERRARI" in soup.text


def test_driver_info_page_not_found(client):
    response = client.get("/report/drivers/?driver_id=XYZ")
    assert response.status_code == 404
    assert b"was not found" in response.data


def test_report_sorting(client):
    response = client.get("/report?order=asc")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    lap_times_in_seconds = convert_to_seconds(extract_lap_times(soup))
    assert lap_times_in_seconds == sorted(lap_times_in_seconds)

    response = client.get("/report?order=desc")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    lap_times_in_seconds_desc = convert_to_seconds(extract_lap_times(soup))
    assert lap_times_in_seconds_desc == sorted(
        lap_times_in_seconds_desc, reverse=True)


def test_report_page_invalid_sorting(client):
    response = client.get("/report?order=xyz")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    lap_times_in_seconds = convert_to_seconds(extract_lap_times(soup))
    assert lap_times_in_seconds == sorted(lap_times_in_seconds)
