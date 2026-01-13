import yaml
import os
import sys
from jinja2 import Environment, FileSystemLoader

OFFER_FILE = "data/offer_backend_senior.yaml"

offer_name = os.path.splitext(os.path.basename(OFFER_FILE))[0]

build_dir = os.path.join("build", offer_name)
os.makedirs(build_dir, exist_ok=True)

env = Environment(
    loader=FileSystemLoader("templates"),
    variable_start_string="<<",
    variable_end_string=">>",
    block_start_string="<%",
    block_end_string="%>"
)

with open("data/master.yaml") as f:
    master = yaml.safe_load(f)

with open(OFFER_FILE) as f:
    offer = yaml.safe_load(f)

experience = []
for job in master["experience"]:
    bullets = []
    for area in offer["focus"]:
        bullets += job.get(area, [])
    if bullets:
        experience.append({
            "company": job["company"],
            "from": job["from"],
            "to": job["to"],
            "bullets": bullets
        })

template = env.get_template("ats.tex")

rendered = template.render(
    name=master["personal"]["name"],
    title=offer["profile"]["title"],
    location=master["personal"]["location"],
    email=master["personal"]["email"],
    phone=master["personal"]["phone"],
    website=master["personal"]["website"],
    github=master["personal"]["github"],
    linkedin=master["personal"]["linkedin"],
    summary=offer["profile"]["summary"],
    experience=experience
)

tex_path = os.path.join(build_dir, f"{offer_name}.tex")
with open(tex_path, "w", encoding="utf-8") as f:
    f.write(rendered)

print(f"LaTeX generated: {tex_path}")

# Compile
os.system(f"pdflatex -interaction=nonstopmode -output-directory={build_dir} {tex_path}")

print(f"PDF generated in: {build_dir}")
