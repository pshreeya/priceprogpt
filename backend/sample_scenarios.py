scenarios = [
    # 1. Tuesday off-season hotel room, comp set stable, low occupancy
    {
        "product_name": "Standard Queen Room",
        "product_description": "A standard queen room at a midscale hotel in a business district.",
        "cost_basis": 60.0,
        "current_price": 95.0,
        "competitor_prices": [100.0, 98.0, 102.0],
        "target_market": "Business travelers, off-season, weekday stay.",
        "currency": "USD"
    },
    # 2. Saturday boutique hotel with concert, comp set raised rates 20%
    {
        "product_name": "Boutique King Suite",
        "product_description": "Boutique hotel suite, city center, concert weekend.",
        "cost_basis": 120.0,
        "current_price": 210.0,
        "competitor_prices": [240.0, 250.0, 230.0],
        "target_market": "Couples and concert-goers, high demand weekend.",
        "currency": "USD"
    },
    # 3. Concert ticket two weeks before event, slow sales, comps selling well
    {
        "product_name": "Concert Ticket - Balcony",
        "product_description": "Balcony seat for major artist, two weeks out.",
        "cost_basis": 35.0,
        "current_price": 60.0,
        "competitor_prices": [65.0, 70.0, 68.0],
        "target_market": "Fans, slow sales for this show, comps selling out.",
        "currency": "USD"
    },
    # 4. Airbnb listing with festival, 8 nights out, 30% comps booked
    {
        "product_name": "2BR Airbnb near Festival Grounds",
        "product_description": "Entire 2-bedroom apartment, walkable to festival.",
        "cost_basis": 80.0,
        "current_price": 150.0,
        "competitor_prices": [160.0, 170.0, 155.0],
        "target_market": "Festival attendees, 8 days out, 30% comps booked.",
        "currency": "USD"
    },
    # 5. E-commerce winter coat, end of season, 40% inventory, comps -25%
    {
        "product_name": "Men's Down Winter Coat",
        "product_description": "Premium down coat, end of winter season.",
        "cost_basis": 45.0,
        "current_price": 90.0,
        "competitor_prices": [70.0, 68.0, 72.0],
        "target_market": "Online shoppers, inventory at 40%, competitors discounting.",
        "currency": "USD"
    },
]

if __name__ == "__main__":
    import json
    print(json.dumps(scenarios, indent=2))