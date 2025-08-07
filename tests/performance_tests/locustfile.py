from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    """
    User class for simulating user behavior on the website.
    This class defines tasks that users perform, such as logging in and booking places.
    """
    wait_time = between(1, 5)  # Wait time between tasks

    @task(1)
    def login(self):
        """
        Task to simulate user login.
        """
        response = self.client.post("/showSummary", data={"email": "functional_test@club.co"})
        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        # Assert that the response time is less than 5 seconds
        assert response.elapsed.total_seconds() < 5, "Page load time exceeded 5 seconds"

    @task(3)
    def book_places(self):
        """
        Task to simulate booking places for a competition.
        This task is more frequent than login to focus on performance testing.
        """
        # Simulate accessing the booking page
        response = self.client.get("/book/Test Competition/Functional Test Club")
        assert response.status_code == 200

        # Simulate submitting the booking form
        response = self.client.post("/purchasePlaces", data={
            "club": "Functional Test Club",
            "competition": "Functional Test Comp",
            "places": "3"
        })
        assert response.status_code == 200
        # Assert that the booking update time is less than 2 seconds
        assert response.elapsed.total_seconds() < 2, "Booking update time exceeded 2 seconds"
