#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Django Note App...${NC}"

# Navigate to project directory
cd "$(dirname "$0")/NoteApp"

# Activate virtual environment
source ../djangoNoteAppenv/Scripts/activate

# Wait for database
echo -e "${BLUE}Waiting for database...${NC}"
python manage.py wait_for_db

# Run migrations
echo -e "${BLUE}Running migrations...${NC}"
python manage.py migrate

# Create superuser if needed
echo -e "${BLUE}Creating superuser if needed...${NC}"
python manage.py create_superuser

# Start server
echo -e "${GREEN}Starting Django server...${NC}"
python manage.py runserver
