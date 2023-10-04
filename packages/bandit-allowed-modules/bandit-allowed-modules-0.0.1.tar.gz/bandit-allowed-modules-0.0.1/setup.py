from setuptools import find_packages, setup

setup(
    name="bandit-allowed-modules",
    version="0.0.1",
    description="Ban all modules except the allowed ones.",
    long_description="A bandit plugin that will Ban all modules except the allowed ones.",
    # url="....",
    packages=["bandit_plugins"],
    author="Asad Iqbal",
    install_requires=[
        "bandit",
    ],
    entry_points={
        "bandit.plugins": [
            "allowed_modules = bandit_plugins.allow_selected_modules:allow_selected"
        ],
    },
)
