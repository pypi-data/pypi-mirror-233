from typing import Literal, List
from pydantic import BaseModel


class PostgresConfig(BaseModel):
    """
    Postgres data source configuration.

    Attributes:
        url: Postgres connection URL.
        table: Postgres table name.
    """

    url: str
    table: str


class MongoConfig(BaseModel):
    """
    Mongo data source configuration.

    Attributes:
        url: Mongo connection URL.
        collection: Mongo collection name.
    """

    url: str
    collection: str


class DataSource(BaseModel):
    """
    Data source configuration.

    Attributes:
        type: Data source type.
        config: Data source configuration. Can be PostgresConfig or MongoConfig.
        fields: Fields to index.
    """

    type: Literal["postgres", "mongo"]
    config: PostgresConfig or MongoConfig
    fields: List[str]


class ProjectConfig(BaseModel):
    """
    Project configuration.

    Attributes:
        data_source: Data source configuration.
        vector_db: Vector database to use.
        embedding_model: Embedding model to use.
    """

    data_source: DataSource
    vector_db: Literal["milvus", "pinecone"]
    embedding_model: Literal["text-embedding-ada-002", "all-MiniLM-L6-v2"]


class Project(BaseModel):
    """
    Project details.

    Attributes:
        id: Project ID.
        config: Project configuration.
    """

    id: str
    config: ProjectConfig


class SearchResult(BaseModel):
    """
    Search result.

    Attributes:
        id: Document ID.
        score: Search score.
    """

    id: str
    score: float
