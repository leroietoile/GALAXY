a = {"a": [1], "b": [2]}
b = list(a["a"])
print(a)
b[0]= 4
print(a)
b[0] = 5
a["a"] = b[0]
print(a)
b[0] = 6
print(a)
