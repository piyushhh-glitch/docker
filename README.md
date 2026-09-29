# Dockerized ML App

A small hands-on Docker practice project that connects a Python machine-learning container to a MySQL container using a Docker network.

The application reads Iris data from MySQL, trains a `DecisionTreeClassifier`, and makes a sample prediction.

> **Purpose:** This project is for learning and practicing Docker concepts with an ML workflow, not for production use.

## Architecture

```text
                    Docker
                       |
                  ml-network
                 /           \
                /             \
           mysql-db          ml-app
           MySQL 8        Python + ML
               |               |
               |          pandas / sklearn
               |               |
               +------ data ---+
```

Adminer can also be used as a browser-based GUI:

```text
Browser -> Adminer -> mysql-db
```

## Tech Stack

- Python 3.12
- MySQL 8
- pandas
- scikit-learn
- mysql-connector-python
- Docker
- Docker Network
- Adminer

## Project Structure

```text
docker-ml-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## 1. Create the Docker Network

```cmd
docker network create ml-network
```

## 2. Start MySQL

Create the MySQL container on the Docker network:

```cmd
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=secret-pass --network=ml-network -p 3307:3306 mysql:8
```

The mapping means:

```text
Windows host:3307 -> MySQL container:3306
```

The ML container does not use `localhost:3307`. It connects to:

```text
mysql-db:3306
```

because both containers are on `ml-network`.

## 3. Create the Database and Table

Enter MySQL:

```cmd
docker exec -it mysql-db mysql -u root -p
```

Use the password:

```text
secret-pass
```

Create the database:

```sql
CREATE DATABASE ml_db;
USE ml_db;
```

Create the table:

```sql
CREATE TABLE iris_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sepal_length FLOAT,
    sepal_width FLOAT,
    petal_length FLOAT,
    petal_width FLOAT,
    species VARCHAR(20)
);
```

Insert the sample data:

```sql
INSERT INTO iris_data
(sepal_length, sepal_width, petal_length, petal_width, species)
VALUES
(5.1, 3.5, 1.4, 0.2, 'setosa'),
(4.9, 3.0, 1.4, 0.2, 'setosa'),
(5.0, 3.4, 1.5, 0.2, 'setosa'),
(5.4, 3.9, 1.7, 0.4, 'setosa'),
(6.2, 3.4, 5.4, 2.3, 'virginica'),
(5.9, 3.0, 5.1, 1.8, 'virginica'),
(6.3, 3.3, 6.0, 2.5, 'virginica'),
(6.5, 3.0, 5.8, 2.2, 'virginica');
```

Verify:

```sql
SELECT * FROM iris_data;
```

## 4. Optional: Start Adminer

Adminer provides a browser-based GUI for MySQL.

```cmd
docker run -d --name adminer --network=ml-network -p 8080:8080 adminer
```

Open:

```text
http://localhost:8080
```

Use:

```text
System:   MySQL
Server:   mysql-db
Username: root
Password: secret-pass
```

## 5. Build the ML Image

Build the image from the `Dockerfile`:

```cmd
docker build -t docker-ml-app .
```

The Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

## 6. Run the ML Container

Run the ML application on the same Docker network:

```cmd
docker run --name ml-app --network=ml-network docker-ml-app
```

The application:

1. Connects to MySQL.
2. Reads `iris_data`.
3. Loads the data into pandas.
4. Trains a Decision Tree classifier.
5. Makes a prediction.

Expected output includes:

```text
Data from MySql:
...
Prediction: ['setosa']
```


## Notes

This is intentionally a small practice project. It uses a manually created MySQL database and a small Iris dataset to focus on understanding Docker fundamentals and container networking.
