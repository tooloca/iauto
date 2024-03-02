from typing import Any, Dict, Optional

import pandas as pd
import sqlalchemy

from ..loader import register_action


@register_action(name="db.create_engine", spec={
    "description": "Create SQL Engine.",
    "arguments": [
        {
            "name": "url",
            "description": "SQLAlchemy-style database connection URL.",
            "type": "string",
            "required": True
        }
    ]
})
def create_engine(*args, url: str, **kwargs) -> sqlalchemy.Engine:
    return sqlalchemy.create_engine(url)


@register_action(name="db.read", spec={
    "description": "Read data from database.",
    "arguments": [
        {
            "name": "sql",
            "description": "SQL.",
            "type": "string",
            "required": True
        },
        {
            "name": "return_type",
            "description": "Return data type, optional, default: dataframe.",
            "type": "string",
            "required": False
        }
    ]
})
def read(
    *args,
    engine: sqlalchemy.Engine,
    sql: str,
    return_type: Optional[str] = None,
    **kwargs
) -> Any:
    df = pd.read_sql(sql=sql, con=engine)

    return_type = (return_type or "").lower()
    if return_type == "dataframe":
        return df
    else:
        return df.to_dict(orient='records')


@register_action(name="db.exec", spec={
    "description": "Execute SQL.",
    "arguments": [
        {
            "name": "sql",
            "description": "SQL.",
            "type": "string",
            "required": True
        },
        {
            "name": "values",
            "description": "SQL parameters.",
            "type": "dict",
            "required": False
        }
    ]
})
def exec(
    *args,
    engine: sqlalchemy.Engine,
    sql: str,
    values: Optional[Dict] = None,
    **kwargs
) -> Any:
    text = sqlalchemy.text(sql)

    with engine.connect() as conn:
        if values is None:
            conn.execute(text)
        else:
            conn.execute(text, values)
        conn.commit()


@register_action(name="db.select", spec={
    "description": "Eexecute select statement.",
    "arguments": [
        {
            "name": "sql",
            "description": "SQL.",
            "type": "string",
            "required": True
        },
        {
            "name": "values",
            "description": "SQL parameters.",
            "type": "dict",
            "required": False
        }
    ]
})
def select(
    *args,
    engine: sqlalchemy.Engine,
    sql: str,
    values: Optional[Dict] = None,
    **kwargs
) -> Any:
    text = sqlalchemy.text(sql)

    with engine.connect() as conn:
        if values is None:
            cursor = conn.execute(text)
        else:
            cursor = conn.execute(text, values)

        columns = list(cursor.keys())
        rows = cursor.all()

        if len(rows) == 0:
            return None
        elif len(rows) == 1:
            return dict(zip(columns, rows[0]))
        else:
            return [dict(zip(columns, r)) for r in rows]
