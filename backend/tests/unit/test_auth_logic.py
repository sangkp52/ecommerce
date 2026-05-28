def test_password_match():
    password = "123456"
    confirmation = "123456"

    assert password == confirmation


def test_password_mismatch():
    password = "123456"
    confirmation = "654321"

    assert password != confirmation


def test_email_contains_at_symbol():
    email = "test@example.com"

    assert "@" in email

def test_password_length():
    password = "123456"

    assert len(password) >= 6

def hash_password(password):
    return "hashed_" + password

def test_hash_password():
    assert hash_password("123") == "hashed_123"

def is_valid_email(email):
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def test_is_valid_email():
    assert is_valid_email("test@gmail.com")
    assert not is_valid_email("invalidemail")

def generate_token(user_id):
    return f"token-{user_id}"

def test_generate_token():
    token = generate_token(1)
    assert token.startswith("token-")