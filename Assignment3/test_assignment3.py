from playwright.sync_api import Playwright, expect, Page
import re


def test_firstTest(page: Page):
    page.goto('https://eventhub.rahulshettyacademy.com/login')
    
    # Login
    page.locator('#email').fill('loguraj568@gmail.com')
    page.locator('#password').fill('March@0329')
    page.get_by_role("button", name="Sign In").click()
    
    # Assert successful login
    expect(page.get_by_role('heading', name="Discover & Book")).to_be_visible()
    
    # Navigation & Filters
    page.get_by_text("Browse Events →").click()
    page.get_by_placeholder("Search events, venues…").fill('World')

    # Select dropdown options
    page.locator("select").filter(has_text="All Categories").select_option("Conference")    
    page.locator("select").filter(has_text="All Cities").select_option("Hyderabad")
    
    event_cards = page.locator('#event-card')    
    expect(event_cards.first).to_be_visible()

    assert event_cards.count() >= 1
    
    first_card = event_cards.first
    title = first_card.locator('h3').inner_text()
    price = first_card.locator('p').inner_text()
    seats = first_card.locator('span').filter(has_text=re.compile(r'seat')).inner_text() 
    no_of_seats = int(seats.split()[0])   
    
    print(title)
    print(price)
    print(seats)

    assert title=='World Tech Summit'
    assert '$' in price
    assert no_of_seats > 0

    first_card.get_by_text('Book Now').click()

    expect(page).to_have_url(re.compile(r'/events/'))
    expect(page.locator('h1')).to_have_text(title)
    expect(page.locator("p").filter(has_text=price)).to_be_visible()

    page.get_by_role('link',name='Events').first.click()
    expect(page).to_have_url('https://eventhub.rahulshettyacademy.com/events')

    expect(event_cards.first).to_be_visible()
    event_cards_count=event_cards.count()
    assert event_cards_count >= 3

    title_list = []
    for index in range(event_cards_count):
        title_locator=event_cards.nth(index).locator('h3')
        title = title_locator.inner_text()
        title_list.append(title)
        print(title)
        assert title != ''

    assert (title_list[0] != title_list[2])

    






    


        
        
        





