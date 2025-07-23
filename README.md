# AWS-Org-Security
script that should come in handy for AWS Organizational Units

Overview
Creates an IAM role (AuditIAMRole) in all member accounts via StackSet.

Allows the management account to assume this role.

Performs IAM audits across all member accounts using a Python script.

Outputs a CSV report on IAM users, access methods, and usage metrics.

Prerequisites
Knowledge
Familiarity with AWS Organizations, IAM, and CloudFormation StackSets.

AWS CLI and Python 3 installed.

🔧 Tools Required
Tool	Version/Requirement
AWS CLI	v2.x
Python	3.7+
boto3	Installed via pip install boto3
AWS Org Setup	With Service-Managed StackSets enabled

Deployment Steps
git clone https://github.com/Gumbeoketch/AWS-Org-Security.git
cd AWS-Org-Security

Update the ManagementAccountId parameter to your AWS Org Management Account ID

chmod +x deploy_audit_role.sh
./deploy_audit_role.sh

Verify StackSet Deployment

aws cloudformation list-stack-set-operations \
  --stack-set-name AuditIAMRoleStackSet2
Then use the returned operation-id:


aws cloudformation describe-stack-set-operation \
  --stack-set-name AuditIAMRoleStackSet2 \
  --operation-id <operation-id>

Running the Audit Script
Edit org_iam_user_report.py:

Replace the list of child_account_ids with your own AWS account IDs.

Ensure that audit_role_name matches the role name in the StackSet (AuditIAMRole).
python3 org_iam_user_report.py

