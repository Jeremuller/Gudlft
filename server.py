import json
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
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
    club["points"] = int(club["points"]) - int(request.form["places"])
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
