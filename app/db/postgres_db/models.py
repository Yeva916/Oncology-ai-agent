from sqlalchemy import JSON,Column, Enum, Float, ForeignKey, Integer, String,func,Index,Text,cast,Computed,literal_column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB,TSVECTOR
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.schemas.util import TaskStatus
from .session import Base

SEARCH_LANG = literal_column("'english'")
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    raw_query = Column(String, nullable=False)
    structured_response = Column(JSON, nullable=False)
    status : Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, values_callable=lambda obj: [e.value for e in obj]),
        default=TaskStatus.PENDING.value,
    )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, nullable=False)
    query_id = Column(Integer, ForeignKey("queries.id",ondelete="CASCADE"), nullable=False)
    final_text = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    clinical_significance = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    sources = Column(JSON, nullable=False)

class logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, nullable=False)
    query_id = Column(Integer, ForeignKey("queries.id",ondelete="CASCADE"), nullable=False)
    module_name = Column(String, nullable=False)
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, nullable=False)
    error_message = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class ClinicalTrial(Base):
    __tablename__ = "clinical_trials"
    id = Column(Integer, primary_key=True, nullable=False)
    nct_id = Column(String, nullable=False, unique=True)
    brief_title = Column(String, nullable=False)
    interventions = Column(JSONB, nullable=True)
    brief_summary = Column(String, nullable=True)
    conditions = Column(JSONB, nullable=True)
    eligibility_criteria = Column(JSONB, nullable=True) # amendments Strings -> JSON
    phases = Column(String, nullable=True)
    locations = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    search_vector = Column(
        TSVECTOR,
        Computed(
            func.setweight(func.to_tsvector(SEARCH_LANG, func.coalesce(brief_title, '')), 'C').op('||')(
                func.setweight(func.to_tsvector(SEARCH_LANG, func.coalesce(cast(conditions, Text), '')), 'A')
            ).op('||')(
                func.setweight(func.to_tsvector(SEARCH_LANG, func.coalesce(brief_summary, '')), 'D')
            ).op('||')(
                func.setweight(func.to_tsvector(SEARCH_LANG, func.coalesce(eligibility_criteria['criteria'].as_string(), '')), 'B')
            ),
            persisted=True
        )
    )
    
    __table_args__ = (
        Index('ix_clinical_trials_search_vector', 'search_vector', postgresql_using='gin'),
    )
