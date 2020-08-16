# This test shows that slicing an array does not modify original array
# fixed with util.CopySliceBack() method

test = [0] * 10
test2 = test[5:]

print (test)
print (test2)

for i in range(0, 5):
    test2[i] = i+1

print (test)
print (test2)
