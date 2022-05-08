from chalice import Chalice


app = Chalice(app_name="users")


if __name__ == "__main__":
    # pylint: disable=unused-import
    # pylint: disable=cyclic-import
    from src.routes import user  # NOQA
