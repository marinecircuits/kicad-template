import os
import re
import sys


def sanitize_project_name(name):
    """Sanitize project name to contain only A-Z, a-z, 0-9, _ and -."""
    sanitized = re.sub(r"[^A-Za-z0-9_-]+", "_", name)  # replace invalid chars
    sanitized = re.sub(r"__+", "_", sanitized)  # collapse multiple underscores
    sanitized = sanitized.strip("_-")  # remove leading/trailing _ or -
    sanitized = sanitized.lower()  # convert to lowercase
    if not sanitized:
        raise ValueError("Project name cannot be empty after sanitization.")
    if sanitized != name:
        print(f"Sanitized project name: '{name}' → '{sanitized}'")
    return sanitized


def update_kicad_comment(file_path, project_name):
    """Update (comment 8 "...") line in a KiCad file to the project name."""
    if not os.path.exists(file_path):
        print(f"Skipped (not found): {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the comment 8 line
    new_content, count = re.subn(
        r'\(comment 8\s+".*?"\)', f'(comment 8 "{project_name}")', content
    )

    if count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated (comment 8) in {file_path}")
    else:
        print(f"No (comment 8) found in {file_path}, skipping update")


def setup_template(project_name):
    project_name = sanitize_project_name(project_name)

    # 1. Rename KiCad template files
    extensions = [".kicad_pcb", ".kicad_sch", ".kicad_pro"]
    renamed_files = []
    for ext in extensions:
        old_name = f"template{ext}"
        new_name = f"{project_name}{ext}"
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            print(f"Renamed: {old_name} → {new_name}")
            renamed_files.append(new_name)
        else:
            print(f"Skipped (not found): {old_name}")

    # 2. Update (comment 8) in KiCad files
    for file_path in renamed_files:
        update_kicad_comment(file_path, project_name)

    # 3. Remove CHANGELOG.md
    changelog_path = "CHANGELOG.md"
    if os.path.exists(changelog_path):
        os.remove(changelog_path)
        print(f"Removed: {changelog_path}")
    else:
        print(f"Skipped (not found): {changelog_path}")

    # 4. Update version in .cz.toml
    cz_path = ".cz.toml"
    if os.path.exists(cz_path):
        with open(cz_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace version value in a TOML key like: version = "x.y.z"
        new_content = re.sub(
            r'version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"', 'version = "0.0.1"', content
        )

        with open(cz_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated version in {cz_path} to 0.0.1")
    else:
        print(f"Skipped (not found): {cz_path}")


if __name__ == "__main__":
    script_name = os.path.basename(sys.argv[0])

    if len(sys.argv) != 2:
        print(f"Usage: python {script_name} <project_name>")
        print()
        print("Sets up a new KiCad project from a template by:")
        print("  - Renaming template.kicad_* files to <project_name>")
        print("  - Updating (comment 8 ...) fields to match <project_name>")
        print("  - Removing CHANGELOG.md")
        print("  - Resetting version in .cz.toml to 0.0.1")
        sys.exit(1)

    project_name = sys.argv[1]
    try:
        setup_template(project_name)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
