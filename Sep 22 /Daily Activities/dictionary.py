
#dictionary
student = {
    "name": "Alice",
    "age": 22,
    "Course": "AIML"
}
print(student["name"])
print(student.get("age"))

student["grade"] = "A"
student["age"] = 23
student.pop("course")
del student["grade"]
print(student)

for key,value in student.items():
    print(key,":", value)

# access nested data
employee = {
    "id" : "E102",
    "name" : "Priya",
    "department" : "finance",
    "skills" : ["Excel","Python", "PowerBI"]
}

print(employee["skills"][1])
