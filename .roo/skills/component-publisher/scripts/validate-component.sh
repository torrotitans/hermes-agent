#!/bin/bash

# Component Validation Script for Torro Design System
# Usage: ./scripts/validate-component.sh <component-name>

set -e

COMPONENT_NAME="$1"
UI_DIR="UI/src/shared/ui"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "Torro Component Validator"
echo "======================================"

if [ -z "$COMPONENT_NAME" ]; then
    echo -e "${YELLOW}No component name provided. Validating all components...${NC}"
    COMPONENTS=$(ls "$UI_DIR"/*.tsx 2>/dev/null | xargs -n1 basename | sed 's/.tsx//')
else
    COMPONENTS="$COMPONENT_NAME"
fi

ERRORS=0
WARNINGS=0

for COMP in $COMPONENTS; do
    echo ""
    echo "Validating: $COMP"
    echo "--------------------------------------"
    
    FILE="$UI_DIR/$COMP.tsx"
    
    if [ ! -f "$FILE" ]; then
        echo -e "${RED}✗ File not found: $FILE${NC}"
        ERRORS=$((ERRORS + 1))
        continue
    fi
    
    # Check 1: File has proper exports
    if grep -q "export.*$COMP" "$FILE"; then
        echo -e "${GREEN}✓ Component export found${NC}"
    else
        echo -e "${RED}✗ Missing component export${NC}"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Check 2: Uses design tokens (no hardcoded hex values except in comments)
    HEX_PATTERN="#[0-9a-fA-F]{3,6}"
    if grep -v "//.*$HEX_PATTERN" "$FILE" | grep -q "$HEX_PATTERN"; then
        echo -e "${RED}✗ Hardcoded hex values found (use design tokens)${NC}"
        ERRORS=$((ERRORS + 1))
    else
        echo -e "${GREEN}✓ No hardcoded color values${NC}"
    fi
    
    # Check 3: Uses Torro color tokens
    if grep -q "torro-" "$FILE"; then
        echo -e "${GREEN}✓ Uses Torro design tokens${NC}"
    else
        echo -e "${YELLOW}! Consider using Torro design tokens${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    # Check 4: Has displayName for debugging
    if grep -q "displayName" "$FILE"; then
        echo -e "${GREEN}✓ Has displayName${NC}"
    else
        echo -e "${YELLOW}! Consider adding displayName for debugging${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    # Check 5: Uses forwardRef if it's a React component
    if grep -q "forwardRef" "$FILE"; then
        echo -e "${GREEN}✓ Uses forwardRef${NC}"
    fi
    
    # Check 6: Has proper TypeScript types
    if grep -q "interface.*Props" "$FILE"; then
        echo -e "${GREEN}✓ Has Props interface${NC}"
    else
        echo -e "${YELLOW}! Consider adding Props interface${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    # Check 7: Uses class-variance-authority for variants
    if grep -q "cva" "$FILE"; then
        echo -e "${GREEN}✓ Uses cva for variants${NC}"
    fi
    
    # Check 8: Has focus-visible styles
    if grep -q "focus-visible" "$FILE"; then
        echo -e "${GREEN}✓ Has focus-visible styles (accessibility)${NC}"
    else
        echo -e "${YELLOW}! Consider adding focus-visible styles for accessibility${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    # Check 9: Uses Tailwind classes
    if grep -q "className" "$FILE"; then
        echo -e "${GREEN}✓ Uses Tailwind className${NC}"
    fi
    
    # Check 10: Apple Liquid Glass effects (optional but recommended)
    if grep -q "backdrop-blur\|border-black/5\|border-white/10\|shadow-panel\|shadow-float\|rounded-\[14px\]\|rounded-\[20px\]" "$FILE"; then
        echo -e "${GREEN}✓ Has Apple Liquid Glass effects${NC}"
    fi
done

# Check if component is exported in index.ts
echo ""
echo "--------------------------------------"
echo "Checking barrel exports (index.ts):"
echo "--------------------------------------"

INDEX_FILE="$UI_DIR/index.ts"

for COMP in $COMPONENTS; do
    if grep -q "export.*$COMP" "$INDEX_FILE"; then
        echo -e "${GREEN}✓ $COMP is exported from index.ts${NC}"
    else
        echo -e "${YELLOW}! $COMP is NOT exported from index.ts${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
done

# Summary
echo ""
echo "======================================"
echo "Validation Summary"
echo "======================================"
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}Validation FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}Validation PASSED${NC}"
    exit 0
fi
