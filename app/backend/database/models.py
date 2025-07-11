from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    JSON,
    Date,
    Float,
    UniqueConstraint,
)

from sqlalchemy.sql import func
from .connection import Base
from ..db import Base

from pgvector.sqlalchemy import Vector


class HedgeFundFlow(Base):
    """Table to store React Flow configurations (nodes, edges, viewport)"""
    __tablename__ = "hedge_fund_flows"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Flow metadata
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # React Flow state
    nodes = Column(JSON, nullable=False)  # Store React Flow nodes as JSON
    edges = Column(JSON, nullable=False)  # Store React Flow edges as JSON
    viewport = Column(JSON, nullable=True)  # Store viewport state (zoom, x, y)
    data = Column(JSON, nullable=True)  # Store node internal states (tickers, models, etc.)
    
    # Additional metadata
    is_template = Column(Boolean, default=False)  # Mark as template for reuse
    tags = Column(JSON, nullable=True)  # Store tags for categorization


class HedgeFundFlowRun(Base):
    """Table to track individual execution runs of a hedge fund flow"""
    __tablename__ = "hedge_fund_flow_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, nullable=False, index=True)  # Foreign key to hedge_fund_flows
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Run execution tracking
    status = Column(String(50), nullable=False, default="IDLE")  # IDLE, IN_PROGRESS, COMPLETE, ERROR
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Run data
    request_data = Column(JSON, nullable=True)  # Store the request parameters (tickers, agents, models, etc.)
    results = Column(JSON, nullable=True)  # Store the output/results from the run
    error_message = Column(Text, nullable=True)  # Store error details if run failed
    
    # Metadata
    run_number = Column(Integer, nullable=False, default=1)  # Sequential run number for this flow

class Alert(Base):
    """Table to store generated alerts"""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ticker = Column(String(10), nullable=False)
    message = Column(Text, nullable=False)
    emailed = Column(Boolean, nullable=False, server_default="0")

class ThemeIndex(Base):
    """Table for news/theme embeddings."""

    __tablename__ = "themes_idx"

    doc_id = Column(String, primary_key=True)
    ticker = Column(String, nullable=False, index=True)
    embed_vec = Column(Vector)


class GuruStats(Base):
    """Table storing CAGR statistics for each investing guru."""

    __tablename__ = "guru_stats"

    id = Column(Integer, primary_key=True, index=True)
    guru_name = Column(String(100), unique=True, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    start_value = Column(Integer, nullable=False)
    end_value = Column(Integer, nullable=False)
    cagr = Column(String, nullable=True)


class Price(Base):
    """Table to store historical price data"""

    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    ticker = Column(String(20), nullable=False, index=True)
    date = Column(Date, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)

    __table_args__ = (UniqueConstraint("ticker", "date", name="uix_ticker_date"),)
