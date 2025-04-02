from langchain.tools import StructuredTool
from pydantic import BaseModel

def write_report(filename, html):
    print(f"Writing report to {filename}...")
    # Ensure the filename ends with .html
    if not filename.endswith('.html'):
        filename += '.html'
    with open(filename, 'w') as f:
        f.write(html)
    print(f"Report successfully written to {filename}")
    return f"Report successfully written to {filename}"


class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str
    
    
write_report_tool = StructuredTool.from_function(
    func=write_report,
    name="write_report",
    args_schema=WriteReportArgsSchema,
    description="Write an HTML file to disk. The filename should be the name of the report file to create, and html should be the complete HTML content of the report. ALWAYS use this tool when asked to create or write a report.",
)