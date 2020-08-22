MAX_INT_16 = 32767          # 0x7fff
MIN_INT_16 = -32768         # 0x8000

# build number list
numberList = []
for i in range(MIN_INT_16, MAX_INT_16+1, 1):
    numberList.append(i)

# print number list
for i in range(0, len(numberList), 1000):
    print(f"values: {numberList[i]}")
print(f"values: {numberList[len(numberList)-1]}")

with open("out_python.raw", "wb") as file:
    for i in range(0, len(numberList)):
        value = numberList[i].to_bytes(2, byteorder="little", signed=True)
        file.write(value)
