# -*- coding: utf-8 -*-
from models import User


def _is_account_valid(body):
    # check valid user
    result_user = User.query.filter(User.name == body['username']).all()

    # username is unique
    if len(result_user) != 1:
        return False

    if User.check_password(result_user[0], body['password']):
        return True
    return False
