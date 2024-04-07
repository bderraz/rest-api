# tvshow_backend


## Poetry

This project uses poetry. It's a modern dependency management
tool.


To set up the project use this set of command:

```bash
bash install.sh
```

To run the project use this set of commands:

```bash
bash run.sh
```
This will start the server on the configured host.

##Important

You can **interact** with the api and find the swagger documentation at `/api/docs`. 
With the configured host, the link will be: http://127.0.0.1:8000/api/docs

From there, you can engage with all available endpoints. The database, it is pre-filled with 10 entries.

You can read more about poetry here: https://python-poetry.org/

## Project structure

```bash
$ tree "tvshow_backend"
tvshow_backend
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```


## Running tests

For running tests on your local machine, simpley run:

1. Run the pytest.
```bash
pytest -vv .
```

## Documentation

Documentation for TV Show Backend

This project is a RESTful API for managing a collection of TV shows. It's built using the FastAPI framework and uses an embedded database for data persistence.

### Endpoints

#### Create a new TV show

- **Method:** POST
- **Endpoint:** `/create`
- **Description:**
  - Accepts a JSON body with the details of the TV show to be created.
  - Uses the TvShowInputDTO schema for input validation.
  - Returns a 201 status code on successful creation.

#### Retrieve all TV shows

- **Method:** GET
- **Endpoint:** `/all`
- **Description:**
  - Returns a list of all TV shows in the database.
  - Uses pagination with limit and offset query parameters.
  - Returns a 200 status code on success.

#### Retrieve a single TV show by its ID

- **Method:** GET
- **Endpoint:** `/detail/{show_id}`
- **Description:**
  - Returns the details of a single TV show.
  - Returns a 404 status code if the TV show is not found.

#### Search TV show by genre

- **Method:** GET
- **Endpoint:** `/search/{genre}`
- **Description:**
  - Returns a list of TV shows that match the specified genre.
  - Returns a 200 status code on success.

#### Update an existing TV show

- **Method:** PUT
- **Endpoint:** `/update/{show_id}`
- **Description:**
  - Accepts a JSON body with the details to be updated.
  - Returns a 200 status code on successful update.
  - Returns a 404 status code if the TV show is not found.

#### Delete a TV show by its ID

- **Method:** DELETE
- **Endpoint:** `/delete/{show_id}`
- **Description:**
  - Deletes the TV show with the specified ID.
  - Returns a 204 status code on successful deletion.
  - Returns a 404 status code if the TV show is not found.

### Improvements for Real-World Scenarios

- **Authentication and Authorization:**
  - Implement authentication and authorization to ensure only authorized users can perform operations, i.e. using a CSRF or JWT token.
- **Error Handling:**
  - Implement robust error handling for better client feedback.
- **Database:**
  - Consider using a more robust database solution for scalability, such as PostgreSQL or MySQL.
- **Testing:**
  - Include comprehensive testing, covering integration, end-to-end, and unit tests.
- **Caching:**
  - Implement caching to improve performance, especially for retrieval and search operations.
- **Rate Limiting:**
  - Implement rate limiting to protect against abuse.
- **Deployment:**
  - Implement a proper deployment strategy, possibly involving Docker, CI/CD, and a cloud provider.
- **Input Validation:**
  - Enhance validation to prevent attacks like SQL injection.
- **Direct ID Interaction:**
  - Implement safeguards against direct ID interaction to mitigate security vulnerabilities, in other words, use UUIDs instead of sequential IDs.
- **Logging:**
  - Implement thorough logging for monitoring and debugging purposes.