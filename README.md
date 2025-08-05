# gudlift-registration

1. Why

    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

   This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

      Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 

3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual
      python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of
      the folder. This means that you can install packages in here without affecting affecting files outside. To
      deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r
      requirements.txt</code>. This will install all the packages listed in the respective file. If you install a
      package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze >
      requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set
      the file to be <code>server.py</code>.
      Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>
      python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

   The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around
   having a DB until we actually need one. The main ones are:

    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will
      accept for login.

   We added one test data in both files, to be used by functional et performance tests.

    5. Testing

       a. Unit, Integration and Functional Tests:

       To ensure the reliability and functionality of the application, we use `pytest` for unit and functional testing.
       You can run the tests using the following command:

       for Unit tests:
   ```bash
   pytest tests/unit_tests -v  
   ```

   for Integration tests:
   ```bash
   pytest tests/integration_tests -v  
   ```

   for Functional tests:
   ```bash
   pytest tests/functional_tests -v  
   ```

   or run every type of tests with
   ```bash
   pytest  
   ```

   This command will execute all the tests located in the tests directory and provide you with a summary of the results.

   b. Performance tests:

   Performance testing is conducted using Locust to simulate user load and measure response times. To run the
   performance tests, use the following command:
      ```bash
      locust -f locustfile.py
      ```

   This will start a web interface where you can configure and monitor the performance tests. The goal is to ensure that
   page load times do not exceed 5 seconds and that updates do not take more than 2 seconds.


6. Test coverage:

   We use the coverage tool to measure how much of our code is tested by the unit and functional tests. To generate a
   coverage report, use the following commands:

   ```bash
   coverage report  server.py
   ```


9. Improvement and optimization:

   Our recent work has focused on enhancing the robustness and transparency of the application:

   **Error Handling**:

   We have significantly improved error handling throughout the application to ensure it can gracefully manage
   unexpected situations and provide meaningful feedback to users.

   **Club Points Display**:

   A new feature has been added to display the points of clubs, providing more transparency and allowing users to make
   informed decisions.


10. Credits:

    This project is part of an educational assignment and was developed as a proof of concept for a competition booking
    platform. The initial application was provided by OpenClassrooms as part of the "Développeur d'Application Python"
    training program. The goal of this project is to demonstrate the ability to enhance and test an existing
    application, focusing on performance, robustness, and user experience improvements.