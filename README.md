# POC Data Pipeline CI/CD

This repository contains a Proof-of-Concept (POC) for a data pipeline with Continuous Integration/Continuous Deployment (CI/CD) capabilities. The pipeline is designed to demonstrate an Extract, Transform, Load (ETL) process using Apache Spark within a Dockerized environment.

## Features

*   **ETL Process**: Implements a basic ETL workflow to process data.
*   **Apache Spark Integration**: Leverages Spark for distributed data processing.
*   **Dockerized Environment**: Encapsulates the Spark application and its dependencies in Docker containers for consistent deployment.
*   **CI/CD Ready**: Designed with CI/CD principles in mind, facilitating automated testing and deployment.
*   **Unit Testing**: Includes unit tests for the ETL logic to ensure data integrity and correctness.

## Architecture

The project consists of the following main components:

*   **`app/`**: Contains the core Python application logic, including the ETL process.
    *   `etl_process.py`: The main script for the ETL operations.
*   **`Docker/`**: Houses the Docker-related files for building the Spark environment.
    *   `Dockerfile-spark`: Defines the Docker image for running the Spark application.
    *   `requirements.txt`: Lists Python dependencies required by the Spark application.
*   **`tests/`**: Contains unit tests for the application.
    *   `test_etl_process.py`: Tests specifically for the ETL logic.

## Getting Started

Follow these instructions to set up and run the data pipeline locally.

### Prerequisites

*   [Docker](https://www.docker.com/get-started/)
*   [Docker Compose](https://docs.docker.com/compose/install/) (optional, for easier orchestration)
*   [Python 3.x](https://www.python.org/downloads/) (for running tests and local development)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/chayut-data-platform.git
    cd chayut-data-platform/poc/poc_data-pipeline_cicd
    ```

2.  **Build the Docker image**:
    Navigate to the `Docker` directory and build the Spark image.
    ```bash
    cd Docker
    docker build -f Dockerfile-spark -t spark-etl-poc .
    cd ..
    ```

### Running the ETL Process

You can run the ETL process using the built Docker image.

```bash
docker run --rm -v "$(pwd)/app:/app" spark-etl-poc python /app/etl_process.py
```
*   `--rm`: Automatically remove the container when it exits.
*   `-v "$(pwd)/app:/app"`: Mounts your local `app` directory into the container at `/app`, allowing the Spark application to access your scripts.

### Running Tests

To run the unit tests, ensure you have Python and `pytest` installed.

1.  **Install dependencies**:
    ```bash
    pip install -r Docker/requirements.txt
    pip install pytest
    ```

2.  **Run tests**:
    ```bash
    pytest tests/
    ```

## Project Structure

```
.
├── .gitignore
├── README.md
├── app/
│   ├── __init__.py
│   └── etl_process.py
├── Docker/
│   ├── Dockerfile-spark
│   └── requirements.txt
└── tests/
    ├── __init__.py
    └── test_etl_process.py
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details (if applicable).