
numbers = [10, 20, 30, 40, 50]
print(numbers[0])
print(numbers[-1])

fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
print(fruits)
fruits.insert(1, "mango")
print(fruits)

fruits.remove("banana")         #remove by value
fruits.pop()                    #remove last element


#Data manipulations
marks = [90, 75, 88, 100, 67]
print(len(marks))
print(max(marks))
print(min(marks))
print(sum(marks))
print(sum(marks)/len(marks))
