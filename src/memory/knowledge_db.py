"""
FN:knowledge_db.py
Knowledge Database - Vector + Graph hybrid memory for Torro Agent.

Classes:
- KnowledgeDB: Hybrid vector-graph knowledge storage and retrieval
- VectorStore: Vector similarity search interface
- GraphStore: Apache AGE graph traversal interface

Functions:
- FN:connect_vector: Connect to pgvector database (lines 45-60)
- FN:connect_graph: Connect to Apache AGE (lines 63-78)
"""

import os
import json
import hashlib
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class KnowledgeNode:
    """Represents a node in the knowledge graph."""
    id: str
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    embeddings: Optional[List[float]] = None


@dataclass
class KnowledgeEdge:
    """Represents an edge in the knowledge graph."""
    id: str
    source_id: str
    target_id: str
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0


class VectorStore:
    """Vector similarity search using pgvector."""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize vector store."""
        self._connection_string = connection_string or os.getenv("DATABASE_URL")
        self._index: Dict[str, KnowledgeNode] = {}
    
    def add(self, node: KnowledgeNode) -> str:
        """
        FN:add_vector
        Add node to vector index.
        
        Args:
            node: Knowledge node with embeddings
            
        Returns:
            Node ID
        """
        if node.embeddings:
            self._index[node.id] = node
        return node.id
    
    def search(self, query_embedding: List[float], limit: int = 5) -> List[KnowledgeNode]:
        """
        FN:search_vector
        Search by vector similarity.
        
        Args:
            query_embedding: Query embedding vector
            limit: Max results to return
            
        Returns:
            List of similar knowledge nodes
        """
        # Simplified cosine similarity search
        results = []
        for node in self._index.values():
            if node.embeddings:
                similarity = self._cosine_similarity(query_embedding, node.embeddings)
                results.append((node, similarity))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return [node for node, _ in results[:limit]]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)


class GraphStore:
    """Apache AGE graph traversal interface."""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize graph store."""
        self._connection_string = connection_string or os.getenv("DATABASE_URL")
        self._nodes: Dict[str, KnowledgeNode] = {}
        self._edges: Dict[str, KnowledgeEdge] = {}
    
    def add_node(self, node: KnowledgeNode) -> str:
        """
        FN:add_node
        Add node to graph.
        
        Args:
            node: Knowledge node to add
            
        Returns:
            Node ID
        """
        self._nodes[node.id] = node
        return node.id
    
    def add_edge(self, edge: KnowledgeEdge) -> str:
        """
        FN:add_edge
        Add edge to graph.
        
        Args:
            edge: Knowledge edge to add
            
        Returns:
            Edge ID
        """
        self._edges[edge.id] = edge
        return edge.id
    
    def traverse(self, start_id: str, max_depth: int = 3) -> List[KnowledgeNode]:
        """
        FN:traverse_graph
        Traverse graph from start node.
        
        Args:
            start_id: Starting node ID
            max_depth: Maximum traversal depth
            
        Returns:
            List of reachable knowledge nodes
        """
        visited = set()
        result = []
        self._dfs(start_id, max_depth, visited, result)
        return result
    
    def _dfs(self, node_id: str, depth: int, visited: set, result: list) -> None:
        """Depth-first search traversal."""
        if node_id in visited or depth < 0:
            return
        
        visited.add(node_id)
        if node_id in self._nodes:
            result.append(self._nodes[node_id])
        
        for edge in self._edges.values():
            if edge.source_id == node_id:
                self._dfs(edge.target_id, depth - 1, visited, result)


class KnowledgeDB:
    """
    Hybrid vector-graph knowledge database.
    
    Combines pgvector for semantic search with Apache AGE
    for logical graph traversal.
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize knowledge database."""
        self._vector_store = VectorStore(connection_string)
        self._graph_store = GraphStore(connection_string)
        self._node_count = 0
        self._edge_count = 0
    
    def add_knowledge(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        FN:add_knowledge
        Add knowledge to both vector and graph stores.
        
        Args:
            content: Knowledge content
            metadata: Additional metadata
            
        Returns:
            Knowledge node ID
        """
        # Generate ID from content hash
        node_id = hashlib.md5(content.encode()).hexdigest()
        
        # Create knowledge node
        node = KnowledgeNode(
            id=node_id,
            label="knowledge",
            properties={
                "content": content,
                **metadata
            }
        )
        
        # Add to both stores
        self._vector_store.add(node)
        self._graph_store.add_node(node)
        
        self._node_count += 1
        return node_id
    
    def search_semantic(self, query: str, limit: int = 5) -> List[KnowledgeNode]:
        """
        FN:search_semantic
        Search knowledge by semantic similarity.
        
        Args:
            query: Search query
            limit: Max results
            
        Returns:
            List of matching knowledge nodes
        """
        # In production, this would use actual embeddings
        # For now, use simple keyword matching
        query_embedding = self._generate_embedding(query)
        return self._vector_store.search(query_embedding, limit)
    
    def search_graph(self, start_id: str, max_depth: int = 3) -> List[KnowledgeNode]:
        """
        FN:search_graph
        Search knowledge by graph traversal.
        
        Args:
            start_id: Starting node ID
            max_depth: Maximum traversal depth
            
        Returns:
            List of connected knowledge nodes
        """
        return self._graph_store.traverse(start_id, max_depth)
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate simple embedding from text (placeholder)."""
        # In production, use actual embedding model
        return [float(ord(c) % 10) for c in text[:100]]
    
    def add_relation(self, source_id: str, target_id: str, relation: str) -> str:
        """
        FN:add_relation
        Add relation between knowledge nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relation: Relation label
            
        Returns:
            Edge ID
        """
        edge_id = f"{source_id}_{target_id}_{relation}"
        edge = KnowledgeEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            label=relation
        )
        self._graph_store.add_edge(edge)
        self._edge_count += 1
        return edge_id
    
    @property
    def stats(self) -> Dict[str, int]:
        """Get database statistics."""
        return {
            "node_count": self._node_count,
            "edge_count": self._edge_count
        }
