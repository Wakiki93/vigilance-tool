import sys
import subprocess

def run_checks():
    print("Running QA Checks...")

    # 1. Run Unit Tests
    print("\n[1/2] Running Unit Tests...")
    test_result = subprocess.run(
        [sys.executable, '-m', 'unittest', 'discover', 'tests'],
        capture_output=False,
        check=False
    )

    if test_result.returncode != 0:
        print("❌ Unit Tests Failed!")
        sys.exit(1)
    print("✅ Unit Tests Passed")

    # 2. Run Linter
    print("\n[2/2] Running Linter (pylint)...")
    # We ignore some errors for the prototype speed (e.g. strict docstrings)
    linter_result = subprocess.run(
        [sys.executable, '-m', 'pylint', 'src', '--disable=C0111,C0103'],
        capture_output=False,
        check=False
    )

    # Pylint returns a bitmask. 0 is perfect.
    # For now, we allow some linting issues but warn.
    if linter_result.returncode != 0:
        print("⚠️  Linter found issues. Please review output above.")
        # Optional: sys.exit(1) if strict
    else:
        print("✅ Linter Clean")

    print("\n🎉 QA Checks Complete!")

if __name__ == "__main__":
    run_checks()
