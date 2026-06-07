def test_app_module_imports():
    """Verify core modules can be imported."""
    from src import app  # noqa: F401


def test_app_title():
    """Verify app module has expected attributes after import."""
    import src.app

    assert hasattr(src.app, "st")
