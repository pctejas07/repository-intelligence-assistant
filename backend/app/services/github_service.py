from pathlib import Path
from git import Repo

from app.core.config import settings
from app.core.logger import logger


class GitHubService:

    @staticmethod
    def extract_repo_name(repo_url: str) -> str:
        """
        Example:
        https://github.com/spring-projects/spring-petclinic.git

        Returns:
        spring-petclinic
        """
        repo_name = repo_url.rstrip("/").split("/")[-1]

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        return repo_name

    @staticmethod
    def clone_repository(repo_url: str) -> dict:

        logger.info(
            f"Cloning repository: {repo_url}"
        )

        repo_name = GitHubService.extract_repo_name(
            repo_url
        )

        repo_path = settings.REPOSITORY_PATH / repo_name

        repo_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if repo_path.exists():

            logger.info(
                f"Repository already exists: {repo_name}"
            )

            return {
                "status": "already_exists",
                "repository_name": repo_name,
                "repository_path": str(repo_path)
            }

        Repo.clone_from(
            repo_url,
            repo_path
        )

        logger.info(
            f"Repository cloned: {repo_name}"
        )

        return {
            "status": "cloned",
            "repository_name": repo_name,
            "repository_path": str(repo_path)
        }