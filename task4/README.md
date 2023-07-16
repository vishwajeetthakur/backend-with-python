# Aggregation Pipeline

1. `$match`:
   This operator filters the data to pass only documents that match the specified condition(s) to the next pipeline stage.
   
   Example:

   ```javascript
   db.collection.aggregate([
     { $match: { 'age': { $gte: 18 } } }
   ])
   ```
   This example passes documents that have an `age` field with a value greater than or equal to `18`.

2. `$project`:
   This operator passes along the documents with the requested fields to the next stage in the pipeline. The specified fields can be existing fields from the input documents or newly computed fields.
   
   Example:
   ```javascript
   db.collection.aggregate([
     { $project: { 'name': 1, 'age': 1 } }
   ])
   ```
   This example passes documents with only the `name` and `age` fields.

3. `$limit`:
   This operator limits the number of documents passed to the next stage in the pipeline.
   
   Example:
   ```javascript
   db.collection.aggregate([
     { $limit: 5 }
   ])
   ```
   This example passes only the first `5` documents to the next stage.

4. `$sort`:
   This operator sorts the documents.
   
   Example:
   ```javascript
   db.collection.aggregate([
     { $sort: { 'age' : -1 } }
   ])
   ```
   This example sorts the documents in descending order based on the `age` field.

5. `$count`:
   This operator counts the number of documents in the pipeline and assigns this count to a specified field.
   
   Example:
   ```javascript
   db.collection.aggregate([
     { $count: "total" }
   ])
   ```
   This example counts the number of documents and assigns this count to a new field named `total`.

6. `$set` / `$addFields`:
   Both operators are the same and add new fields to documents. The operator stage outputs documents that contain both the existing fields from the input documents and the newly added fields. `$project` can also add new fields, but it includes only the fields specified in the projection, excluding all others.

   Example:
   ```javascript
   db.collection.aggregate([
     { $addFields: { 'totalAge': { $sum: "$age" } } }
   ])
   ```
   This example adds a new field `totalAge` which is the sum of the `age` field across documents.

7. `$push`:
   This operator appends a specified value to an array.
   
   Example:
   ```javascript
   db.collection.aggregate([
     {
       $group: {
         _id: "$category",
         items: { $push: "$item" }
       }
     }
   ])
   ```
   This example groups documents by the `category` field and for each assortment of grouped documents, it pushes the `item` field values into an array.

8. `$avg`:
   This operator calculates the average of specified values.

   Example:
   ```javascript
   db.collection.aggregate([
     {
       $group: {
         _id: "$category",
         averageAge: { $avg: "$age" }
       }
     }
   ])
   ```
   This example groups documents by the `category` field and then calculates and assigns the average `age` to the `averageAge` field for each group of documents.
   