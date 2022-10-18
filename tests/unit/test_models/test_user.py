import pytest

from src.models.user import User, UserRegisterInput


@pytest.mark.parametrize(
    "user,expected_item",
    [
        (User(email="asdasd@op.pl", password="some_password"), {"PK": "user#asdasd@op.pl", "SK": "user#asdasd@op.pl"}),
        (
            User(email="abcdefg@op.pl", password="some_password"),
            {"PK": "user#abcdefg@op.pl", "SK": "user#abcdefg@op.pl"},
        ),
    ],
)
def test_user_model_to_item(user: User, expected_item: dict[str, str]) -> None:
    item = user.to_item()

    assert item["PK"] == expected_item["PK"]
    assert item["SK"] == expected_item["SK"]


@pytest.mark.parametrize(
    "item,expected_model",
    [
        (
            {"PK": "user#asdasd@op.pl", "SK": "user#asdasd@op.pl", "password": "some_password"},
            User(email="asdasd@op.pl", password="some_password"),
        ),
        (
            {"PK": "user#onetwothree@op.pl", "SK": "user#onetwothree@op.pl", "password": "some_password"},
            User(email="onetwothree@op.pl", password="some_password"),
        ),
    ],
)
def test_user_model_from_item(item: dict[str, str], expected_model: User) -> None:
    user = User.from_item(item=item)
    assert user.email == expected_model.email


@pytest.mark.parametrize(
    "password,password_again",
    [("abcdefg12345", "abcdefgh1234555"), ("aljsdadj312", "alskjdalsaa"), ("asdfghjkla", "anqwajdhas67das8d")],
)
def test_user_register_input_raises_value_error_when_passwords_do_not_match(
    password: str, password_again: str
) -> None:
    with pytest.raises(ValueError):
        UserRegisterInput(email="testemail@test.test", password=password, password_again=password_again)
