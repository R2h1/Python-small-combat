import itertools as itr
import time

start = time.time()
print(start)
words = "qwertyuiopasdfghjklzxcvbnm0123456789"


password_list = itr.product(words,repeat=3)

for password in password_list:
    print("".join(password))

    
end = time.time()
cost_time=end-start


print(cost_time)
