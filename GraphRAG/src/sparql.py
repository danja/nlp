"""Sparql graph store index."""

# right now is a do-nothing machine

import json
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import fsspec
# from dataclasses_json import DataClassJsonMixin

from llama_index.graph_stores.types import (
    DEFAULT_PERSIST_DIR,
    DEFAULT_PERSIST_FNAME,
    GraphStore,
)

logger = logging.getLogger(__name__)


@dataclass
class SparqlGraphStore(GraphStore):
    """Sparql Graph Store Connector"""

    graph_dict: Dict[str, List[List[str]]] = field(default_factory=dict)

    def get_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2
    ) -> Dict[str, List[List[str]]]:
        """Get subjects' rel map in max depth."""
        if subjs is None:
            subjs = list(self.graph_dict.keys())
        rel_map = {}
        for subj in subjs:
            rel_map[subj] = self._get_rel_map(subj, depth=depth)
        return rel_map

    def _get_rel_map(self, subj: str, depth: int = 2) -> List[List[str]]:
        """Get one subect's rel map in max depth."""
        if depth == 0:
            return []
        rel_map = []
        if subj in self.graph_dict:
            for rel, obj in self.graph_dict[subj]:
                rel_map.append([subj, rel, obj])
                rel_map += self._get_rel_map(obj, depth=depth - 1)
        return rel_map

# see SimpleGraphStoreData


class SparqlGraphStore(GraphStore):
    """Sparql Graph Store.


    Args:
        Sparql_graph_store_data_dict (Optional[dict]): data dict
            containing the triplets. See SparqlGraphStoreData
            for more details.
    """

    def __init__(
        self,
        data: Optional[SparqlGraphStoreData] = None,
        fs: Optional[fsspec.AbstractFileSystem] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        self._data = data or SparqlGraphStoreData()
        self._fs = fs or fsspec.filesystem("file")

    @classmethod
    def from_persist_dir(
        cls,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> "SparqlGraphStore":
        """Load from persist dir."""
        persist_path = os.path.join(persist_dir, DEFAULT_PERSIST_FNAME)
        return cls.from_persist_path(persist_path, fs=fs)

    @property
    def client(self) -> None:
        """Get client.
        Not applicable for this store.
        """
        return None

    def get(self, subj: str) -> List[List[str]]:
        """Get triplets."""
        return self._data.graph_dict.get(subj, [])

    def get_rel_map(
        self, subjs: Optional[List[str]] = None, depth: int = 2
    ) -> Dict[str, List[List[str]]]:
        """Get depth-aware rel map."""
        return self._data.get_rel_map(subjs=subjs, depth=depth)

    def upsert_triplet(self, subj: str, rel: str, obj: str) -> None:
        """Add triplet."""
        if subj not in self._data.graph_dict:
            self._data.graph_dict[subj] = []
        if (rel, obj) not in self._data.graph_dict[subj]:
            self._data.graph_dict[subj].append([rel, obj])

    def delete(self, subj: str, rel: str, obj: str) -> None:
        """Delete triplet."""
        if subj in self._data.graph_dict:
            if (rel, obj) in self._data.graph_dict[subj]:
                self._data.graph_dict[subj].remove([rel, obj])
                if len(self._data.graph_dict[subj]) == 0:
                    del self._data.graph_dict[subj]

    def persist(
        self,
        persist_path: str = os.path.join(
            DEFAULT_PERSIST_DIR, DEFAULT_PERSIST_FNAME),
        fs: Optional[fsspec.AbstractFileSystem] = None,
    ) -> None:
        """Persist the SparqlGraphStore to a directory."""
        fs = fs or self._fs
        dirpath = os.path.dirname(persist_path)
        if not fs.exists(dirpath):
            fs.makedirs(dirpath)

        with fs.open(persist_path, "w") as f:
            json.dump(self._data.to_dict(), f)

    def get_schema(self, refresh: bool = False) -> str:
        """Get the schema of the Sparql Graph store."""
        raise NotImplementedError(
            "SparqlGraphStore does not support get_schema")

    def query(self, query: str, param_map: Optional[Dict[str, Any]] = {}) -> Any:
        """Query the Sparql Graph store."""
        raise NotImplementedError("SparqlGraphStore does not support query")

    @classmethod
    def from_persist_path(
        cls, persist_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
    ) -> "SparqlGraphStore":
        """Create a SparqlGraphStore from a persist directory."""
        fs = fs or fsspec.filesystem("file")
        if not fs.exists(persist_path):
            logger.warning(
                f"No existing {__name__} found at {persist_path}. "
                "Initializing a new graph_store from scratch. "
            )
            return cls()

        logger.debug(f"Loading {__name__} from {persist_path}.")
        with fs.open(persist_path, "rb") as f:
            data_dict = json.load(f)
            data = SparqlGraphStoreData.from_dict(data_dict)
        return cls(data)

    @classmethod
    def from_dict(cls, save_dict: dict) -> "SparqlGraphStore":
        data = SparqlGraphStoreData.from_dict(save_dict)
        return cls(data)

    def to_dict(self) -> dict:
        return self._data.to_dict()
