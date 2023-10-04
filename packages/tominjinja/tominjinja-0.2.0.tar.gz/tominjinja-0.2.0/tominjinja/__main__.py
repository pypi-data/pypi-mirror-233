from argparse import ArgumentParser
from jinja2 import Template
from toml import loads
from pathlib import Path
from rich_argparse import RichHelpFormatter


def render_template(config_path: Path, template_path: Path) -> str:
    template = Template(source=template_path.read_text())
    config = loads(config_path.read_text())
    return template.render(config)

argparser = ArgumentParser(
    prog="tominjinja", 
    description="Renders a Jinja template with variables from TOML configuration file.",
    epilog="Returns the result to standard output.",
    formatter_class=RichHelpFormatter
)
argparser.add_argument("config_path", type=Path, help="TOML configuration file path.")
argparser.add_argument("template_path", type=Path, help="Jinja template file path.")
args = argparser.parse_args()

result = render_template(args.config_path, args.template_path)
print(result)