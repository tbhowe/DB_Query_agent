from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel
import os

class WriteReportArgsSchema(BaseModel):
    """Schema for the arguments of the write_report tool."""
    file_name: str
    html: str


def write_report(file_name, html):
    """Writes an HTML report to a file.

    Args:
        filename (str): The file path to write the HTML report to.
        html (str): The HTML report to write to the file.
    """
    current_script_dir = os.path.dirname(__file__)
    reports_dir = os.path.join(current_script_dir, '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    file_path = os.path.join(reports_dir, file_name)
    with open(file_path, "w") as f:
        f.write(html)

write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML report to a file. Use this tool whenever someone asks for a report.",
    func=write_report,
    args_schema=WriteReportArgsSchema
)