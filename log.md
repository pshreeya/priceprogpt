How did I incorporate AI tools (Claude & GitHub Copilot) to build this?

- I used Claude to help me understand how Pydantic library works to be able to set up the pricing.py backend.

- Asked "what fields I'm missing that would be essential for a pricing recommendation". It suggested "inventory remaining" information as well as "lead time days" information to put within the "Pricing Input" class.

- Used Claude to brainstorm 12 candidate scenarios across 4 domains, picked the 5 most diverse, wrote the actual payloads myself.

- Used GitHub Copilot to get a rough structure for the frontend. I wrote the API fetch hook and error handling by hand because I wanted fine-grained control over the loading and validation-error states.

Debugging:
I was facing an error with the reference prices line:
reference_price: list[float] = Field(..., gt=0, description="Reference competitor prices for the product"). When I asked GitHub Copilot, it told me the error was occuring because of the use of gt=0 on a list field in Pydantic. It told me that gt constraint only applies to single numeric values, not lists. It also suggested to incorporate a field validator for reference prices list so each element of the list is a price greater than 0.
