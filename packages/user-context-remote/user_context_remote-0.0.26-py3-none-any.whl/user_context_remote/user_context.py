import os
from url_local.url_circlez import UrlCirclez
import json
from typing import Any
import sys
from url_local import action_name_enum, entity_name_enum, component_name_enum
from language_local.lang_code import LangCode
from dotenv import load_dotenv
import requests
from httpstatus import HTTPStatus
load_dotenv()
BRAND_NAME = os.getenv('BRAND_NAME')
ENVIORNMENT_NAME = os.getenv('ENVIRONMENT_NAME')
AUTHENTICATION_API_VERSION = 1
# TODO: As we don't want to using the logger, add a mini logger function/method from sdk package


class UserContext:
    _instance = None

    def __new__(cls, email: str = None, password: str = None, _jwt_token: str = None):
        if cls._instance is None:
            cls._instance = super(UserContext, cls).__new__(cls)
            if email is not None and password is not None:
                cls._instance._initialize(username=email, password=password)
            else:
                cls._instance._initialize(_jwt_token=_jwt_token)
        return cls._instance

    def _initialize(self, username: str = None, password: str = None, _jwt_token: str = None):
        self.real_user_id = None
        self.real_profile_id = None
        self.effective_user_id = None
        self.effective_profile_id = None
        self.lang_code = None
        self.real_first_name = None
        self.real_last_name = None
        self.real_display_name = None
        if (username is not None and password is not None):
            self.jwt_token = None
            data = self._authenticate_by_email_and_password(username, password)
        else:
            self.jwt_token = _jwt_token
            data = self._authenticate_by_jwt_token(_jwt_token=_jwt_token)
        self.get_user_data_login_response(validate_jwt_response=data)

    @staticmethod
    # TODO: Change the method name to login_using_username_and_password()
    def login(username: str = None, password: str = None, jwt_token: str = None):
        # logger.start(object={"username": username, "passowrd": password})
        if UserContext._instance is None:
            if jwt_token is not None:
                UserContext._instance = UserContext(_jwt_token=jwt_token)
            else:
                if username is None:
                    username = os.getenv("PRODUCT_USERNAME")
                if password is None:
                    password = os.getenv("PRODUCT_PASSWORD")
                if username is None or password is None or username == "" or password == "":
                    return None
                UserContext._instance = UserContext(
                    email=username, password=password)
        user = UserContext._instance
        # logger.end(object={"user": str(user)})
        return user

    def _set_real_user_id(self, user_id: int) -> None:
        # logger.start(object={"user_id": user_id})
        self.real_user_id = user_id
        # logger.end()

    def _set_real_profile_id(self, profile_id: int) -> None:
        # logger.start(object={"profile_id": profile_id})
        self.real_profile_id = profile_id
        # logger.end()

    def get_real_user_id(self) -> int:
        # logger.start()
        # logger.end(object={"user_id": self.user_id})
        return self.real_user_id

    def get_real_profile_id(self) -> int:
        # logger.start()
        # logger.end(object={"user_id": self.profile_id})
        return self.real_profile_id

    def get_curent_lang_code(self) -> str:
        # logger.start()
        # logger.end(object={"language": self.language})
        return self.lang_code

    def _set_current_lang_code(self, language: LangCode) -> None:
        # logger.start(object={"language": language.value})
        self.lang_code = language.value
        # logger.end()

    def _set_real_first_name(self, first_name: str) -> None:
        # logger.start(object={"first_name": first_name})
        self.real_first_name = first_name
        # logger.end()

    def _set_real_last_name(self, last_name: str) -> None:
        # logger.start(object={"first_name": last_name})
        self.real_last_name = last_name
        # logger.end()

    def get_real_first_name(self) -> str:
        # logger.start()
        # logger.end(object={"first_name": self.first_name})
        return self.real_first_name

    def get_real_last_name(self) -> str:
        # logger.start()
        # logger.end(object={"last_name": self.last_name})
        return self.real_last_name

    def _set_real_name(self, name: str) -> None:
        # logger.start(object={"first_name": last_name})
        self.real_display_name = name
        # logger.end()

    def get_real_name(self) -> str:
        # logger.start()
        # logger.end(object={"first_name": self.first_name})
        return self.real_display_name

    def get_jwt_token(self) -> str:
        return self.jwt_token

    def get_effective_user_id(self) -> int:
        return self.effective_user_id

    def get_effective_profile_id(self) -> int:
        return self.effective_profile_id

    def _set_effective_user_id(self, user_id: int) -> None:
        self.effective_user_id = user_id

    def _set_effective_profile_id(self, profile_id: int) -> None:
        self.effective_profile_id = profile_id

    def _authenticate_by_email_and_password(self, email: str, password: str) -> str:
        # logger.start(object={"email": email, "password": password})
        try:
            url_circlez = UrlCirclez()
            url_jwt = url_circlez.endpoint_url(
                brand_name=BRAND_NAME,
                environment_name=ENVIORNMENT_NAME,
                component=component_name_enum.ComponentName.AUTHENTICATION.value,
                entity=entity_name_enum.EntityName.AUTH_LOGIN.value,
                version=AUTHENTICATION_API_VERSION,
                action=action_name_enum.ActionName.LOGIN.value
            )
            data = {"email": email, "password": password}
            headers = {"Content-Type": "application/json"}
            output = requests.post(
                url=url_jwt, data=json.dumps(data, separators=(",", ":")), headers=headers
            )
            if output.status_code != HTTPStatus.OK:
                print(output.text, file=sys.stderr)
                raise Exception(output.text)
            self.jwt_token = output.json()["data"]["token"]
            # logger.end(object={"user_jwt_token": user_jwt_token })
            return output
        except Exception as e:
            print(
                "Error(Exception): user-context-remote-python _authenticate() " + str(e), file=sys.stderr)
            # TODO: logger.exception(object=e)
            # TODO: logger.end()
            raise

    def _authenticate_by_jwt_token(self, _jwt_token: str) -> str:
        # TODO: Change UrlCirclez to OurUrl() as we are not only Circlez
        url_circlez = UrlCirclez()
        authentication_login_validate_jwt_url = url_circlez.endpoint_url(
            brand_name=BRAND_NAME,
            environment_name=ENVIORNMENT_NAME,
            component=component_name_enum.ComponentName.AUTHENTICATION.value,
            entity=entity_name_enum.EntityName.AUTH_LOGIN.value,
            version=AUTHENTICATION_API_VERSION,
            action=action_name_enum.ActionName.VALIDATE_JWT.value
        )
        data = {"jwtToken": _jwt_token}
        headers = {"Content-Type": "application/json"}
        output = requests.post(
            url=authentication_login_validate_jwt_url, data=json.dumps(data, separators=(",", ":")), headers=headers
        )
        if output.status_code != HTTPStatus.OK:
            # TODO:  we should replace all calls to print() to print_log( repo, file, class, method_function, message) in python-sdk so we'll have unified way to see the log messages.
            print(output.text, file=sys.stderr)
            raise Exception(output.text)
        return output

    # TODO: We should also get the email from user_jwt_token
    def get_user_data_login_response(self, validate_jwt_response: str) -> None:
        if "userDetails" in validate_jwt_response.json()["data"]:
            if "profileId" in validate_jwt_response.json()["data"]["userDetails"]:
                profile_id = validate_jwt_response.json(
                )["data"]["userDetails"]["profileId"]
                self._set_real_profile_id(int(profile_id))
                self._set_effective_profile_id(int(profile_id))
            if "userId" in validate_jwt_response.json()["data"]["userDetails"]:
                user_id = validate_jwt_response.json(
                )["data"]["userDetails"]["userId"]
                self._set_effective_user_id(int(user_id))
                self._set_real_user_id(int(user_id))
            if "lang_code" in validate_jwt_response.json()["data"]["userDetails"]:
                lang_code = validate_jwt_response.json(
                )["data"]["userDetails"]["lang_code"]
                self._set_current_lang_code(lang_code)
            if "firstName" in validate_jwt_response.json()["data"]["userDetails"]:
                first_name = validate_jwt_response.json(
                )["data"]["userDetails"]["firstName"]
                self._set_real_first_name(first_name)
            if "lastName" in validate_jwt_response.json()["data"]["userDetails"]:
                last_name = validate_jwt_response.json(
                )["data"]["userDetails"]["lastName"]
                self._set_real_last_name(last_name)
            # TODO: split the if, add each one separately to name. If none of the exist name = email
            if self.real_first_name is not None and self.real_last_name is not None:
                name = first_name+" "+last_name
                self._set_real_name(name)


