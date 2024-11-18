import pytest
from kc_user_importer.models import User, GroupUserInfo


def test_User_init():
    test_file = "tests/entra_bulk_users_export.csv"
    with open(test_file, mode="r", encoding='utf-8-sig') as fh:
        header = fh.readline().strip().split(",")
        user_data = dict(zip(header, fh.readline().strip().split(",")))
        user = User.model_validate(user_data)

    assert user.displayName == "Bruce Wayne"
    assert user.mail == "wayne.b@wayne.org"


def test_GroupUserInfo_init():
    assert GroupUserInfo
