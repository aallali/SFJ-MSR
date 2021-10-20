
import secrets
from datetime import datetime
from app.auth.auth_handler import signJWT

async def find_user_by_prop(prop, db, propval):
    row = await db["users"].find_one({prop: propval})
    if row:
        return row
    else:
        return None


async def insert_user(user, db):
    user.token = secrets.token_urlsafe(32)
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    _jwtsign = dict(signJWT(user.email))
    _jwtsign['access_token'] = _jwtsign['access_token'].decode('ascii')
    dbuser = await db["users"].insert_one(dict(user))
    return {'dbuser': dbuser, '_jwtsign': _jwtsign}