# lstr: Partially lockable Python Strings

`lstr` is a Python package for partially lockable strings.

## Example

Create an `lstr` via a regular string:

```python
from lstr import lstr

greeting = lstr("Hello, world!")
print(greeting)  # "Hello, world!"
```

Update an `lstr` by invoking `replace()` with the replacement string, the index to insert at, and the length of current string to replace.

```text
index:   0  1  2  3  4  5  6  7  8  9 10 11 12
string:  H  e  l  l  o  ,     w  o  r  l  d  !
```

For example, to change "Hello" to "Hey", the replacement would start at index `0` and have length `5`:

```python
from lstr import lstr

greeting = lstr("Hello, world!")
greeting.replace("Hey", index=0, length=5)
print(greeting)  # "Hey, world!"
```

To prevent the word "Hello" being changed, add a lock on that range:

```python
from lstr import lstr

greeting = lstr("Hello, world!")
greeting.lock(index=0, length=5)

greeting.replace("Hey", index=0, length=5)  # False
print(greeting)  # "Hello, world!"

greeting.replace(" there", index=5, length=7)  # True
print(greeting)  # "Hello there!"
```

## Installation

`lstr` requires Python 3.8 or later.

```bash
pip install lstr
```

## Usage

- `lstr(value: str, locks: List[Lock] = [])` requires a base string value, and optionally accepts a list of locks to apply.
- `lstr.can_replace(index: int, length: int) -> bool` indicates whether or not a range can be replaced.
- `lstr.lock(index: int, length: int) -> None` adds a lock.
- `lstr.replace(value: str, index: int, length: int) -> bool` attempts to replace a given range with a new value. Returns `True` if the replacement was permitted, otherwise `False`.

## Thank you! 🎉

My name is **Cariad**, and I'm an [independent freelance DevOps engineer](https://cariad.io).

I'd love to spend more time working on projects like this, but--as a freelancer--my income is sporadic and I need to chase gigs that pay the rent.

If this project has value to you, please consider [☕️ sponsoring](https://github.com/sponsors/cariad) me. Sponsorships grant me time to work on _your_ wants rather than _someone else's_.

Thank you! ❤️
