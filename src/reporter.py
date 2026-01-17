from src.scorer import get_change_score

def generate_report(old_file_path, new_file_path, risk_score, risk_info, differences):
    # pylint: disable=unused-argument
    """Generate a text report for the CLI or PR comment."""

    if isinstance(differences, list):
        diff_list = differences
    else:
        diff_list = differences.get('differences', [])

    report = []
    report.append(f"{risk_info['emoji']} API Risk Score: {risk_score}/10")
    report.append(f"Risk Level: {risk_info['risk_level']}")
    report.append(f"Summary: {risk_info['message']}")
    report.append("Recommended Actions:")
    report.append(f"{risk_info['reviewer_action']}")
    report.append("\nChanges Detected:")

    if not diff_list:
        report.append("No API changes detected.")
    else:
        for change in diff_list:
            change_type = change.get('type', 'unknown')
            score = get_change_score(change_type)
            path = change.get('path', 'unknown path')
            method = change.get('method', '')

            icon = "[!]" if score > 0 else "[OK]"
            report.append(f"- {icon} {change_type} ({score} pts): {method} {path}")

    return "\n".join(report)
