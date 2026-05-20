import json
import os
from sql_generator import decompose_question, generate_sql, fix_sql
from validator import is_valid_select
from database import execute_query

os.makedirs('logs', exist_ok=True)

def log_execution(log_data):
    """Appends execution results to logs/query_logs.json"""
    log_file = "logs/query_logs.json"
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            pass
    logs.append(log_data)
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

def run_pipeline(question):
    payload = {
        "question": question, "decomposition": None, "sql": None, 
        "result": [], "status": "failed", "retry_needed": False, "error": None
    }

    try:
        # 1. Decompose (LLM Call 1)
        payload["decomposition"] = decompose_question(question)
        
        # 2. Generate (LLM Call 2)
        sql = generate_sql(payload["decomposition"])
        payload["sql"] = sql

        # 3. Validate (Rule-Based)
        is_safe, msg = is_valid_select(sql)
        if not is_safe:
            payload["error"] = msg
            log_execution(payload)
            return payload

        # 4. Execute 
        db_response = execute_query(sql)

        # 5. Retry Logic (Exact 1 Retry, LLM Call 3)
        if db_response["status"] == "failed":
            payload["retry_needed"] = True
            payload["error"] = db_response["error"]
            
            fixed_sql = fix_sql(question, sql, db_response["error"])
            payload["sql"] = fixed_sql
            
            # Re-validate
            is_safe_retry, msg_retry = is_valid_select(fixed_sql)
            if not is_safe_retry:
                payload["error"] = "Retry failed validation: " + msg_retry
                log_execution(payload)
                return payload
                
            # Re-execute
            retry_db_response = execute_query(fixed_sql)
            if retry_db_response["status"] == "success":
                payload["status"] = "success"
                payload["result"] = retry_db_response["result"]
                payload["error"] = None
            else:
                payload["error"] = "Retry execution failed: " + retry_db_response["error"]
        else:
            payload["status"] = "success"
            payload["result"] = db_response["result"]

    except Exception as e:
        payload["error"] = str(e)

    # 6. Output & Log
    log_execution(payload)
    return payload