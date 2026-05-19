import os
import re

directory = "/home/salmarina/Faucetguru_site/blog-content-final/"
files = [f for f in os.listdir(directory) if f.endswith(".md")]

issues = []

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Metadata check
    if not (content.startswith("---\n") and "title:" in content and "description:" in content):
        issues.append(f"{filename}: Missing metadata (Title/Description).")

    # 2. H1 check
    if not re.search(r"^#\s+", content, re.MULTILINE):
        issues.append(f"{filename}: Missing H1 header.")

    # 3. H2 check (Conclusion)
    if not re.search(r"^##\s+(Conclusión|Conclusion)", content, re.IGNORECASE | re.MULTILINE):
        issues.append(f"{filename}: Missing Conclusion H2.")

    # 4. FAQ check (5+)
    # FAQs often start with **? or similar. Let's count bolded questions or lines with ?
    # Let's assume FAQ is under ## FAQ or ## Preguntas frecuentes
    faq_section = re.search(r"##\s+(FAQ|Preguntas Frecuentes)([\s\S]*?)(##|$)", content, re.IGNORECASE)
    if faq_section:
        faqs = re.findall(r"^\*\*(.*?)\?\*\*", faq_section.group(2), re.MULTILINE)
        if len(faqs) < 5:
            # Maybe they are not bolded? Let's check for lines with ?
            faqs_lines = re.findall(r"^\d*\.?\s*.*\?", faq_section.group(2), re.MULTILINE)
            if len(faqs_lines) < 5:
                issues.append(f"{filename}: Insufficient FAQs (found {len(faqs) + len(faqs_lines)}).")
    else:
        issues.append(f"{filename}: Missing FAQ section.")

    # 5. Internal Links check
    links = re.findall(r"\[.*?\]\(\./(.*?)\)", content)
    for link in links:
        if not os.path.exists(os.path.join(directory, link)):
            issues.append(f"{filename}: Broken internal link: {link}")

for issue in issues:
    print(issue)
