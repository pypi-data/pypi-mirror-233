from pytest import fixture, skip


def has_launch_browser(launch_browser):
    browser = None
    try:
        browser = launch_browser()
        return True
    except Exception:
        return False
    finally:
        if browser:
            browser.close()


@fixture(name="_has_page", scope="session")
def fixture_has_page(launch_browser):
    """
    Requires pytest-playwright package
    """
    if not has_launch_browser(launch_browser):
        skip("playwright browser not found")


@fixture(name="page_if", scope="function")
def fixture_page_if(_has_page, page):
    """
    Requires pytest-playwright package
    """
    yield page
