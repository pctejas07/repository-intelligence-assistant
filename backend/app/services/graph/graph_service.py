import networkx as nx

from app.services.graph.graph_builder import (
    GraphBuilder
)


class GraphService:

    @staticmethod
    def build_graph(
        chunks
    ):

        graph_data = (
            GraphBuilder.build(
                chunks
            )
        )

        graph = (
            nx.MultiDiGraph()
        )

        # Add nodes

        for node in (
            graph_data["nodes"]
        ):

            graph.add_node(
                node.id,
                node_type=node.node_type,
                name=node.name,
                language=node.language,
                file_path=node.file_path
            )

        # Add edges

        for edge in (
            graph_data["edges"]
        ):

            graph.add_edge(
                edge.source,
                edge.target,
                relation=edge.relation
            )

        return graph

    @staticmethod
    def get_dependencies(
        graph,
        node_name: str
    ):

        if not graph.has_node(
            node_name
        ):

            return []

        return list(
            graph.successors(
                node_name
            )
        )

    @staticmethod
    def get_dependents(
        graph,
        node_name: str
    ):

        if not graph.has_node(
            node_name
        ):

            return []

        return list(
            graph.predecessors(
                node_name
            )
        )

    @staticmethod
    def get_node_info(
        graph,
        node_name: str
    ):

        if not graph.has_node(
            node_name
        ):

            return None

        return graph.nodes[
            node_name
        ]

    @staticmethod
    def get_all_nodes(
        graph
    ):

        return list(
            graph.nodes()
        )

    @staticmethod
    def get_all_edges(
        graph
    ):

        return list(
            graph.edges(
                data=True
            )
        )