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