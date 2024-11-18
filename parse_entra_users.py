import argparse
import re
import json
from typing import List, DefaultDict
from collections import defaultdict
from pathlib import Path

from rich import print
from pydantic_core import to_jsonable_python

from kc_user_importer.models import User, GroupUserInfo, UserRepresentation


def get_group_user_info(filename: Path) -> List[GroupUserInfo]:
    users = []
    with open(filename, mode="r", encoding='utf-8-sig') as fh:
        header = fh.readline().strip().split(",")
        for user in fh:
            user = user.strip()
            # Contains displayName in quotes because name itself contains a
            # comma, unable to string split
            mo = re.search(re.compile('\"[a-zA-Z].+\"'), user)
            if mo:
                # Original display name, Create dummy replacement
                # Replace original with the dummy in line
                orig = mo.group()
                safe = orig.replace(",", "+")
                # Proceed to split as normal and return original name to same
                # position
                user = user.replace(orig, safe).split(",")
                user[2] = orig.strip('\"')

                users.append(GroupUserInfo.model_validate(dict(zip(header, user))))
            else:
                # Contains no quotes, so can string split(",") normally
                user = user.split(",")
                users.append(GroupUserInfo.model_validate(dict(zip(header, user))))
    return users


def get_user_groups(groups: dict) -> DefaultDict:
    group_membership = defaultdict(list)
    for name, group in groups.items():
        for gu in group:
            group_membership[gu.email].append(name)
    return group_membership


def parse_users_file(filename: str, group_lookup) -> List[UserRepresentation]:
    users = []
    with open(filename, mode="r", encoding='utf-8-sig') as fh:
        header = fh.readline().strip().split(",")
        for user_data in fh:
            user_data = user_data.strip().split(",")
            user_data = User.model_validate(dict(zip(header, user_data)))

            if user_data.mail != "":
                firstName, *rest = user_data.displayName.split()
                groups = [*['btc-all'], *group_lookup.get(user_data.mail, [])]
                p = UserRepresentation(
                    username=user_data.mail,
                    email=user_data.mail,
                    firstName=firstName,
                    lastName=' '.join(rest),
                    groups=groups,
                )
                users.append(p)
    return users


"""UserRepresentation example
{
    "username": "clark.kent@gmail.com",
    "email": "clark.kent@gmail.com",
    "firstName": "Clark",
    "lastName": "Kent",
    "enabled": true,
    "emailVerified": false,
    "attributes": {},
    "groups": ["btc-all", "btc-gbm"],
    "realmRoles": ["offline_access", "uma_authorization", "_unregistered_user"]
}
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Extract users from user bulk or group bulk files")
    parser.add_argument("-i", "--in-file", required=True)
    parser.add_argument("-o", "--out-file", default="users.json")
    # parser.add_argument("-gf", "--group-file")
    parser.add_argument("-g", "--groups", 
                        help="Directory containing Microsoft Entra Group bulk download files", 
                        required=True)
    args = parser.parse_args()

    # Gather groups together
    group_membership = {}
    if args.groups:
        for teamlab in Path(args.groups).glob('*.csv'):
            group_membership[teamlab.stem] = get_group_user_info(teamlab)

    group_lookup = get_user_groups(group_membership)

    # Parse users file into KeyCloak UserPresentations
    users = parse_users_file(args.in_file, group_lookup)
    with open(args.out_file, 'w') as f:
        json.dump(to_jsonable_python(users, exclude_none=True), f)
