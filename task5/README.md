## MongoDB Aggregate Pipeline Stages

### $group

The `$group` stage groups documents by a specified expression and applies aggregate functions to them. It allows you to perform operations like counting, summing, averaging, and more on grouped data.

Example:

```javascript
db.sales.aggregate([
  {
    $group: {
      _id: "$category",
      totalRevenue: { $sum: "$amount" },
      averageQuantity: { $avg: "$quantity" }
    }
  }
])
```

This example groups sales documents by their category, calculates the total revenue for each category using `$sum`, and calculates the average quantity using `$avg`.

Additional Use Case:
- Grouping and calculating statistics on customer orders by date or product category.
- Grouping and summarizing website traffic data by country or device type.

### $lookup

The `$lookup` stage performs a left outer join between two collections in the same database to combine data from multiple collections into a single result set. It matches documents from the "local" collection with documents from the "foreign" collection based on specified conditions.

Example:

```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "products",
      localField: "productId",
      foreignField: "_id",
      as: "product"
    }
  }
])
```

This example joins the "orders" collection with the "products" collection based on the "productId" field, and adds the matching product documents as an array to each order document using the "as" field.

Additional Use Case:
- Combining user data from a "users" collection with their related comments from a "comments" collection.
- Enriching log data with additional information from a separate "metadata" collection.

### $unwind

The `$unwind` stage deconstructs an array field from the input documents, creating a separate document for each element of the array. It allows you to perform operations on individual array elements.

Example:

```javascript
db.books.aggregate([
  { $unwind: "$authors" },
  { $project: { title: 1, author: "$authors" } }
])
```

This example unwinds the "authors" array field in the "books" collection, creating a separate document for each author. Then, it projects the "title" and "author" fields.

Additional Use Case:
- Analyzing survey data with multiple choices, where each choice is stored as an array element.
- Exploring event data with multiple participants, where each participant is stored as an array element.

### $bucket

The `$bucket` stage groups documents into "buckets" based on a specified expression and user-defined boundaries. It allows you to categorize documents into discrete groups.

Example:

```javascript
db.scores.aggregate([
  {
    $bucket: {
      groupBy: "$score",
      boundaries: [0, 60, 70, 80, 90, 100],
      default: "Other",
      output: {
        count: { $sum: 1 }
      }
    }
  }
])
```

This example buckets student scores into predefined ranges and counts the number of scores in each bucket.

Additional Use Case:
- Segmenting customer data based on purchase amounts into different spending tiers.
- Grouping website traffic data into time-based intervals for analysis.

### $bucketAuto

The `$bucketAuto` stage automatically determines the bucket boundaries based on the distribution of values in a specified field. It creates buckets of approximately equal document counts.

Example:

```javascript
db.products.aggregate([
  {
    $bucketAuto: {
      groupBy: "$price",
      buckets: 5,
      output: {
        count: { $sum: 1 }
      }
    }
  }
])
```

This example automatically creates five buckets based on the distribution of product prices and counts the number of products in each bucket.

Additional Use Case:
- Analyzing population distribution based on age ranges, where the bucket boundaries are determined automatically.
- Grouping data based on dynamically changing ranges, such as temperature ranges in weather data.

### $facets

The `$facets` stage enables multiple aggregations to be computed within a single aggregation pipeline. It allows you to compute multiple sets of aggregations on the same dataset efficiently.

Example:

```javascript
db.sales.aggregate([
  {
    $facet: {
      totalRevenue: [{ $group: { _id: null, total: { $sum: "$amount" } } }],
      avgQuantity: [{ $group: { _id: null, average: { $avg: "$quantity" } } }]
    }
  }
])
```

This example computes the total revenue and average quantity as separate aggregations using the `$facet` stage.

Additional Use Case:
- Analyzing e-commerce data by computing multiple metrics such as total sales, average order value, and most popular products within a single pipeline.

---