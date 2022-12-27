# Coffee Shop

This coffee shop application facilitates shop owners to digitally run the cafe. It:
1. Allows public users to view the drink menu.
2. Allows the baristas to see the recipe information.
3. Allows the shop managers to create new drinks and edit exiting drinks.
4. Displays all drinks are in graphics representing the ingredients and their proportions.

The app requires authentication and uses role-based access management strategy to control different types of user behavior in the app.

## About the Stack

### Backend

- Server: Python 3, Flask. 
    Flask is a lightwegith backend microservice framework that works with Python. Flask will handle requests and responses for this application.
- Database: sqlite, SQLAlchemy.
    SQLAlchemy is the Python SQL toolkit and Object Relational Mapper (ORM). The Object Relational Mapper allows classes to be mapped to database models. It provides a generalized interface for creating and executing database-agnostic code without needing to write SQL statements.
- Authentication: Auth0, python-jose.
    Auth0 provides authentication and authrization services. Our app uses Auth0 as a light-weight third-part solution to avoid the cost, time, and risk in building our own solution to authenticate and authorize users.
    jose JavaScript Object Signing and Encryption for JWTs. It's a python package useful for encoding, decoding and verifying JWTS (Json Web Tokens).

### Frontend

- The app frontend depends on Nodejs and Node Package Manager (NPM).
- Ionic Cli. The Ionic Command Line Interface is required to serve and build the frontend.

## Getting Started

### Install Dependencies

#### Python

This app is built in Python 3.7. Go to [Python Docs](https://python.org/downloads) to download and install the right version of Python on your device.

#### Virtual Environment

It's recommended to work with virtual environments whenever using python for projects. This keeps your dependencies for each project seperated and organized. You are welcome to use existing python virtual environments you already have on your device. The virtual environment I used for this project is Conda, if you have conda on your device, you can enter the following command to create virtual environment for this app.

```
conda create --name [project name] python=3.7
conda activate [project name]
```

#### Pip Dependencies

Once you have your virtual environment setup and activated, navigate to the project folder and go to the `/backend` directory to install python dependencies.

```bash
cd backend
pip install requirements.txt
```
This will install all the rquired packages we selected within the `requirements.txt` file

#### Install Node and NPM

The app frontend depends on Nodejs and Node Package Manager. Before continuing, download and install Node (the download includes NPM) from https://nodejs.com/en/download.

#### Install Ionic Cli

Follow instructions on the [Ionic Framework Docs](https://ionicframework.com/docs/intro/cli) to install Ionic Command Line Interface.

#### Install frontend dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory. Open the terminal and run:

```
nmp install
```

### Running the server

Start the server from within the `./src` directory. Each time you open a new terminal session, run:

```
export FLASK_APP=api.py
```

To run the server, execute:

```
flask run --reload
```
If you include the `--reload` flag, it will detect file changes and restart the server automatically.

### Running frontend in Dev mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, navigate into the frontend directory and run:

```
ionic serve
```

## Key software design related to Authentication and Authorization

The authentication system used for this app is Auth0. To create your own Coffee Shop app, register a new Auth0 account and configure the environment variables in `./src/environments/environments.ts` to match your own applicaiton.

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain. (This might be assigned by default if using a free account)
3. Create a new, single page web application
4. Create a new API
    - Enable RBAC in API Settings
    - Enable Add Permission in the Access Token
5. Create new API permissions:
    - get:drinks
    - get:drinks-detail
    - post:drinks
    - patch:drinks
    - delete:drinks
6. Create new roles:
    - Barista
        - can get:drinks-detail
        - can get:drinks
    - Manager
        - can perform all actions

### Configure environment variables

Open the configuration file in the fronend folder `./frontend/src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

### Authentication

`./src/app/services/auth.service.ts` contains the logic to direct a user to the Auth0 login page, managing the JWT token upon successful callback, and handle setting and retrieving the token from the local store. This token is then consumed by our DrinkService (`./src/app/services/drinks.service.ts`) and passed as an Authorization header when making requests to our backend.

### Authorization

The Auth0 JWT includes claims for permissions based on the user's role within the Auth0 system. This project makes use of these claims using the `auth.can(permission)` method which checks if particular permissions exist within the JWT permissions claim of the currently logged in user. This method is defined in `./src/app/services/auth.service.ts` and is then used to enable and disable buttons in `./src/app/pages/drink-menu/drink-form/drink-form.html.`
