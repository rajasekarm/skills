def require_user(session):
    if not session.get("user_id"):
        raise PermissionError("Sign in required")
    return session["user_id"]
