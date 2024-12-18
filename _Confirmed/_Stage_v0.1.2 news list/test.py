import json

# Load the config.json file
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Load the html_pattern.json file
with open("html_patterns.json", "r", encoding="utf-8") as pattern_file:
    html_pattern = json.load(pattern_file)

# Iterate through websites in config and html_pattern to add data sources
for website in html_pattern["websites"]:
    site_id = website["site_id"]

    # Find corresponding website in config.json
    matching_site = next(
        (site for site in config["websites"] if site["site_id"] == site_id), None
    )

    if matching_site:
        data_sources = {item["name"]: item["source"] for item in matching_site["data_to_scrape"]}

        # Add source to each field in the patterns
        for field, details in website["patterns"].items():
            if field in data_sources:
                details["source"] = data_sources[field]

# Save the updated html_pattern.json
with open("html_pattern_updated.json", "w", encoding="utf-8") as updated_pattern_file:
    json.dump(html_pattern, updated_pattern_file, ensure_ascii=False, indent=2)

print("html_pattern_updated.json has been created with added data sources.")
