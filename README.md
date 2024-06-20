# ACCESS KEY MANAGEMENT SYSTEM

This system is designed to generate unique access keys in form of strings, for IT personnel. Each access key generated has a length of 16 characters, and has an expiry date, which is set to 30 days after creation


# FEATURES
    Every new user is expected to sign up or register with a valid email.
    The app uses email for authentication. An OTP would be sent to the email provided by the user

    Admins and IT personnel each have unique dashboards with appropriate functionalities
    Admins are able to manage the access keys for each registered IT personnel. They can revoke and track the status of all the access keys for each user registered as an IT personnel.
    IT personnel can view their access keys (active, expired and revoked) and request for new keys


# PREREQUISITES
    Python 3.8+
    Django 3.2+
    PostgreSQL or any other compatible database


# INSTALLATION
    #Clone repository
    git clone https://github.com/selormatsu5/access_key_manager.git
    cd access_key_manager


    #Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate (For Windows use `venv\Scripts\activate`)


    #Install dependencies
    pip install -r requirements.txt


    #Set up the database depending on your prefered one (This system uses PostgreSQL as default)


    #Run migrations
    python manage.py makemigrations
    python manage.py migrate


    #Create a superuser
    python manage.py createsuperuser


    #Run the development server
    python manage.py runserver


    Your terminal would provide the url where you can access the app.
    It would look something like this 'http://127.0.0.1:8000/'


This app is simple and easy to use.
