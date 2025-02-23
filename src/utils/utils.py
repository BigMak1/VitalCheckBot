def is_admin(user_id: int) -> bool:
    from config.config import ADMIN_ID
    return str(user_id) == ADMIN_ID