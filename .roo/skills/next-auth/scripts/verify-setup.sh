#!/bin/bash
# NextAuth.js v5 Verification Script
# Validates the NextAuth.js v5 setup

set -e

echo "=========================================="
echo "NextAuth.js v5 Setup Verification"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track verification status
ERRORS=0
WARNINGS=0

# Function to check if a file exists
check_file() {
  if [ -f "$1" ]; then
    echo -e "${GREEN}✓${NC} $2: $1"
    return 0
  else
    echo -e "${RED}✗${NC} $2: $1 (missing)"
    ERRORS=$((ERRORS + 1))
    return 1
  fi
}

# Function to check if a directory exists
check_dir() {
  if [ -d "$1" ]; then
    echo -e "${GREEN}✓${NC} $2: $1"
    return 0
  else
    echo -e "${RED}✗${NC} $2: $1 (missing)"
    ERRORS=$((ERRORS + 1))
    return 1
  fi
}

# Function to check if a string exists in a file
check_string_in_file() {
  if grep -q "$2" "$1" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} $3 in $1"
    return 0
  else
    echo -e "${YELLOW}⚠${NC} $3 not found in $1"
    WARNINGS=$((WARNINGS + 1))
    return 1
  fi
}

# Function to check environment variable
check_env_var() {
  if [ -n "$2" ]; then
    echo -e "${GREEN}✓${NC} $1 is set"
    return 0
  else
    echo -e "${YELLOW}⚠${NC} $1 is not set"
    WARNINGS=$((WARNINGS + 1))
    return 1
  fi
}

echo ""
echo "Step 1: Checking package.json..."
echo "--------------------------------"
check_file "package.json" "Package manifest"
check_string_in_file "package.json" "next-auth" "next-auth dependency"

echo ""
echo "Step 2: Checking auth configuration files..."
echo "--------------------------------------------"
check_file "auth.ts" "Main auth entry point"
check_file "auth.config.ts" "Auth configuration"
check_string_in_file "auth.ts" "NextAuth" "NextAuth import in auth.ts"
check_string_in_file "auth.config.ts" "NextAuthConfig" "NextAuthConfig type"

echo ""
echo "Step 3: Checking API route handler..."
echo "-------------------------------------"
check_dir "app/api/auth" "Auth API directory"
check_file "app/api/auth/[...nextauth]/route.ts" "Auth route handler"
check_string_in_file "app/api/auth/[...nextauth]/route.ts" "handlers" "Handler export"

echo ""
echo "Step 4: Checking middleware..."
echo "------------------------------"
check_file "middleware.ts" "Middleware file"
check_string_in_file "middleware.ts" "auth" "Auth import in middleware"
check_string_in_file "middleware.ts" "matcher" "Middleware matcher config"

echo ""
echo "Step 5: Checking environment variables..."
echo "-----------------------------------------"
if [ -f ".env.local" ]; then
  check_string_in_file ".env.local" "AUTH_SECRET" "AUTH_SECRET"
  check_string_in_file ".env.local" "AUTH_TRUST_HOST" "AUTH_TRUST_HOST"
else
  echo -e "${YELLOW}⚠${NC} .env.local not found (check .env.local.template)"
  WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "Step 6: Checking TypeScript types..."
echo "------------------------------------"
if [ -f "types/next-auth.d.ts" ]; then
  echo -e "${GREEN}✓${NC} Type definitions: types/next-auth.d.ts"
  check_string_in_file "types/next-auth.d.ts" "NextAuth" "NextAuth module declaration"
else
  echo -e "${YELLOW}⚠${NC} Type definitions not found (optional)"
  WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "Step 7: Checking login page..."
echo "------------------------------"
if [ -f "app/login/page.tsx" ]; then
  echo -e "${GREEN}✓${NC} Login page: app/login/page.tsx"
  check_string_in_file "app/login/page.tsx" "signIn" "signIn usage"
else
  echo -e "${YELLOW}⚠${NC} Login page not found (optional)"
  WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Errors:${NC} $ERRORS"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
  echo -e "${GREEN}✓ All critical checks passed!${NC}"
  if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warning(s) found. Review above for details.${NC}"
  fi
  echo ""
  echo "Next steps:"
  echo "1. Fill in your OAuth provider credentials in .env.local"
  echo "2. Run 'npm run dev' to start the development server"
  echo "3. Visit http://localhost:3000/login to test authentication"
  exit 0
else
  echo -e "${RED}✗ $ERRORS critical error(s) found. Please fix before proceeding.${NC}"
  exit 1
fi
