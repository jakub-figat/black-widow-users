from chalice import Chalice


app = Chalice(app_name="users")


# pylint: disable=unused-import
# pylint: disable=cyclic-import
from chalicelib.routes import token  # NOQA
from chalicelib.routes import user  # NOQA
