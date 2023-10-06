from pydantic import BaseModel


class MovedBlock(BaseModel):
    """A Pydantic model representing a Terraform `moved` block.
    https://developer.hashicorp.com/terraform/language/modules/develop/refactoring#moved-block-syntax
    """

    moved_from: str
    moved_to: str

    def to_terraform(self) -> str:
        """Converts this model to a Terraform moved block"""
        return f"""
moved {{
  from = {self.moved_from}
  to   = {self.moved_to}
}}
"""
