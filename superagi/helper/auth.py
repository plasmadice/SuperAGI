from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from superagi.config.config import get_config
from fastapi_sqlalchemy import db
from superagi.models.organisation import Organisation
from superagi.models.user import User


def check_auth(Authorize: AuthJWT = Depends()):
    env = get_config("ENV", "DEV")
    if env == "PROD":
        Authorize.jwt_required()
    return Authorize


def get_user_organisation(Authorize: AuthJWT = Depends(check_auth)):
    env = get_config("ENV", "DEV")

    if env == "DEV":
        email = "super6@agi.com"
    else:
        # Retrieve the email of the logged-in user from the JWT token payload
        email = Authorize.get_jwt_subject()

    # Query the User table to find the user by their email
    user = db.session.query(User).filter(User.email == email).first()
    organisation = db.session.query(Organisation).filter(Organisation.id == user.organisation_id).first()
    return organisation