"""
Context Engineering Module

This module provides comprehensive context engineering infrastructure for agents,
formalizing context as a graph of connections to enable meaningful agent
understanding and memory. It integrates RAG with knowledge graphs to provide
persistent context for intelligent agents.

Key Features:
    - Context graph construction from entities and relationships
    - Agent memory management with RAG integration
    - Entity linking across sources with URI assignment
    - Hybrid context retrieval (vector + graph + memory)
    - Conversation history management
    - Context accumulation and synthesis
    - Graph-based context traversal and querying

Main Classes:
    - ContextGraphBuilder: Builds context graphs from various sources
    - AgentMemory: Manages persistent agent memory with RAG
    - EntityLinker: Links entities across sources with URIs
    - ContextRetriever: Retrieves relevant context from multiple sources

Example Usage:
    >>> from semantica.context import ContextGraphBuilder, AgentMemory
    >>> builder = ContextGraphBuilder()
    >>> graph = builder.build_from_entities_and_relationships(entities, relationships)
    >>> memory = AgentMemory(vector_store=vs, knowledge_graph=kg)
    >>> memory_id = memory.store("User asked about Python", metadata={"type": "conversation"})
    >>> results = memory.retrieve("Python", max_results=5)

Author: Semantica Contributors
License: MIT
"""

from .context_graph import ContextGraphBuilder, ContextNode, ContextEdge
from .entity_linker import EntityLinker, EntityLink, LinkedEntity
from .agent_memory import AgentMemory, MemoryItem
from .context_retriever import ContextRetriever, RetrievedContext

__all__ = [
    "ContextGraphBuilder",
    "ContextNode",
    "ContextEdge",
    "EntityLinker",
    "EntityLink",
    "LinkedEntity",
    "AgentMemory",
    "MemoryItem",
    "ContextRetriever",
    "RetrievedContext",
]
