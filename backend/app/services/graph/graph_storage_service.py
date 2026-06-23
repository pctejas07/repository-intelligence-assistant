import os
import pickle

from app.core.config import settings
from app.core.exceptions import (
    RepositoryNotFoundException
)


class GraphStorageService:

    GRAPH_DIR = "graphs"

    @classmethod
    def initialize(cls):

        os.makedirs(
            cls.GRAPH_DIR,
            exist_ok=True
        )

    @classmethod
    def save_graph(
        cls,
        repository_name: str,
        graph
    ):

        cls.initialize()

        graph_path = os.path.join(
            cls.GRAPH_DIR,
            f"{repository_name}.pkl"
        )

        with open(
            graph_path,
            "wb"
        ) as file:

            pickle.dump(
                graph,
                file
            )

        return graph_path

    @classmethod
    def load_graph(
        cls,
        repository_name: str
    ):

        graph_path = os.path.join(
            cls.GRAPH_DIR,
            f"{repository_name}.pkl"
        )

        if not os.path.exists(
            graph_path
        ):
            raise RepositoryNotFoundException(
                repository_name
            )

        with open(
            graph_path,
            "rb"
        ) as file:

            return pickle.load(
                file
            )

    @classmethod
    def graph_exists(
        cls,
        repository_name: str
    ):

        graph_path = os.path.join(
            cls.GRAPH_DIR,
            f"{repository_name}.pkl"
        )

        return os.path.exists(
            graph_path
        )