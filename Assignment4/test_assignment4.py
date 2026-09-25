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
            details[key]=values
        Title = self.page.get_by_role('heading').first.inner_text()
        details['Title'] = Title
        return details

    def check_details(self, booking_details, test):
            count = 0
            for i in booking_details.keys():
                for j in test:
                    if booking_details[i] in j:
                        count +=1
                        break
            assert count == (len(booking_details)-1)

    # def get_booking_details(self,search_word):
    #     self.page.get_by_role('button',name='View My Bookings').click()
    #     event_card_locator = self.page.locator('#booking-card')
    #     expect(event_card_locator.first).to_be_visible()
    #     event_card_locator_count = event_card_locator.count()
    #     for index in range(event_card_locator_count):
    #         is_present = event_card_locator.nth(index).filter(has_text=search_word).is_visible()
    #         if is_present:
    #             event_card_locator.nth(index).filter(has_text=search_word).get_by_role('button',name ='View Details').click()
    #             break
    #     expect(self.page).to_have_url(re.compile(r"/\d+$"))
    #     expect(self.page.locator('.space-y-4')).to_be_visible()
    #     texts = self.page.locator('.space-y-4').locator('span').all_inner_texts()
    #     booking_dictonary = {}
    #     for i in range(0,len(texts)-1,2):
    #         booking_dictonary[texts[i]] = texts[i+1]
    #     return booking_dictonary

            
    def book_tickets(self,no_of_tickets,name,email,phone):
        form_locator=self.page.locator(".space-y-4")
        for _ in range(no_of_tickets-1):
            self.page.get_by_role("button", name="+").click()
        form_locator.locator('#customerName').fill(name)
        form_locator.locator('#customer-email').fill(email)
        form_locator.locator('#phone').fill(phone)
        form_locator.get_by_role('button',name='Confirm Booking').click()
        expect(self.page.get_by_text(re.compile(r'Booking Confirmed'))).to_be_visible()

    def verify_first_test(self):
        self.page.get_by_role('button',name='View My Bookings').click()
        event_card_locator = self.page.locator('#booking-card')
        expect(event_card_locator.first).to_be_visible()
        expect(event_card_locator.first.get_by_role('heading',name='World Tech Summit')).to_be_visible()
        expect(event_card_locator.first.locator('.booking-ref')).not_to_have_text('')
        expect(event_card_locator.first).to_have_text(re.compile(r'1 ticket'))

    def verify_second_test(self, booking_reference=''):
        self.page.get_by_role('button',name='View My Bookings').click()
        event_card_locator = self.page.locator('#booking-card')
        expect(event_card_locator.first).to_be_visible()
        expect(event_card_locator.first.locator('.booking-ref')).to_have_text(booking_reference)
        expect(event_card_locator.first).to_have_text(re.compile(r'2 ticket'))
        first_tile = event_card_locator.first.locator('h3').inner_text()
        second_title = event_card_locator.last.locator('h3').inner_text()
        assert (first_tile != second_title)

    def verify_third_test(self, booking_reference):
        event_card_locator = self.page.locator('#booking-card',has_text=booking_reference)
        expect(event_card_locator).to_be_visible()
        expect(event_card_locator.locator('span',has_text='confirmed')).to_be_visible()
        event_card_locator = event_card_locator.inner_text()
        split_lines = event_card_locator.split('\n')
        return split_lines
         
    

    def verify_fourth_test(self, booking_reference1,booking_reference2):
        event_card_locator = self.page.locator('#booking-card',has_text=booking_reference1['Booking Ref'])
        expect(event_card_locator).to_be_visible()
        booking_id = event_card_locator.locator('#booking-id').inner_text()
        booking_id = booking_id[1:]
        event_card_locator.get_by_role('button',name='View Details').click()
    
        expect(self.page).to_have_url(re.compile(booking_id))
        expect(self.page.get_by_text(booking_reference1['Booking Ref']).first).to_be_visible()
        expect(self.page.get_by_role('heading',name=booking_reference1['Title'])).to_be_visible()
        expect(self.page.get_by_text(str(booking_reference1['Tickets']), exact=True)).to_be_visible()
        expect(self.page.get_by_text(str(booking_reference1['Total'])).first).to_be_visible()
        expect(self.page.get_by_text(booking_id)).to_be_visible()

        self.page.get_by_role('button',name='My Bookings').click()
        event_card_locator = self.page.locator('#booking-card',has_text=booking_reference2['Booking Ref'])
        expect(event_card_locator).to_be_visible()
        event_card_locator.get_by_role('button',name='View Details').click()
        expect(self.page.get_by_text(booking_reference2['Booking Ref']).first).to_be_visible()
        expect(self.page.get_by_role('heading',name = booking_reference2['Title']).first).to_be_visible()
        expect(self.page.get_by_text(str(booking_reference2['Tickets']), exact=True)).to_be_visible()
        expect(self.page.get_by_text(str(booking_reference2['Total'])).first).to_be_visible()
        expect(self.page.get_by_text(str(booking_reference1['Total'])).first).not_to_be_visible()




def test_login_verification(page: Page):
    login_page = Verification(page)
    login_page.login('loguraj568@gmail.com','March@0329')

    login_page.search_for_booking(search_word='World',city='Hyderabad')
    login_page.book_tickets(no_of_tickets=1,name='Prithvi',email='loguraj568@gmail.com',phone='7708196869')
    booking_details1 = login_page.retrive_booking_details().copy()
    print(booking_details1)
    login_page.verify_first_test()
    
    # full_booking_details1 = login_page.get_booking_details(search_word='World')
    # print(full_booking_details1)

    login_page.search_for_booking(search_word='Dilli',city='Delhi')
    login_page.book_tickets(no_of_tickets=2,name='Prithvi',email='loguraj568@gmail.com',phone='7708196869')
    booking_details2 = login_page.retrive_booking_details().copy() #because we are using single object for all
    print(booking_details2)

    login_page.verify_second_test(booking_reference=booking_details2['Booking Ref'])
    test1 = login_page.verify_third_test(booking_reference=booking_details1['Booking Ref']).copy()
    test2 = login_page.verify_third_test(booking_reference=booking_details2['Booking Ref']).copy()
    
    login_page.check_details(booking_details1, test1)
    login_page.check_details(booking_details2, test2)

    login_page.verify_fourth_test(booking_reference1=booking_details1,booking_reference2=booking_details2)




    





