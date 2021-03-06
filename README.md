# lstr: partially lockable Python strings

`lstr` is a Python package for partially lockable strings.

## Installation

`lstr` requires Python 3.8 or later.

```bash
pip install lstr
```

## Examples

### Creating an lstr

```python
from lstr import lstr

greeting = lstr("Hello, world!")
print(greeting)
```

```text
Hello, world!
```

### Getting help with indexes

```python
from lstr import lstr

greeting = lstr("Hello, world!")
print(repr(greeting))
```

```text
  0  1  2  3  4  5  6  7  8  9 10 11 12
  H  e  l  l  o  ,     w  o  r  l  d  !
```

### Inserting text

```python
from lstr import lstr

greeting = lstr("Good morning, Bobby!")
greeting.write("Captain ", index=14)
print(greeting)
```

```text
Good morning, Captain Bobby!
```

### Overwriting text

```python
from lstr import lstr

greeting = lstr("Good morning, Captain Bobby!")
greeting.write("Fleet Admiral", index=14, length=7)
print(greeting)
```

```text
Good morning, Fleet Admiral Bobby!
```

### Substituting text

```python
from lstr import lstr

greeting = lstr("Good morning, Fleet Admiral Bobby!")
greeting.sub("morning", "evening")
print(greeting)
```

```text
Good evening, Fleet Admiral Bobby!
```

### Substituting text with a regular expression

```python
from lstr import lstr

greeting = lstr("Good evening, Fleet Admiral Bobby!")
greeting.sub(r"(Fleet Admiral)", r"🎉\g<1>🎉")
print(greeting)
```

```text
Good evening, 🎉Fleet Admiral🎉 Bobby!
```

### Locking a range

```python
from lstr import lstr

greeting = lstr("Good morning, Fleet Admiral Bobby!")
greeting.lock(index=14, length=13)

greeting.write("Ensign", index=14, length=13)
print(greeting)
```

```text
Good morning, Fleet Admiral Bobby!
```

### Locking a substitution

```python
from lstr import lstr

greeting = lstr("Good morning, Captain Bobby!")
greeting.sub("Captain", "Fleet Admiral", lock=True)
greeting.sub("Fleet Admiral", "Ensign")

print(greeting)
```

```text
Good morning, Fleet Admiral Bobby!
```

### Equality

`lstr` instances are considered equal only if their string value and locks are identical.

```python
lstr("f", locks=[Lock(index=1, length=2)]) == lstr("f", locks=[Lock(index=1, length=2)])
lstr("f", locks=[Lock(index=1, length=2)]) != lstr("f", locks=[Lock(index=3, length=4)])
```

`lstr` and `str` instances are considered equal if the string value is identical, regardless of the locks.

```python
lstr("f") == "f"
lstr("f") != "g"
```

## Thank you! 🎉

My name is **Cariad**, and I'm an [independent freelance DevOps engineer](https://cariad.io).

I'd love to spend more time working on projects like this, but--as a freelancer--my income is sporadic and I need to chase gigs that pay the rent.

If this project has value to you, please consider [☕️ sponsoring](https://github.com/sponsors/cariad) me. Sponsorships grant me time to work on _your_ wants rather than _someone else's_.

Thank you! ❤️
