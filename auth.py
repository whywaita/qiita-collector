# -*- coding: utf-8 -*-
from models import User


def _is_account_valid(login_name):
    result_search = User.query.filter(User.name == login_name).all()
    print(result_search)

    if len(result_search) == 0:
        return False
    return True
