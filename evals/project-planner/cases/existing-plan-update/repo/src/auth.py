def authenticated(session):
    return bool(session.get("user_id"))
