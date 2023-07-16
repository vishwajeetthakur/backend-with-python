# CRUD OPERATIONS

To create a database:
```
use mydatabase
```

Get all databases:
```
show dbs
```

To use a database:
```
use <DATABASE_NAME>
```

To create a collection in a database:
```
db.createCollection('<collection_name>')
```

To insert a document in a database:
```
db.collection_name.insertOne({ name: "Vishwa", age: 22 })
```

To insert multiple documents in a database:
```
db.collection_name.insertMany([{ name: "Vishwa", age: 22 }, { name: 'abc', age: 19 }])
```

To search for a document in a collection:
```
db.collection_name.findOne({ key: value })
```

To search for documents in a collection:
```
db.collection_name.find({ key: value })
```

To update a document:
```
db.collection_name.updateOne({ key: value }, { $set: { keyToUpdate: updatedValue } })
```

To update multiple documents:
```
db.collection_name.updateMany({ key: value }, { $set: { keyToUpdate: updatedValue } })
```

To delete a document:
```
db.collection_name.deleteOne({ key: value })
```

To delete multiple documents:
```
db.collection_name.deleteMany({ key: value })
```

## OPERATORS

### 1. Comparison Operators

- `$eq`: Equal to
  - Usage: `db.collection_name.find({ age: { $eq: 25 } })`

- `$gt`: Greater than
  - Usage: `db.collection_name.find({ age: { $gt: 30 } })`

- `$lt`: Less than
  - Usage: `db.collectionName.find({ age: { $lt: 30 } })`

- `$lte`: Less than or equal
  - Usage: `db.collectionName.find({ age: { $lte: 30 } })`

- `$ne`: Not equal to
  - Usage: `db.collectionName.find({ status: { $ne: "completed" } })`

- `$gt` and `$lt` combined: Within a specified range
  - Usage: `db.collectionName.find({ age: { $gt: 20, $lt: 30 } })`

- `$regex`: Matches values based on a regular expression pattern
  - Usage: `db.collectionName.find({ name: { $regex: /^Joh/ } })`
  - find documents where the "name" field starts with "Joh" using a regular expression

### 2. Logical Operators

- `$and`: Joins query clauses with a logical AND. All conditions must be met
  - Usage: `db.collection_name.find({ $and: [{ age: 25 }, { city: "New Delhi" }] })`

- `$or`: Joins query clauses with a logical OR. Anyone should hold true.
  - Usage: `db.collection_name.find({ $or: [{ age: 25 }, { city: "New York" }] })`

- `$nor`: Joins query clauses with a logical NOR.
  - Usage: `db.collectionName.find({ $nor: [{ age: 25 }, { city: "New York" }] })`
  - find documents where neither the "age" field is equal to 25 nor the "city" field is "New York".

- `$not`: Inverts the effect of a query expression.
  - Usage: `db.collectionName.find({ age: { $not: { $gt: 30 } } })`
  - where the "age" field is not greater than 30

- `$exists` with `$not`: Matches documents that do not have the specified field.
  - Usage: `db.collectionName.find({ age: { $exists: false } })`
  - documents that do not have the "age" field

- `$in` with `$nin`: Matches values that are not in the specified array
  - Usage: `db.collectionName.find({ color: { $nin: ["red", "blue"] } })`
  - documents where the "color" field is neither "red" nor "blue"

- `$and` with `$or`: Combines logical AND and OR operators.
  - Usage: `db.collectionName.find({ $and: [{ category: "electronics" }, { $or: [{ price: { $gt: 500 } }, { brand: "Apple" }] }] })`
  - documents where the "category" field is "electronics" and either the "price" field is greater than 500 or the "brand" field is "Apple"

### 3. Array Operators

- `$in`: Matches any of the values specified in an array
  - Usage: `db.collection_name.find({ color: { $in: ["red", "blue"] } })`

- `$all`: Matches arrays that contain all the specified elements
  - Usage: `db.collection_name.find({ tags: { $all: ["mongodb", "database"] } })`
  - find documents where the "tags" field contains both "mongodb" and "database" elements

- `$elemMatch`: Matches documents that contain an array field with at least one element matching the specified query
  - Usage: `db.collectionName.find({ scores: { $elemMatch: { $gt: 80, $lt: 90 } } })`
  - documents where the "scores" array field contains at least one element that is greater than 80 and less than 90

- `$size`: Matches documents where the size of the array field is equal to the specified value.
  - Usage: `db.collectionName.find({ tags: { $size: 3 } })`
  - documents where the "tags" array field contains exactly 3 elements

- `$pull`: Removes all occurrences of a specified value from an array field.
  - Usage: `db.collectionName.updateOne({ _id: ObjectId("...") }, { $pull: { colors: "red" } })`
  - document by removing all occurrences of the value "red" from the "colors" array field

### 4. Element Operators

- `$exists`: Matches documents that have the specified field
  - Usage: `db.collection_name.find({ age: { $exists: true } })`
  - documents that have the "age" field

- `$type`: Matches documents where the value of a field is of a specified BSON type
  - Usage: `db.collection_name.find({ age: { $type: "number" } })`
  - find documents where the "age" field is of type number

- `$regex`: Matches values based on a regular expression pattern.
  - Usage: `db.collectionName.find({ name: { $regex: /^Joh/ } })`
  - documents where the "name" field starts with "Joh" using a regular expression

- `$text`: Performs a full-text search on a text index
  - Usage: `db.collectionName.find({ $text: { $search: "coffee" } })`
  - documents where the text index includes the word "coffee"

- `$mod`: Performs a modulo operation on the value of a field
  - Usage: `db.collectionName.find({ count: { $mod: [5, 0] } })`
  - documents where the "count" field is divisible evenly by 5

