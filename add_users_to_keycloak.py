import os
import sys
import argparse
import requests
import json

from typing import Optional
from rich import print
from pydantic_core import to_jsonable_python

from kc_user_importer.models import UserRepresentation


class KeyCloakApi():

    def __init__(self, host: str, access_token: Optional[str] = None):
        self.host = host

        if access_token:
            self.token = access_token
        else:
            try:
                self.token = os.environ['ACCESS_TOKEN']
            except KeyError:
                sys.exit("Please set ACCESS_TOKEN in env")

    def fetch_access_token(self):
        # ClientId
        # ClientSecret
        # Realm

        raise NotImplementedError

    def create_keycloak_user(self, user: UserRepresentation):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            "Authorization": f"Bearer {self.token}"
        }
        url = f"{self.host}/auth/admin/realms/external/users"
        print(headers)
        print(to_jsonable_python(user))
        r = requests.post(url, json=to_jsonable_python(user), headers=headers)
        print(r.request.headers)
        print(r.request.body)
        print(r.status_code)
        print(r.text)

    def get_user(self, username: str) -> dict:
        print(username)
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*',
            "Authorization": f"Bearer {self.token}"
        }
        endpoint = "/auth/admin/realms/external/users"
        params = {"username": username}
        url = f"{self.host}{endpoint}"
        r = requests.get(url, headers=headers, params=params)

        print(r.request.headers)
        print(r.request.body)
        print(r.status_code)
        print(r.json()[0])
        return r.json()[0]

    def get_userid_by_username(self, username: str) -> str:
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*',
            "Authorization": f"Bearer {self.token}"
        }
        endpoint = "/auth/admin/realms/external/users"
        params = {"username": username}
        url = f"{self.host}{endpoint}"
        r = requests.get(url, headers=headers, params=params)

        print(r.request.headers)
        print(r.request.body)
        print(r.status_code)
        print(r.json()[0])
        return r.json()[0]['id']

    def remove_role(self, user_id: str | None) -> None:
        """
        DELETE /auth/admin/realms/{Realm}/users/{userid}/role-mappings/realm
        curl --request POST \
          --url http://localhost/auth/admin/realms/{Realm}/users/{userid}/role-mappings/realm \
          --header 'authorization: Bearer eyJh......h3RLw' \
          --header 'content-type: application/json' \
          --data '[
            {
                "id": "95ced797-c50c-465a-9674-b3b69376b91c",
                "name": "_unregistered_user",
            }
        ]'
        """
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*',
            "Authorization": f"Bearer {self.token}"
        }
        endpoint = f"/auth/admin/realms/external/users/{user_id}/role-mappings/realm"
        url = f"{self.host}{endpoint}"
        role = {
            "id": "95ced797-c50c-465a-9674-b3b69376b91c",
            "name": "_unregistered_user"
        }
        print(url)
        r = requests.delete(url, json=[role], headers=headers)
        print(r)
        print(r.request.body)
        print(r.status_code)
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-u', '--users',
                            help="users.json file of KeyCloak UserRepresentations",
                        required=True)
    args = parser.parse_args()

    kapi = KeyCloakApi(host="https://keycloak.cbioportal.mskcc.org")

    # Read users from json
    with open(args.users, 'r') as fh:
        users = json.load(fh)

    for user_data in users:
        user = UserRepresentation(**user_data)
        if not user.email == "":
            # Remove _unregistered_user role from all users
            try:
                user_id = kapi.get_userid_by_username(user.username)
                print(user_id)
                # kapi.remove_role(user_id=user_id)
            except Exception as e:
                print(e)

            # Create new user in Keycloak
            # kapi.create_keycloak_user(user)
        # break
