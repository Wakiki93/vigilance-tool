from deepdiff import DeepDiff
import yaml
import json
import os

# Helper to convert set to list for JSON serialization
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        # DeepDiff defines custom objects for paths, we might need to stringify them
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

def load(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

print("Loading specs...")
old = load('tests/sample_old.yaml')
new = load('tests/sample_new.yaml')

print("Running DeepDiff...")
# Using the exact same settings as differ.py
ddiff = DeepDiff(old, new, ignore_order=True, view='tree')

# extract the raw dict for inspection (tree view objects are complex, so we might want text view for the dump)
# Let's dump both text view and tree view keys
ddiff_text = DeepDiff(old, new, ignore_order=True) # default view

print("Dumping to deepdiff_dump.json...")
with open('deepdiff_dump.json', 'w') as f:
    json.dump(ddiff_text, f, cls=SetEncoder, indent=2)

print("Dump complete. Check deepdiff_dump.json")
