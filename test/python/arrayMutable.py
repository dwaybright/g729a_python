# Shows that array elements are mutable in methods called

def mod(array):
    array[3] = 4

test = [0] * 10
mod(test)

print(test)
