#!/usr/bin/env python3
"""
Generate a sample HTML report with tags using the test data
This script works without full dependencies by manually constructing the minimal data structure
"""
import json
import sys
from pathlib import Path

def generate_sample_report():
    """Generate a sample HTML report with tags"""
    
    # Load test authorization details
    test_file = Path('test/files/example-authz-details.json')
    with open(test_file) as f:
        auth_data = json.load(f)
    
    # Create a minimal results structure with tags
    results = {
        "users": {},
        "roles": {},
        "groups": {},
        "aws_managed_policies": {},
        "customer_managed_policies": {},
        "inline_policies": {},
        "exclusions": {},
        "links": {}
    }
    
    # Add users with tags
    for user in auth_data['UserDetailList']:
        user_id = user['UserId']
        results['users'][user_id] = {
            "arn": user['Arn'],
            "create_date": user['CreateDate'],
            "id": user_id,
            "name": user['UserName'],
            "inline_policies": {},
            "groups": {},
            "path": user['Path'],
            "customer_managed_policies": {},
            "aws_managed_policies": {},
            "is_excluded": False,
            "tags": user.get('Tags', [])
        }
    
    # Add roles with tags
    for role in auth_data['RoleDetailList']:
        role_id = role['RoleId']
        results['roles'][role_id] = {
            "arn": role['Arn'],
            "assume_role_policy": {
                "PolicyDocument": role.get('AssumeRolePolicyDocument', {})
            },
            "create_date": role['CreateDate'],
            "role_last_used": role.get('RoleLastUsed', {}).get('LastUsedDate'),
            "id": role_id,
            "name": role['RoleName'],
            "inline_policies": {},
            "instance_profiles": role.get('InstanceProfileList', []),
            "instances_count": len(role.get('InstanceProfileList', [])),
            "path": role['Path'],
            "customer_managed_policies": {},
            "aws_managed_policies": {},
            "is_excluded": False,
            "tags": role.get('Tags', [])
        }
    
    # Add groups (no tags support)
    for group in auth_data['GroupDetailList']:
        group_id = group['GroupId']
        results['groups'][group_id] = {
            "arn": group['Arn'],
            "name": group['GroupName'],
            "create_date": group['CreateDate'],
            "id": group_id,
            "inline_policies": {},
            "path": group['Path'],
            "customer_managed_policies": {},
            "aws_managed_policies": {},
            "is_excluded": False
        }
    
    # Try to import and use the actual report generator
    try:
        sys.path.insert(0, '.')
        from cloudsplaining.output.report import HTMLReport
        
        html_report = HTMLReport(
            account_id="012345678901",
            account_name="sample-with-tags",
            results=results,
            minimize=False
        )
        
        html_content = html_report.get_html_report()
        
        # Write to file
        output_file = Path('sample-report-with-tags.html')
        output_file.write_text(html_content, encoding='utf-8')
        
        print("✓ Sample HTML report generated successfully!")
        print(f"✓ File: {output_file.absolute()}")
        print(f"✓ Size: {len(html_content) / 1024 / 1024:.2f} MB")
        print("\nTo view the report:")
        print(f"  open {output_file.absolute()}")
        print("\nPrincipals with tags:")
        print("  - User 'obama': 2 tags (Environment, Owner)")
        print("  - Role 'MyOtherRole': 2 tags (Application, CostCenter)")
        
        return True
        
    except ImportError as e:
        print(f"✗ Cannot import cloudsplaining modules: {e}")
        print("\nTo generate the full HTML report, install dependencies:")
        print("  pip install -e .")
        print("\nAlternatively, run the scan command:")
        print("  cloudsplaining scan --input-file test/files/example-authz-details.json --output .")
        
        # Save the JSON results instead
        output_file = Path('sample-results-with-tags.json')
        output_file.write_text(json.dumps(results, indent=2, default=str), encoding='utf-8')
        print(f"\n✓ Saved JSON results to: {output_file.absolute()}")
        print("  This shows the data structure with tags included")
        
        return False

if __name__ == '__main__':
    success = generate_sample_report()
    sys.exit(0 if success else 1)
