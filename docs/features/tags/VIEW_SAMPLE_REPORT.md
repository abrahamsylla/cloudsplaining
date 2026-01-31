# View Sample Report with Tags

## Quick Start - View the Demo

### Option 1: Open the HTML Demo (Recommended - No Dependencies)
```bash
open sample-tags-demo.html
```

This standalone HTML file shows:
- ✅ How tags appear in the Principal Metadata section
- ✅ User with tags (obama: Environment, Owner)
- ✅ Role with tags (MyOtherRole: Application, CostCenter)
- ✅ User without tags (biden: shows "None")
- ✅ JSON output format examples
- ✅ Use cases and benefits

**File Location:** `cloudsplaining/sample-tags-demo.html`

---

### Option 2: View JSON Results
```bash
cat sample-results-with-tags.json | jq '.'
```

Or view specific tags:
```bash
# User tags
cat sample-results-with-tags.json | jq '.users.obama.tags'

# Role tags
cat sample-results-with-tags.json | jq '.roles.MyOtherRole.tags'
```

**File Location:** `cloudsplaining/sample-results-with-tags.json`

---

### Option 3: Generate Full HTML Report (Requires Dependencies)

If you want to generate the actual Cloudsplaining HTML report with tags:

#### Step 1: Install Dependencies
```bash
pip install -e .
```

#### Step 2: Run Scan
```bash
cloudsplaining scan \
  --input-file test/files/example-authz-details.json \
  --output /tmp/
```

#### Step 3: Open Report
```bash
open /tmp/iam-report-example-authz-details.html
```

Then navigate to:
1. Click "IAM Principals" tab
2. Click on user "obama" or role "MyOtherRole"
3. Look for the "Tags" section in the metadata panel
4. Click the button to expand and see tags

---

## What You'll See

### In the HTML Demo (`sample-tags-demo.html`)

**User "obama" with tags:**
```
Tags    [2] ▼ Show
        ┌─────────────────────────┐
        │ • Environment: Production│
        │ • Owner: SecurityTeam    │
        └─────────────────────────┘
```

**Role "MyOtherRole" with tags:**
```
Tags    [2] ▼ Show
        ┌──────────────────────────────┐
        │ • Application: DataProcessing│
        │ • CostCenter: Engineering    │
        └──────────────────────────────┘
```

**User "biden" without tags:**
```
Tags    None
```

### In the JSON Output (`sample-results-with-tags.json`)

```json
{
  "users": {
    "obama": {
      "tags": [
        {"Key": "Environment", "Value": "Production"},
        {"Key": "Owner", "Value": "SecurityTeam"}
      ]
    }
  },
  "roles": {
    "MyOtherRole": {
      "tags": [
        {"Key": "Application", "Value": "DataProcessing"},
        {"Key": "CostCenter", "Value": "Engineering"}
      ]
    }
  }
}
```

---

## Files Available

| File | Description | Size | Dependencies |
|------|-------------|------|--------------|
| `sample-tags-demo.html` | Standalone HTML demo | 14 KB | None ✅ |
| `sample-results-with-tags.json` | JSON output with tags | 5.6 KB | None ✅ |
| `test/files/example-authz-details.json` | Test input data | ~100 KB | None ✅ |

---

## Browser Compatibility

The HTML demo works in all modern browsers:
- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari
- ✅ Opera

No JavaScript frameworks required - uses vanilla JS and Bootstrap CSS from CDN.

---

## Next Steps

1. **View the demo**: `open sample-tags-demo.html`
2. **Review the JSON**: `cat sample-results-with-tags.json | jq '.'`
3. **Generate real report**: Install dependencies and run scan on your AWS data

---

## Troubleshooting

### "Cannot open file"
```bash
# Use full path
open /Users/asylla/Documents/github/cloudsplaining/sample-tags-demo.html

# Or navigate to directory first
cd cloudsplaining
open sample-tags-demo.html
```

### "jq command not found"
```bash
# Install jq
brew install jq  # macOS
# or
apt-get install jq  # Linux

# Or view without jq
cat sample-results-with-tags.json
```

### Want to generate full report but missing dependencies
```bash
# Install Python dependencies
pip install -e .

# Or use pip3
pip3 install -e .

# Then run scan
cloudsplaining scan --input-file test/files/example-authz-details.json --output .
```

---

## Summary

✅ **Easiest**: Open `sample-tags-demo.html` in your browser  
✅ **JSON View**: `cat sample-results-with-tags.json | jq '.'`  
✅ **Full Report**: Install deps → Run scan → Open HTML report

All files are in the `cloudsplaining/` directory.
