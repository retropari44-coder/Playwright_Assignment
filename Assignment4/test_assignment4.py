from playwright.sync_api import Playwright, expect, Page
import re

class Verification:
    def __init__(self,page: Page):
        self.page = page

    def login(self,username,password):
        self.page.goto('https://eventhub.rahulshettyacademy.com/login')
        self.page.locator('#email').fill(username)
        self.page.locator('#password').fill(password)
        self.page.get_by_role("button", name="Sign In").click()
        expect(self.page.get_by_role('heading', name="Discover & Book")).to_be_visible()

    def search_for_booking(self,search_word,categories ='All Categories',city='All Cities'):
        self.page.get_by_role('link',name='Events').first.click()
        self.page.get_by_placeholder("Search events, venues…").fill(search_word)
        self.page.locator("select").filter(has_text="All Categories").select_option(categories)
        self.page.locator("select").filter(has_text="All Cities").select_option(city)
        event_cards = self.page.locator('#event-card')
        expect(event_cards.first).to_be_visible()
        event_cards_count = event_cards.count()
        print("Event Cards Count is ",event_cards_count)
        for index in range(event_cards_count):
            word = event_cards.nth(index).locator('h3').inner_text()
            print("Title:",word)
            if search_word in word:
                event_cards.nth(index).get_by_text('Book Now').click()
                break
        expect(self.page).to_have_url(re.compile(r'/events/'))
        expect(self.page.locator('h1')).to_contain_text(search_word, ignore_case=True)

    def retrive_booking_details(self,details={}):
        booked_locator = self.page.locator('.text-center.py-6')
        booked_details_locator = booked_locator.locator('.flex.items-center.justify-between.text-sm')
        print(booked_details_locator.count())
        for index in range(booked_details_locator.count()):
            key = booked_details_locator.nth(index).locator('span').first.inner_text()
            values= booked_details_locator.nth(index).locator('span').last.inner_text()
            print(f'{key}:{values}')
            details[key]=values
        
        return details


    def book_tickets(self,no_of_tickets,name,email,phone):
        form_locator=self.page.locator(".space-y-4")
        for _ in range(no_of_tickets-1):
            self.page.get_by_role("button", name="+").click()
        form_locator.locator('#customerName').fill(name)
        form_locator.locator('#customer-email').fill(email)
        form_locator.locator('#phone').fill(phone)
        form_locator.get_by_role('button',name='Confirm Booking').click()
        expect(self.page.get_by_text(re.compile(r'Booking Confirmed'))).to_be_visible()

    

def test_login_verification(page: Page):
    login_page = Verification(page)
    login_page.login('loguraj568@gmail.com','March@0329')
    login_page.search_for_booking(search_word='World',city='Hyderabad')
    login_page.book_tickets(no_of_tickets=1,name='Prithvi',email='loguraj568@gmail.com',phone='7708196869')
    login_page.search_for_booking(search_word='Dilli',city='Delhi')
    login_page.book_tickets(no_of_tickets=2,name='Prithvi',email='loguraj568@gmail.com',phone='7708196869')


    





