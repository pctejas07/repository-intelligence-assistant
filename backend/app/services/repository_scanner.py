from pathlib import Path


class RepositoryScanner:

    SUPPORTED_EXTENSIONS = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "React",
        ".tsx": "React TypeScript"
    }

    @staticmethod
    def scan_repository(repository_path: str) -> dict:

        repo_path = Path(repository_path)

        if not repo_path.exists():
            raise FileNotFoundError(
                f"Repository not found: {repository_path}"
            )

        files = []
        language_count = {}

        for file in repo_path.rglob("*"):

            if not file.is_file():
                continue

            extension = file.suffix.lower()

            if extension not in RepositoryScanner.SUPPORTED_EXTENSIONS:
                continue

            language = RepositoryScanner.SUPPORTED_EXTENSIONS[extension]

            language_count[language] = (
                language_count.get(language, 0) + 1
            )

            files.append({
                "file_name": file.name,
                "file_path": str(file),
                "language": language
            })

        return {
            "repository_path": str(repo_path),
            "total_supported_files": len(files),
            "language_breakdown": language_count,
            "files": files
        }