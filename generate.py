import yaml
import os
import requests
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

def escape_latex(text):
    """Escape special LaTeX characters"""
    if not isinstance(text, str):
        return text
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    return text

def _build_links(offer):
    """Build links list from offer config or .env"""
    links = []
    
    # Primero intenta obtener links del YAML de la oferta
    if "links" in offer:
        for link in offer["links"]:
            if isinstance(link, dict) and link.get("url"):
                links.append({
                    "name": link.get("name", "Link"),
                    "url": link["url"]
                })
    else:
        # Si no hay links en oferta, usa los del .env
        link_config = [
            ("Portfolio", "PORTFOLIO"),
            ("GitHub", "GITHUB"),
            ("LinkedIn", "LINKEDIN"),
            ("Itch.io", "ITCH"),
        ]
        for name, env_var in link_config:
            url = os.getenv(env_var)
            if url:
                links.append({"name": name, "url": url})
    
    return links

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
    if not offer_file.endswith((".yaml", ".yml")):
        continue

    offer_path = os.path.join(OFFERS_DIR, offer_file)
    offer_name = os.path.splitext(offer_file)[0]
    safe_name = offer_name.replace(" ", "_")

    try:
        with open(offer_path, encoding="utf-8") as f:
            offer = yaml.safe_load(f)

        build_path = os.path.join(BUILD_DIR, safe_name)
        os.makedirs(build_path, exist_ok=True)

        # --- Get focus skills ---
        skills = offer["focus"].get("skills", [])

        # --- Filter experience ---
        experience = []
        for job in master.get("experience", []):
            if any(r in offer["focus"]["roles"] for r in job["roles"]):
                experience.append(job)

        # --- Download photo ---
        photo_url = os.getenv("PHOTO_URL")
        photo_path = os.path.join(build_path, "profile.jpg")
        photo_tex_path = None

        if photo_url and photo_url.startswith("http"):
            try:
                r = requests.get(photo_url, timeout=5)
                if r.status_code == 200:
                    with open(photo_path, "wb") as img:
                        img.write(r.content)
                    photo_tex_path = "profile.jpg"
            except Exception as e:
                print(f"  Warning: Could not download photo: {e}")

        rendered = template.render(
            name=escape_latex(os.getenv("NAME")),
            headline=escape_latex(offer["profile"].get("headline", master.get("personal", {}).get("headline", ""))),
            title=escape_latex(offer["profile"]["title"]),
            location=escape_latex(os.getenv("LOCATION")),
            email=escape_latex(os.getenv("EMAIL")),
            phone=escape_latex(os.getenv("PHONE")),
            photo=photo_tex_path,
            links=_build_links(offer),
            summary=escape_latex(offer["profile"]["summary"]),
            skills=[escape_latex(s) for s in skills],
            experience=experience,
            projects=master.get("projects") if offer["show"].get("projects") else None,
            talks=master.get("talks") if offer["show"].get("talks") else None,
            certifications=master.get("certifications"),
            education=master.get("education")
        )

        tex_path = os.path.join(build_path, f"{safe_name}.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        os.system(f'pdflatex -interaction=nonstopmode -output-directory="{build_path}" "{tex_path}"')

        print(f"Generated build/{safe_name}/{safe_name}.pdf")
        
    except Exception as e:
        print(f"Error processing {offer_file}: {e}")

print("All CVs generated.")
