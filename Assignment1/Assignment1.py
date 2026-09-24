from playwright.sync_api import Page,expect
import re

def test_loginpage(page:Page):
    page.goto('https://eventhub.rahulshettyacademy.com')
    expect(page.get_by_role('heading', name='Sign in to EventHub')).to_be_visible()
    expect(page.get_by_placeholder("you@email.com")).to_be_visible()
    expect(page.get_by_role('button', name='Sign In')).to_be_visible()
    

def test_passwordpage(page:Page):
    page.goto('https://eventhub.rahulshettyacademy.com')
    expect(page.locator('#password')).to_be_visible()
    expect(page).to_have_url(re.compile(r'/login'))  #expect(page).to_have_url('url')
    expect(page.get_by_role('heading', name='Sign in to EventHub')).to_be_visible()