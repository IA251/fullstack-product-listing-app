# Product Listing App

## Overview

This project is a small product catalog application built with a containerized frontend and backend. The backend fetches real product data from an external service, normalizes it, and exposes a clean API. The frontend consumes that API and displays search results, pagination, and product galleries in a responsive table.

## Key Features

- Paginated product listing
- Search products by keyword
- Product card display with thumbnail images
- Expandable gallery with additional product images
- Containerized architecture using Docker Compose

## Technology Stack

- Backend: Python, FastAPI, httpx, Pydantic
- Frontend: Vanilla JavaScript, HTML, CSS, Nginx
- Deployment: Docker, Docker Compose

## Project Structure

- `backend/`
  - `Dockerfile`
  - `entrypoint.sh`
  - `main.py`
  - `requirements.txt`
  - `products/apis/products_apis.py`
  - `products/repositories/products_repository.py`
  - `products/schemas/products_schema.py`
  - `products/services/products_service.py`
- `frontend/`
  - `Dockerfile`
  - `app.js`
  - `index.html`
  - `styles.css`
- `docker-compose.yml`
- `README.md`

## How the Application Works

### Backend

The backend lives in `backend/` and is responsible for:

- Serving HTTP endpoints using FastAPI
- Fetching product data from `https://dummyjson.com/products`
- Normalizing and validating product data using service and schema layers
- Returning paginated JSON responses to the frontend

Important backend structure:

- `products/repositories/products_repository.py`
  - Handles network communication with the external API using `httpx.AsyncClient`
  - Provides methods for fetching products and searching products
- `products/services/products_service.py`
  - Applies business logic, pagination, and response normalization
  - Converts raw API fields into a frontend-friendly payload
- `products/schemas/products_schema.py`
  - Defines Pydantic response models for consistent validation

The backend exposes two endpoints:

- `GET /products` — returns product listings with pagination
- `GET /products/search` — returns search results by query text with pagination

### Frontend

The frontend is a simple single-page app served from `frontend/` by Nginx.

It performs the following functions:

- Loads the product list from the backend API
- Displays products in a table with columns for title, description, price, rating, stock, brand, category, and thumbnail
- Includes search input for filtering products by text
- Renders next/previous pagination controls
- Shows image galleries for each product when the gallery button is clicked

The frontend code is in `frontend/app.js`, and it expects the backend API to be reachable at `http://localhost:8000`.

## Data Flow

1. User opens the app in the browser at `http://localhost:5500`.
2. The frontend requests product data from the backend API.
3. The backend fetches raw data from DummyJSON, normalizes it, and returns a clean response.
4. The frontend renders the results and pagination controls in the browser.

## Installation and Run

### Clone the repository

1. Open a terminal and run:
   ```powershell
   gh repo clone IA251/fullstack-product-listing-app
   ```
2. Enter the cloned folder:
   ```powershell
   cd fullstack-product-listing-app
   ```

### Using Docker Compose

1. Build the containers:
   ```powershell
   docker compose build --no-cache
   ```
2. Start the application:
   ```powershell
   docker compose up
   ```
3. Open the frontend in the browser:
   - `http://localhost:5500`

The backend API will be available at:
- `http://localhost:8000`

## Assumptions and Important Decisions

- The backend is responsible for fetching data from the external DummyJSON API and applying search and pagination logic before returning responses to the frontend.
- Data is not stored in a local database; it is retrieved in real time from an external service.
- The frontend is used only to display data and handle basic UI interactions, such as opening a product gallery.
- Search and pagination are handled on the server side to satisfy the task requirements and keep the client structure clean and simple.
- The project is separated into backend and frontend parts to clearly separate business logic from presentation.



