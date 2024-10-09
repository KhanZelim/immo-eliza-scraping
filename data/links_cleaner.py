import xml.etree.ElementTree as ET

tree = ET.parse("./raw_links/classifieds-000.xml")
root = tree.getroot()

ns = {
    "default": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xhtml": "http://www.w3.org/1999/xhtml"
}

unique_links = set()

for url in root.findall("default:url", ns):
    for link in url.findall("xhtml:link", ns):
        if link.attrib.get("hreflang") == "en-BE":
            unique_links.add(link.attrib["href"])

with open("./clean_links/classifieds-000.xml", "w") as clean_links:
    for unique_link in unique_links:
        clean_links.write(unique_link)
        clean_links.write("\n")