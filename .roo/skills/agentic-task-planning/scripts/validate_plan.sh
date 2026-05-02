#!/bin/bash
# FN:validate_plan.sh
# Validates agentic task plan format and structure
# 
# Usage: ./validate_plan.sh <plan_file.md>
# Returns: 0 if valid, 1 if invalid

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if plan file is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: No plan file provided${NC}"
    echo "Usage: $0 <plan_file.md>"
    exit 1
fi

PLAN_FILE="$1"

# Check if file exists
if [ ! -f "$PLAN_FILE" ]; then
    echo -e "${RED}Error: File not found: $PLAN_FILE${NC}"
    exit 1
fi

echo -e "${YELLOW}Validating plan: $PLAN_FILE${NC}"
echo ""

ERRORS=0
WARNINGS=0

# Check 1: Filename format (YYYYMMDD_HHMMSS_task_name.md)
FILENAME=$(basename "$PLAN_FILE")
if [[ ! "$FILENAME" =~ ^[0-9]{8}_[0-9]{6}_.+\.md$ ]]; then
    echo -e "${RED}✗ Filename format invalid: $FILENAME${NC}"
    echo "  Expected: YYYYMMDD_HHMMSS_<task_name>.md"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ Filename format valid${NC}"
fi

# Check 2: File is in correct directory
if [[ ! "$PLAN_FILE" =~ /agentic/plan/ ]]; then
    echo -e "${RED}✗ File not in /agentic/plan/ directory${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ File in correct directory${NC}"
fi

# Check 3: Has main task title
if ! grep -q "^# Task:" "$PLAN_FILE"; then
    echo -e "${RED}✗ Missing main task title (# Task: <name>)${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ Has main task title${NC}"
fi

# Check 4: Has phases with checkbox format
PHASE_COUNT=$(grep -c "^## Phase" "$PLAN_FILE" || true)
if [ "$PHASE_COUNT" -eq 0 ]; then
    echo -e "${RED}✗ No phases found${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ Found $PHASE_COUNT phase(s)${NC}"
fi

# Check 5: Has subtasks with checkboxes
SUBTASK_COUNT=$(grep -c "^\- \[.\]" "$PLAN_FILE" || true)
if [ "$SUBTASK_COUNT" -eq 0 ]; then
    echo -e "${RED}✗ No subtasks with checkboxes found${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ Found $SUBTASK_COUNT subtask(s)${NC}"
fi

# Check 6: All subtasks have status markers
INCOMPLETE_SUBTASKS=$(grep "^\- \[ \]" "$PLAN_FILE" | wc -l | tr -d ' ')
COMPLETED_SUBTASKS=$(grep "^\- \[x\]" "$PLAN_FILE" | wc -l | tr -d ' ')
echo -e "${YELLOW}  Subtask status: $COMPLETED_SUBTASKS completed, $INCOMPLETE_SUBTASKS pending${NC}"

# Check 7: Has test module references
TEST_MODULE_COUNT=$(grep -c "### Test Module" "$PLAN_FILE" || true)
if [ "$TEST_MODULE_COUNT" -eq 0 ]; then
    echo -e "${RED}✗ No test module sections found${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ Found $TEST_MODULE_COUNT test module section(s)${NC}"
fi

# Check 8: Has mock data references
MOCK_DATA_COUNT=$(grep -c "assets/test_data/" "$PLAN_FILE" || true)
if [ "$MOCK_DATA_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}⚠ No mock data references found${NC}"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓ Found $MOCK_DATA_COUNT mock data reference(s)${NC}"
fi

# Check 9: Has token budget mentioned
if ! grep -q "Token Budget" "$PLAN_FILE"; then
    echo -e "${YELLOW}⚠ No token budget specified${NC}"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓ Has token budget specified${NC}"
fi

# Check 10: Validate YAML frontmatter (if present)
if grep -q "^---$" "$PLAN_FILE"; then
    if ! grep -q "token_budget:" "$PLAN_FILE"; then
        echo -e "${YELLOW}⚠ YAML frontmatter present but missing token_budget${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN}✓ YAML frontmatter valid${NC}"
    fi
fi

echo ""
echo "====================================="
echo "Validation Summary"
echo "====================================="
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}✗ Plan validation FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Plan validation PASSED${NC}"
    exit 0
fi
