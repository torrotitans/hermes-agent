#!/bin/bash

# validate-visual-parity.sh
# Automated visual parity validation for Figma-to-code implementation
# 
# Usage: ./validate-visual-parity.sh [options]
#   --figma-spec <path>   Path to Figma spec JSON
#   --code-spec <path>    Path to code spec JSON
#   --output <path>       Output report path (default: ./parity-report.json)
#   --threshold <number>  Pass threshold score (default: 90)
#   --help                Show this help message

set -e

# Default values
FIGMA_SPEC=""
CODE_SPEC=""
OUTPUT_PATH="./parity-report.json"
THRESHOLD=90

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --figma-spec)
      FIGMA_SPEC="$2"
      shift 2
      ;;
    --code-spec)
      CODE_SPEC="$2"
      shift 2
      ;;
    --output)
      OUTPUT_PATH="$2"
      shift 2
      ;;
    --threshold)
      THRESHOLD="$2"
      shift 2
      ;;
    --help)
      echo "Usage: $0 [options]"
      echo ""
      echo "Options:"
      echo "  --figma-spec <path>   Path to Figma spec JSON"
      echo "  --code-spec <path>    Path to code spec JSON"
      echo "  --output <path>       Output report path (default: ./parity-report.json)"
      echo "  --threshold <number>  Pass threshold score (default: 90)"
      echo "  --help                Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$FIGMA_SPEC" ]; then
  echo "❌ Error: --figma-spec is required"
  exit 1
fi

if [ -z "$CODE_SPEC" ]; then
  echo "❌ Error: --code-spec is required"
  exit 1
fi

# Check if files exist
if [ ! -f "$FIGMA_SPEC" ]; then
  echo "❌ Error: Figma spec file not found: $FIGMA_SPEC"
  exit 1
fi

if [ ! -f "$CODE_SPEC" ]; then
  echo "❌ Error: Code spec file not found: $CODE_SPEC"
  exit 1
fi

echo "🔍 Starting Visual Parity Validation..."
echo ""
echo "Figma Spec: $FIGMA_SPEC"
echo "Code Spec:  $CODE_SPEC"
echo "Output:     $OUTPUT_PATH"
echo "Threshold:  $THRESHOLD"
echo ""

# Generate parity report using Node.js
node - "$FIGMA_SPEC" "$CODE_SPEC" "$OUTPUT_PATH" "$THRESHOLD" << 'NODE_SCRIPT'
const fs = require('fs');
const path = require('path');

const figmaSpecPath = process.argv[2];
const codeSpecPath = process.argv[3];
const outputPath = process.argv[4];
const threshold = parseInt(process.argv[5], 10);

// Read spec files
const figmaSpec = JSON.parse(fs.readFileSync(figmaSpecPath, 'utf8'));
const codeSpec = JSON.parse(fs.readFileSync(codeSpecPath, 'utf8'));

// Comparison function
function compareProperties(figma, code) {
  const diffs = [];
  const allKeys = new Set([...Object.keys(figma), ...Object.keys(code)]);

  for (const key of allKeys) {
    const figmaValue = figma[key];
    const codeValue = code[key];

    if (figmaValue !== codeValue) {
      let severity = 'low';
      
      // Determine severity based on property type
      if (key.includes('color') || key.includes('Color')) {
        severity = 'critical';
      } else if (key.includes('size') || key.includes('Size')) {
        severity = 'high';
      } else if (key.includes('radius') || key.includes('Radius')) {
        severity = 'medium';
      }

      diffs.push({
        property: key,
        figma: figmaValue,
        code: codeValue,
        severity: severity,
        fix: `Update ${key} from "${codeValue}" to "${figmaValue}"`
      });
    }
  }

  return diffs;
}

// Calculate score
function calculateScore(diffs, totalProperties) {
  if (totalProperties === 0) return 100;
  
  const criticalCount = diffs.filter(d => d.severity === 'critical').length;
  const highCount = diffs.filter(d => d.severity === 'high').length;
  const mediumCount = diffs.filter(d => d.severity === 'medium').length;
  const lowCount = diffs.filter(d => d.severity === 'low').length;

  // Weight penalties
  const penalty = (criticalCount * 20) + (highCount * 10) + (mediumCount * 5) + (lowCount * 2);
  const score = Math.max(0, 100 - penalty);

  return Math.round(score);
}

// Compare specs
const diffs = compareProperties(figmaSpec.spec || figmaSpec, codeSpec.spec || codeSpec);
const totalProperties = new Set([...Object.keys(figmaSpec.spec || figmaSpec), ...Object.keys(codeSpec.spec || codeSpec)]).size;
const score = calculateScore(diffs, totalProperties);
const passed = score >= threshold;

// Generate report
const report = {
  timestamp: new Date().toISOString(),
  figmaSpec: figmaSpecPath,
  codeSpec: codeSpecPath,
  score: score,
  threshold: threshold,
  passed: passed,
  totalProperties: totalProperties,
  diffCount: diffs.length,
  diffs: diffs,
  summary: {
    critical: diffs.filter(d => d.severity === 'critical').length,
    high: diffs.filter(d => d.severity === 'high').length,
    medium: diffs.filter(d => d.severity === 'medium').length,
    low: diffs.filter(d => d.severity === 'low').length
  }
};

// Write report
fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));

// Output summary
console.log('📊 Parity Check Results:');
console.log('');
console.log(`  Score:      ${score}/100`);
console.log(`  Threshold:  ${threshold}`);
console.log(`  Status:     ${passed ? '✅ PASSED' : '❌ FAILED'}`);
console.log(`  Properties: ${totalProperties}`);
console.log(`  Diffs:      ${diffs.length}`);
console.log('');

if (diffs.length > 0) {
  console.log('🔍 Differences Found:');
  console.log('');
  
  for (const diff of diffs) {
    const icon = diff.severity === 'critical' ? '🔴' : 
                 diff.severity === 'high' ? '🟠' : 
                 diff.severity === 'medium' ? '🟡' : '🟢';
    console.log(`  ${icon} ${diff.property}`);
    console.log(`     Figma: ${diff.figma}`);
    console.log(`     Code:  ${diff.code}`);
    console.log(`     Fix:   ${diff.fix}`);
    console.log('');
  }
}

console.log(`📄 Full report saved to: ${outputPath}`);

// Exit with appropriate code
process.exit(passed ? 0 : 1);
NODE_SCRIPT

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
  echo "✅ Visual parity validation PASSED"
else
  echo "❌ Visual parity validation FAILED"
  echo ""
  echo "Review the report and apply fixes:"
  echo "  cat $OUTPUT_PATH"
fi

exit $exit_code
