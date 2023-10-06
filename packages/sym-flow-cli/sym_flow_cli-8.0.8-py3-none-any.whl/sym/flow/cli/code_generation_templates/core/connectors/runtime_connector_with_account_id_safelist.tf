############ Runtime Connector Setup ##############
# The runtime_connector module creates an IAM Role that the Sym Runtime can assume to execute operations in your AWS account.
module "runtime_connector" {
  source  = "symopsio/runtime-connector/aws"
  version = "~> 2.0"

  environment = local.environment_name

  # Allow the Runtime Connector Role to assume IAM Roles in the SSO Account as well.
  account_id_safelist = [data.aws_caller_identity.sso.account_id]
}
