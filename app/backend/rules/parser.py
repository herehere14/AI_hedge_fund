import os
import yaml
from typing import List, Any
from sqlalchemy.sql import operators
from sqlalchemy import and_
from sqlalchemy.orm import Query
from app.backend.models.stock import Stock

RULES_DIR = os.path.join(os.path.dirname(__file__))


def load_strategy(strategy_id: str) -> dict:
    path = os.path.join(RULES_DIR, f"{strategy_id}.yml")
    with open(path, "r") as f:
        return yaml.safe_load(f)


_OP_MAP = {
    '<': lambda col, val: col < val,
    '<=': lambda col, val: col <= val,
    '>': lambda col, val: col > val,
    '>=': lambda col, val: col >= val,
    '==': lambda col, val: col == val,
    '!=': lambda col, val: col != val,
    'in': lambda col, val: col.in_(val),
    'not in': lambda col, val: ~col.in_(val),
}


def strategy_to_filters(strategy: dict) -> List[Any]:
    filters = []
    for rule in strategy.get('filters', []):
        field = getattr(Stock, rule['field'])
        op = rule['op']
        value = rule['value']
        if op not in _OP_MAP:
            raise ValueError(f"Unsupported operator: {op}")
        filters.append(_OP_MAP[op](field, value))
    return filters