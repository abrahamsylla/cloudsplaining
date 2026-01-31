# Example Output: Tags in JSON and HTML Reports

## JSON Output Example

### User with Tags
```json
{
  "users": {
    "obama": {
      "arn": "arn:aws:iam::012345678901:user/obama",
      "create_date": "2019-12-18 19:10:08+00:00",
      "id": "obama",
      "name": "obama",
      "inline_policies": {},
      "groups": {
        "admin": { ... }
      },
      "path": "/",
      "customer_managed_policies": { ... },
      "aws_managed_policies": { ... },
      "is_excluded": false,
      "tags": [
        {
          "Key": "Environment",
          "Value": "Production"
        },
        {
          "Key": "Owner",
          "Value": "SecurityTeam"
        }
      ]
    }
  }
}
```

### Role with Tags
```json
{
  "roles": {
    "MyOtherRole": {
      "arn": "arn:aws:iam::012345678901:role/MyOtherRole",
      "assume_role_policy": { ... },
      "create_date": "2019-08-16 17:27:59+00:00",
      "role_last_used": null,
      "id": "MyOtherRole",
      "name": "MyOtherRole",
      "inline_policies": { ... },
      "instance_profiles": [],
      "instances_count": 0,
      "path": "/",
      "customer_managed_policies": {},
      "aws_managed_policies": { ... },
      "is_excluded": false,
      "tags": [
        {
          "Key": "Application",
          "Value": "DataProcessing"
        },
        {
          "Key": "CostCenter",
          "Value": "Engineering"
        }
      ]
    }
  }
}
```

### User/Role without Tags
```json
{
  "users": {
    "userwithlotsofpermissions": {
      "arn": "arn:aws:iam::012345678901:user/userwithlotsofpermissions",
      "create_date": "2019-12-18 19:10:08+00:00",
      "id": "ASIAZZUSERZZPLACEHOLDER",
      "name": "userwithlotsofpermissions",
      "inline_policies": { ... },
      "groups": { ... },
      "path": "/",
      "customer_managed_policies": { ... },
      "aws_managed_policies": { ... },
      "is_excluded": false,
      "tags": []
    }
  }
}
```

---

## HTML Report Display

### Principal Metadata Section (with Tags)

```
┌─────────────────────────────────────────────────────────┐
│ Principal Metadata                                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ARN                    arn:aws:iam::012345678901:user/obama
│                                                         │
│ ID                     obama                           │
│                                                         │
│ Excluded from scan     false                           │
│                                                         │
│ Created                2019-12-18 19:10:08+00:00       │
│                                                         │
│ Tags                   [2] ▼                           │
│                        ┌─────────────────────────────┐ │
│                        │ • Environment: Production   │ │
│                        │ • Owner: SecurityTeam       │ │
│                        └─────────────────────────────┘ │
│                                                         │
│ Inline Policies        [0] ▼                           │
│                                                         │
│ AWS-Managed Policies   [1] ▼                           │
│                                                         │
│ Customer-Managed       [0] ▼                           │
│ Policies                                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Principal Metadata Section (without Tags)

```
┌─────────────────────────────────────────────────────────┐
│ Principal Metadata                                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ARN                    arn:aws:iam::012345678901:user/biden
│                                                         │
│ ID                     biden                           │
│                                                         │
│ Excluded from scan     false                           │
│                                                         │
│ Created                2019-12-18 19:10:08+00:00       │
│                                                         │
│ Tags                   None                            │
│                                                         │
│ Inline Policies        [1] ▼                           │
│                                                         │
│ AWS-Managed Policies   [1] ▼                           │
│                                                         │
│ Customer-Managed       [0] ▼                           │
│ Policies                                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## UI Interaction Flow

### 1. Navigate to IAM Principals
- Click "IAM Principals" tab in the report
- See list of users, roles, and groups

### 2. Select a Principal
- Click on a user (e.g., "obama") or role (e.g., "MyOtherRole")
- Principal metadata panel appears on the right

### 3. View Tags
- **If tags exist**: See button with count (e.g., "[2]")
- Click button to expand and see Key:Value list
- **If no tags**: See "None" text (no button)

### 4. Collapsible Behavior
- Tags section is collapsible (like other metadata sections)
- Click button to toggle expand/collapse
- Preserves space when not viewing tags

