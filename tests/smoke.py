from lstr import Lock, lstr

# index:   0  1  2  3  4  5  6  7  8  9 10 11 12
# string:  H  e  l  l  o  ,     w  o  r  l  d  !

greeting = lstr("Hello, world!", locks=[Lock(index=0, length=5)])
greeting.lock(index=12, length=1)

assert str(greeting) == "Hello, world!"
assert greeting.replace("Hey", index=0, length=5) == False
assert str(greeting) == "Hello, world!"

assert greeting.replace("?", index=12, length=1) == False
assert str(greeting) == "Hello, world!"

assert greeting.replace(" there", index=5, length=7) == True
assert str(greeting) == "Hello there!"
