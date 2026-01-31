#!/usr/bin/env python3
"""Verification script to test tags propagation"""
import json
import sys

# Load the test authorization details
with open('test/files/example-authz-details.json') as f:
    auth_data = json.load(f)

print("=" * 60)
print("VERIFICATION: Tags in Input Data")
print("=" * 60)

# Check users
print("\nUsers with tags in input:")
for user in auth_data['UserDetailList']:
    tags = user.get('Tags', [])
    if tags:
        print(f"  - {user['UserName']}: {len(tags)} tags")
        for tag in tags:
            print(f"      {tag['Key']}: {tag['Value']}")

# Check roles
print("\nRoles with tags in input:")
for role in auth_data['RoleDetailList']:
    tags = role.get('Tags', [])
    if tags:
        print(f"  - {role['RoleName']}: {len(tags)} tags")
        for tag in tags:
            print(f"      {tag['Key']}: {tag['Value']}")

print("\n" + "=" * 60)
print("Input verification complete!")
print("=" * 60)
print("\nTo verify full integration:")
print("1. Install dependencies: pip install -e .")
print("2. Run scan: cloudsplaining scan --input-file test/files/example-authz-details.json --output /tmp/")
print("3. Check JSON output: cat /tmp/iam-results-*.json | jq '.users.obama.tags'")
print("4. Open HTML report: open /tmp/iam-report-*.html")
