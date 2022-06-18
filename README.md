# Kurl Django Login / Register Example

## Setup

### Without docker
- `pipenv install --user`

### Environment Variables

Copy `.env.example` to `.env` in root directory.

#### Setup Emailer
For email testing, I used [mailtraip](https://mailtrap.io/ "mailtraip") to simulate emailer for account activation. Setup the following variables
- `EMAIL_HOST`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_PORT`

#### Setup Activation URL
For account activation URL, setup `ACTIVATION_URL` the same host and port this project will run.

#### Setup Client for OAuth
Run
```bash
python manage.py createapplication confidential password --client-id {CLIENT_ID} --client-secret {CLIENT_SECRET}
```
Replace {CLIENT_ID} and {CLIENT_SECRET} with your desired values.

### Run
Run using
```bash
python manage.py runserver
```