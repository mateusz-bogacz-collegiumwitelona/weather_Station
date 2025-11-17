#!/bin/bash

#################################################
# Weather Station - Complete Automatic Setup
# Author: Mateusz Bogacz-Drewniak
# Description: One-click installation script
#################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

error() {
    echo -e "${RED}❌ Error: $1${NC}"
    exit 1
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo ""
    echo "======================================"
    echo -e "${GREEN}$1${NC}"
    echo "======================================"
    echo ""
}

if [ ! -f /proc/device-tree/model ]; then
    warning "Not running on Raspberry Pi, but continuing anyway..."
else
    success "Running on Raspberry Pi"
fi

clear

print_header "Weather Station - Automatic Setup"

info "This script will:"
echo "  1. Install system dependencies (Python, Node.js, npm)"
echo "  2. Setup mDNS (Avahi) for local domain access"
echo "  3. Install Python and npm dependencies"
echo "  4. Initialize the database"
echo "  5. Build the frontend"
echo "  6. Create and enable systemd services"
echo "  7. Start the weather station"
echo ""

read -p "Do you want to proceed? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    info "Setup aborted by user."
    exit 0
fi

PROJECT_DIR=$(pwd)
info "Project directory: $PROJECT_DIR"

if [ ! -d "backend" ] && [ ! -f "main.py" ]; then
    error "Cannot find backend directory or main.py. Are you in the correct directory?"
fi

if [ ! -d "frontend" ] && [ ! -d "forntend" ]; then
    error "Cannot find frontend directory. Are you in the correct directory?"
fi

if [ -d "forntend" ]; then
    warning "Found 'forntend' directory (typo). Renaming to 'frontend'..."
    mv forntend frontend
    success "Renamed to 'frontend'"
fi

if [ -d "backend" ]; then
    BACKEND_DIR="$PROJECT_DIR/backend"
else
    BACKEND_DIR="$PROJECT_DIR"
fi

FRONTEND_DIR="$PROJECT_DIR/frontend"

info "Backend directory: $BACKEND_DIR"
info "Frontend directory: $FRONTEND_DIR"

echo ""
read -p "Enter hostname for your weather station (default: weatherstation): " HOSTNAME
HOSTNAME=${HOSTNAME:-weatherstation}
success "Hostname will be set to: $HOSTNAME.local"

print_header "Step 1/7: Installing System Dependencies"

info "Updating system packages..."
sudo apt update || error "Failed to update package list"

info "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    avahi-daemon \
    avahi-utils \
    i2c-tools \
    python3-smbus \
    || error "Failed to install system packages"

success "System dependencies installed."

print_header "Step 2/7: Configuring Hardware Interfaces"

info "Enabling I2C interface..."
sudo raspi-config nonint do_i2c 0 || warning "Could not enable I2C automatically"

info "Enabling SPI interface..."
sudo raspi-config nonint do_spi 0 || warning "Could not enable SPI automatically"

success "Hardware interfaces configured."

print_header "Step 3/7: Setting up mDNS (Avahi)"

info "Enabling and starting Avahi daemon..."
sudo systemctl enable avahi-daemon || error "Failed to enable Avahi daemon"
sudo systemctl start avahi-daemon || error "Failed to start Avahi daemon"

info "Setting hostname to $HOSTNAME..."
sudo hostnamectl set-hostname "$HOSTNAME" || error "Failed to set hostname"

if ! grep -q "127.0.1.1.*$HOSTNAME" /etc/hosts; then
    info "Updating /etc/hosts..."
    sudo sed -i "s/127.0.1.1.*/127.0.1.1\t$HOSTNAME/" /etc/hosts
fi

sudo systemctl restart avahi-daemon
success "mDNS configured - Your station will be available at: $HOSTNAME.local"

print_header "Step 4/7: Setting up Python Backend"

cd "$BACKEND_DIR" || error "Failed to navigate to backend directory"

