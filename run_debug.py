import sys
import os

# Ensure path
sys.path.append(os.getcwd())

from src.main import main
from click.testing import CliRunner

runner = CliRunner()
print("Invoking main via CliRunner...")
result = runner.invoke(main, ['--old', 'tests/sample_old.yaml', '--new', 'tests/sample_new.yaml'])

print(f"Exit Code: {result.exit_code}")
print("--- STDOUT ---")
print(result.output)
print("--- EXCEPTION ---")
if result.exception:
    print(result.exception)
