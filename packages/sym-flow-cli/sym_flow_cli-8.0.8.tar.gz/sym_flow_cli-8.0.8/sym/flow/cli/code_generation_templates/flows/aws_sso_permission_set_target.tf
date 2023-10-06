# Use a data resource to get the existing permission set's ARN
data "aws_ssoadmin_permission_set" "SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME_SYM_TEMPLATE_VAR_PERMISSION_SET_NAME" {
  provider = aws.sso

  # data.aws_ssoadmin_instances.this is defined in connectors.tf
  instance_arn = one(data.aws_ssoadmin_instances.this.arns)
  name         = "SYM_TEMPLATE_VAR_PERMISSION_SET_NAME"
}

# An AWS SSO Permission Set Assignment target that your Sym Strategy can manage access to
resource "sym_target" "SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME_permission_set_target" {
  type = "aws_sso_permission_set"

  name  = "SYM_TEMPLATE_VAR_FLOW_NAME-permission-set"
  label = "SYM_TEMPLATE_VAR_PERMISSION_SET_NAME"

  settings = {
    # `type=aws_sso_permission_set` sym_targets need both an AWS Permission Set
    # ARN and an AWS Account ID to make an SSO account assignment.
    permission_set_arn = data.aws_ssoadmin_permission_set.SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME_SYM_TEMPLATE_VAR_PERMISSION_SET_NAME.arn
    account_id         = "SYM_TEMPLATE_VAR_ACCOUNT_ID"
  }
}
