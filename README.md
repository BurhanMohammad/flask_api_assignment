
# Flask API with MongoDB

This is a Flask API that interacts with a MongoDB database to perform CRUD operations on user templates. The API is secured using JWT access tokens to ensure that each user can only access their own resources.

## Requirements

- Python 3.x
- Flask
- Flask-JWT-Extended
- pymongo


## Postman test apis link

[APi's links](https://api.postman.com/collections/28546968-4e2b8880-d940-43e4-a04c-cbf7f32844f6?access_key=PMAT-01H5EKKPEP49Y803WNX4WEBXYK)


## Testing with Postman

To test the API using Postman:

- Start the API server as mentioned in the "Usage" section.

- Open Postman.
- Import the provided Postman collection file (flask-api-mongodb.postman_collection.json) into Postman.
- Configure the necessary environment variables in Postman, such as base_url, access_token, etc.
-Send requests to the API endpoints using the provided collection.

## Conclusion

This Flask API provides endpoints to register users, authenticate them, and perform CRUD operations on user templates. It integrates with a MongoDB database and utilizes JWT access tokens for authentication and authorization.
