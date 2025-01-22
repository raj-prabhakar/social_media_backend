# Social Media Backend

A Django REST Framework-based backend for a social media platform. This project provides a robust API for managing user relationships, posts, feeds, and user authentication using JWT tokens.

## Features

- Custom User Authentication
- JWT Authentication with Simple JWT
- Post Management
- User Relationships
- News Feed
- PostgreSQL Database Integration

## Prerequisites

- Python 3.x
- PostgreSQL
- pip

## Installation

1. Clone the repository:
    ```bash
    git clone [repository-url]
    cd social-media-backend
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root and add your database configuration:
    ```
    DATABASE_URL=postgres://username:password@localhost:5432/dbname
    ```

5. Run migrations:
    ```bash
    python manage.py migrate
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Project Structure

The project consists of several Django apps:

- `accounts` - Custom user model and authentication
- `posts` - Post creation and management
- `relationships` - User relationships and interactions
- `feed` - News feed generation and management

## API Authentication

The API uses JWT (JSON Web Token) authentication. The following configurations are set:

- Access Token Lifetime: 60 minutes
- Refresh Token Lifetime: 1 day
- Authentication Header: Bearer

## Database

The project uses PostgreSQL as its database. The connection is configured using environment variables through the `DATABASE_URL`.

## API Endpoints

The API endpoints are organized around the following resources:
- User Authentication
- Posts
- User Relationships
- Feed

Here is the link of the Postman Collection of complete APIs : https://solar-meadow-67595.postman.co/workspace/My-Workspace~3d2d1f70-73a4-4b31-8879-e51f5db12257/collection/31250549-dc86d4c1-998b-437d-ab17-601568b4dc74?action=share&creator=31250549
