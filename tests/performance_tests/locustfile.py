from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Attendre entre 1 et 5 secondes entre les tâches

    @task
    def load_welcome_page(self):
        # Simuler la connexion et l'accès à la page de bienvenue
        response = self.client.post("/showSummary", data={"email": "functional_test@club.co"})
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 5, "Page load time exceeded 5 seconds"

    @task(3)
    def book_places(self):
        # Simuler la réservation de places pour une compétition
        # D'abord, accéder à la page de réservation
        response = self.client.get("/book/Test Competition/Functional Test Club")
        assert response.status_code == 200

        # Ensuite, soumettre le formulaire de réservation
        response = self.client.post("/purchasePlaces", data={
            "club": "Functional Test Club",
            "competition": "Test Competition",
            "places": "3"
        })
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 2, "Booking update time exceeded 2 seconds"

    def on_start(self):
        # Optionnel : Configuration ou initialisation avant le début des tests
        pass