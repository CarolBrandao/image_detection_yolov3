from image_detection_yolov3 import __version__
from image_detection_yolov3.helpers import create_app
from fastapi import status
from fastapi.testclient import TestClient

def test_version():
    assert __version__ == '0.1.0'

def test_home_endpoint() -> None:  # noqa
    """Verify endpoint works correctly when querying prod-deployed model."""

    # When
    client = TestClient(create_app())
    response = client.get(url='/')

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert "Congratulations" in response.text

def test_predict_endpoint() -> None:  # noqa
    """Verify endpoint works correctly when querying prod-deployed model."""

    # When
    client = TestClient(create_app())
    response = client.post(
        url='/predict',
        params={
            'model': 'yolov3-tiny',
        },
    )

    # Then
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.status_code == 422