
method1 = []
method2 = []

with open("out.raw", "rb") as file:
    byteValue = file.read(2)

    while byteValue != b"":
        intValueOne = int.from_bytes(byteValue, "big", signed=True)
        intValueTwo = int.from_bytes(byteValue, "little", signed=True)

        method1.append(intValueOne)
        method2.append(intValueTwo)

        byteValue = file.read(2)

for i in range(0, len(method1), 1000):
    print(f"method1: {method1[i]}")
print(f"method1: {method1[len(method1)-1]}")
print("\n")

for i in range(0, len(method2), 1000):
    print(f"method2: {method2[i]}")
print(f"method2: {method2[len(method2)-1]}")
