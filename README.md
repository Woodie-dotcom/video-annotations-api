# ⚙️ Video Annotations Backend API

This repository contains the backend service responsible for storing and providing video annotation data (people present in time intervals) via an HTTP API. It is designed to be used by companion clients, such as the [mpv-xray Lua script](https://github.com/Woodie-dotcom/mpv-xray).

The backend is built using **Python (FastAPI)**, stores data in a **PostgreSQL** database, and is fully containerized using **Docker** and **Docker Compose** for easy setup and deployment.

## ✨ Features

-   **RESTful API**: Exposes annotation data via a `GET /api/v1/annotations` endpoint.
-   **Persistent Storage**: Uses PostgreSQL database managed within Docker. Data persists across container restarts using a Docker volume.
-   **Containerized**: Bundles the API server, database, and dependencies using Docker for consistent setup.
-   **Easy Orchestration**: Uses Docker Compose to define, build, and run the multi-container application (API + DB).
-   **Secure Configuration**: Reads sensitive database credentials from environment variables (via a `.env` file), keeping secrets out of source code.
-   **Health Checks**: Includes a basic health check for the database service.
-   **Automatic Docs**: Provides interactive API documentation (Swagger UI) via FastAPI, accessible at `/docs`.

## 🛠️ Requirements

-   **Docker Engine**: Must be installed on your host machine. ([Install Docker](https://docs.docker.com/engine/install/))
-   **Docker Compose**:
    -   V2 (recommended, integrated into Docker CLI): `docker compose` command. ([Install Docker Compose](https://docs.docker.com/compose/install/))
    -   V1 (standalone): `docker-compose` command.

## 🚀 Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Woodie-dotcom/video-annotations-api.git](https://www.google.com/search?q=https://github.com/Woodie-dotcom/video-annotations-api.git)
    cd video-annotations-api
    ```

2.  **Create Environment File:**
    * Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    * **Edit the `.env` file** with your preferred text editor.
    * **Crucially, replace the placeholder passwords** (`your_admin_password_here`, `your_reader_password_here`) with strong, secure passwords.
    * Verify the `POSTGRES_ADMIN_USER` and `POSTGRES_DB_NAME` match the database you intend to use or create. The `POSTGRES_READER_USER` should also be set up in your database with `SELECT` privileges (the service uses this user for read operations).

3.  **Build and Run:**
    * Docker Compose will automatically pull the required PostgreSQL image and build the API image based on the `api/Dockerfile`.
    * Start the services in detached mode (background):
        ```bash
        # Use 'docker compose' (V2) if available
        docker compose up --build -d

        # Or use 'docker-compose' (V1) if using the older version
        # docker-compose up --build -d
        ```
    * The `--build` flag is only necessary the first time or after making changes to the API's code (`api/` directory) or `api/Dockerfile`. Subsequent starts can usually omit it (`docker compose up -d`).

## ⚙️ Configuration (`.env` File)

The `.env` file configures the database credentials. Ensure these variables are set:

-   `POSTGRES_ADMIN_USER`: The superuser for the PostgreSQL database (used for initialization and health checks). Default: `admin`.
-   `POSTGRES_ADMIN_PASSWORD`: The password for the admin user. **(Set this!)**
-   `POSTGRES_DB_NAME`: The name of the database to use. Default: `media_db`.
-   `POSTGRES_READER_USER`: The less-privileged user the API will use to connect and read data. Default: `user_reader`.
-   `POSTGRES_READER_PASSWORD`: The password for the reader user. **(Set this!)**

**Note:** The `.gitignore` file prevents the `.env` file (containing secrets) from being committed to Git.

## ▶️ Running the Service

-   **Start:** `docker compose up -d` (or `docker-compose up -d`)
-   **View Logs:** `docker compose logs -f` (or `docker-compose logs -f`) (Use `-f api` or `-f db` to follow logs for a specific service).
-   **Stop and Remove Containers:** `docker compose down` (or `docker-compose down`) (Use `docker compose down -v` to also remove the data volume - **USE WITH CAUTION!**)

The API will be accessible on `http://localhost:8123` (or the port you configured in `docker-compose.yml`).

## 📄 API Endpoint

### Get Annotations

-   **URL:** `/api/v1/annotations`
-   **Method:** `GET`
-   **Query Parameter:**
    -   `filename` (string, **required**): The exact filename of the video for which to retrieve annotations.
-   **Success Response (200 OK):**
    -   **Content-Type:** `application/json`
    -   **Body:** A JSON object where keys are person names (string) and values are lists of time intervals. Each interval is a list containing two strings: start time (`"HH:MM:SS"`) and end time (`"HH:MM:SS"`).
        ```json
        {
          "Person One": [
            ["00:01:15", "00:05:30"],
            ["00:07:00", "00:08:12"]
          ],
          "Person Two": [
            ["00:01:20", "00:06:00"]
          ]
        }
        ```
-   **Error Response (404 Not Found):**
    -   **Content-Type:** `application/json`
    -   **Body:**
        ```json
        {
          "detail": "Annotations not found for filename: <requested_filename>"
        }
        ```
-   **Interactive Documentation:** Visit `http://localhost:8123/docs` in your browser for the automatically generated Swagger UI, where you can explore and test the API endpoint interactively.

## 🗄️ Database

-   Uses **PostgreSQL** (Version 17 by default, defined in `docker-compose.yml`).
-   Expects three main tables: `videos`, `people`, `annotations` (refer to schema details if needed).
-   Data is stored persistently in the Docker named volume `postgres_data_vol`.

## 🔗 Frontend Client

This backend is designed to work with the `mpv-xray` Lua script for mpv:

➡️ **[https://github.com/Woodie-dotcom/mpv-xray](https://github.com/Woodie-dotcom/mpv-xray)**

---
