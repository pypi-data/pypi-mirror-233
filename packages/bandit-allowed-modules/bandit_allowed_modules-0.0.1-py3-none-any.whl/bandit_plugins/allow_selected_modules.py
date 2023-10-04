import bandit
from bandit.core import issue
from bandit.core import test_properties as test


def starts_with_allowed_module(input_str, allowed_modules):
    for module in allowed_modules:
        if input_str == module or input_str.startswith(module + "."):
            return True
    return False


@test.checks("Import")
@test.checks("Call")
@test.test_id("TBT001")
def allow_selected(context):
    # Define a list of modules that make network requests
    allowed_modules = ["tensorflow", "torch", "torchvision", "math"]

    imported = context._context["imports"]
    import_aliases = context._context["import_aliases"]

    for module in imported:
        if not starts_with_allowed_module(module, allowed_modules):
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                text=f"Import of [{module}] other than {allowed_modules} not allowed.",
            )
