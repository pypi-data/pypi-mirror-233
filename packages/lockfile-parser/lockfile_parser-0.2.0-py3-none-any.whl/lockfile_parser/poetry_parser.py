import toml

class PoetryLockParser:
    """
    A parser for Python's poetry.lock files.
    
    Provides methods to query and analyze dependencies and their sources.
    """

    def __init__(self, path: str):
        """
        Initialize the parser with the path to a poetry.lock file.
        
        Args:
            path (str): Path to the poetry.lock file.
        """
        with open(path, 'r') as f:
            self.data = toml.load(f)
        self.package_map = {pkg['name']: pkg for pkg in self.data.get('package', [])}

    def get_version(self, package_name: str) -> str:
        """
        Get the version of a specific package.
        
        Args:
            package_name (str): Name of the package.
        
        Returns:
            str: Version of the package or None if package not found.
        """
        pkg = self.package_map.get(package_name)
        return pkg['version'] if pkg else None

    def get_dependencies(self, package_name: str) -> list:
        """
        Get the dependencies of a specific package.
        
        Args:
            package_name (str): Name of the package.
        
        Returns:
            list: List of dependencies or None if package not found.
        """
        pkg = self.package_map.get(package_name)
        return list(pkg.get('dependencies', {}).keys()) if pkg else None

    def get_parent_dependencies(self, package_name: str) -> list:
        """
        Get the parent dependencies of a specific package.
        
        Args:
            package_name (str): Name of the package.
        
        Returns:
            list: List of parent dependencies.
        """
        return [name for name, pkg in self.package_map.items() if package_name in pkg.get('dependencies', {})]

    def get_non_pypi_packages(self) -> dict:
        """
        Get a structured dictionary of non-PyPI packages with unique versions.
        
        Returns:
            dict: Dictionary with the structure:
                  {package_name: {'version': version, 'source': source_type}}
        """
        non_pypi = {}
        for name, pkg in self.package_map.items():
            if 'source' in pkg and pkg['source']['type'] != 'pypi':
                non_pypi[name] = {
                    'version': pkg['version'],
                    'source': pkg['source']['type'],
                    'url': pkg['source']['url']
                }
        return non_pypi
