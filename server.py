# server.py
# created 27/01/2021 at 10:50 by Antoine 'AatroXiss' BEAUDESSON
# last modified 25/01/2021 at 10:50 by Antoine 'AatroXiss' BEAUDESSON

""" server.py

To do:
    - pep8 corrections
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.2.10"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports
from datetime import datetime
import json

# third party imports
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for
)

# local application imports

# other imports

# constants
PATH_CLUBS = 'clubs.json'
PATH_COMPETITIONS = 'competitions.json'
POINTS_PER_PLACE = 3
MAX_PER_CLUB = 12


def load_clubs():
    """
    Loads club's data from the json file.
    As the app is an MVP we do not need to use a database.
    Data is not saved in the json file.
    Everytime the app is run, the json file is reloaded.

    :return: list_of_clubs which is the list of clubs in the JSON file.
    """
    with open(PATH_CLUBS) as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    """
    Loads competitions's data from the json file.
    As the app is an MVP we do not need to use a database.
    Data is not saved in the json file.
    Everytime the app is run, the json file is reloaded.

    :return: list_of_competitions which is in the JSON file.
    """
    with open(PATH_COMPETITIONS) as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


competitions = load_competitions()
clubs = load_clubs()

app = Flask(__name__)
app.secret_key = 'something_special'


@app.route('/')
def index():
    """
    Route for index page.
    Asks the user mail to login.
    Mail must be valid and be a part of the club's list.

    :return: index.html
    """
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    """
    Route for the summary page.
    Shows email of logged in user and list of competitions.
    If not, the user is redirected to the index page.

    :return: summary.html
    """

    email = request.form['email']

    try:
        club = [club for club in clubs if club['email'] == email][0]
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )
    except IndexError:
        if email == "":
            flash("Error: field is empty")
            return render_template('index.html')
        else:
            flash("Error: email is not registered")
            return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """"
    Route for the book page.
    This page allows the user to book a place in the selected competition.
    Booking shouldn't be allowed if:
        - competition occurs in the past
        - the club from url is not in the club's list
        - the competition from url is not in the competition's list

    :param competition: competition's name
    :param club: club's name
    :return: booking.html
    """

    try:
        found_club = [c for c in clubs if c['name'] == club][0]
    except IndexError:
        flash('Error: club not found')
        return render_template('index.html')
    try:
        found_comp = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash('Error: competition not found')
        return render_template('index.html')

    if found_comp and found_club:
        return render_template(
            'booking.html',
            competition=found_comp,
            club=found_club
        )
    else:
        flash('Something went wrong')
        return redirect(
            'welcome.html',
            club=club,
            competitions=competitions
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    """
    Route for the purchase places page.
    Check if the place reservation is possible.
    The constraints are:
        - the competition must not be in the past
        - the club must have enough places
        - the club cannot book more than 12 places
        - the competition has a number of places left > 0

    If the constraints are respected, the place is booked.
    The system performs modficiation of the data.
    A message is flashed in the template to inform the user.
    Using POINTS_PER_PLACE constants.

    :return: welcome.html
    """
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]  # noqa
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    places_remaining = int(competition['numberOfPlaces'])

    if datetime.now() > datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S'):  # noqa
        flash('Error: you can not book a place for past competitions')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    elif places_required > (int(club['points']) / POINTS_PER_PLACE):
        flash('Error: you do not have enough points')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    elif places_required > places_remaining:
        flash('Error: there are not enough places available')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    elif places_required > MAX_PER_CLUB:
        flash('Error: you cannot book more than 12 places')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    else:
        flash('Great-booking complete!')
        flash('You have booked {} places'.format(places_required))
        club['points'] = int(club['points']) - (places_required * POINTS_PER_PLACE)  # noqa
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required  # noqa
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )


@app.route('/clubsBoard', methods=['GET'])
def clubs_board():
    """
    Route clubsBoard, which show a table of all clubs and there points.
    This page is public.

    :return: clubsBoard.html
    """
    return render_template(
        'clubsBoard.html',
        clubs=clubs
    )


@app.route('/logout')
def logout():
    """
    ROute for logout.
    the redirection breaks the session.

    :return: index.html
    """
    return redirect(url_for('index'))
