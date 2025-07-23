# 📘 AWS-Org-Security

A security audit toolkit for AWS Organizations.
This repository contains scripts to **automate cross-account IAM audits** across all member accounts within an AWS Organization. It includes security relevant inventory of EC2, S3, RDS and Secrets Manager

---

## 💾 1. Overview

This project helps you:

1. 🚀 Deploy an **IAM role (AuditIAMRole)** to all member accounts using AWS CloudFormation StackSets.
2. 🔐 Allow the **management account** to assume the audit role.
3. 🕵️‍♂️ Run a **Python script to audit IAM users** across all accounts.
4. 📊 Output a **CSV report** of IAM users, login methods, and access key usage.

---

## 📋 2. Prerequisites

### 2.1 Required Knowledge

* Familiarity with **AWS Organizations**, **IAM**, and **CloudFormation StackSets**
* Basic usage of **AWS CLI** and **Python**

### 2.2 Tools Required

| Tool             | Version / Requirement                     |
| ---------------- | ----------------------------------------- |
| AWS CLI          | v2.x                                      |
| Python           | 3.7+                                      |
| `boto3`          | Installed via `pip install boto3`         |
| AWS Organization | Service-Managed StackSets must be enabled |

---

## 🛠️ 3. Deployment Steps

### 3.1 Clone the Repository

```bash
git clone https://github.com/Gumbeoketch/AWS-Org-Security.git
cd AWS-Org-Security
```

---

### 3.2 Update Template Parameter

Edit `audit-iam-role.yaml` and set your actual **AWS Management Account ID** under:

```yaml
Parameters:
  ManagementAccountId:
    Type: String
    Description: The AWS account ID of the Organizations management account
```

---

### 3.3 Deploy the IAM Role via StackSet

Make the script executable and run it:

```bash
chmod +x deploy_audit_role.sh
./deploy_audit_role.sh
```

> ⚠️ This will create a StackSet and deploy the IAM role to accounts within the specified OU and region (defaults to `eu-west-1`).

---

### 3.4 Verify StackSet Deployment

1. List StackSet operations:

```bash
aws cloudformation list-stack-set-operations \
  --stack-set-name AuditIAMRoleStackSet2
```

2. Then verify a specific operation using its `operation-id`:

```bash
aws cloudformation describe-stack-set-operation \
  --stack-set-name AuditIAMRoleStackSet2 \
  --operation-id <operation-id>
```

---

## 🧪 4. Running the Audit Script

### 4.1 Configure the Python Script

Open `org_iam_user_report.py` and update:

* Replace `child_account_ids` with your actual **AWS account IDs**.
* Ensure `audit_role_name` matches the StackSet role name (`AuditIAMRole` by default).

---

### 4.2 Run the Script

```bash
python3 org_iam_user_report.py
```

✅ This will:

* Assume the IAM role in each member account
* Collect IAM user data (including service accounts, access key usage, login method, etc.)
* Save results to a file: `org_iam_user_report.csv`

---

## 📌 5. Notes

* The IAM role includes permissions for:

  * IAM
  * EC2
  * S3
  * RDS
  * Secrets Manager
* You can extend these permissions in `audit-iam-role.yaml`.

---

## 🧼 6. Clean Up

To remove the deployed StackSet and instances:

```bash
aws cloudformation delete-stack-instances \
  --stack-set-name AuditIAMRoleStackSet2 \
  --regions eu-west-1 \
  --deployment-targets OrganizationalUnitIds=["r-nbug"] \
  --no-retain-stacks

aws cloudformation delete-stack-set \
  --stack-set-name AuditIAMRoleStackSet2
```

---

## 👤 Author

**Michael Oketch**
GitHub: [@Gumbeoketch](https://github.com/Gumbeoketch)

---
