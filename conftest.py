import pytest


@pytest.fixture(autouse=True)
def test_app_data_dir(tmp_path, monkeypatch):
    app_data = tmp_path / "DeskPilotTestData"
    monkeypatch.setattr("utils.APP_DATA_DIR", str(app_data))
    monkeypatch.setattr("utils.SETTINGS_FILE", str(app_data / "settings.json"))
    monkeypatch.setattr("utils.LOG_DIR", str(app_data / "logs"))
    monkeypatch.setattr("utils.LOG_FILE", str(app_data / "logs" / "app.log"))
    monkeypatch.setattr("core_settings.APP_DATA_DIR", str(app_data))
    monkeypatch.setattr("core_settings.SETTINGS_FILE", str(app_data / "settings.json"))
