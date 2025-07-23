 import boto3
import csv
from datetime import datetime, timezone

# Replace with your org account IDs
child_account_ids = ['424462704852', '731472798505', '316790910104', '790548586308', '232891840807', '116295093192', '417722652017', '491557514556', '752211425412', '044622796377', '233966641716', '149867961755', '081826788571', '732197023401', '996466182295', '044872349859', '116201929255']
audit_role_name = "AuditIAMRole"

# Create report file
with open('org_iam_user_report.csv', mode='w', newline='') as csv_file:
    fieldnames = [
        'AccountID', 'UserName', 'IsServiceAccount', 'UserCreatedDaysAgo',
        'LastUsedDate', 'HasConsoleAccess', 'HasAccessKeys'
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for account_id in child_account_ids:
        role_arn = f"arn:aws:iam::{account_id}:role/{audit_role_name}"

        # Assume role
        sts = boto3.client('sts')
        try:
            response = sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName='AuditSession'
            )
        except Exception as e:
            print(f"❌ Failed to assume role in {account_id}: {e}")
            continue

        creds = response['Credentials']
        iam = boto3.client(
            'iam',
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken']
        )

        # List IAM users
        paginator = iam.get_paginator('list_users')
        for page in paginator.paginate():
            for user in page['Users']:
                user_name = user['UserName']
                create_date = user['CreateDate']
                now = datetime.now(timezone.utc)
                days_active = (now - create_date).days
                is_service = user_name.startswith('svc_') or user_name.endswith('_svc')

                # Get password last used
                try:
                    user_detail = iam.get_user(UserName=user_name)['User']
                    last_used_date = user_detail.get('PasswordLastUsed')
                except Exception:
                    last_used_date = None

                last_used_str = last_used_date.strftime('%Y-%m-%d') if last_used_date else 'Never'
                has_console_access = last_used_date is not None

                # Check access keys
                try:
                    access_keys = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
                    has_access_keys = len(access_keys) > 0
                except Exception:
                    has_access_keys = False

                writer.writerow({
                    'AccountID': account_id,
                    'UserName': user_name,
                    'IsServiceAccount': is_service,
                    'UserCreatedDaysAgo': days_active,
                    'LastUsedDate': last_used_str,
                    'HasConsoleAccess': has_console_access,
                    'HasAccessKeys': has_access_keys
                })

print("✅ IAM report for org written to org_iam_user_report.csv")
