from glob import glob


def to_import_path(path):
    return path.replace('/', '.').replace('\\', '.').replace('.py', '')


fixtures = glob('**/tests/**/fixtures/[!_]*.py', recursive=True)

pytest_plugins = [
    to_import_path(fixture) for fixture in fixtures
]
