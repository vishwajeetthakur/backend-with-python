
# FastAPI Application Setup

To run the FastAPI application, follow the steps below:

1. Create a virtual environment and activate it.
2. Install the `fastapi` package using `pip`:
   ```
   pip install fastapi
   ```
3. Install the `uvicorn` package along with the `standard` extras using `pip`:
   ```
   pip install "uvicorn[standard]"
   ```
4. Run the application using `uvicorn`:
   ```
   uvicorn main:app --reload
   ```

## Additional Information

1. To see the application running, visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)
2. To access the inbuilt OpenAPI documentation, visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. To access the new version of the inbuilt OpenAPI documentation, visit: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Please note that the application runs on `http://127.0.0.1:8000` by default, and the documentation URLs provide access to the API documentation and interactive documentation interface.