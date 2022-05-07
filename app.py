from chalice import Chalice


app = Chalice(app_name="users")

from src.routes import user
