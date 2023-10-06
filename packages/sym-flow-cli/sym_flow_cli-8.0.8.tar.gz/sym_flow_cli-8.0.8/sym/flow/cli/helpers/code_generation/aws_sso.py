import importlib.resources as pkg_resources
import sys
from pathlib import Path
from typing import Optional

import click
import hcl2
import inquirer

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import flows
from sym.flow.cli.helpers.terraform import get_terraform_module

from .aws import AWSFlowGeneration


class AWSSSOFlowGeneration(AWSFlowGeneration):
    SYM_SSO_PROFILE = "sym-sso-provisioning"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Ensure that they have an SSO Profile that will work with the generated aws_sso_connector.tf
        if not self.has_sym_sso_provisioning_profile():
            cli_output.error(
                f"To generate an AWS SSO Flow, an AWS profile named '{self.SYM_SSO_PROFILE}' with permissions "
                "to create an IAM role in your AWS SSO management account is required. Please generate one with:"
            )
            cli_output.actionable(f"aws configure sso --profile {self.SYM_SSO_PROFILE}")
            sys.exit(1)

        # We just want one newline before we start prompting, not a newline each time we re-prompt.
        click.echo("")

        # Define these attributes to be populated based on the target types selected by the user.
        self.permission_set_name: Optional[str] = None
        self.account_id: Optional[str] = None
        self.sso_group_name: Optional[str] = None
        self.sso_group_resource_name: Optional[str] = None

        self.target_types = inquirer.list_input(
            "How would you like to manage your AWS SSO Users?",
            choices=[
                ("AWS SSO Permission Sets", ["aws_sso_permission_set"]),
                ("AWS SSO Groups", ["aws_sso_group"]),
                ("A mix of AWS SSO Permission Set Assignments and Groups", ["aws_sso_permission_set", "aws_sso_group"]),
            ],
        )

        if "aws_sso_permission_set" in self.target_types:
            self.permission_set_name = click.prompt(
                f'{click.style("What is the name of the AWS SSO permission set you would like to assign to users?", bold=True)} '
                f'{click.style("(e.g. AdminAccess)", dim=True, italic=True)}',
                type=str,
            )

            self.account_id = click.prompt(
                f'{click.style(f"What AWS Account ID is this permission set provisioned to?", bold=True)}',
                type=str,
                prompt_suffix="",
            )

        if "aws_sso_group" in self.target_types:
            self.sso_group_name = click.prompt(
                f'{click.style("What is the name of the AWS SSO group you would like to escalate users to?", bold=True)} '
                f'{click.style("(e.g. My SSO Group)", dim=True, italic=True)}',
                type=str,
            )

            # SSO Group names can contain spaces. Replace the spaces with underscores so we can use the group name
            # in the TF resource name
            self.sso_group_resource_name = self.sso_group_name.replace(" ", "_").lower()

        self.aws_region: Optional[str] = self._get_aws_region()

    def has_sym_sso_provisioning_profile(self) -> bool:
        """Returns True if the user already has a profile named sym-sso-provisioning"""
        try:
            with open(Path.home() / ".aws/config", "r") as aws_config_file:
                aws_config = aws_config_file.read()

            return "profile sym-sso-provisioning" in aws_config
        except FileNotFoundError:
            # If `.aws/config doesn't exist, return false
            return False

    @property
    def impl_filepath(self) -> str:
        return f"{self.working_directory}/impls/aws_sso_{self.flow_resource_name}_impl.py"

    @classmethod
    def get_flow_tf_filepath(cls, flow_name: str, working_directory: str = ".") -> str:
        return f"{working_directory}/aws_sso_{cls._get_flow_resource_name(flow_name)}.tf"

    def generate(self) -> None:
        """Generate the impl and Terraform files required to configure an AWS SSO Flow."""
        # Generate any core requirements that don't already exist in this directory.
        self._append_connector_module("runtime_connector")
        self._create_impls_directory()
        self._add_runtime_id_to_environment()

        # Generate the AWS SSO specific files.
        self._append_connector_module("sso_connector")
        self._add_sso_account_id_safelist()

        self._generate_impl()

        with open(self.flow_tf_filepath, "w") as f:
            aws_sso_targets = []
            aws_sso_target_ids = []

            if "aws_sso_permission_set" in self.target_types:
                aws_sso_permission_set_target_tf = self._format_template(
                    pkg_resources.read_text(flows, "aws_sso_permission_set_target.tf"),
                    {
                        "SYM_TEMPLATE_VAR_PERMISSION_SET_NAME": self.permission_set_name,
                        "SYM_TEMPLATE_VAR_ACCOUNT_ID": self.account_id,
                    },
                )
                aws_sso_targets.append(aws_sso_permission_set_target_tf)
                aws_sso_target_ids.append(f"sym_target.{self.flow_resource_name}_permission_set_target.id")

            if "aws_sso_group" in self.target_types:
                aws_sso_group_target_tf = self._format_template(
                    pkg_resources.read_text(flows, "aws_sso_group_target.tf"),
                    {
                        "SYM_TEMPLATE_VAR_SSO_GROUP_NAME": self.sso_group_name,
                        "SYM_TEMPLATE_VAR_SSO_GROUP_RESOURCE_NAME": self.sso_group_resource_name,
                    },
                )
                aws_sso_targets.append(aws_sso_group_target_tf)
                aws_sso_target_ids.append(f"sym_target.{self.flow_resource_name}_sso_group_target.id")

            aws_sso_tf = self._format_template(
                pkg_resources.read_text(flows, "aws_sso.tf"),
                {
                    "SYM_TEMPLATE_VAR_AWS_SSO_TARGETS": "\n".join(aws_sso_targets),
                    "SYM_TEMPLATE_VAR_AWS_SSO_SYM_TARGET_IDS": ", ".join(aws_sso_target_ids),
                },
            )
            f.write(aws_sso_tf)

    def _add_sso_account_id_safelist(self) -> None:
        """Parses the connectors.tf file and adds the account ID safelist input to the runtime_connector module
        if it does not yet exist
        """

        # Open the file in Read + Write mode
        with open(self.connectors_tf_filepath, "r+") as f:
            # Parse the existing connectors.tf into a dict, including line numbers
            connectors_tf = hcl2.load(f, with_meta=True)

            # The runtime_connector module is guaranteed to exist, because we append it at the beginning of the
            # generation if it does not yet exist.
            runtime_connector = get_terraform_module(connectors_tf, "runtime_connector")

            # If the runtime_connector does not have the account_id_safelist input already defined, then we
            # will want to replace the module with one that defines the SSO Account in the account_id_safelist
            # and re-write the file.
            if not runtime_connector.get("account_id_safelist"):
                # Read the file as an array of lines
                f.seek(0)
                connector_tf_lines = f.readlines()

                # The array index of the closing bracket of the runtime_connector module.
                runtime_connector_end = runtime_connector["__end_line__"] - 1

                # We want to insert the `account_id_safelist` right before the closing bracket of the module.
                # Slice the file to get the contents before and after the closing bracket
                before_closing_bracket = connector_tf_lines[0:runtime_connector_end]
                closing_bracket_and_after = connector_tf_lines[runtime_connector_end:]
                account_id_safelist_lines = [
                    "  # Allow the Runtime Connector Role to assume IAM Roles in the SSO Account as well.\n",
                    "  account_id_safelist = [data.aws_caller_identity.sso.account_id]\n",
                ]

                # Insert the account_id_safelist lines before the end of the runtime_connector module closing bracket
                # and reconstruct the connectors.tf file.
                updated_connectors_tf = before_closing_bracket + account_id_safelist_lines + closing_bracket_and_after

                # Ensure the file pointer is pointing to the beginning of the file
                f.seek(0)

                # Write the updated contents to connectors.tf
                for line in updated_connectors_tf:
                    f.write(line)

                # Truncate any trailing text after our file pointer to ensure that the file contains only the
                # contents that we just wrote.
                # See: https://stackoverflow.com/questions/6648493/how-to-open-a-file-for-both-reading-and-writing#comment100583908_15976014
                f.truncate()
