# AWS IAM Tags Implementation Summary

## Overview
Added support for AWS IAM resource tags (users and roles) in both JSON and HTML report outputs.

## Changes Made

### 1. Python Backend Changes

#### `cloudsplaining/scan/user_details.py`
- **Line ~162**: Added `self.tags = user_detail.get("Tags")` to capture tags from AWS API response
- **Line ~298**: Added `"tags": self.tags` to JSON output in `UserDetail.json` property

#### `cloudsplaining/scan/role_details.py`
- **Line ~162**: Tags already captured as `self.tags = role_detail.get("Tags")`
- **Line ~340**: Added `"tags": self.tags` to JSON output in `RoleDetail.json` property

### 2. Frontend Changes

#### `cloudsplaining/output/src/components/principals/PrincipalMetadata.vue`
- Added new "Tags" section after "Created" field
- Displays tag count in collapsible button
- Shows tags as Key:Value list when expanded
- Shows "None" when no tags present
- Works for users, roles, and groups (though groups don't support tags per AWS API)

### 3. Test Data Updates

#### `cloudsplaining/test/files/example-authz-details.json`
- Added 2 sample tags to user "obama":
  - Environment: Production
  - Owner: SecurityTeam
- Added 2 sample tags to role "MyOtherRole":
  - Application: DataProcessing
  - CostCenter: Engineering

### 4. Build Artifacts
- Rebuilt Vue.js bundle: `cloudsplaining/output/dist/js/index.js` (2.0 MB)
- No breaking changes to existing functionality

## JSON Output Format (Backward Compatible)

### Before (existing keys preserved):
```json
{
  "users": {
    "user-id": {
      "arn": "...",
      "name": "...",
      "create_date": "...",
      ...
    }
  }
}
```

### After (additive only):
```json
{
  "users": {
    "user-id": {
      "arn": "...",
      "name": "...",
      "create_date": "...",
      "tags": [
        {"Key": "Environment", "Value": "Production"},
        {"Key": "Owner", "Value": "SecurityTeam"}
      ],
      ...
    }
  }
}
```

## HTML Report Changes

Tags now appear in the Principal Metadata section:
- Displayed after "Created" field
- Collapsible button shows tag count
- Clicking reveals Key:Value pairs
- Empty tags show "None" (graceful degradation)

## AWS API Reference

Tags are included in the AWS IAM `GetAccountAuthorizationDetails` API response:

- **UserDetail.Tags**: Array of Tag objects (max 50)
  - Docs: https://docs.aws.amazon.com/IAM/latest/APIReference/API_UserDetail.html
  
- **RoleDetail.Tags**: Array of Tag objects (max 50)
  - Docs: https://docs.aws.amazon.com/IAM/latest/APIReference/API_RoleDetail.html

- **Tag Structure**: `{"Key": "string", "Value": "string"}`
  - Docs: https://docs.aws.amazon.com/IAM/latest/APIReference/API_Tag.html

## Verification Steps

### 1. Verify Input Data
```bash
python3 verify_tags.py
```

### 2. Run Full Scan (requires dependencies)
```bash
# Install dependencies
pip install -e .

# Run scan
cloudsplaining scan --input-file test/files/example-authz-details.json --output /tmp/

# Check JSON output
cat /tmp/iam-results-*.json | jq '.users.obama.tags'
cat /tmp/iam-results-*.json | jq '.roles.MyOtherRole.tags'

# Open HTML report
open /tmp/iam-report-*.html
```

### 3. Verify in HTML Report
- Navigate to "IAM Principals" tab
- Click on user "obama" or role "MyOtherRole"
- Look for "Tags" section in metadata
- Click button to expand and see Key:Value pairs

## Backward Compatibility

✅ **Fully backward compatible**
- Existing JSON keys unchanged
- New "tags" field is additive only
- Old reports without tags will show null/empty (graceful)
- No breaking changes to API or data structures

## Risks & Limitations

### Low Risk
- Tags field is optional in AWS API (can be null/empty)
- Graceful handling of missing tags in both JSON and HTML

### Known Limitations
- Groups don't support tags per AWS IAM API (not implemented)
- Managed policies don't support tags in GetAccountAuthorizationDetails response

## Files Modified

1. `cloudsplaining/scan/user_details.py` - Capture and output user tags
2. `cloudsplaining/scan/role_details.py` - Output role tags (capture already existed)
3. `cloudsplaining/output/src/components/principals/PrincipalMetadata.vue` - Display tags in UI
4. `cloudsplaining/test/files/example-authz-details.json` - Add sample tags for testing
5. `cloudsplaining/output/dist/js/index.js` - Rebuilt Vue.js bundle

## Testing

- ✅ Python syntax validation passed
- ✅ Vue.js lint validation passed
- ✅ Build completed successfully
- ✅ Input data verification passed
- ⚠️ Full integration test requires dependency installation

## Next Steps

To complete verification:
1. Install Python dependencies: `pip install -e .`
2. Run full scan test
3. Verify JSON output contains tags
4. Verify HTML report displays tags correctly
