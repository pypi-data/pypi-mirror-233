from __future__ import annotations

import os.path
from datetime import datetime
from typing import Optional

import pyrebase

from firelit.utils import load_yaml


class FirebaseAdmin:
    """
    Firebase Admin class: handling user authentication and database
    """

    def __init__(self, config: Optional[str | dict] = None):
        if config is None:
            if "firelit_config.yaml" in os.listdir():
                firebase_config = load_yaml("firelit_config.yaml")
            elif "firelit_config.yml" in os.listdir():
                firebase_config = load_yaml("firelit_config.yml")
            else:
                raise ValueError(
                    "You must provide a valid path to a yaml file or a dictionary"
                )
        else:
            if isinstance(config, dict):
                firebase_config = config
            elif isinstance(config, str):
                if os.path.exists(config) and (
                    os.path.split(config)[1].endswith(".yaml")
                    or os.path.split(config)[1].endswith(".yml")
                ):
                    firebase_config = load_yaml(config)
                else:
                    raise ValueError(
                        "Invalid config file. You must provide a valid path to a yaml file or a dictionary"
                    )

            else:
                raise ValueError(
                    "Invalid config file. You must provide a valid path to a yaml file or a dictionary"
                )

        # initializing app
        self.firebase = pyrebase.initialize_app(firebase_config)

        # Actual user (email, password) dictionary
        self.user = None
        # Realtime database
        self.db = None
        # Authentication
        self.auth = self.firebase.auth()
        # User info
        self.user_info = None
        # Authentication status
        self.authentication_status = False
        # Licence
        self.licence = dict(valid=False, expiration_date=None)

    def login(self, email: str, password: str) -> None:
        """
        Args:
            email: user email
            password: user password

        Returns:

        Handling user login, returning True (successfully) or False (invalid)
        """

        if self.authentication_status:
            print("User already authenticated")
            return

        try:
            # Login with email and password
            self.user = self.auth.sign_in_with_email_and_password(email, password)
            print("%s : login correctly executed" % email)

            # Getting realtime database
            self.db = self.firebase.database()

            self.user_info = (
                self.db.child("users")
                .child(self.user["localId"])
                .get(token=self.user["idToken"])
                .val()
            )

            (
                is_licence_valid,
                licence_expiration_date,
            ) = self.check_license_expiration()

            self.licence = dict(
                valid=is_licence_valid, expiration_date=licence_expiration_date
            )

            self.authentication_status = True

        except Exception as e:
            print("Cannot perform login for %s: invalid username or password" % email)
            print(e)
            self.authentication_status = False

    def check_license_expiration(self) -> tuple:
        """
        Returns: (validity boolean, license expiration date)

        Check user's licence expiration and validity
        """

        # Getting user's information from Realtime Database
        user_info = self.user_info

        # If user's licence can expire, checking expiration date
        if user_info["expires"]:
            licence_expiration_date = datetime.fromisoformat(
                user_info["expiration date"]
            )
            if licence_expiration_date <= datetime.now():
                print("Licence expired on: %s" % licence_expiration_date)
                return False, licence_expiration_date
            else:
                print("Valid licence found")
                return True, licence_expiration_date
        else:
            print("Valid licence found")
            return True, None

    @property
    def authenticated(self) -> bool:
        """
        :return: authentication status

        Check if user is authenticated
        """
        return self.authentication_status

    def reset_connection(self):
        # Actual user (email, password) dictionary
        self.user = None
        # Realtime database
        self.db = None
        # Authentication
        self.auth = self.firebase.auth()
        # User info
        self.user_info = None
        # Authentication status
        self.authentication_status = False
