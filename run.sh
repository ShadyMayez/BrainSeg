#!/bin/bash
# Brain Tumor Segmentation - Run Script
# =====================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  Brain Tumor Segmentation${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Parse arguments
BACKEND_ONLY=false
FRONTEND_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --backend)
            BACKEND_ONLY=true
            shift
            ;;
        --frontend)
            FRONTEND_ONLY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--backend|--frontend]"
            exit 1
            ;;
    esac
done

# Run Backend
run_backend() {
    echo -e "${BLUE}Starting Backend...${NC}"
    cd backend
    
    # Check virtual environment
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    if [ ! -f "venv/.installed" ]; then
        echo -e "${YELLOW}Installing backend dependencies...${NC}"
        pip install --upgrade pip
        pip install -r requirements.txt
        touch venv/.installed
    fi
    
    # Create directories
    mkdir -p ../models/saved_models ../models/checkpoints
    mkdir -p uploads outputs
    
    # Check for model
    if [ ! -f "../models/saved_models/best_model.keras" ]; then
        echo -e "${YELLOW}Warning: Model not found at models/saved_models/best_model.keras${NC}"
        echo -e "${YELLOW}Please place your trained model in this location${NC}"
    fi
    
    echo -e "${GREEN}Backend starting at http://localhost:8000${NC}"
    echo -e "${GREEN}API Docs: http://localhost:8000/api/docs${NC}"
    echo ""
    
    python src/main.py &
    BACKEND_PID=$!
    cd ..
}

# Run Frontend
run_frontend() {
    echo -e "${BLUE}Starting Frontend...${NC}"
    cd frontend
    
    # Check node_modules
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        npm install
    fi
    
    echo -e "${GREEN}Frontend starting at http://localhost:5173${NC}"
    echo ""
    
    npm run dev &
    FRONTEND_PID=$!
    cd ..
}

# Main execution
if [ "$BACKEND_ONLY" = true ]; then
    run_backend
    wait $BACKEND_PID
elif [ "$FRONTEND_ONLY" = true ]; then
    run_frontend
    wait $FRONTEND_PID
else
    run_backend
    sleep 3  # Wait for backend to start
    run_frontend
    
    echo -e "${GREEN}=====================================${NC}"
    echo -e "${GREEN}  Application Started!${NC}"
    echo -e "${GREEN}=====================================${NC}"
    echo ""
    echo -e "Frontend: ${BLUE}http://localhost:5173${NC}"
    echo -e "Backend:  ${BLUE}http://localhost:8000${NC}"
    echo -e "API Docs: ${BLUE}http://localhost:8000/api/docs${NC}"
    echo ""
    echo "Press Ctrl+C to stop"
    
    wait
fi
