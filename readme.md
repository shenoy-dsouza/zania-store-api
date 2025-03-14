# RESTful API for E-Commerce Platform

## Objective  
This project is a **take-home assignment** for an interview, requiring the development of a **RESTful API** for a simple e-commerce platform. The API enables users to view available products, add new products, and place orders. The solution includes exception handling, comprehensive test cases, and a Dockerized container for easy deployment.  

For detailed project requirements provided by the interviewer, refer to the document below:  
📝 **Interview Document**: [Google Doc](https://docs.google.com/document/d/1T7TtA2_1w3QgYrpgzpG7ftgsAyBG5flveUxlrBu0DY4/edit?tab=t.0)

## Features
- View available products
- Add new products
- Place orders with stock validation
- Order processing and inventory management
- Exception handling for errors like insufficient stock

## Technologies Used
- **Django Rest Framework (DRF)** for API development
- **MySQL** as the database
- **Docker & Docker Compose** for containerization
- **pytest** for testing

## Business Logic & Constraints
### Stock Management
- Validate stock levels when placing an order.
- Deduct stock if the order is successful.

### Order Validation
- Ensure sufficient stock is available before confirming an order.
- Return an appropriate error response if stock is insufficient.

## Setup & Installation
### Prerequisites
Ensure you have the following installed:
- **Docker** & **Docker Compose**
- **Python** (for running locally without Docker)

### Running the Project (With or Without Docker)
1. Clone the repository:
   ```sh
   git clone https://github.com/shenoy-dsouza/zania-store-api.git
   cd zania-store-api
   ```
2. Set up environment variables:
    - Create a `.env` file from `.env.example`:
    ```sh
    cp .env.example .env
    ```
    - Configure it as follows:
    ```sh
    DJANGO_SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=your_db_host
    DATABASE_PORT=your_db_port
    ```

## Environment Variables
Use a `.env` file to configure environment variables.

⚠️ **Do not include actual credentials in `.env.example`—it's for reference only.**

A `.env.example` file is included in the repository to guide configuration but should not contain real values.
Example `.env` file:
```sh
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=zania_store
DATABASE_USER=zania
DATABASE_PASSWORD=zania
DATABASE_HOST=localhost
DATABASE_PORT=3306
```






> **Note:** This file is for reference only. Do not include actual credentials here.

### Running the Project with Docker
1. Build and run the project using Docker:
   ```sh
    docker compose up --build -d
   ```
2. The API will be available at:
   ```sh
   http://localhost:8000
   ```

### Running the Project Locally (Without Docker)
1. Set up a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Apply database migrations:
    ```sh
    python manage.py migrate
    ```
4. Start the development server:
    ```sh
    python manage.py runserver
    ```
5. The API will be available at:
    ```sh
    http://127.0.0.1:8000
    ```

## API Endpoints
| Method | Endpoint      | Description                   |
|--------|--------------|-------------------------------|
| GET    | `/products/`  | Retrieve all products        |
| POST   | `/products/`  | Add a new product            |
| POST   | `/orders/`    | Place an order               |

## API Authentication  
This API does not include authentication mechanisms (such as token-based authentication or session management) because the requirements did not specify it. All endpoints are publicly accessible. If authentication is needed in a production environment, Django Rest Framework (DRF) provides various authentication options such as JWT (JSON Web Token).

## API Documentation
The API documentation is available at:

📝 **Swagger UI**: http://127.0.0.1:8000/apis/docs/

📝 **Raw OpenAPI YAML**: http://127.0.0.1:8000/apis/api_doc.openapi.yaml

Additionally, an `api_doc.yml` file is included in the `docs/` folder.

## Testing
To run tests inside the Docker container:
```sh
docker compose exec app pytest
```
