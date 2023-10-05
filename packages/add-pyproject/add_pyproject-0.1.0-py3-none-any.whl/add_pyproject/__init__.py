# SPDX-FileCopyrightText: 2023-present Keto D. Zhang <ketozhang@gmail.com>
#
# SPDX-License-Identifier: MIT
import tomlkit


def main(packages: list[str]):
    """Adds packages to pyproject.toml"""
    with open("pyproject.toml", "rt", encoding="utf-8") as f:
        pyproject = tomlkit.load(f)

    for package in packages:
        print(f"Adding {package} to pyproject.toml")
        pyproject["project"]["dependencies"].append(package)

    with open("pyproject.toml", "w", encoding="utf-8") as f:
        tomlkit.dump(pyproject, f)
