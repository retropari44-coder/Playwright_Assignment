import copy
import time
from playwright.sync_api import Page, expect
import re


class CreateBooking:
    def __init__(self,page: Page):
        self.page = page

    def login(self):
        self.page.goto('https://eventhub.rahulshettyacademy.com/login')
        self.page.locator('#email').fill('loguraj568@gmail.com')
        self.page.locator('#password').fill('March@0329')
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

    def book_tickets(self,no_of_tickets,name,email,phone):
        form_locator=self.page.locator(".space-y-4")
        for _ in range(no_of_tickets-1):
            form_locator.get_by_role("button", name="+").click()
        form_locator.locator('#customerName').fill(name)
        form_locator.locator('#customer-email').fill(email)
        form_locator.locator('#phone').fill(phone)
        form_locator.get_by_role('button',name='Confirm Booking').click()
        expect(self.page.get_by_text(re.compile(r'Booking Confirmed'))).to_be_visible()

class HandlingRoute(CreateBooking):

    def __init__(self, page: Page):
        super().__init__(page)

        self.patched_booking_store = {}
        self.original_booking_store = {}

    def response_filler1(self, route):
        response = route.fetch()
        data = response.json()
        self.original_booking_store = data.get("data")
        updated_data = copy.deepcopy(data)    #deepcopy (to store the value in different address)
        if updated_data.get("data"):
            first_record = updated_data["data"][0]
            first_record["bookingRef"] = "D-2PHOUR"
            first_record["totalPrice"] = "900"
            first_record["quantity"] = 3
            first_record["event"]["title"] = "Balu Mahendra"
            self.patched_booking_store = first_record
        print("Updated Data:", self.patched_booking_store)
        print("Original Data:", self.original_booking_store)
        route.fulfill(json=updated_data)

    def verify_patch_filler(self):
        patched_reference = self.patched_booking_store["bookingRef"]
        patched_title = self.patched_booking_store["event"]["title"]
        patched_total_price = self.patched_booking_store["totalPrice"]
        original_data = self.original_booking_store[1]
        original_data_reference = original_data["bookingRef"]
        original_data_title = original_data["event"]["title"]
        original_data_total_price = int(original_data["totalPrice"])
        original_data_id = self.patched_booking_store["id"]

        print(patched_reference)
        print(patched_title)
        print(patched_total_price)

        print(original_data_reference)
        print(original_data_title)
        print(original_data_total_price)
        
        patched_locator = self.page.locator("#booking-card").filter(has_text=patched_reference)

        expect(patched_locator).to_be_visible()
        expect(patched_locator.locator("h3",has_text=patched_title)).to_be_visible()
        expect(patched_locator).to_contain_text(f"${patched_total_price}")

        original_locator = self.page.locator("#booking-card").filter(has_text=original_data_reference)
        expect(original_locator).to_be_visible()
        expect(original_locator.locator("h3",has_text=original_data_title)).to_be_visible()
        expect(original_locator).to_contain_text(f"${original_data_total_price:,}")
        button_locator = patched_locator.get_by_role("link", name="View Details")
        event_id = button_locator.get_attribute('href')
        id = event_id.split('/')[2]
        assert id == str(original_data_id)
        

    def response_filler2(self,route):
        route.fulfill(json={"data":self.patched_booking_store})

    def detail_patch_filler(self):
        patched_reference = self.patched_booking_store["bookingRef"]
        patched_title = self.patched_booking_store["event"]["title"]
        patched_total_price = self.patched_booking_store["totalPrice"]
        patched_tickets = self.patched_booking_store['quantity']

        expect(self.page.get_by_text(patched_reference).first).to_be_visible()
        expect(self.page.get_by_text(patched_title).first).to_be_visible()
        expect(self.page.get_by_text(patched_total_price)).to_be_visible()
        expect(self.page.get_by_text(str(patched_tickets),exact= True)).to_be_visible()
        expect(self.page.get_by_text('loguraj568@gmail.com').first).to_be_visible()

        
def test_login_verification(page: Page):
    login_page = CreateBooking(page)
    login_page.login()

    login_page.search_for_booking(search_word='World',city='Hyderabad')
    login_page.book_tickets(no_of_tickets=1,name='Prithvi',email='loguraj568@gmail.com',phone='7708196869')

    login_page.search_for_booking(search_word='Dilli',city='Delhi')
    login_page.book_tickets(no_of_tickets=2,name='Prithvi',email='loguraj568@gmail.com',phone='7708196869')

def test_routeverification(page:Page):
    booking = HandlingRoute(page)
    page.route('https://api.eventhub.rahulshettyacademy.com/api/bookings*',booking.response_filler1)
    page.route('https://api.eventhub.rahulshettyacademy.com/api/bookings/*',booking.response_filler2)
    booking.login()
    page.get_by_role("link", name="My Bookings").first.click()
    expect(page.get_by_role("heading",name="My Bookings")).to_be_visible()
    expect(page.locator(".space-y-4.mb-8")).to_be_visible()
    booking.verify_patch_filler()
    page.get_by_role('button',name='View Details').first.click()
    time.sleep(1)
    booking.detail_patch_filler()
    page.get_by_role("link", name="My Bookings").first.click()
    expect(page.locator(".space-y-4.mb-8")).to_be_visible()
    booking.verify_patch_filler()



    






