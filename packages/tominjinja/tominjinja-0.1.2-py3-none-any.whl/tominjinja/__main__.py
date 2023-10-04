from argparse import ArgumentParser
from jinja2 import Template
from toml import loads
from pathlib import Path


def render_template(config_path: Path, template_path: Path) -> str:
    template = Template(source=template_path.read_text())
    config = loads(config_path.read_text())
    return template.render(config)

argparser = ArgumentParser()
argparser.add_argument("config_path", type=Path)
argparser.add_argument("template_path", type=Path)
args = argparser.parse_args()

result = render_template(args.config_path, args.template_path)
print(result)