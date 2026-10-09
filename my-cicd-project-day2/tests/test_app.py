# Import our Flask application from app.py.
from app import app


# Test the main application endpoint.
def test_home():

    # Create Flask's test client.
    # This lets us test the application without
    # starting the real Flask server.
    client = app.test_client()

    # Send a GET request to "/".
    response = client.get("/")

    # Check that the request was successful.
    assert response.status_code == 200


# Test the health-check endpoint.
def test_health():

    # Create Flask's test client.
    client = app.test_client()

    # Send a GET request to "/health".
    response = client.get("/health")

    # The health endpoint should return HTTP 200.
    assert response.status_code == 200

    # Check that the expected health message exists.
    assert b"Application is healthy" in response.data
