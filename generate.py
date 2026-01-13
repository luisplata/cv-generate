import yaml
import os
import requests
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

MASTER_FILE = "data/master/master.yaml"
OFFERS_DIR = "data/offers"
BUILD_DIR = "build"

env = Environment(
    loader=FileSystemLoader("templates"),
    variable_start_string="<<",
    variable_end_string=">>",
    block_start_string="<%",
    block_end_string="%>"
)

with open(MASTER_FILE, encoding="utf-8") as f:
    master = yaml.safe_load(f)

template = env.get_template("ats.tex")

os.makedirs(BUILD_DIR, exist_ok=True)

for offer_file in os.listdir(OFFERS_DIR):
    if not offer_file.endswith(".yaml"):
        continue

    offer_path = os.path.join(OFFERS_DIR, offer_file)
    offer_name = os.path.splitext(offer_file)[0]
    safe_name = offer_name.replace(" ", "_")


    with open(offer_path, encoding="utf-8") as f:
        offer = yaml.safe_load(f)

    build_path = os.path.join(BUILD_DIR, safe_name)
    os.makedirs(build_path, exist_ok=True)

    # --- Get focus skills ---
    skills = offer["focus"].get("skills", [])

    # --- Filter experience ---
    experience = []
    for job in master["experience"]:
        if any(r in offer["focus"]["roles"] for r in job["roles"]):
            experience.append(job)

    # --- Download photo ---
    photo_url = os.getenv("PHOTO_URL")
    photo_path = os.path.join(build_path, "profile.jpg")

    if photo_url and photo_url.startswith("http"):
        r = requests.get(photo_url)
        with open(photo_path, "wb") as img:
            img.write(r.content)

    # LaTeX-safe relative path
    photo_tex_path = "profile.jpg"

    rendered = template.render(
        name=os.getenv("NAME"),
        headline=offer["profile"].get("headline", master.get("personal", {}).get("headline", "")),
        title=offer["profile"]["title"],
        location=os.getenv("LOCATION"),
        email=os.getenv("EMAIL"),
        phone=os.getenv("PHONE"),
        photo=photo_tex_path,
        portfolio=os.getenv("PORTFOLIO"),
        github=os.getenv("GITHUB"),
        linkedin=os.getenv("LINKEDIN"),
        itch=os.getenv("ITCH"),
        summary=offer["profile"]["summary"],
        skills=skills,
        experience=experience,
        projects=master.get("projects") if offer["show"]["projects"] else None,
        talks=master.get("talks") if offer["show"]["talks"] else None,
        certifications=master.get("certifications"),
        education=master.get("education")
    )

    tex_path = os.path.join(build_path, f"{safe_name}.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    os.system(f'pdflatex -interaction=nonstopmode -output-directory="{build_path}" "{tex_path}"')

    print(f"Generated build/{safe_name}/{safe_name}.pdf")

print("All CVs generated.")