info "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --break-system-packages || \
    pip3 install -r requirements.txt || \
    error "Failed to install Python dependencies"
    success "Python dependencies installed."
else
    error "requirements.txt not found in $BACKEND_DIR"
fi

info "Initializing database..."
python3 << 'EOF' || error "Failed to initialize database"
try:
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")
except Exception as e:
    print(f"Error: {e}")
    exit(1)
EOF

success "Backend setup complete."

print_header "Step 5/7: Setting up Frontend"

cd "$FRONTEND_DIR" || error "Failed to navigate to frontend directory"

info "Installing npm dependencies..."
npm install || error "Failed to install npm dependencies"
success "npm dependencies installed."

info "Building frontend..."
npm run build || error "Failed to build frontend"
success "Frontend build complete."

print_header "Step 6/7: Creating systemd services"

info "Creating backend service..."
sudo tee /etc/systemd/system/weather-backend.service > /dev/null <<EOF
[Unit]
Description=Weather Station Backend API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BACKEND_DIR
Environment="PATH=/home/$USER/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
success "Backend service created."

info "Creating frontend service..."
sudo tee /etc/systemd/system/weather-frontend.service > /dev/null <<EOF
[Unit]
Description=Weather Station Frontend
After=network.target weather-backend.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$FRONTEND_DIR
Environment="PATH=/home/$USER/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/npm run preview -- --host 0.0.0.0 --port 5173
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
success "Frontend service created."

print_header "Step 7/7: Enabling and starting services"

info "Reloading systemd daemon..."
sudo systemctl daemon-reload

info "Enabling services..."
sudo systemctl enable weather-backend || error "Failed to enable backend service"
sudo systemctl enable weather-frontend || error "Failed to enable frontend service"
success "Services enabled (will start automatically on boot)."

info "Starting backend service..."
sudo systemctl start weather-backend || error "Failed to start backend service"

info "Starting frontend service..."
sudo systemctl start weather-frontend || error "Failed to start frontend service"

info "Waiting for services to start..."
sleep 5

print_header "Verifying Installation"

if sudo systemctl is-active --quiet weather-backend; then
    success "Backend service is running"
else
    error "Backend service failed to start. Check logs with: sudo journalctl -u weather-backend -n 50"
fi

if sudo systemctl is-active --quiet weather-frontend; then
    success "Frontend service is running"
else
    error "Frontend service failed to start. Check logs with: sudo journalctl -u weather-frontend -n 50"
fi

IP_ADDRESS=$(hostname -I | awk '{print $1}')

print_header "Installation Complete!"

echo ""
echo -e "${GREEN}Your Weather Station is now running!${NC}"
echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo ""
echo -e "Frontend (Dashboard):"
echo -e "${GREEN}http://$HOSTNAME.local:5173${NC}"
echo -e "${GREEN}http://$IP_ADDRESS:5173${NC}"
echo ""
echo -e "Backend (API):"
echo -e "${GREEN}http://$HOSTNAME.local:8000${NC}"
echo -e "${GREEN}http://$IP_ADDRESS:8000${NC}"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo ""
echo "Check status:"
echo "sudo systemctl status weather-backend"
echo "sudo systemctl status weather-frontend"
echo ""
echo "View logs:"
echo "sudo journalctl -u weather-backend -f"
echo "sudo journalctl -u weather-frontend -f"
echo ""
echo " Restart services:"
echo "sudo systemctl restart weather-backend"
echo "sudo systemctl restart weather-frontend"
echo ""
echo "Stop services:"
echo "sudo systemctl stop weather-backend weather-frontend"
echo ""
echo "Start services:"
echo "sudo systemctl start weather-backend weather-frontend"
echo ""
echo -e "${YELLOW}Note:${NC} Services will start automatically on system boot!"
echo ""
echo -e "${GREEN}Enjoy your Weather Station!${NC}"
echo ""