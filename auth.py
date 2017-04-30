# -*- coding: utf-8 -*-
from models import User


def _is_account_valid(body):
    result_search = User.query.filter(User.name == body['username']).all()

    if len(result_search) == 0:
        return False
    return True
