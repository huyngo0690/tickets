# My FastAPI Project

This project is built using FastAPI and includes functionality to handle user authentication, ticket management, and more. It uses Alembic for database migrations and Docker for easy deployment and environment management.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose

### Running the Application

To run the application, simply execute the `setup.sh` script in root folder. This script sets up your environment, including the necessary Docker env, and starts the FastAPI server.

Run the following command in the root directory of the project:

```bash
./setup.sh

### Notes:

- **No UI**: This project I did not finish UI, only APIs.
- **Other note**: I am using alembic for model migration. If you want to run locally for debug, You should change MySQL host to your localhost or MYSQL server in application/core/settings.py.
