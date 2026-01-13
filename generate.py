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

# Get languages from .env
languages = os.getenv("LANGUAGES", "es").split(",")
languages = [lang.strip() for lang in languages]

env = Environment(
    loader=FileSystemLoader("templates"),
    variable_start_string="<<",
    variable_end_string=">>",
    block_start_string="<%",
    block_end_string="%>"
)

with open(MASTER_FILE, encoding="utf-8") as f:
    master = yaml.safe_load(f)

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

        # --- Download photo (una sola vez) ---
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

        # Determine if offer has multi-language support
        is_multilang = isinstance(offer["profile"], dict) and any(lang in offer["profile"] for lang in languages)

        # Generate PDF for each language
        for lang in languages:
            # Skip if offer doesn't support this language
            if is_multilang and lang not in offer["profile"]:
                continue

            # Load template for this language
            template_name = f"ats_{lang}.tex" if os.path.exists(os.path.join("templates", f"ats_{lang}.tex")) else "ats.tex"
            template = env.get_template(template_name)

            # Get language-specific content
            if is_multilang:
                title = offer["profile"][lang]["title"]
                summary = offer["profile"][lang]["summary"]
                skills = offer["focus"]["skills"].get(lang, [])
            else:
                # Fallback to non-multilang structure
                title = offer["profile"]["title"]
                summary = offer["profile"]["summary"]
                skills = offer["focus"].get("skills", [])

            # --- Filter experience ---
            experience = []
            for job in master.get("experience", []):
                if any(r in offer["focus"]["roles"] for r in job["roles"]):
                    # Translate experience to target language
                    job_copy = job.copy()
                    if isinstance(job.get("period"), dict):
                        job_copy["period"] = job["period"].get(lang, job["period"].get("es", ""))
                    if isinstance(job.get("achievements"), dict):
                        job_copy["achievements"] = job["achievements"].get(lang, job["achievements"].get("es", []))
                    experience.append(job_copy)

            # Translate projects
            projects = None
            if offer["show"].get("projects") and master.get("projects"):
                projects = []
                for proj in master.get("projects", []):
                    proj_copy = proj.copy()
                    if isinstance(proj.get("name"), dict):
                        proj_copy["name"] = proj["name"].get(lang, proj["name"].get("es", ""))
                    if isinstance(proj.get("description"), dict):
                        proj_copy["description"] = proj["description"].get(lang, proj["description"].get("es", ""))
                    projects.append(proj_copy)

            # Translate education
            education = None
            if master.get("education"):
                education = []
                for edu in master.get("education", []):
                    edu_copy = edu.copy()
                    if isinstance(edu.get("year"), dict):
                        edu_copy["year"] = edu["year"].get(lang, edu["year"].get("es", ""))
                    education.append(edu_copy)

            rendered = template.render(
                name=escape_latex(os.getenv("NAME")),
                headline=escape_latex(master.get("personal", {}).get("headline", "")),
                title=escape_latex(title),
                location=escape_latex(os.getenv("LOCATION")),
                email=escape_latex(os.getenv("EMAIL")),
                phone=escape_latex(os.getenv("PHONE")),
                photo=photo_tex_path,
                links=_build_links(offer),
                summary=escape_latex(summary),
                skills=[escape_latex(s) for s in skills],
                experience=experience,
                projects=projects,
                talks=master.get("talks") if offer["show"].get("talks") else None,
                certifications=master.get("certifications"),
                education=education
            )

            # Generate file names with language suffix
            lang_suffix = f"_{lang}" if is_multilang else ""
            tex_path = os.path.join(build_path, f"{safe_name}{lang_suffix}.tex")
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            os.system(f'pdflatex -interaction=nonstopmode -output-directory="{build_path}" "{tex_path}"')

            print(f"Generated build/{safe_name}/{safe_name}{lang_suffix}.pdf")
        
    except Exception as e:
        print(f"Error processing {offer_file}: {e}")

print("All CVs generated.")
