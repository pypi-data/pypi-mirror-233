import importlib.resources as pkg_resources
import re
from abc import ABC

import hcl2

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation_templates import (  # import the *package* containing the tf files
    core,
)
from sym.flow.cli.helpers.code_generation.core import FlowGeneration
from sym.flow.cli.helpers.terraform import get_terraform_resource


class AWSFlowGeneration(FlowGeneration, ABC):
    """A superclass containing common utility methods needed for generating AWS-strategies"""

    REQUIRES_AWS: bool = True
    INTEGRATIONS_REGEX = r"integrations\s+=\s+\{[^\}]+\}"

    def _add_runtime_id_to_environment(self):
        # Parse the environment.tf file to see if we need to append a sym_runtime
        with open(self.environment_tf_filepath, "r") as f:
            # Parse the file into a dict, including line numbers
            environment_tf = hcl2.load(f, with_meta=True)

        if not (sym_environment := get_terraform_resource(environment_tf, "sym_environment", "this")):
            cli_output.fail(
                "The sym_environment.this resource is missing in environment.tf",
                hint=f"To manually configure this resource, check out https://docs.symops.com/docs/aws",
            )

        if not sym_environment.get("runtime_id"):
            # Add the runtime_id to the sym_environment
            with open(self.environment_tf_filepath, "r+") as f:
                environment_tf_lines = f.readlines()

                # Indices to slice the environment.tf into the contents before/after the sym_environment resource
                sym_environment_start = sym_environment["__start_line__"] - 1
                sym_environment_end = sym_environment["__end_line__"]

                # Slice the existing file into contents before and after the sym_environment resource.
                before_sym_environment = environment_tf_lines[0:sym_environment_start]
                existing_sym_environment = environment_tf_lines[sym_environment_start:sym_environment_end]
                after_sym_environment = environment_tf_lines[sym_environment_end:]

                # Get the existing integrations block
                if regex_match := re.search(self.INTEGRATIONS_REGEX, "".join(existing_sym_environment)):
                    integrations_block = regex_match[0]
                else:
                    # For some reason there was no integrations block, so default to just the slack_id
                    integrations_block = "integrations = {\n    slack_id = sym_integration.slack.id\n  }"

                # Generate a sym_environment block with runtime_id defined
                sym_environment_with_runtime = pkg_resources.read_text(core, "environment_with_runtime.tf")
                sym_environment_with_runtime = self._format_template(
                    sym_environment_with_runtime,
                    {
                        "SYM_TEMPLATE_VAR_ENVIRONMENT_INTEGRATIONS": integrations_block,
                    },
                )

                # Ensure the file pointer is pointing to the beginning of the file
                f.seek(0)

                # Write the file contents before the sym_environment resource as-is
                for line in before_sym_environment:
                    f.write(line)

                # Write the new new sym_environment resource, containing the runtime_id
                f.write(sym_environment_with_runtime)

                # Write the file contents after the sym_environment resource as-is
                for line in after_sym_environment:
                    f.write(line)

                # Truncate any trailing text after our file pointer to ensure that the file contains only the
                # contents that we just wrote.
                f.truncate()
