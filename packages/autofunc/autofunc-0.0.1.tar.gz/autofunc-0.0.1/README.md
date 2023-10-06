# autofunc

Easily define Python functions for structured output from GPT-4.

## Install

```
pip install autofunc
```

## Usage

Expects `OPENAI_API_KEY` to be defined in your environment.

### Define your function

```python
from autofunc import AutoFunc


swap_animals = AutoFunc("Swap the animals in the sentence. Eg. The dog barked at the cat -> the cat meowed at the dog")
```

### Call it

```python
swap_animals("The tigers growled at each other until they saw the snakes slithering near the trees.")

'The snakes hissed at each other until they saw the tigers prowling near the trees.'
```

### Use `pydantic` for structured output

```python
from pydantic import BaseModel, Field

class TravelDescription(BaseModel):
    from_city: str = Field(description="City name including the country")
    to_city: str = Field(description="City name including the country")
    mode_of_travel: str = Field(description="eg. train or flight")
    description: str = Field(description="A one-line description of a fictional journey, in the style of an adventure game. Simple present tense.")
    duration: str

travel_fn = AutoFunc("Describe travelling between the two provided cities.", TravelDescription)
```

```python
travel_fn("londres to paris")

{
 'from_city': 'London, United Kingdom',
 'to_city': 'Paris, France',
 'mode_of_travel': 'train',
 'description': 'You embark on a journey from the bustling city of London, crossing the English Channel through the Eurotunnel, to the romantic city of Paris.',
 'duration': '2 hours 20 minutes'
}
```

## Notes

:warning: This was primarily written for personal use, and is neither well-tested nor documented. There are similar and much better projects out there, such as [magentic](https://github.com/jackmpcollins/magentic).
