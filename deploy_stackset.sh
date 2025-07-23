#!/bin/bash

# === Configuration ===
STACK_SET_NAME="AuditIAMRoleStackSet2"
TEMPLATE_FILE="audit-iam-role.yaml"
MGMT_ACCOUNT_ID="$MasterAccountID"
OU_ID="$RootAccountID" # aws organizations list-roots
REGION="eu-west-1"

# === Step 1: Create the StackSet ===
echo "📦 Creating StackSet: $STACK_SET_NAME ..."
aws cloudformation create-stack-set \
  --stack-set-name "$STACK_SET_NAME" \
  --template-body "file://$TEMPLATE_FILE" \
  --capabilities CAPABILITY_NAMED_IAM \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --parameters ParameterKey=ManagementAccountId,ParameterValue=$MGMT_ACCOUNT_ID

# === Step 2: List Organization Root (for reference/debugging) ===
echo "🧭 Listing AWS Organization roots ..."
aws organizations list-roots

# === Step 3: Deploy Stack Instances to specific OU ===
echo "🚀 Deploying StackSet instances to OU $OU_ID ..."
aws cloudformation create-stack-instances \
  --stack-set-name "$STACK_SET_NAME" \
  --deployment-targets OrganizationalUnitIds=["$OU_ID"] \
  --regions "$REGION" \
  --operation-preferences FailureToleranceCount=0,MaxConcurrentCount=1

# === Optional Step: Wait briefly or guide user to fetch operation ID ===
echo "⏳ Waiting for StackSet operation to start..."
sleep 5
echo "🔎 Fetch the latest operation ID using describe-stack-set-operations:"
echo "aws cloudformation list-stack-set-operations --stack-set-name $STACK_SET_NAME"

# === Step 4: Verify Deployment ===
echo ""
echo " To verify deployment, run the command below once you have the Operation ID:"
echo "aws cloudformation describe-stack-set-operation \\"
echo "  --stack-set-name $STACK_SET_NAME \\"
echo "  --operation-id <paste-operation-id-here>"
