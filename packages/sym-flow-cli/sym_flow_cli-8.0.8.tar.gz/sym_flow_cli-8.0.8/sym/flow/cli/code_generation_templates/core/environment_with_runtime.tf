resource "sym_environment" "this" {
  name            = local.environment_name
  error_logger_id = sym_error_logger.slack.id
  runtime_id      = module.runtime_connector.sym_runtime.id

  SYM_TEMPLATE_VAR_ENVIRONMENT_INTEGRATIONS
}
