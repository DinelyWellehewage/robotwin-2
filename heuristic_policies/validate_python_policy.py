import ast
import sys
from pathlib import Path


ALLOWED_CTX_METHODS = {
    "select_arm",
    "approach_actor",
    "move_relative",
    "check_success",
}


FORBIDDEN_NAMES = {
    "task",
    "robot",
    "scene",
    "open",
    "exec",
    "eval",
    "__import__",
}


class PolicyValidator(ast.NodeVisitor):
    """
    Static validator for generated heuristic Python policies.

    The policy must use only the restricted `ctx` interface.
    """

    def __init__(self):
        self.errors = []
        self.policy_function_count = 0

    def error(self, node, message):
        line = getattr(node, "lineno", "?")
        self.errors.append(f"line {line}: {message}")

    def visit_Import(self, node):
        self.error(node, "imports are not allowed")

    def visit_ImportFrom(self, node):
        self.error(node, "imports are not allowed")

    def visit_FunctionDef(self, node):
        if node.name == "policy":
            self.policy_function_count += 1

            if len(node.args.args) != 1 or node.args.args[0].arg != "ctx":
                self.error(
                    node,
                    "policy must have exactly one argument named ctx",
                )
        else:
            self.error(
                node,
                f"unsupported function definition: {node.name}",
            )

        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in FORBIDDEN_NAMES:
            self.error(
                node,
                f"forbidden name: {node.id}",
            )

        self.generic_visit(node)

    def visit_Call(self, node):
        # Only calls of the form ctx.<allowed_method>(...) are permitted.
        if not isinstance(node.func, ast.Attribute):
            self.error(
                node,
                "only ctx.<method>(...) calls are allowed",
            )
        else:
            attr = node.func

            if not (
                isinstance(attr.value, ast.Name)
                and attr.value.id == "ctx"
                and attr.attr in ALLOWED_CTX_METHODS
            ):
                self.error(
                    node,
                    "unsupported method call",
                )

        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Attribute access is allowed only for the approved ctx methods.
        if isinstance(node.ctx, ast.Load):
            if not (
                isinstance(node.value, ast.Name)
                and node.value.id == "ctx"
                and node.attr in ALLOWED_CTX_METHODS
            ):
                self.error(
                    node,
                    "direct attribute access is not allowed",
                )

        self.generic_visit(node)


def validate_python_policy(path):
    source = Path(path).read_text()

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"syntax error: {exc}") from exc

    validator = PolicyValidator()
    validator.visit(tree)

    if validator.policy_function_count != 1:
        validator.errors.append(
            "policy file must contain exactly one function named policy"
        )

    if validator.errors:
        raise ValueError("\n".join(validator.errors))

    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_python_policy.py POLICY.py")
        raise SystemExit(2)

    try:
        validate_python_policy(sys.argv[1])
    except ValueError as exc:
        print("INVALID")
        print(exc)
        raise SystemExit(1)

    print("VALID")


if __name__ == "__main__":
    main()
