#!/bin/bash

# Content Creator Pro - Deployment Script
# This script helps deploy the application to Vercel (frontend) and Railway (backend)

set -e

echo "🚀 Starting Content Creator Pro Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v vercel &> /dev/null; then
        print_error "Vercel CLI is not installed. Please install it with: npm i -g vercel"
        exit 1
    fi
    
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI is not installed. Please install it with: npm i -g @railway/cli"
        exit 1
    fi
    
    print_success "All dependencies are installed"
}

# Deploy backend to Railway
deploy_backend() {
    print_status "Deploying backend to Railway..."
    
    # Check if we're in the right directory
    if [ ! -f "run.py" ]; then
        print_error "run.py not found. Please run this script from the project root."
        exit 1
    fi
    
    # Deploy to Railway
    railway up --service backend
    
    print_success "Backend deployed to Railway"
}

# Deploy frontend to Vercel
deploy_frontend() {
    print_status "Deploying frontend to Vercel..."
    
    # Change to frontend directory
    cd frontend
    
    # Check if we're in the right directory
    if [ ! -f "package.json" ]; then
        print_error "package.json not found. Please run this script from the project root."
        exit 1
    fi
    
    # Deploy to Vercel
    vercel --prod
    
    # Go back to root
    cd ..
    
    print_success "Frontend deployed to Vercel"
}

# Main deployment function
main() {
    print_status "Starting deployment process..."
    
    # Check dependencies
    check_dependencies
    
    # Ask user which parts to deploy
    echo ""
    echo "What would you like to deploy?"
    echo "1) Backend only (Railway)"
    echo "2) Frontend only (Vercel)"
    echo "3) Both (Full deployment)"
    echo "4) Exit"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            deploy_backend
            ;;
        2)
            deploy_frontend
            ;;
        3)
            deploy_backend
            deploy_frontend
            ;;
        4)
            print_status "Deployment cancelled"
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please enter 1-4."
            exit 1
            ;;
    esac
    
    print_success "Deployment completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Update environment variables in Railway dashboard"
    echo "2. Update environment variables in Vercel dashboard"
    echo "3. Test your deployed application"
}

# Run main function
main "$@" 