import time

from playwright.sync_api import Page, expect
from urllib.parse import urlparse, parse_qs
import re

data = {
    "data": [
        {
            "id": 300,
            "title": "Live Beats Music Festival",
            "description": "Celebrate the Festival of Lights at the grandest Diwali Mela in North India. Enjoy 200+ stalls of artisanal crafts, street food, folk performances, fireworks, and cultural showcases spanning three vibrant evenings.",
            "category": "Festival",
            "venue": "Pragati Maidan Exhibition Grounds",
            "city": "Delhi",
            "eventDate": "2026-10-20T17:00:00.000Z",
            "price": "300",
            "totalSeats": 10000,
            "availableSeats": 8187,
            "imageUrl": "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?w=800",
            "isStatic": True,
            "userId": None,
            "createdAt": "2026-09-14T02:39:14.874Z",
            "updatedAt": "2026-09-26T09:10:31.751Z"
        },
        {
            "id": 301,
            "title": "International City Marathon",
            "description": "An unforgettable evening of live music performed by A-list playback singers under the open Mumbai sky. Featuring chart-toppers from the last three decades with a stunning light show and pyrotechnics.",
            "category": "Concert",
            "venue": "Dome, NSCI SVP Stadium, Worli",
            "city": "Mumbai",
            "eventDate": "2026-07-11T19:00:00.000Z",
            "price": "2500",
            "totalSeats": 3000,
            "availableSeats": 2913,
            "imageUrl": "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800",
            "isStatic": True,
            "userId": None,
            "createdAt": "2026-09-14T02:39:14.864Z",
            "updatedAt": "2026-09-26T00:49:44.205Z"
        },
        {
            "id": 302,
            "title": "Global Food & Culture Festival",
            "description": "A premier technology conference bringing together 500+ industry leaders, startup founders, and engineers for two days of keynotes, workshops, and networking. Topics include AI/ML, cloud infrastructure, DevSecOps, and the future of the Indian tech ecosystem.",
            "category": "Conference",
            "venue": "Hyderabad, Hitech city",
            "city": "Hyderabad",
            "eventDate": "2026-04-18T09:00:00.000Z",
            "price": "1500",
            "totalSeats": 500,
            "availableSeats": 53,
            "imageUrl": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800",
            "isStatic": True,
            "userId": None,
            "createdAt": "2026-09-14T02:39:14.852Z",
            "updatedAt": "2026-09-25T17:16:12.588Z"
        }, 
        {
            "id": 303,
            "title": "Hip Hop Tamizha Concert",
            "description": "Return of the Dragon Machi World Tour Homecoming Finale",
            "category": "Workshop",
            "venue": "Bangalore City",
            "city": "Bangalore",
            "eventDate": "2026-04-18T09:00:00.000Z",
            "price": "200",
            "totalSeats": 400,
            "availableSeats": 163,
            "imageUrl": "https://images.t2u.io/upload/event/listing/0-46555-AWSS381ea547e-9648-4eaf-aae2-505b956d4cfe-w4rj.jpg",
            "isStatic": True,
            "userId": None,
            "createdAt": "2026-09-14T02:39:14.852Z",
            "updatedAt": "2026-09-25T17:16:12.588Z"
        }
    ]
}

def response_filler1(route):
    url = route.request.url      #print(parsed.scheme)-'https', print(parsed.netloc) -'eventhub.rahulshettyacademy.com' , print(parsed.path)-'/events/283', print(parsed.query)-status=confirmed', print(parsed.fragment)  # 'details'
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    category = params.get('category', [None])[0]
    city = params.get('city', [None])[0]

    # Filter data based on query parameters
    filtered_events = data["data"]
    if category or city:
        filtered_events = [item for item in filtered_events if (item.get('category') == category or item.get('city') == city)]
    route.fulfill(json={"data": filtered_events})

def response_filler2(route):
    url = route.request.url       
    event_id = url.split('/')[-1]
    events = data["data"]
    filtered_events = [
        item for item in events if item.get("id") == int(event_id)
    ]
    if filtered_events:
        route.fulfill(json={"data":filtered_events[0]})
    else:
        route.fulfill(json={"data":[]})
    

def test_firstTest(page:Page):
    page.goto('https://eventhub.rahulshettyacademy.com/login')
    page.route('https://api.eventhub.rahulshettyacademy.com/api/events?*', response_filler1)
    page.route('https://api.eventhub.rahulshettyacademy.com/api/events/*',response_filler2)
    page.locator('#email').fill('loguraj568@gmail.com')
    page.locator('#password').fill('March@0329')
    page.get_by_role("button", name="Sign In").click()
    page.get_by_role("link",name='Events').first.click()
    expect(page.get_by_text("Upcoming Events")).to_be_visible()
    event_cards = page.locator('#event-card')
    expect(event_cards.first).to_be_visible()
    event_cards_count = event_cards.count() 
    assert event_cards_count == 4

    for index in range(event_cards_count):
        title_locator = event_cards.nth(index).filter(has_text=data["data"][index]['title'])
        expect(title_locator).to_be_visible()
        price = int(data["data"][index]['price'])
        raw_price = f"${price:,}"   #it will format the rupees
        price_locator = title_locator.filter(has_text=raw_price)
        expect(price_locator).to_be_visible()
        expect(title_locator.filter(has_text=str(data["data"][index]['availableSeats']))).to_be_visible()
        title_link = title_locator.get_by_role("link", name=data["data"][index]["title"])
        expect(title_link).to_have_attribute("href", f"/events/{data['data'][index]['id']}")

    expect(event_cards.filter(has_text='World Tech Summit')).not_to_be_visible()
    page.get_by_placeholder("Search events, venues…").fill("Global Food")
    page.locator("select").filter(has_text="All Categories").select_option("Conference") 
    page.locator("select").filter(has_text="All Cities").select_option("Hyderabad")

    expect(page.locator("h3",has_text='Global Food & Culture Festival')).to_be_visible()
    time.sleep(1)
    expect(event_cards.first).to_be_visible()
    event_cards_count = event_cards.count() 
    assert event_cards_count == 1
    
    title = event_cards.first.locator('h3').inner_text()
    price = event_cards.first.locator('p').inner_text()
    card_text = event_cards.first.locator('span').all_inner_texts()
    link_locator = page.get_by_role("link", name=title)
    event_id = link_locator.get_attribute('href')    
    venues_seats  = card_text[3].split(',')
    venues = venues_seats[0]+','+venues_seats[1]
    city  = card_text[2]
    seats = card_text[4].split(' ')[0]

    print('Title is:',title)
    print('Price is:',price)
    print('Seats is:',seats)
    print('City is:',city)
    print('Venue is:',venues)
    print('event_id is', event_id)
    event_cards.first.get_by_text('Book Now').click()

    expect(page).to_have_url(re.compile(event_id))
    expect(page.get_by_text(title).first).to_be_visible()
    expect(page.get_by_text(re.compile(venues))).to_be_visible()
    expect(page.get_by_text(price).first).to_be_visible()
    expect(page.get_by_text(re.compile(rf'{seats}'))).to_be_visible()

    form_locator = page.locator('.space-y-4')
    expect(form_locator.get_by_text("1", exact=True)).to_be_visible()
    expect(form_locator.get_by_text(price).last).to_be_visible()

    form_locator.get_by_role('button',name='+').click()
    price = price[1:]
    price = price.replace(',','').replace('$','')
    calculating_price = int(price) * 2
    calculating_price = f"${calculating_price:,}"
    expect(form_locator.get_by_text(calculating_price).last).to_be_visible()
