import string
import random

alphabet = list(string.ascii_lowercase)
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
letter_amount = random.randint(100, 1000)
number_amount = 1000 - letter_amount
length = random.randint(100, 200)

c1 = 0
c2 = 0
random_key = []

while c1 < letter_amount:
    random_key.append(random.choice(alphabet))
    c1 += 1

while c2 < number_amount:
    random_key.append(random.choice(nums))
    c2 += 1

key = random.sample(random_key, length)
open("key.txt").write("".join(str(e) for e in key))
