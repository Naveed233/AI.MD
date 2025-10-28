# 🚀 How to Run the MD System

## Option 1: Using Docker (Recommended - Easiest)

### Step 1: Install Docker Desktop

**For macOS:**
```bash
# Download from: https://www.docker.com/products/docker-desktop
# Or install via Homebrew:
brew install --cask docker
```

**For other platforms:**
- Visit: https://www.docker.com/products/docker-desktop
- Download and install Docker Desktop

### Step 2: Start Docker Desktop

- Open Docker Desktop application
- Wait for it to fully start (Docker icon in menu bar should be steady)

### Step 3: Build and Run

```bash
# Navigate to project
cd /Users/naveedmaqbool/Desktop/Sen/md-system

# Build all Docker images (first time - takes 5-10 minutes)
make build

# Start all services
make up

# View logs
make logs
```

### Step 4: Access the System

Open your browser to:
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **ML Service**: http://localhost:8080

### Step 5: Test the System

```bash
# Test backend health
curl http://localhost:8000/api/v1/health

# Test ML service health  
curl http://localhost:8080/health

# Make a prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "age": 35,
    "purchase_history": 20,
    "avg_order_value": 150.50,
    "last_purchase_days": 7,
    "region": "North America",
    "seasonality_factor": 1.2
  }'
```

---

## Option 2: Run Services Individually (No Docker)

If you don't want to use Docker, you can run each service separately:

### Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Open: http://localhost:3000
```

### Backend (Laravel)

```bash
cd backend

# Install dependencies
composer install

# Generate application key
php artisan key:generate

# Run migrations (if database is set up)
php artisan migrate

# Start server
php artisan serve

# Open: http://localhost:8000
```

### ML Service (FastAPI)

```bash
cd ml_service

# Install Python dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8080

# Open: http://localhost:8080
```

---

## Option 3: Deploy to Google Cloud Platform

If you want to deploy to GCP (cloud), see `DEPLOYMENT.md` for complete instructions.

Quick start:
```bash
# Install gcloud CLI
# Then run:
./infra/gcp_setup.sh

# Deploy
make deploy
```

---

## Useful Commands

Once running with Docker:

```bash
# View logs from all services
make logs

# View logs from specific service
docker compose logs -f ml_service

# Stop all services
make down

# Restart services
make down && make up

# Rebuild after making changes
make build && make up

# Clean everything (removes containers and volumes)
make clean
```

---

## Troubleshooting

### Port Already in Use
```bash
# If port 3000, 8000, or 8080 is already in use:
# Option 1: Stop other services using those ports
lsof -ti:3000 | xargs kill
lsof -ti:8000 | xargs kill
lsof -ti:8080 | xargs kill

# Option 2: Modify docker-compose.yml to use different ports
```

### Services Won't Start
```bash
# Check Docker is running
docker ps

# View error logs
docker compose logs

# Rebuild everything
make clean && make build && make up
```

### Can't Connect to Database
```bash
# Start database first
docker compose up db

# Check database is running
docker compose ps

# View database logs
docker compose logs db
```

---

## Development Workflow

1. **Start services**: `make up`
2. **Make changes** to code
3. **Services auto-reload** (if using individual services or with volume mounts)
4. **View logs**: `make logs` or `docker compose logs -f SERVICE_NAME`
5. **Stop services**: `make down`

---

## Production Deployment

See `DEPLOYMENT.md` for detailed instructions on deploying to GCP Cloud Run.

