# QuantInvest
Quantitative Investment Software 

This is an old school full-stack project that isn't in a functional state right now. Might work on it in the future. 

## Running QuantInvest

To run QuantInvest on a local machine, the following is needed:
- Python 3 virtual environment with all required dependencies
- Setup environment variables using autoenv
- Run mongodb docker container while mapping necessary ports
- Run flask application using werkzeug development server (production uses gunicorn)

### Cloning the repository
$ git clone https://github.com/RamiAwar/QuantInvest

### Python virtual environment setup
``` 
$ python3 -m venv venv 
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

### Environment variables setup
```
(venv)$ deactivate
pip install autoenv
echo "source `which activate.sh`" >> ~/.bashrc
source ~/.bashrc
touch .env
```

Inside the .env file, add the following:
```
source venv/bin/activate
export APP_SETTINGS="config.DevelopmentConfig"
export FLASK_APP=entry.py
export FLASK_DEBUG=1
```

The contents of ```.env``` will get executed every time you CD into this folder, automatically activating the python virtual 
environment and setting the above environment variables.

### MongoDB Docker Container
A standard docker mongodb container can be run, while mapping local port 27017 to docker port 27017. This is done in one line inside
```run_dockerized_mongodb.sh```. To execute the script, give it execution permission first.
```
chmod +x run_dockerized_mongodb.sh
./run_dockerized_mongodb.sh
```

### Running the app

Move out of the directory of the project then back (cd) in to activate the python environment, and then run the flask app using:
```
(venv)$ flask run
```
