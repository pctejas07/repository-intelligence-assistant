from app.models.graph import (
    GraphNode,
    GraphEdge
)

from app.models.chunk import (
    CodeChunk
)


class GraphBuilder:

    @staticmethod
    def build(
        chunks: list[CodeChunk]
    ):

        nodes = []

        edges = []

        node_ids = set()

        for chunk in chunks:

            GraphBuilder._build_chunk_graph(
                chunk,
                nodes,
                edges,
                node_ids
            )

        return {
            "nodes": nodes,
            "edges": edges
        }

    @staticmethod
    def _build_chunk_graph(
        chunk,
        nodes,
        edges,
        node_ids
    ):

        # Current chunk node

        if chunk.name not in node_ids:

            nodes.append(
                GraphNode(
                    id=chunk.name,
                    node_type=chunk.chunk_type,
                    name=chunk.name,
                    language=chunk.language,
                    file_path=chunk.file_path
                )
            )

            node_ids.add(
                chunk.name
            )

        # Method belongs to class

        if chunk.parent_class:

            GraphBuilder._add_node(
                chunk.parent_class,
                "class",
                nodes,
                node_ids
            )

            edges.append(
                GraphEdge(
                    source=chunk.parent_class,
                    target=chunk.name,
                    relation="contains"
                )
            )
            
             # Method calls other methods

            if chunk.chunk_type == "method":

                for called_method in chunk.calls:

                    target_method = (
                        f"{chunk.parent_class}."
                        f"{called_method}"
                    )

                    GraphBuilder._add_node(
                        target_method,
                        "method",
                        nodes,
                        node_ids
                    )

                    edges.append(
                        GraphEdge(
                            source=chunk.name,
                            target=target_method,
                            relation="calls"
                        )
                    )

        # Only CLASS chunks create
        # extends / implements / imports

        if chunk.chunk_type in (
            "classs",
            "interface"
        ):

            # Extends

            if chunk.extends:

                GraphBuilder._add_node(
                    chunk.extends,
                    "class",
                    nodes,
                    node_ids
                )

                edges.append(
                    GraphEdge(
                        source=chunk.name,
                        target=chunk.extends,
                        relation="extends"
                    )
                )

            # Implements

            for interface in chunk.implements:

                GraphBuilder._add_node(
                    interface,
                    "interface",
                    nodes,
                    node_ids
                )

                edges.append(
                    GraphEdge(
                        source=chunk.name,
                        target=interface,
                        relation="implements"
                    )
                )

            # Imports

            for imported in chunk.imports:

                GraphBuilder._add_node(
                    imported,
                    "import",
                    nodes,
                    node_ids
                )

                edges.append(
                    GraphEdge(
                        source=chunk.name,
                        target=imported,
                        relation="imports"
                    )
                )

    @staticmethod
    def _add_node(
        node_name,
        node_type,
        nodes,
        node_ids
    ):

        if node_name in node_ids:

            return

        nodes.append(
            GraphNode(
                id=node_name,
                node_type=node_type,
                name=node_name
            )
        )

        node_ids.add(
            node_name
        )