---

## Query Examples

### Using jq to extract tags from JSON output

```bash
# Get all tags for a specific user
jq '.users.obama.tags' /tmp/iam-results-*.json

# Get all tags for a specific role
jq '.roles.MyOtherRole.tags' /tmp/iam-results-*.json

# Find all users with a specific tag key
jq '.users | to_entries[] | select(.value.tags[]?.Key == "Environment") | .key' /tmp/iam-results-*.json

# Find all roles with a specific tag value
jq '.roles | to_entries[] | select(.value.tags[]?.Value == "Production") | .key' /tmp/iam-results-*.json

# Count principals with tags
jq '[.users, .roles] | map(to_entries[] | select(.value.tags != null and (.value.tags | length) > 0)) | length' /tmp/iam-results-*.json

# List all unique tag keys across all principals
jq '[.users, .roles] | map(to_entries[].value.tags[]?.Key) | unique' /tmp/iam-results-*.json
```

---

## Real-World Use Cases

### 1. Cost Allocation
```json
{
  "tags": [
    {"Key": "CostCenter", "Value": "Engineering"},
    {"Key": "Project", "Value": "DataPipeline"},
    {"Key": "Environment", "Value": "Production"}
  ]
}
```
**Use**: Track IAM resource costs by department, project, or environment

### 2. Compliance & Governance
```json
{
  "tags": [
    {"Key": "Owner", "Value": "SecurityTeam"},
    {"Key": "DataClassification", "Value": "Confidential"},
    {"Key": "ComplianceScope", "Value": "SOC2"}
  ]
}
```
**Use**: Identify principals handling sensitive data or in compliance scope

### 3. Lifecycle Management
```json
{
  "tags": [
    {"Key": "CreatedBy", "Value": "terraform"},
    {"Key": "ManagedBy", "Value": "platform-team"},
    {"Key": "ExpirationDate", "Value": "2026-12-31"}
  ]
}
```
**Use**: Track who created/manages principals and when to review/retire them

### 4. Application Mapping
```json
{
  "tags": [
    {"Key": "Application", "Value": "PaymentProcessor"},
    {"Key": "Component", "Value": "API"},
    {"Key": "Version", "Value": "v2.1"}
  ]
}
```
**Use**: Map IAM principals to applications and components for impact analysis

---

## Filtering & Reporting Ideas

### Generate Tag-Based Reports

```bash
# Create CSV of all principals with their tags
jq -r '
  [.users, .roles] | 
  map(to_entries[]) | 
  map({
    type: (if .value.arn | contains(":user/") then "User" else "Role" end),
    name: .value.name,
    tags: (.value.tags // [] | map("\(.Key)=\(.Value)") | join("; "))
  }) | 
  ["Type,Name,Tags"] + map([.type, .name, .tags] | @csv) | 
  .[]
' /tmp/iam-results-*.json > principals-tags.csv
```

### Find Untagged Principals

```bash
# List all principals without tags
jq -r '
  [.users, .roles] | 
  map(to_entries[]) | 
  map(select(.value.tags == null or (.value.tags | length) == 0)) | 
  map(.value.name) | 
  .[]
' /tmp/iam-results-*.json
```

### Tag Compliance Check

```bash
# Check if all principals have required tags
REQUIRED_TAGS=("Owner" "Environment" "CostCenter")

jq --argjson required '["Owner","Environment","CostCenter"]' '
  [.users, .roles] | 
  map(to_entries[]) | 
  map({
    name: .value.name,
    tags: (.value.tags // [] | map(.Key)),
    missing: ($required - (.value.tags // [] | map(.Key)))
  }) | 
  map(select(.missing | length > 0))
' /tmp/iam-results-*.json
```

---

## Summary

✅ **Tags are now visible in:**
- JSON output files (`iam-results-*.json`)
- HTML report UI (Principal Metadata section)

✅ **Tag format:**
- Array of objects: `[{"Key": "...", "Value": "..."}]`
- Empty array `[]` when no tags
- Null-safe handling throughout

✅ **Use cases enabled:**
- Cost allocation and tracking
- Compliance and governance
- Lifecycle management
- Application mapping
- Custom reporting and filtering
