from playwright.sync_api import sync_playwright, Playwright,expect
import re


class APIutils:

    def getToken(self, playwright):
        api_request_context = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        response = api_request_context.post("/api/auth/login",data={"email": "loguraj568@gmail.com","password": "March@0329"})
        print(response.json()["token"])
        return response.json()["token"]

    def get_live_events(self, playwright):
        token = self.getToken(playwright)
        api_request_context = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        response = api_request_context.get("/api/events",headers={"Authorization": f'Bearer {token}',"Content-Type": "application/json"})
        data = response.json().get('data',{})
        return data

    def book_tickets(self,playwright,event_id):
        token = self.getToken(playwright)
        api_request_context = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        response = api_request_context.post("/api/bookings",headers={"Authorization": f'Bearer {token}'},data={"customerEmail":"loguraj568@gmail.com","customerName":"Prithvi","customerPhone":"7708196869","quantity":2,"eventId":event_id})
        data = response.json()
        assert data.get('success')
        print(data.get('data').get('id'))
        assert data.get('data').get('id')
        return data.get('data')

    def cancel_booking(self,playwright,event_id):
        token = self.getToken(playwright)
        api_request_context = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        response = api_request_context.delete(f"/api/bookings/{event_id}",headers={"Authorization": f'Bearer {token}'})
        data = response.json()
        assert(data['success'])
        assert(data['message'] == 'Booking cancelled')
        return data['message']

    def get_booked_events(self,playwright,event_id):
        token = self.getToken(playwright)
        api_request_context = playwright.request.new_context(base_url="https://api.eventhub.rahulshettyacademy.com")
        response = api_request_context.get(f"/api/bookings/{event_id}",headers={"Authorization": f'Bearer {token}'})
        data = response.json()
        print(data)
        assert data['error'] == f'Booking with id {event_id} not found'



with sync_playwright() as playwright:
    token_obj = APIutils()
    events = token_obj.get_live_events(playwright)
    booking_id = 0
    for event in events:
        if event.get('availableSeats') >=2 :
            booking_id = event.get('id')
            break
    tickets = token_obj.book_tickets(playwright,booking_id)
    print(tickets)
    booking_ref = tickets.get('bookingRef')
    booking_id = tickets.get('id')
    customerName = tickets.get('customerName')
    customerEmail = tickets.get('customerEmail')
    customerPhone = tickets.get('customerPhone')
    quantity = tickets.get('quantity')
    totalPrice = tickets.get('totalPrice')
    title = tickets.get('event').get('title')

    token = token_obj.getToken(playwright)
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    #script to inject token in session local storage
    page.add_init_script(f"""localStorage.setItem('eventhub_token', '{token}')""")
    page.goto('https://eventhub.rahulshettyacademy.com/bookings')
    event_card = page.locator('#booking-card',has_text=booking_ref)
    expect(event_card).to_be_visible()
    expect(event_card.locator('h3').get_by_text(title)).to_be_visible()
    expect(event_card.get_by_text(f'${int(totalPrice):,}')).to_be_visible()
    expect(event_card.get_by_text(f'{quantity} tickets')).to_be_visible()
    event_card.get_by_role('button',name='View Details').click()

    expect(page.get_by_role("heading", name="Event Details")).to_be_visible()
    expect(page).to_have_url(re.compile(rf'{booking_id}'))
    expect(page.get_by_text(customerEmail).first).to_be_visible()
    expect(page.get_by_text(str(quantity),exact=True)).to_be_visible()
    expect(page.get_by_text(f'${int(totalPrice):,}')).to_be_visible()

    message = token_obj.cancel_booking(playwright,booking_id)
    token_obj.get_booked_events(playwright,booking_id)
    
    page.locator('#nav-bookings',has_text='My Bookings').click()
    page.reload()
    expect(event_card).not_to_be_visible()
    

    
    

