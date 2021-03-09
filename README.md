# lstr: partially lockable Python strings

`lstr` is a Python package for partially lockable strings.

## Installation

`lstr` requires Python 3.8 or later.

```bash
pip install lstr
```

## Example

### Creating an lstr

```python
from lstr import lstr

greeting = lstr("Hello, world!")
print(greeting)  # "Hello, world!"
```

### Writing text

One way to update an `lstr` is via `write()`. This will replace a specific range of characters with a new string.

For example, to change "Hello" to "Hey", write `Hey` at index `0` for length `5`:

```python
from lstr import lstr

greeting = lstr("Hello, world!")
greeting.write("Hey", index=0, length=5)
print(greeting)  # "Hey, world!"
```

### Getting help with indexes

To get help figuring out exactly which character is at exactly which index, call `repr()` for your `lstr`:

```python
from lstr import lstr

greeting = lstr("Hello, world!")
print(repr(greeting))
```

```text
  0  1  2  3  4  5  6  7  8  9 10 11 12
  H  e  l  l  o  ,     w  o  r  l  d  !
```

### Substituting text

The second method for updating an `lst` is via `sub()`. This will replace matches of a regular expression with a new string.

To replace one substring with another:

```python
from lstr import lstr

greeting = lstr("Hello!")
greeting.sub("l", "b")
print(greeting)  # "Hebbo!"
```

To replace each match of a regular expression with a group's value:

```python
from lstr import lstr

document = lstr("How *exciting!* So *bold!*")
document.sub(r"\*([^*]+)\*", r"<em>\g<1></em>")
print(document)  # "How <em>exciting!</em> So <em>bold!</em>"
```

### Locking

To prevent any changes to a region of the `lst`, lock it via `lock()`.

To prevent changes to the word "Hello" in "Hello, world!" create a lock from index `0` for length `5`:

```python
from lstr import lstr

greeting = lstr("Hello, world!")

print(repr(greeting))
#  0  1  2  3  4  5  6  7  8  9 10 11 12
#  H  e  l  l  o  ,     w  o  r  l  d  !

greeting.lock(index=0, length=5)
```

Now any changes to that region will be denied:

```python
from lstr import lstr

greeting = lstr("Hello, world!")
greeting.lock(index=0, length=5)

greeting.sub("Hello", "Hey")  # False
print(greeting)  # "Hello, world!"
```

Text outside of that region can still be updated

```python
from lstr import lstr

greeting = lstr("Hello, world!")
greeting.lock(index=0, length=5)

greeting.sub("Hello", "Hey")  # False
print(greeting)  # "Hello, world!"

greeting.sub("world", "there")  # True
print(greeting)  # "Hello, there!"
```

## `lstr` class

### `lstr(value: str, locks: List[Lock] = [])`

`lstr` must be created with a string value, and an optional list of `Lock` instances. Additional locks can be added later via the `lock()` method.

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

### Length

Calling `len()` for an `lstr` instance will return the length of the string value.

### Repr

Calling `repr()` for an `lstr` instance will return a string describing the index numbers, characters and locks.

```python
from lstr import lstr, Lock

greeting = lstr("Hello, world!", locks=[Lock(index=0, length=5)])
print(repr(greeting))

#  0  1  2  3  4  5  6  7  8  9 10 11 12
#  H  e  l  l  o  ,     w  o  r  l  d  !
#  ^  ^  ^  ^  ^
```

### Str

Calling `str()` for an `lstr` instance will return the string value.

### `can_sub(self, pattern: str, replacement: str) -> bool`

`can_sub()` indicates whether or not the specified substitution will succeed for all instances.

### `can_write(self, index: int, length: int) -> bool`

`can_write()` indicates whether or not the specified range can be overwritten.

### `lock(self, index: int, length: int) -> None`

`lock()` describes a new locked range.

### `sub(self, pattern: str, replacement: str, allow_partial: bool = False) -> bool`

`sub()` attempts to substitute all matching patterns with a replacement string.

- `pattern` is the pattern to search for. This can be a simple string or a regular expression.
- `replacement` is the string to replace matches with. This can be a simple string or an expression expansion to reference a matched group.
- `allow_partial` indicates whether to allow only unlocked matches to be substituted (i.e. a partial update) or to require all matches to be in unlocked ranges (i.e. to force a full update or no update at all).

`sub()` returns `True` if every matching instance of the pattern could be updated.

### `write(self, value: str, index: int, length: int) -> bool`

`write()` attempts to write a new string into a range.

- `value` is the string to write.
- `index` is the index to start writing at.
- `length` is the length of the original string to overwrite. This can be `0` to insert the string without overwriting. If this length is shorter than the string being written then the base string will become shorter. Likewise, if this length is longer than the string will grow.

`write()` returns `True` if the range could be written.

## Thank you! 🎉

My name is **Cariad**, and I'm an [independent freelance DevOps engineer](https://cariad.io).

I'd love to spend more time working on projects like this, but--as a freelancer--my income is sporadic and I need to chase gigs that pay the rent.

If this project has value to you, please consider [☕️ sponsoring](https://github.com/sponsors/cariad) me. Sponsorships grant me time to work on _your_ wants rather than _someone else's_.

Thank you! ❤️
