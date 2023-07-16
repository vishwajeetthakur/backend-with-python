# Task 6 -- Hands On Aggregation

Task is to complete the same in groups (in your teams)

Load Atlas Sample Dataset - [https://www.mongodb.com/docs/atlas/sample-data/#load-sample-data-1](https://www.mongodb.com/docs/atlas/sample-data/#load-sample-data-1)

Build the following queries -

1. In db `sample_mflix`, collection `movies`, find the unique countries.

   ```javascript
   db.movies.aggregate([
     { $unwind: '$countries' },
     { $group: { '_id': null, unique_countries: { $addToSet: '$countries' } } }
   ])
   ```

2. In db `sample_mflix`, collection `movies`, find the unique genres for country France.

   ```javascript
   db.movies.aggregate([
     { $unwind: '$countries' },
     { $match: { countries: 'France' } },
     { $unwind: '$genres' },
     { $group: { '_id': null, unique_genres: { $addToSet: '$genres' } } }
   ])
   ```

3. In db `sample_mflix`, collection `movies`, find all movies having IMDb rating more than 7 and Tomato critic rating more than 8 with at least 50 reviews.

   ```javascript
   db.movies.aggregate([
     {
       $match: {
         'imdb.rating': { $gt: 7 },
         'tomatoes.critic.rating': { $gt: 8 },
         'tomatoes.critic.numReviews': { $gte: 50 }
       }
     }
   ])
   ```

4. In db `sample_mflix`, collection `movies`, find the decade (1960, 1970, 1980, etc...) in which the most movies were released.

   ```javascript
   db.movies.aggregate([
     {
       $bucket: {
         groupBy: '$year',
         boundaries: [1960, 1970, 1980, 1990, 2000, 2010],
         default: "other",
         output: { "count": { $sum: 1 } }
       }
     }
   ])
   ```

5. In db `sample_mflix`, collections `movies` and `comments`, find the name/title of the movie having the most comments.

   ```javascript
   db.comments.aggregate([
     { $group: { '_id': '$movie_id', count: { $sum: 1 } } },
     { $sort: { 'count': -1 } },
     { $limit: 1 },
     {
       $lookup: {
         from: 'movies',
         localField: '_id',
         foreignField: '_id',
         as: 'movie_info'
       }
     },
     { $project: { "Movie_name": "$movie_info.title" } }
   ])
   ```

6. In db `sample_airbnb`, collection `listingsAndReviews`, find the average price of all properties in Porto market (`address.market`).

   ```javascript
   db.listingsAndReviews.aggregate([
     { $match: { 'address.market': 'Porto' } },
     { $group: { '_id': null, Average: { $avg: '$price' } } }
   ])
   ```

7. In db `sample_airbnb`, collection `listingsAndReviews`, find the number of properties within a 10km range of the coordinates [-8.61308, 41.1413].

   ```javascript
   db.listingsAndReviews.createIndex({ "address.location": "2dsphere" })
   db.listingsAndReviews.aggregate([
     {
       $geoNear: {
         near: { type: "Point", coordinates: [-8.61308, 41.1413] },
         distanceField: "dist.calculated",
         maxDistance: 10000,
         spherical: true
       }
     },
     { $count: "properties_in_range" }
   ])
   ```

8. In db `sample_restaurants`, collection `restaurants`, find the top 5 restaurants with the highest average grade score (`grades.score`).

   ```javascript
   db.restaurants.aggregate([
     { $unwind: '$grades' },
     { $group: { '_id': '$_id', 'name': { $first: '$name' }, 'average': { $avg: '$grades.score' } } },
     { $sort: { 'average': -1 } },
     { $limit: 5 }
   ])
   ```
