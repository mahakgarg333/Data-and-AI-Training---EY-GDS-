import json

#Python dictionary
student = {
    "name": "Rahul",
    "age": 21,
    "courses": ["AI", "ML"],
    "marks": {"AI":85, "ML":90}
}
#write to a json file
with open("student.json", "w") as f:
    json.dump(student, f, indent=4)

with open("student.json", "r") as f:
    student = json.load(f)

print(student)
