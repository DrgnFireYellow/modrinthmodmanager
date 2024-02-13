import modrinth
import requests
import click
import questionary

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
    

if __name__ == "__main__":
    modrinthmodmanager()