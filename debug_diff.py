from deepdiff import DeepDiff
import yaml
import pprint

def load(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

old = load('tests/sample_old.yaml')
new = load('tests/sample_new.yaml')

ddiff = DeepDiff(old, new, ignore_order=True)
pprint.pprint(ddiff, width=200)
