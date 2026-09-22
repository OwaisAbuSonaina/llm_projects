from utils.brochure_generation import brochure_system_prompt, get_brochure_user_prompt
from utils.client import client

openai = client

def prompt_and_generate_brochure(url: str, company_name: str | None = None) -> dict:
    if not url:
        raise ValueError("URL cannot be empty.")

    # Derive company name if not provided
    name = company_name.strip() if company_name else url.split("//")[-1].split("/")[0].replace("www.", "")

    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(name, url)},
        ],
    )
    content = response.choices[0].message.content

    safe_filename = "".join(c for c in name if c.isalnum() or c in ("-", "_")).rstrip()
    filename = f"{safe_filename or 'company'}_brochure.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "company_name": name,
        "filename": filename,
        "content": content
    }