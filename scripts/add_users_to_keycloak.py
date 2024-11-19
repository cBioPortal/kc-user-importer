import os
import sys
import argparse
import requests
import json

from typing import Optional
from rich import print
from pydantic_core import to_jsonable_python
from requests import Response

from kc_user_importer.models import UserRepresentation


class KeyCloakConnection:
    def __init__(self, client_id: str, client_secret: str, realm: str,
                 grant_type: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.realm = realm
        self.grant_type = grant_type


class KeyCloakAPI:

    def __init__(self, host: str, access_token: Optional[str] = None):
        self.host = host

        if access_token:
            self.token = access_token
        else:
            try:
                self.token = os.environ['ACCESS_TOKEN']
            except KeyError:
                sys.exit("Please set ACCESS_TOKEN in env")

        self.headers = {
            'Content-type': 'application/json',
            'Accept': '*/*',
            "Authorization": f"Bearer {self.token}"
        }

    def fetch_access_token(self, connection):
        raise NotImplementedError

    def create_keycloak_user(self, user: UserRepresentation) -> Response:
        headers = self.headers
        headers['Accept'] = 'text/plain'
        url = f"{self.host}/auth/admin/realms/external/users"
        r = requests.post(url, json=to_jsonable_python(user), headers=headers)
        return r

    def get_user(self, username: str) -> dict:
        print(username)
        endpoint = "/auth/admin/realms/external/users"
        params = {"username": username}
        url = f"{self.host}{endpoint}"
        r = requests.get(url, headers=self.headers, params=params)
        return r.json()[0]

    def get_userid_by_username(self, username: str) -> str:
        endpoint = "/auth/admin/realms/external/users"
        params = {"username": username}
        url = f"{self.host}{endpoint}"
        r = requests.get(url, headers=self.headers, params=params)
        return r.json()[0]['id']

    def remove_role(self, user_id: str | None, role: dict) -> Response:
        endpoint = f"/auth/admin/realms/external/users/{user_id}/role-mappings/realm"
        url = f"{self.host}{endpoint}"
        r = requests.delete(url, json=[role], headers=self.headers)
        return r


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-u', '--users',
                            help="users.json file of KeyCloak UserRepresentations",
                        required=True)
    args = parser.parse_args()

    kapi = KeyCloakAPI(host="https://keycloak.cbioportal.mskcc.org")

    # Read users from json
    with open(args.users, 'r') as fh:
        users = json.load(fh)

    for user_data in users:
        user = UserRepresentation(**user_data)
        if not user.email == "":
            print(user)
            # Create new user in Keycloak
            try:
                kapi.create_keycloak_user(user)
            except Exception as e:
                print(e)

            # Remove the _unregistered_user role from all users
            # try:
            #     user_id = kapi.get_userid_by_username(user.username)
            #     print(user_id)
            #     role = {
            #         "id": "95ced797-c50c-465a-9674-b3b69376b91c",
            #         "name": "_unregistered_user"
            #     }
            #     kapi.remove_role(user_id=user_id, role=role)
            # except Exception as e:
            #     print(e)
