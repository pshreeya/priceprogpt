Backend:
I used Claude to help me to understand how Pydantic library works, as well as set up the pricing.py backend.

Pydantic library: a data validation library, allows to define data models using Python's type annotations, models automatically validate the data against the types specified.

Asked "what fields am I missing that would be essential for a pricing recommendation". It suggested inventory remaining information as well as lead time days information within the Pricing Input class.

I was facing an error with the reference prices line:
reference_price: list[float] = Field(..., gt=0, description="Reference competitor prices for the product").

I asked GitHub Copilot to help me troubleshoot, it said I can't use gt=0 on a list field in Pydantic as the gt constraint only applies to single numeric values, not lists.

It also suggested to incorporate a field validator for reference prices list so each element of the list is a price greater than 0.

Claude LLM set up:

Asked "What failure modes are likely?", "What edge cases am I not handling?" with respect to the prompt.

Scenario examples:
Used Claude to brainstorm 12 candidate scenarios across 4 domains, picked the 5 most diverse, wrote the actual payloads myself.

Front-end:
Used GitHub Copilot for form scaffolding and card layout; wrote the API fetch hook and error handling by hand because I wanted fine-grained control over the loading and validation-error states.
