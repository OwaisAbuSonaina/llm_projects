from brochure_generation import brochure_system_prompt, get_brochure_user_prompt
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key")

MODEL = "gpt-5-nano"
openai = OpenAI()

def prompt_and_generate_brochure():
    print("\n" + "="*50)
    print("      COMPANY BROCHURE GENERATOR")
    print("="*50)
    print("Please enter the full URL of the website you'd like")
    print("to generate a brochure for (e.g., https://example.com).\n")
    
    url = input("Enter website URL: ").strip()
    if not url:
        print("Error: No URL provided. Aborting.")
        return

    company_name = input("Enter the company name (optional, press Enter to derive from URL): ").strip()
    if not company_name:
        company_name = url.split("//")[-1].split("/")[0].replace("www.", "")

    print(f"\nGenerating brochure for {company_name}...")
    
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
    )
    content = response.choices[0].message.content

    safe_filename = "".join(c for c in company_name if c.isalnum() or c in ("-", "_")).rstrip()
    filename = f"{safe_filename or 'company'}_brochure.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nSuccess! Brochure saved as '{filename}' in the current folder.\n")
