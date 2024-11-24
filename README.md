
# coding-challenge

# Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Build the Docker containers:
```bash
docker-compose build
```

3. Start the services:
```bash
docker-compose up
```

The API will be available at `http://localhost:6200`.

## API Endpoints

### Get Weather Data

Retrieve weather data for a specific station within a date range. (Example:)

```bash
curl -X GET "localhost:6200/api/weather?station_id=USC00253365&start_date=2010-01-01&end_date=2010-12-31&page=1&per_page=2" \
     -H "Content-Type: application/json"
```

#### Parameters:
- `station_id` (required): Weather station identifier
- `start_date` (required): Start date in YYYY-MM-DD format
- `end_date` (required): End date in YYYY-MM-DD format
- `page` (optional): Page number for pagination (default: 1)
- `per_page` (optional): Number of records per page (default: 10)

### Get Weather Statistics

Retrieve weather statistics for a specific station and year.  (Example:)

```bash
curl -X GET "http://localhost:6200/api/weather/stats?station_id=USC00253365&year=2010&page=1&per_page=2" \
     -H "Content-Type: application/json"
```

#### Parameters:
- `station_id` (required): Weather station identifier
- `year` (required): Year for statistics (YYYY format)
- `page` (optional): Page number for pagination (default: 1)
- `per_page` (optional): Number of records per page (default: 10)

## Development

To stop the services:
```bash
docker-compose down
```