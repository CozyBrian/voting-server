# API Documentation for Flask Application

This API provides endpoints to manage users, roles, candidates, and voting for an election system. It also includes features for sending and confirming OTPs (One-Time Passwords) for user verification.

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
   - [1. Get All Users](#get-all-users)
   - [2. Enroll User](#enroll-user)
   - [3. Find User by Phone Number](#find-user-by-phone-number)
   - [4. Send OTP](#send-otp)
   - [5. Confirm OTP](#confirm-otp)
   - [6. Initialize Database and Populate](#initialize-database-and-populate)
   - [7. Get All Roles](#get-all-roles)
   - [8. Get Role by ID](#get-role-by-id)
   - [9. Create Role](#create-role)
   - [10. Create Dummy Roles](#create-dummy-roles)
   - [11. Get Candidates for a Role](#get-candidates-for-a-role)
   - [12. Create Candidate for a Role](#create-candidate-for-a-role)
   - [13. Create Dummy Candidates](#create-dummy-candidates)
   - [14. Check if User has Voted for Role](#check-if-user-has-voted-for-role)
   - [15. Vote for a Candidate](#vote-for-a-candidate)
   - [16. Get Results for a Role](#get-results-for-a-role)

## Introduction <a name="introduction"></a>

This API is designed for an election system where users can be enrolled, roles can be created, candidates can be added for those roles, and users can vote for their preferred candidates. It also provides functionality to send and confirm OTPs for user verification.

## Authentication <a name="authentication"></a>

This API does not require authentication. However, you should ensure that the endpoints are secured in a production environment to prevent unauthorized access.

## Endpoints <a name="endpoints"></a>

### 1. Get All Users <a name="get-all-users"></a>

- **URL:** `/`
- **Method:** `GET`
- **Description:** Retrieve a list of all registered users.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    [
      {
        "username": "John Doe",
        "dob": "1990-01-01",
        "gender": "Male",
        "number": "+1234567890",
        "classOfUser": "Student"
      },
      // More user objects...
    ]
    ```

### 2. Enroll User <a name="enroll-user"></a>

- **URL:** `/enroll_user`
- **Method:** `POST`
- **Description:** Enroll a new user with the provided user details.
- **Request Body:**
  ```json
  {
    "username": "John Doe",
    "dob": "1990-01-01",
    "gender": "Male",
    "number": "+1234567890",
    "classOfUser": "Student"
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "John Doe": "added"
    }
    ```

### 3. Find User by Phone Number <a name="find-user-by-phone-number"></a>

- **URL:** `/find_user`
- **Method:** `POST`
- **Description:** Find a user by their phone number.
- **Request Body:**
  ```json
  {
    "number": "+1234567890"
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "username": "John Doe",
      "dob": "1990-01-01",
      "gender": "Male",
      "number": "+1234567890",
      "classOfUser": "Student"
    }
    ```

### 4. Send OTP <a name="send-otp"></a>

- **URL:** `/send_otp`
- **Method:** `POST`
- **Description:** Send an OTP (One-Time Password) to the user's phone number for verification.
- **Request Body:**
  ```json
  {
    "number": "+1234567890"
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "message": "OTP has been sent"
    }
    ```

### 5. Confirm OTP <a name="confirm-otp"></a>

- **URL:** `/confirm_otp`
- **Method:** `POST`
- **Description:** Confirm the OTP (One-Time Password) sent to the user's phone number for verification.
- **Request Body:**
  ```json
  {
    "number": "+1234567890",
    "otp": "123456"
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:** If OTP is valid
    ```json
    {
      "username": "John Doe",
      "dob": "1990-01-01",
      "gender": "Male",
      "number": "+1234567890",
      "classOfUser": "Student"
    }
    ```
  - If OTP is invalid
    ```json
    {
      "error": "Invalid OTP"
    }
    ```

### 6. Initialize Database and Populate <a name="initialize-database-and-populate"></a>

- **URL:** `/init_setup`
- **Method:** `GET`
- **Description:** Create database tables and populate initial data (roles and candidates).
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "message": "Success"
    }
    ```

### 7. Get All Roles <a name="get-all-roles"></a>

- **URL:** `/roles`
- **Method:** `GET`
- **Description:** Retrieve a list of all available roles.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    [
      {
        "id": 1,
        "role": "President"
      },
      // More role objects...
    ]
    ```

### 8. Get Role by ID <a name="get-role-by-id"></a>

- **URL:** `/role`
- **Method:** `GET`
- **Description:** Retrieve a role by its ID.
- **Query Parameters:**
  - `role_id` (integer) - The ID of the role to retrieve.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "id": 1,
      "role": "President"
    }
    ```

### 9. Create Role <a name="create-role"></a>

- **URL:** `/create_role`
- **Method:** `POST`
- **Description:** Create

 a new role.
- **Request Body:**
  ```json
  {
    "role": "Treasurer"
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "message": "Role added"
    }
    ```

### 10. Create Dummy Roles <a name="create-dummy-roles"></a>

- **URL:** `/create_dummy_roles`
- **Method:** `POST`
- **Description:** Create default roles for testing or initialization purposes.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "message": "Roles added"
    }
    ```

### 11. Get Candidates for a Role <a name="get-candidates-for-a-role"></a>

- **URL:** `/candidates`
- **Method:** `GET`
- **Description:** Retrieve a list of candidates for a specific role.
- **Query Parameters:**
  - `role_id` (integer) - The ID of the role for which to retrieve candidates.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    [
      {
        "id": 1,
        "role_id": 1,
        "candidate": "Candidate 1"
      },
      // More candidate objects...
    ]
    ```

### 12. Create Candidate for a Role <a name="create-candidate-for-a-role"></a>

- **URL:** `/create_candidate`
- **Method:** `POST`
- **Description:** Create a new candidate for a specific role.
- **Request Body:**
  ```json
  {
    "role_id": 1,
    "candidate": "Candidate 2"
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "message": "Candidate added"
    }
    ```

### 13. Create Dummy Candidates <a name="create-dummy-candidates"></a>

- **URL:** `/create_dummy_candidates`
- **Method:** `POST`
- **Description:** Create default candidates for testing or initialization purposes.
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "message": "Candidates added"
    }
    ```

### 14. Check if User has Voted for Role <a name="check-if-user-has-voted-for-role"></a>

- **URL:** `/has_user_voted`
- **Method:** `POST`
- **Description:** Check if a user has already voted for a specific role.
- **Request Body:**
  ```json
  {
    "number": "+1234567890",
    "role_id": 1
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "status": true
    }
    ```
    or
    ```json
    {
      "status": false
    }
    ```

### 15. Vote for a Candidate <a name="vote-for-a-candidate"></a>

- **URL:** `/vote`
- **Method:** `POST`
- **Description:** Allow a user to vote for a candidate in a specific role.
- **Request Body:**
  ```json
  {
    "number": "+1234567890",
    "role_id": 1,
    "candidate_id": 1
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "message": "Vote added"
    }
    ```

### 16. Get Results for a Role <a name="get-results-for-a-role"></a>

- **URL:** `/results`
- **Method:** `POST`
- **Description:** Retrieve the election results for a specific role, including candidate names and vote counts.
- **Request Body:**
  ```json
  {
    "role_id": 1
  }
  ```
- **Response:**
  - **Status Code:** 200 OK
  - **Body:**
    ```json
    {
      "role": "President",
      "candidates": ["Candidate 1", "Candidate 2"],
      "votes": [50, 30]
    }
    ```
    - `role` (string): The name of the role.
    - `candidates` (array of strings): Names of candidates.
    - `votes` (array of integers): Vote counts for each candidate.

This concludes the API documentation for the Flask application. You can use these endpoints to manage users, roles, candidates, and the voting process for your election system.