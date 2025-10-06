Commands 
db
test
use university
switched to db university
// Insert one student
db.students.insertOne({})
{
 acknowledged: true,
 insertedId: ObjectId('68dfa4158d71a6b54bff222d')
}
db.students.insertOne({
  student_id: 1,
  name: "Rahul",
  age: 21,
  city: "Mumbai",
  course: "AI",
  marks: 85
})
{
 acknowledged: true,
 insertedId: ObjectId('68dfa4e78d71a6b54bff222e')
}
db.students.insertMany(
  { student_id: 2, name: "Priya", age: 22, city: "Delhi", course: "ML", marks: 90},
  { student_id: 3, name: "Arjun", age: 20, city: "Bengaluru", course: "Data science", marks: 78},
  { student_id: 4, name: "Neha", age: 23, city: "Hyderabad", course: "AI", marks: 88},
  { student_id: 5, name: "Vikram", age: 22, city: "Chennai", course: "ML", marks: 95}
)
MongoInvalidArgumentError: Argument "docs" must be an array of documents
db.students.insertMany([
  { student_id: 2, name: "Priya", age: 22, city: "Delhi", course: "ML", marks: 90},
  { student_id: 3, name: "Arjun", age: 20, city: "Bengaluru", course: "Data science", marks: 78},
  { student_id: 4, name: "Neha", age: 23, city: "Hyderabad", course: "AI", marks: 88},
  { student_id: 5, name: "Vikram", age: 22, city: "Chennai", course: "ML", marks: 95}
])

{
 acknowledged: true,
 insertedIds: {
   '0': ObjectId('68dfa8928d71a6b54bff222f'),
   '1': ObjectId('68dfa8928d71a6b54bff2230'),
   '2': ObjectId('68dfa8928d71a6b54bff2231'),
   '3': ObjectId('68dfa8928d71a6b54bff2232')
 }
}
db.students.find()
{
 _id: ObjectId('68dfa4158d71a6b54bff222d')
}
{
 _id: ObjectId('68dfa4e78d71a6b54bff222e'),
 student_id: 1,
 name: 'Rahul',
 age: 21,
 city: 'Mumbai',
 course: 'AI',
 marks: 85
}
{
 _id: ObjectId('68dfa8928d71a6b54bff222f'),
 student_id: 2,
 name: 'Priya',
 age: 22,
 city: 'Delhi',
 course: 'ML',
 marks: 90
}
{
 _id: ObjectId('68dfa8928d71a6b54bff2230'),
 student_id: 3,
 name: 'Arjun',
 age: 20,
 city: 'Bengaluru',
 course: 'Data science',
 marks: 78
}
{
 _id: ObjectId('68dfa8928d71a6b54bff2231'),
 student_id: 4,
 name: 'Neha',
 age: 23,
 city: 'Hyderabad',
 course: 'AI',
 marks: 88
}
{
 _id: ObjectId('68dfa8928d71a6b54bff2232'),
 student_id: 5,
 name: 'Vikram',
 age: 22,
 city: 'Chennai',
 course: 'ML',
 marks: 95
}
db.students.findOne({name:"Rahul"})
{
 _id: ObjectId('68dfa4e78d71a6b54bff222e'),
 student_id: 1,
 name: 'Rahul',
 age: 21,
 city: 'Mumbai',
 course: 'AI',
 marks: 85
}
db.students.find({marks:{$gt: 85}})
{
 _id: ObjectId('68dfa8928d71a6b54bff222f'),
 student_id: 2,
 name: 'Priya',
 age: 22,
 city: 'Delhi',
 course: 'ML',
 marks: 90
}
{
 _id: ObjectId('68dfa8928d71a6b54bff2231'),
 student_id: 4,
 name: 'Neha',
 age: 23,
 city: 'Hyderabad',
 course: 'AI',
 marks: 88
}
{
 _id: ObjectId('68dfa8928d71a6b54bff2232'),
 student_id: 5,
 name: 'Vikram',
 age: 22,
 city: 'Chennai',
 course: 'ML',
 marks: 95
}
db.students.find({},{name: 1,course: 1, _id: 0})
{}
{
 name: 'Rahul',
 course: 'AI'
}
{
 name: 'Priya',
 course: 'ML'
}
{
 name: 'Arjun',
 course: 'Data science'
}
{
 name: 'Neha',
 course: 'AI'
}
{
 name: 'Vikram',
 course: 'ML'
}
db.students.updateOne({name: "Neha"}, {$set: {marks: 92, course: "Advanced AI"}})
{
 acknowledged: true,
 insertedId: null,
 matchedCount: 1,
 modifiedCount: 1,
 upsertedCount: 0
}
db.students.updateOne({name: "Neha"}, {$set: {marks: 92, course: "Advanced AI"}})
{
 acknowledged: true,
 insertedId: null,
 matchedCount: 1,
 modifiedCount: 0,
 upsertedCount: 0
}
db.students.updateMany({course: "AI"},{$set: {grade: "A"}})

{
 acknowledged: true,
 insertedId: null,
 matchedCount: 1,
 modifiedCount: 1,
 upsertedCount: 0
}
db.students.deleteOne({ name: "Arjun" })
{
 acknowledged: true,
 deletedCount: 1
}
db.students.deleteMany({ marks: {$lt: 80 }})

