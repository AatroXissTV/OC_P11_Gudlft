# gudlift-registration

Gudlft registration is a proof of concept (POC) project to show a light-weight version of a competition booking platform. It aims to keep things as light as possible, and use feedback from the users to iterate.

## Download and create a virtual environment

For this project, you need to have Python 3.10 installed on your machine. Make sure to also install pip.
Then open a terminal and navigate to the directory where you want to install the project. Now, you can run the following commands:

This project uses the following technologies:
* Python v3.10
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Locust](https://locust.io/)
* [Pytest](https://docs.pytest.org/en/latest/)] 

1. From repository download files and clone the folder.

        $ git clone https://github.com/AatroXissTV/OC_P11_Gudlft.git Gudlft
        $ cd Gudlft

2. Create a Python environment.

        $ python3 -m venv venv

3. Activate the virtual environment.

        $ source venv/bin/activate  # MacOS or Linux
        $ source env/Scripts/activate  # for Windows
    
4. Install the dependencies.

        $ pip install -r requirements.txt


## Run the application

Before running the application, you will need to set and environment variable as required by Flask.
In the current setup, the app is powered with JSON files. This is to get around having a DB until we actually need one. 
The main ones are:

* competitions.json - list of competitions
* clubs.json - list of clubs. You can look here to see what email addresses the app will accept for login.

1. Flask requires that you set an environment variable.

        $ export FLASK_APP=server.py

2. You should be ready to run the surver now. Run the following command:

        $ flask run  # or
        $ python -m flask run


## Modify the Points per Place

The points per place can easily be modified in the `server.py` file.
You just have to change the value of `POINTS_PER_PLACE` to whatever you want.
Please make sure to run the tests right after changing the value to make sure it works.


## Testing

I have written unit tests, integration tests and functional tests for the application. You can run them by running the following command:

        $ pytest

To mesure performance of the application, you can run the following command:

        $ locust -f tests/performance_test/performance_test.py

To see the locust server you will need to go to <code>http://localhost:8089/</code> and enter this url as the host: <code>http://127.0.0.1:5000</code>


## Updates

This project is still in development. If you have any suggestions or comments, please feel free to contact me at [AatroXissTV](https://twitter.com/AatroXissTV).

## Author

This software was made by Antoine "AatroXiss" Beaudesson with ❤️ and ☕

## Support

Contributions, issues and features requests are welcome ! Feel free to give a ⭐️ if you liked this project.
