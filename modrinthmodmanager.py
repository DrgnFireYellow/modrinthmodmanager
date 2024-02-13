import modrinth
import requests
import rich_click as click
import questionary
import os

@click.group
def modrinthmodmanager():
    pass

@modrinthmodmanager.command
@click.argument("query")
def search(query: str):
    results = modrinth.Projects.Search(query).hits
    result_names = []
    for result in results:
        result_names.append(result.name)
    mod = modrinth.Projects.Search(questionary.select("Search Results:", result_names, qmark="🔎").ask()).hits[0]
    versions = mod.versions.copy()
    versions.reverse()
    version_infos = []
    version_names = []
    for version in versions[:5]:
        version_infos.append(mod.getVersion(version))
    for version in version_infos:
        version_names.append(version.name)
    selected_version = questionary.select("Select a version:", version_names, qmark="📂").ask()
    for version in version_infos:
        if version.name == selected_version:
            with open(version.files[0]["filename"], "wb") as modfile:
                modfile.write(requests.get(version.files[0]["url"]).content)

@modrinthmodmanager.command
def delete():
    directory_contents = os.listdir(".")
    mods = []
    for file in directory_contents:
        if file.endswith(".jar") or file.endswith(".zip"):
            mods.append(file)
    file_to_delete = questionary.select("Choose a mod to delete:", mods, qmark="🗑️").ask()
    if questionary.confirm("Are you sure?", False).ask():
        os.remove(file_to_delete)


if __name__ == "__main__":
    modrinthmodmanager()