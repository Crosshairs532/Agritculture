# Agriculture Database - Data Science Project

# Completed Features (Report 1)

## Endpoint 1: Farm Summary (`/farms/summary`)

- Aggregates Total Revenue, Net Profit, Input Cost, and Average Loss % across all farms.
- Supports filtering by:
  - region
  - farm type
  - year
  - season

---

## Endpoint 2: Single Farm Performance (`/farms/{farm_id}/performance`)

- Provides a detailed breakdown of a specific farm's performance across different crops and markets.
- Handles ID-to-Name mapping via `dim_farm`.

---

## Endpoint 3: Top Farms Ranking (`/farms/top`)

- Dynamically ranks the top `N` farms based on:
  - Profit
  - Revenue
  - Yield
- Implements descending sorting and rank numbering.

---

## Endpoint 4: Loss Analysis (`/farms/loss-analysis`)

- Identifies post-harvest loss problem areas by calculating:
  - loss tonnage
  - loss percentages
- Provides a granular breakdown by:
  - region
  - crop category
  - quality grade

---

# 🛠 Technology Stack

| Category               | Technology                           |
| ---------------------- | ------------------------------------ |
| API Framework          | FastAPI                              |
| Data Processing        | Pandas & NumPy                       |
| Database Layer         | SQLAlchemy + PyMySQL                 |
| Validation             | Pydantic (BaseModels) & Python Enums |
| Environment Management | python-dotenv                        |
| Containerization       | Docker (Bonus Implementation)        |

---

# Project Structure

```text
├── src/
│   ├── api/            # FastAPI Endpoint definitions
│   ├── service/        # Business Logic & Pandas Processing (OOP Services)
|   |-- schemas/        # Configuration, Pydantic Models, and Constants
│   ├── exception/      # Custom Exception handling logic
│   └── logger/         # Structured application logging
├── config/             # Database engine & connection management
├── .env                # Environment variables (Credentials)
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image configuration
└── README.md           # Documentation
```

---

## 2. Clone the Project

```bash
git clone https://github.com/Crosshairs532/Agritculture.git
```

## 3. Configuration

Create a `.env` file in the root directory and add the following database credentials:

```env
HOST=
PORT=
DB=
USER=
PASSWORD=
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🏃 Running the Application

## Option A: Local Execution from the root folder

```bash
 python main.py
```

The API will be available at:

```text
http://localhost:8000
```

## Option B: Using Docker

I have already pre-built the Docker image and pushed it to Docker Hub. You can run the application without building it from source.

```bash

version: '3.8'
services:
  api:
    image: crosshairs532/agriculture:latest
    container_name: agriculture_api_container
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: always
```

1.  **Ensure your `.env` file is ready** in the root directory with the database credentials.
2.  **Pull and Run via Docker Compose:**

    ```bash
    docker-compose up
    ```

    _Note: This will automatically pull the image from Docker Hub and start the service._

3.  **Alternative: Running via Docker CLI (without Compose):**

    ```bash
    docker run -p 8000:8000 --env-file .env crosshairs532/agriculture:latest
    ```

4.  **Access the API:**
    - Swagger UI: `http://localhost:8000/docs`
