import json
from datetime import datetime
import os

def safe_load_json(file_path, fallback=None):
    """Load JSON safely and return fallback if not found or invalid."""
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return fallback or {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Could not decode JSON: {file_path}")
        return fallback or {}

# Paths
aurora_path = "AuroraSync.json"
holdings_path = "Holdings.json"
dividends_path = "Dividends.json"

# Load data
aurora_data = safe_load_json(aurora_path, {})
holdings_data = safe_load_json(holdings_path, [])
dividends_data = safe_load_json(dividends_path, [])

# Insert feeds into main AuroraSync
aurora_data["isa_feed"] = holdings_data
aurora_data["dividends_feed"] = dividends_data

# Update integrity section
aurora_data.setdefault("integrity", {})
aurora_data["integrity"]["last_validated"] = datetime.utcnow().isoformat()
aurora_data["integrity"]["is_valid"] = True

# Save updated AuroraSync.json
with open(aurora_path, "w", encoding="utf-8") as f:
    json.dump(aurora_data, f, indent=2, ensure_ascii=False)

print("✅ AuroraSync.json updated successfully with new Holdings and Dividends data.")
