# Quest Maker API

## User Service Endpoints Documentation

This document provides documentation for the user endpoints implemented in the User Service for the Quest Maker API.

### User Endpoints

#### `POST /`

Create new user instance.

- **Request:**
  - Body:
    - `email`: Email address of the user.
    - `firstName` (optional): First name of the user.
    - `lastName` (optional): Last name of the user.
    - `roleIds` (optional): List of role IDs assigned to the user.
    - `organizationId` (optional): List of organization IDs the user belongs to.
    - `userType` (default: 'regular'): Type of user.
    - `auth_id` (ObjectId): ObjectId for the related auth instance.

- **Response:**
  - Returns the ID of the newly created user instance.

- **Error Handling:**
  - Throws an HTTPException if there is an error creating the user in the User service.

#### `GET /`

Read user instance information.

- **Request:**
  - Headers:
    - `Authorization`: Bearer token.

- **Response:**
  - Returns user instance information for the authorized user.

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.

#### `PUT /`

Update user instance information.

- **Request:**
  - Headers:
    - `Authorization`: Bearer token.
  - Body:
    - `email`: New email address for the user.
    - `firstName` (optional): New first name for the user.
    - `lastName` (optional): New last name for the user.
    - `roleIds` (optional): New list of role IDs for the user.
    - `organizationId` (optional): New list of organization IDs for the user.

- **Response:**
  - Returns string `'Successfully updated'`.

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.


#### `POST /list/`

Fetches a list of users based on optional filters.

- **Request:**
    - Body:
        - `roleIds` (optional): List of role IDs assigned to the user.
        - `organizationId` (optional): List of organization IDs the user belongs to.

  - Headers: 
    - `Authorization`: Bearer token.

- **Response:**
    - `Status Code`: 200 OK
    - `Body`: List of UserResponse (Response body model for user details)

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.

#### `DELETE /`

Delete user instance.

- **Request:**
  - Headers:
    - `Authorization`: Bearer token.

- **Response:**
  Returns string `'Successfully deleted'` if the user instance is deleted.

- **Error Handling:**
  - Throws an HTTPException with status code 403 if the token lacks the necessary scope.

### Pydantic Models

The following Pydantic models are used for request and response data:

- `UserCreate`
- `UserUpdate`
- `UserResponse`
- `UserInDB`

---

# Cloning and Running the Web Server

Follow the instructions below to clone a GitHub repository, install the required dependencies using `pip install`, and run the web server using `uvicorn`.

## Prerequisites

Make sure you have the following installed on your system:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) (preferably Python 3.x)
- [pip](https://pip.pypa.io/) (Python package installer)

## Steps

1. **Clone the GitHub Repository:**

   Open a terminal or command prompt and run the following command to clone the GitHub repository:

   ```bash
   git clone https://github.com/akinolaemmanuel49/QuestMakerAPIUserService.git
   ```

2. **Navigate to the Project Directory:**

   Change your working directory to the cloned repository:

   ```bash
   cd QuestMakerAPIUserService
   ```

3. **Install Requirements:**

   Run the following command to install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   This command reads the dependencies listed in the `requirements.txt` file and installs them.

4. **Run the Web Server:**

   Once the requirements are installed, run the following command to start the web server using `uvicorn`:

   ```bash
   uvicorn main:app --port 8002 --reload
   ```

   - `main:app` specifies the location of the FastAPI app instance.
   - `--port 8002` sets the port number to 8002 (you can choose a different port if needed).
   - `--reload` enables automatic reloading of the server when code changes are detected (useful for development).

5. **Access the Web Server:**

   Open your web browser and go to [http://localhost:8002](http://localhost:8002) (or the port you specified) to access the running web server.

   The application should be up and running, and you can interact with the specified API endpoints.

6. **Use FastAPI builtin swagger docs:**

    Open your web browser and go to [http://localhost:8002/docs](http://localhost:8002/docs) (or the port you specified) to access the running documentation web app.

---

# Handling the .env File

To handle the provided `.env` file, follow these basic instructions:

1. **Create a MongoDB Cluster:**

   - Create a MongoDB cluster using the free tier on the [MongoDB Atlas](https://www.mongodb.com/atlas/database) platform.
   - Obtain the cluster connection string.

2. **Fill in Missing Values:**

   - Open the `.env` file in a text editor.
   - Fill in the missing values for the following variables:
     - `MONGODB_CLUSTER`: Replace it with the MongoDB cluster connection string.
     - `MONGODB_USERNAME`: Set your MongoDB username.
     - `MONGODB_PASSWORD`: Set your MongoDB password.
     - `JWT_SECRET_KEY`: Choose a secret value for JWT token signing.
     - Ensure other variables like `JWT_EXPIRATION_TIME_IN_MINUTES`, `JWT_REFRESH_EXPIRATION_TIME_IN_HOURS`, `JWT_ALGORITHM`, and `ENCRYPTION_SCHEMES` have appropriate values. You can use the provided values or customize them based on your requirements.

3. **Save and Rename:**

   - Save the changes to the `.env` file.
   - Rename the file from `.env` to just `.env`. Ensure there is no additional extension (e.g., `.txt`).

4. **Keep Secure:**

   - Ensure that the `.env` file is kept secure and not shared publicly. It contains sensitive information like passwords and secret keys.
