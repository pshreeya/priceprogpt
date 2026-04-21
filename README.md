# priceadvisor

Setting the right price is one of the hardest descisons faced by company executives. Most small-to-mid sized sellers still do it by gut feel, static rules (always 10% below competitor X) or rigid seasonal calendars. 

This is a full-stack app that explores whether an LLM model, given only a handful of structured inpits and free-text context, can produce a pricing recommendation with approprite reasoning useful for a human to make an effective pricing descion. 

How it works?
Enter a product type, current price, reference prices (competitors/market), and qualitative context signals (demand, events, inventory).
The Claude LLM returns a structured pricing recommendation with a confidences score, reasoning, and risk flags. 

Some potential use cases include determining the appropriate prices for:
- hotel rooms
- concert tickets
- Airbnb stays
- e-commerce



