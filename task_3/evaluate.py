import pandas as pd
from executor import run_pipeline

def run_benchmark():
    # Load dataset from the data folder
    try:
        df = pd.read_csv("data/benchmark_dataset.csv")
    except FileNotFoundError:
        print("Error: benchmark_dataset.csv not found in data/ folder.")
        return

    print(f"{'Question':<35} | {'Generated':<10} | {'Executed Success':<17} | {'Retry Needed':<12} | {'Final Status':<12}")
    print("-" * 95)
    
    results = []
    success_count = 0
    retry_success_count = 0
    
    for _, row in df.iterrows():
        question = row["Question"]
        output = run_pipeline(question)
        
        generated = "Yes" if output["sql"] else "No"
        executed = "Yes" if output["status"] == "success" else "No"
        retry = "Yes" if output["retry_needed"] else "No"
        
        if executed == "Yes":
            success_count += 1
            if retry == "Yes":
                retry_success_count += 1
                
        results.append(output)
        # Print row-by-row status
        print(f"{question[:33]:<35} | {generated:<10} | {executed:<17} | {retry:<12} | {output['status']:<12}")

    total = len(df)
    failed = total - success_count
    
    print("\n" + "="*50)
    print("--- Final Benchmark Metrics ---")
    print(f"Total Queries: {total}")
    print(f"SQL Execution Success Rate: {(success_count/total)*100:.1f}%")
    
    total_retries_attempted = sum(1 for r in results if r["retry_needed"])
    if total_retries_attempted > 0:
        retry_rate = (retry_success_count / total_retries_attempted) * 100
        print(f"Retry Success Rate: {retry_rate:.1f}% (Fixed {retry_success_count} out of {total_retries_attempted} errors)")
    
    print(f"Total Failed Queries: {failed}")
    print("="*50)

if __name__ == "__main__":
    run_benchmark()