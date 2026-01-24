# Route Intelligence Platform - Quick Start Guide

## 🚀 Quick Installation

### **Step 1: Install Git LFS**

First, install Git Large File Storage (LFS) based on your operating system:

#### **For macOS:**

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git LFS via Homebrew
brew install git-lfs

# Initialize Git LFS globally
git lfs install
```

#### **For Ubuntu/Debian Linux:**

```bash
# Method 1: Using apt package manager
sudo apt-get update
sudo apt-get install git-lfs

# Method 2: Using packagecloud.io (alternative)
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs

# Initialize Git LFS
git lfs install
```

### **Step 2: Clone the Repository**

```bash
# Clone the repository (includes LFS files)
git clone https://github.com/sharooque7/route_intelligence.git

# Navigate to the project directory
cd route_intelligence
```

### **Step 3: Pull Large Files**

```bash
# Pull all Git LFS files (this downloads the actual large files)
git lfs pull

# Alternative: Pull specific LFS objects if needed
git lfs fetch --all
git lfs checkout
```

### **Step 4: Start the Application**

```bash
# Build and start all Docker containers in detached mode
docker compose up --build -d

# View container logs
docker compose logs -f
```

### **Step 5: Access the Application**

- **Frontend Dashboard:** http://localhost:81
- **Backend API:** http://localhost:8000
- **Database:** PostgreSQL on localhost:5432

**UI Credentials:**

- Username: `admin`
- Password: `admin123`

**DB Credentials:**

- Username: `ainzson`
- Password: `ainzson123`
- DB: route_intelligence_db

## 📁 Project Structure

```
route_intelligence/
├── backend/          # FastAPI backend with route optimization logic
├── frontend/         # React Vite frontend with dashboard
├── nginx/           # Reverse proxy configuration
├── docker-compose.yml
└── README.md
```

## 🐳 Docker Services Overview

| Service      | Port           | Description                                |
| ------------ | -------------- | ------------------------------------------ |
| **frontend** | 81 (via nginx) | React dashboard for route visualization    |
| **backend**  | 8000           | FastAPI with route optimization algorithms |
| **database** | 5432           | PostgreSQL with route data                 |
| **nginx**    | 81             | Reverse proxy and static file server       |
