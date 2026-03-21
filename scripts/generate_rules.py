import json
import os

def generate_sample_rules():
    rules = {
        "rules": [
            {
                "id": "CUSTOM_1",
                "name": "Custom Rule 1",
                "pattern": "custom_pattern",
                "severity": "Medium",
                "category": "Custom",
                "description": "User-defined custom rule",
                "enabled": True
            }
        ]
    }
    
    os.makedirs("rules", exist_ok=True)
    
    with open("rules/custom_rules.json", "w") as f:
        json.dump(rules, f, indent=2)
    
    print("Generated custom_rules.json")

if __name__ == "__main__":
    generate_sample_rules()
