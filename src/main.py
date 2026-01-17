import click
import sys
# Fix path to ensure imports work when running as script/module
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.loader import load_openapi_spec
from src.differ import compare_specs
from src.scorer import calculate_raw_score, normalize_to_1_10_scale, determine_risk_level_and_action
from src.reporter import generate_report

@click.command()
@click.option('--old', 'old_spec_file', required=True, help='Path to the original OpenAPI specification file.')
@click.option('--new', 'new_spec_file', required=True, help='Path to the new OpenAPI specification file.')
@click.option('--output', 'output_file', help='Path to save the report.')
def main(old_spec_file, new_spec_file, output_file):
    """
    API Breaking Change Risk Vigilance Tool.
    
    Compares two OpenAPI specifications and assigns a risk score (1-10).
    """
    click.echo("Starting API Risk Assessment...\n")
    
    # 1. Load Specs
    old_spec = load_openapi_spec(old_spec_file)
    new_spec = load_openapi_spec(new_spec_file)
    
    if not old_spec or not new_spec:
        click.echo("Failed to load one or both specs. Exiting.")
        sys.exit(1)
        
    # 2. Compare Specs
    click.echo("Comparing specifications...")
    diff_result = compare_specs(old_spec, new_spec)
    
    # 3. Score Changes
    raw_score = calculate_raw_score(diff_result)
    risk_score = normalize_to_1_10_scale(raw_score)
    risk_info = determine_risk_level_and_action(risk_score)
    
    # 4. Generate Report
    report = generate_report(old_spec_file, new_spec_file, risk_score, risk_info, diff_result)
    
    click.echo(report)
    
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            click.echo(f"\nReport saved to {output_file}")
        except Exception as e:
            click.echo(f"Error saving report: {e}")

if __name__ == '__main__':
    main()
