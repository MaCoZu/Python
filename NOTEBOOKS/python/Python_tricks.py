# decorator with 'wraps'

# @wraps(func) preserves the original function's metadata (name, docstring, etc.). Without it, my_function.__name__ would be "wrapper" instead.

import time
from functools import wraps


def timer2(func):
    @wraps(func)  # ← Preserves metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


@timer2
def my_function2(sleep_time=1):
    """sleeps a few seconds"""
    time.sleep(sleep_time)
    return "done"


print(my_function2.__name__)  # "my_function2" ✓
print(my_function2.__doc__)  # "sleeps a few seconds" ✓


# decorator is a function that wraps another function to modify or extend its behavior without changing its code.


# timer() receives the decorated function (my_function()) and returns the wrapper
def timer(func):
    # wrapper enhances the decorated fct and receives the arguments of the original fct
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # before original fct

        # original receives it's own arguments form the wrapper and executes the core fct.
        result = func(*args, **kwargs)

        # after original fct
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")

        # return original fct results
        return result

    # return the wrapper results
    return wrapper


# Usage
@timer  # wraps my_function
# 'my_function' now points to 'wrapper', not the original
def my_function(sleep_time=1):  # timer receives the original my_function as 'func'
    time.sleep(sleep_time)
    return "done"  # timer returns 'wrapper'


# You're actually calling wrapper()
my_function(4)


# ----------------------------------------------------------------------------------------------
# Type Annotations
# ----------------------------------------------------------------------------------------------


# Type hints are annotations that specify what types variables, parameters, and returns should be. They're optional documentation that tools (mypy) can check.
def greeting(name: str) -> str:
    """
    Returns a greeting message for the given name."""
    return f"Hello {name}"


## Basic
name: str = "Alice"
age: int = 25
price: float = 9.99
active: bool = True

## Collections
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 100}
coords: tuple[int, int] = (10, 20)
unique: set[str] = {"a", "b"}

## Optional (can be None)

middle_name: str | None = None  # same as str | None

## Union (multiple types)

id: int | str = "abc123"  # same as int | str

## Any (escape hatch - any type allowed)
from typing import Any

data: Any = "whatever"  # defeats type checking

from collections.abc import Callable

callback: Callable[[int, str], bool]  # takes int, str; returns bool

# ----------------------------------------------------------------------------------------
# Merging Dictionaries
# ----------------------------------------------------------------------------------------
# initialize two dictionaries
dict1 = {"a": 1, "b": 4}
dict2 = {"c": 2}

# merge dictionaries
dict1.update(dict2)
print(dict1)

# new way
merged = dict1 | dict2
print(merged)


# ----------------------------------------------------------------------------------------
# Sorting with Key
# ----------------------------------------------------------------------------------------
people = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 20}]
sorted_name = sorted(people, key=lambda x: x["name"])
sorted_age = sorted(people, key=lambda x: x["age"])
print(sorted_name)
print(sorted_age)

# ----------------------------------------------------------------------------------------
# Enumerate
# ----------------------------------------------------------------------------------------
for index, value in enumerate(["a", "b", "c"]):
    print(index, value)


# ----------------------------------------------------------------------------------------
# List comprehension
# ----------------------------------------------------------------------------------------
## generate lists by applying an expression to each item in an iterable and then filters
even_numbers = [x**2 for x in range(10) if x % 2 == 0 and x != 0]
print(even_numbers)


numbers = [1, 2, 3, 4, 5]
result = ["Even" if num % 2 == 0 else "Odd" for num in numbers]
print(result)


# ----------------------------------------------------------------------------------------
# Nested List Comprehension
# ----------------------------------------------------------------------------------------
users = [
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"},
]

friendship_pairs = [
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    (8, 9),
]

# Initialize the dict with an empty list for each user id:
friendships = {user["id"]: [] for user in users}

# And loop over the friendship pairs to populate it:
for i, j in friendship_pairs:
    friendships[i].append(j)  # Add j as a friend of user i
    friendships[j].append(i)  # Add i as a friend of user j


# Example 1: Friends of Friends
def foaf_ids_bad(user):
    """foaf is short for "friend of a friend" """
    return [
        foaf_id  # Step 3 collect values
        for friend_id in friendships[user["id"]]  # Step 1 get key
        for foaf_id in friendships[friend_id]  # Step 2 fetch values per key
    ]


