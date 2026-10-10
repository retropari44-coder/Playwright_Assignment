import re
import pytest
from playwright.sync_api import Playwright, expect, Page

# @pytest.mark.parametrize("browserInstance1,browserInstance2", [("chromium", "firefox")])
# def test_firstTest(playwright: Playwright, browserInstance):
#     if browserInstance == "chromium":
#         browser = playwright.chromium.launch()
#     elif browserInstance == "firefox":
#         browser = playwright.firefox.launch()
#     context = browser.new_context(base_url='https://eventhub.rahulshettyacademy.com')
#     page = context.new_page()    
#     page.goto('/login')    
#     expect(page).to_have_title(re.compile(r'EventHub'))
#     expect(page.get_by_placeholder('you@email.com')).to_be_visible()
#     expect(page.get_by_role('button', name='Sign In')).to_be_visible()    
#     context.close()
#     browser.close()

def test_firstTest(login_page):
    login_page.goto('/login')
    expect(login_page).to_have_title(re.compile(r'EventHub'))
    expect(login_page.get_by_placeholder('you@email.com')).to_be_visible()
    expect(login_page.get_by_role('button', name='Sign In')).to_be_visible()


# 2. Native Playwright page fixture test
def test_secondTest(page: Page):
    page.goto('https://eventhub.rahulshettyacademy.com/login')
    locator = page.get_by_placeholder('you@email.com')
    locator.fill('beginner@sample.com')
    assert (locator.input_value() == 'beginner@sample.com')


# 3. Manual Playwright instance test
def test_thirdTest(login_page):
    login_page.goto('https://eventhub.rahulshettyacademy.com/login')
    expect(login_page.get_by_role('heading', name='Sign in to EventHub')).to_be_visible()

    locator = login_page.get_by_placeholder('you@email.com')
    assert locator.input_value() == ''
    

