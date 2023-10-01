import toml
import re

class CargoLockParser:
    """
    A parser for Rust's Cargo.lock files.
    
    Provides methods to query and analyze dependencies and their sources.
    """

    def __init__(self, path: str):
        """
        Initialize the parser with the path to a Cargo.lock file.
        
        Args:
            path (str): Path to the Cargo.lock file.
        """
        with open(path, 'r') as f:
            self.data = toml.load(f)
        self.package_map = {pkg['name']: pkg for pkg in self.data['package']}

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
        return [dep.split(' ', 1)[0] for dep in pkg.get('dependencies', [])] if pkg else None

    def get_parent_dependencies(self, package_name: str) -> list:
        """
        Get the parent dependencies of a specific package.
        
        Args:
            package_name (str): Name of the package.
        
        Returns:
            list: List of parent dependencies.
        """
        return [name for name, pkg in self.package_map.items() if package_name in [dep.split(' ', 1)[0] for dep in pkg.get('dependencies', [])]]

    def get_non_crates_io_packages(self) -> dict:
        """
        Get a structured dictionary of non-crates.io packages with unique commits.
        
        Returns:
            dict: Nested dictionary with the structure:
                  {remote: {group: {repo: {'branches' or 'tags': {branch or tag: [commits]}}}}}
        """
        non_crates_io = {}
        
        # Regex to extract components from the source URL
        pattern = re.compile(r'(?P<protocol>.*://)(?P<remote>[^/]+)/(?P<group>[^/]+)/(?P<repo>[^?#]+)(?:\?branch=(?P<branch>[^#]+))?(?:\?tag=(?P<tag>[^#]+))?#(?P<commit>.*)')
        
        for _, pkg in self.package_map.items():
            source = pkg.get('source')
            if source and not source.startswith('registry+https://github.com/rust-lang/crates.io-index'):
                match = pattern.match(source)
                if match:
                    components = match.groupdict()
                    # Build the nested dictionary structure with sets for unique commits
                    repo_dict = non_crates_io \
                        .setdefault(components['remote'], {}) \
                        .setdefault(components['group'], {}) \
                        .setdefault(components['repo'], {}) \
                        .setdefault('branches' if components['branch'] else 'tags', {})
                    commits = repo_dict.setdefault(components['branch'] or components['tag'], set())
                    commits.add(components['commit'])
        
        # Convert sets back to lists for ordered commits
        for _, groups in non_crates_io.items():
            for _, repos in groups.items():
                for _, types in repos.items():
                    for _, branches_or_tags in types.items():
                        for branch_or_tag, commits in branches_or_tags.items():
                            branches_or_tags[branch_or_tag] = list(commits)
        
        return non_crates_io
