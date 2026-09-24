import pytest
from playwright.sync_api import Playwright

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chromium", help="browser option"
    )

@pytest.fixture(scope='function')
def login_page(playwright: Playwright, request):
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "chromium":
        browser = playwright.chromium.launch()
    elif browser_name == "firefox":
        browser = playwright.firefox.launch()
    context = browser.new_context(base_url="https://eventhub.rahulshettyacademy.com")
    page = context.new_page()
    yield page
    context.close()
    browser.close()