# Step 2: Get each friend's friends
# Equivalent loops:
# for friend_id in my_friends:
#     for foaf_id in their_friends:
#         collect foaf_id


# Example 2: Friends of Friends (filtered)
from collections import Counter  # not loaded by default


def friends_of_friends(user):
    user_id = user["id"]
    return Counter(
        foaf_id  # 3. collect from
        for friend_id in friendships[user_id]  # 1. For each of my friends,
        for foaf_id in friendships[friend_id]  # 2. find their friends
        if foaf_id != user_id  # 2.1 who aren't me
        and foaf_id not in friendships[user_id]  # 2.2 and aren't my friends.
    )


print(friends_of_friends(users[3]))  # Counter({0: 2, 5: 1})


# Example 3: Users with target interest

interests = [
    (0, "Hadoop"),
    (0, "Big Data"),
    (0, "HBase"),
    (0, "Java"),
    (0, "Spark"),
    (0, "Storm"),
    (0, "Cassandra"),
    (1, "NoSQL"),
    (1, "MongoDB"),
    (1, "Cassandra"),
    (1, "HBase"),
    (1, "Postgres"),
    (2, "Python"),
    (2, "scikit-learn"),
    (2, "scipy"),
    (2, "numpy"),
    (2, "statsmodels"),
    (2, "pandas"),
    (3, "R"),
    (3, "Python"),
    (3, "statistics"),
    (3, "regression"),
    (3, "probability"),
    (4, "machine learning"),
    (4, "regression"),
    (4, "decision trees"),
    (4, "libsvm"),
    (5, "Python"),
    (5, "R"),
    (5, "Java"),
    (5, "C++"),
    (5, "Haskell"),
    (5, "programming languages"),
    (6, "statistics"),
    (6, "probability"),
    (6, "mathematics"),
    (6, "theory"),
    (7, "machine learning"),
    (7, "scikit-learn"),
    (7, "Mahout"),
    (7, "neural networks"),
    (8, "neural networks"),
    (8, "deep learning"),
    (8, "Big Data"),
    (8, "artificial intelligence"),
    (9, "Hadoop"),
    (9, "Java"),
    (9, "MapReduce"),
    (9, "Big Data"),
]


def data_scientists_who_like(target_interest):
    """Find the ids of all users who like the target interest."""
    return [
        user_id  # collect first element
        for user_id, user_interest in interests  # unpack tuple
        if user_interest == target_interest  # condition on second element
    ]


# ----------------------------------------------------------------------------------------
# Identifying the Differences in Lists
# ----------------------------------------------------------------------------------------
list_1 = [1, 3, 5, 7, 8]
list_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

solution_1 = list(set(list_2) - set(list_1))
solution_2 = list(set(list_1) ^ set(list_2))  # symmetric difference operator (^)
solution_3 = list(set(list_1).symmetric_difference(set(list_2)))  # symmetric difference methods

print(f"Solution 1: {solution_1}")
print(f"Solution 2: {solution_2}")
print(f"Solution 3: {solution_3}")


# ----------------------------------------------------------------------------------------
# Exception Handling
# ----------------------------------------------------------------------------------------


def get_ratio(x: int, y: int) -> float:
    """ration calculation"""
    try:
        ratio = x / y
    except ZeroDivisionError:
        print("cannot divide by zero")
        y = y + 1
        ratio = x / y
    return ratio


print(get_ratio(x=400, y=0))

# ----------------------------------------------------------------------------------------
# Ternary Operator
# ----------------------------------------------------------------------------------------

# conditional checks and assign values or execute expressions in a single line
for i in range(5):
    even_or_odd = "Even" if i % 2 == 0 else "Odd"
    print(even_or_odd)

n = 5
# nested if-else statements
res = "Positive" if n > 0 else "Negative" if n < 0 else "Zero"
print(res)

# (condition_is_false, condition_is_true)[condition]
res = ("Odd", "Even")[n % 2 == 0]
print(res)


# condition_dict = {True: value_if_true, False: value_if_false}
# Key is True or False based on the condition a > b.
# The corresponding value (a or b) is then selected.
a = 30
b = 40
m1 = {True: a, False: b}[a > b]
print(m1)

# ----------------------------------------------------------------------------------------
# Print parameters
# ----------------------------------------------------------------------------------------
a = ["english", "french", "spanish", "german", "twi"]

# String appended after the last value
print(*a, end=" ...")
print("\n")

# String appended after the last value
print(*a, sep=", ")

