import json, datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


# Dictionary to keep track of booked places
booked_places = {}


def get_current_date():
    """Return the current date."""
    return datetime.date.today()


def get_booked_places(club_name, competition_name):
    """
    Retrieve the number of places booked by a club for a competition.
    """
    return booked_places.get((club_name, competition_name), 0)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """
    Handle email form submission and display the appropriate page.

    Checks if the provided email is associated with a registered club.
    Renders a welcome page for valid emails or an error message for invalid or missing emails.
    """
    try:
        # Get the email from the form data
        email = request.form["email"]

        # Find a club with the provided email
        club = next((club for club in clubs if club["email"] == email), None)

        # If no club is found, show an error message and return to the index page
        if club is None:
            flash("The email you entered isn't found, please try again.")
            return render_template("index.html")

        # If a club is found, show the welcome page with club and competition details
        return render_template("welcome.html", club=club, competitions=competitions)

    except KeyError:
        # If the email field is missing, show an error message and return to the index page
        flash("Form isn't complete, please enter an email address.")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong, please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    """
    Handle the purchase of competition places by a club.

    Validates sufficient club points and competition places before processing,
    and the 12 limit places before processing.

    Updates competition places and deducts points from the club upon successful purchase.
    Keep the booking_tracking dictionary up to date

    Returns:
        Rendered welcome page with updated club and competition details.
    """

    # Retrieve competition, club details and number of places required from the form data
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])

    # Check if the club has enough points to make the purchase
    if int(club["points"]) < places_required:
        flash("Not enough points to book the required number of places.")
        return render_template("welcome.html", club=club, competitions=competitions)

    # Check if there are enough places available in the competition
    elif int(competition["numberOfPlaces"]) < places_required:
        flash("Not enough places available in the competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    # Check if the club has already booked 12 or more places for this competition
    key = (club["name"], competition["name"])
    if booked_places.get(key, 0) + places_required > 12:
        flash("A club cannot book more than 12 places in total for a competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    else:
        # Update the number of places and points
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - places_required
        )
        club["points"] = int(club["points"]) - int(request.form["places"])

        # Update the booked places tracking
        key = (club["name"], competition["name"])
        booked_places[key] = booked_places.get(key, 0) + places_required

        # Display a confirmation message, and render welcome template
        flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
