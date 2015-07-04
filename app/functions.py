import re

def clean_markdown(raw_md):
    cleanr = re.compile("<.*?>")
    cleaned_md = re.sub(cleanr, "", raw_md)
    return cleaned_md