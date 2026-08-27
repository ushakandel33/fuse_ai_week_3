import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "text2sql_assignment"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432"),
    )


def execute_query(sql):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()

        return {
            "status": "success",
            "result": result,
            "error": None,
        }

    except Exception as e:
        if conn:
            conn.rollback()

        return {
            "status": "failed",
            "result": [],
            "error": str(e),
        }

    finally:
        if conn:
            conn.close()