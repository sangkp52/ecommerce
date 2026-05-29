from application import create_app

def test_app_starts():
    app = create_app()
    assert app is not None