# from #logger_local.#loggerComponentEnum import #loggerComponentEnum
# from #logger_local.#logger import #logger

# USER_CONTEXT_LOCAL_PYTHON_COMPONENT_ID = 197
# USER_CONTEXT_LOCAL_PYTHON_COMPONENT_NAME = "User Context python package"
# DEVELOPER_EMAIL = "idan.a@circ.zone"
# obj = {
#     'component_id': USER_CONTEXT_LOCAL_PYTHON_COMPONENT_ID,
#     'component_name': USER_CONTEXT_LOCAL_PYTHON_COMPONENT_NAME,
#     'component_category': #loggerComponentEnum.ComponentCategory.Code.value,
#     'developer_email': DEVELOPER_EMAIL
# }
# #logger = #logger.create_#logger(object=obj)

    # Commented as we get the decoded user_jwt_token from the authentication service and the user-context do not have access to th JWT_SECRET_KEY
    # def get_user_json_by_user_jwt_token(self, jwt_token: str) -> None:
    #     if jwt_token is None or jwt_token == "":
    #         raise Exception(
    #             "Your .env PRODUCT_NAME or PRODUCT_PASSWORD is wrong")
    #     #logger.start(object={"jwt_token": jwt_token})
    #     try:
    #         secret_key = os.getenv("JWT_SECRET_KEY")
    #         if secret_key is not None:
    #             decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=[
    #                                          "HS256"], options={"verify_signature": False})
    #             self.profile_id = int(decoded_payload.get('profileId'))
    #             self.user_id = int(decoded_payload.get('userId'))
    #             self.language = decoded_payload.get('language')
    #             #logger.end()
    #     except jwt.ExpiredSignatureError as e:
    #         # Handle token expiration
    #         #logger.exception(object=e)
    #         print("Error:JWT token has expired.", sys.stderr)
    #         #logger.end()
    #         raise
    #     except jwt.InvalidTokenError as e:
    #         # Handle invalid token
    #         #logger.exception(object=e)
    #         print("Error:Invalid JWT token.", sys.stderr)
    #         #logger.end()
    #         raise
