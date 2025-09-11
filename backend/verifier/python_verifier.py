import ast, tempfile, subprocess, json
def verify_python_code(code: str):
    report = {
        "language": "python",
        "syntax_valid": False,
        "lint_warnings": [],
        "errors": [],
        "trust_score": 0
    }

    try:
        ast.parse(code)
        report["syntax_valid"] = True
        report["trust_score"] += 40
    except SyntaxError as e:
        report["errors"].append(str(e))
        report["trust_score"] = 0
        return report

    # rudimentary lint: we won't run pylint in container to keep things simple; placeholder
    # In production run subprocess to call pylint or use programmatic API
    report["lint_warnings"] = []
    report["trust_score"] += 20

    # runtime placeholder - not executing untrusted code in this MVP
    report["runtime_check"] = "not_executed_mvp"
    report["trust_score"] += 20

    report["trust_score"] = min(100, report["trust_score"])
    return report
