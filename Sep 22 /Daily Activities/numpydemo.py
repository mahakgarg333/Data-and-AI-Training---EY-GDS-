import numpy as np
#1d array
arr1 = np.array([1,2,3,4,5])
arr2 = np.array([[1,2,3],[4,5,6]])
print(arr1)
print(arr2)


marks = np.array([10,20,30,40,50])
print(marks.max())
print(marks.min())
print(marks.mean())

data = np.array([10,20,30,40,50])
print("First 3 elements:", data[:3])
print("Reversed:", data[::-1])
print("Sum:", np.sum(data))
print("Standard deviation:", np.std(data))