print("\n")

for language in a:
    print(language, end=" ")

print("\n")

for language in a:
    print(language, end=" | ")


# ----------------------------------------------------------------------------------------
# Slicing
# ----------------------------------------------------------------------------------------
# reverse a String
a = "Hello World!"
print(a[::-1])

# ----------------------------------------------------------------------------------------
# reverse a List
# ----------------------------------------------------------------------------------------
Lst = [60, 70, 30, 20, 90, 10, 50]
print(Lst[::-1])


# ----------------------------------------------------------------------------------------
# Lambda function - anonymous function
# ----------------------------------------------------------------------------------------

(lambda x, y: x**y)(5, 3)  # lambda arguments: expression


# can be assigned to a variable
def square(x):
    return x**2


square(5)


# lambda best used inside other fct anonymously
tuples = [(1, "d"), (2, "b"), (4, "a"), (3, "c")]
sorted(tuples, key=lambda x: x[1])  # sort by second value in the tuple


# ----------------------------------------------------------------------------------------
# time performance counter
# ----------------------------------------------------------------------------------------
# more accurate than time.time, for timing your code
start = time.perf_counter()
time.sleep(1)
end = time.perf_counter()
print(end - start)


# ----------------------------------------------------------------------------------------
# The Walrus Operator (:=) – Assign and Use in One Step
# ----------------------------------------------------------------------------------------

"""Introduced in **Python 3.8**, the **walrus operator (**:=**)** allows assignment inside expressions, making the code more concise. The `~` operator performs a bitwise inversion of integers, flipping their bits to the opposite value. The result can be explained by the formula:"""

# With the walrus operator
if (num := int(input("Enter a number: "))) > 10:
    print(f"Number {num} is greater than 10")

# Without the walrus operator
data = input("Enter a number: ")
if int(data) > 10:
    print(f"Number {data} is greater than 10")


# ----------------------------------------------------------------------------------------
# Dictionary.get() with Default Values
# ----------------------------------------------------------------------------------------

# Instead of checking if a key exists in a dictionary, ***.get()*** allows retrieving values with a fallback default. -> Prevents KeyError.
person = {"name": "Alice", "age": 25}
print(person.get("city", "Unknown"))  # Key 'city' doesn't exist


# Unpacking with \* in Function Calls and Loops
# Python allows **iterable unpacking** with ***\**** , making function calls and loops cleaner.
def greet(name, age):
    print(f"Hello, {name}. You are {age} years old.")


data = ("John", 30)
greet(*data)  # Unpacking tuple into function arguments

# ----------------------------------------------------------------------------------------
# Using zip() to Iterate Over Multiple Iterables
# ----------------------------------------------------------------------------------------
# zip() simplifies iterating over multiple lists at once.
names = ["Alice", "Bob", "Charlie"]
scores2 = [85, 90, 78]


for name, score in zip(names, scores2, strict=False):
    print(f"{name} scored {score}")

# ----------------------------------------------------------------------------------------
# Quick File Reading with Path().read\_text()
# ----------------------------------------------------------------------------------------

# Instead of ***open()***, use ***pathlib.Path*** for a cleaner file-reading approach.
from pathlib import Path

content = Path("README.md").read_text()
print(content)


# Swapping Variables Without a Temp Variable
# Python allows swapping variables in a single line.

a, b = 5, 10
a, b = b, a  # Swaps values without a temporary variable
print(a, b)


# Using Counter for Quick Frequency Counting
# collections.Counter is an efficient way to count occurrences in a list.
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
freq = Counter(words)
print(freq)


# ----------------------------------------------------------------------------------------
# any() and all() for Quick Checks
# ----------------------------------------------------------------------------------------

# Instead of writing loops for conditions, ***any()*** and ***all()*** make checking multiple conditions easier.

numbers = [3, 5, 7, 9]
print(any(num % 2 == 0 for num in numbers))  # Checks if at least one even number exists
print(all(num > 0 for num in numbers))  # Checks if all numbers are positive


# ----------------------------------------------------------------------------------------
# enumerate() for Index-Based Looping
# ----------------------------------------------------------------------------------------

# Instead of manually maintaining an index, ***enumerate()*** provides an automatic counter.

colors = ["red", "blue", "green"]
for index, color in enumerate(colors, start=1):
    print(f"{index}: {color}")
    print(f"{index}: {color}")
    print(f"{index}: {color}")
    print(f"{index}: {color}")
