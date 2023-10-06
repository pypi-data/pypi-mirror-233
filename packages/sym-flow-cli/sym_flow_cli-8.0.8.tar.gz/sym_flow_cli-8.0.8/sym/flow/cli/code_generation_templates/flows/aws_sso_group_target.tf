# Use a data resource to get the existing AWS SSO Group's Group ID
data "aws_identitystore_group" "SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME_SYM_TEMPLATE_VAR_SSO_GROUP_RESOURCE_NAME" {
  provider = aws.sso

  # data.aws_ssoadmin_instances.this is defined in connectors.tf
  identity_store_id = one(data.aws_ssoadmin_instances.this.identity_store_ids)

  alternate_identifier {
    unique_attribute {
      attribute_path  = "DisplayName"
      attribute_value = "SYM_TEMPLATE_VAR_SSO_GROUP_NAME"
    }
  }
}

# An AWS SSO Group target that your Sym Strategy can manage access to
resource "sym_target" "SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME_sso_group_target" {
  type  = "aws_sso_group"
  name  = "SYM_TEMPLATE_VAR_FLOW_NAME-sso-group"
  label = data.aws_identitystore_group.SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME_SYM_TEMPLATE_VAR_SSO_GROUP_RESOURCE_NAME.display_name

  settings = {
    # `type=aws_sso_group` sym_targets have a required setting `group_id`,
    # which must be the AWS SSO Group ID the requester will be escalated to when this target is selected.
    group_id = data.aws_identitystore_group.SYM_TEMPLATE_VAR_FLOW_RESOURCE_NAME_SYM_TEMPLATE_VAR_SSO_GROUP_RESOURCE_NAME.group_id
  }
}
