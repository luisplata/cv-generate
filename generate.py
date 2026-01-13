import yaml
import os
from jinja2 import Environment, FileSystemLoader

MASTER_FILE = "data/master/master.yaml"
OFFERS_DIR = "data/offers"
BUILD_DIR = "build"

os.makedirs(BUILD_DIR, exist_ok=True)

env = Environment(
    loader=FileSystemLoader("templates"),
    variable_start_string="<<",
    variable_end_string=">>",
    block_start_string="<%",
    block_end_string="%>"
)

# Load master
with open(MASTER_FILE, encoding="utf-8") as f:
    master = yaml.safe_load(f)

# Load template
template = env.get_template("ats.tex")

# Process every offer
for offer_file in os.listdir(OFFERS_DIR):
    if not offer_file.endswith(".yaml"):
        continue

    offer_path = os.path.join(OFFERS_DIR, offer_file)
    offer_name = os.path.splitext(offer_file)[0]

    print(f"Processing {offer_name}...")

    with open(offer_path, encoding="utf-8") as f:
        offer = yaml.safe_load(f)

    build_path = os.path.join(BUILD_DIR, offer_name)
    os.makedirs(build_path, exist_ok=True)

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

    tex_path = os.path.join(build_path, f"{offer_name}.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    os.system(f"pdflatex -interaction=nonstopmode -output-directory={build_path} {tex_path}")

    print(f"Generated: {build_path}/{offer_name}.pdf")

print("All offers processed.")
