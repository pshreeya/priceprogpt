const scenarios = [
  {
    label: "Off-season hotel, low demand",
    data: {
      product_type: "hotel_room",
      current_price: 95,
      reference_prices: [100, 98, 102],
      demand_signal: 0.25,
      inventory_remaining: 40,
      lead_time_days: 2,
      context_notes:
        "Tuesday stay, business district, off-season. 80% of rooms still unsold.",
    },
  },
  {
    label: "Boutique hotel, concert weekend",
    data: {
      product_type: "hotel_room",
      current_price: 210,
      reference_prices: [240, 250, 230],
      demand_signal: 0.9,
      inventory_remaining: 6,
      lead_time_days: 4,
      context_notes:
        "Major concert Saturday, city-center boutique. Comp set raised rates 20% in past 48h.",
    },
  },
  {
    label: "Concert ticket, slow sales 2 weeks out",
    data: {
      product_type: "event_ticket",
      current_price: 60,
      reference_prices: [65, 70, 68],
      demand_signal: 0.35,
      inventory_remaining: 180,
      lead_time_days: 14,
      context_notes:
        "Balcony seats, mid-tier headliner. Competitors selling faster than us.",
    },
  },
  {
    label: "Airbnb, festival week, 8 days out",
    data: {
      product_type: "short_term_rental",
      current_price: 150,
      reference_prices: [160, 170, 155],
      demand_signal: 0.75,
      inventory_remaining: 1,
      lead_time_days: 8,
      context_notes:
        "2BR apartment walkable to festival grounds. 30% of comp set already booked.",
    },
  },
  {
    label: "Winter coat, end of season",
    data: {
      product_type: "ecom_item",
      current_price: 90,
      reference_prices: [70, 68, 72],
      demand_signal: 0.3,
      inventory_remaining: 120,
      lead_time_days: 30,
      context_notes:
        "Premium down coat, end of winter. Competitors already at 25% off. Need to clear for spring inventory.",
    },
  },
];

export default scenarios;
