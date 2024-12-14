from fastapizero.settings import Settings


def test_settings(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'sqlite:///test.db')
    settings = Settings()

    assert settings.DATABASE_URL == 'sqlite:///test.db'
