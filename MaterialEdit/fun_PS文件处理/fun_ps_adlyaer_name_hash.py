"""加密广告图层名"""

from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
