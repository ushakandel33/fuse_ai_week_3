import json
from executor import run_pipeline

def main():
    print("==================================================")
    print("🤖 Text-to-SQL Pipeline (Terminal Mode)")
    print("Type 'exit' or 'quit' to stop.")
    print("==================================================\n")

    while True:
        question = input("\nEnter your question: ").strip()
        
        if question.lower() in ['exit', 'quit']:
            print("Exiting pipeline. Goodbye!")
            break
            
        if not question:
            continue

        print("\n⏳ Processing Prompt Chain...")
        
        # Run the pipeline
        output = run_pipeline(question)

        # Print the results nicely to the terminal
        print("\n--- 1. Decomposition ---")
        if output["decomposition"]:
            try:
                # Try to print formatted JSON
                print(json.dumps(json.loads(output["decomposition"]), indent=2))
            except:
                print(output["decomposition"])
        else:
            print("Failed to decompose.")

        print("\n--- 2. Generated SQL ---")
        print(output["sql"])

        print("\n--- 3. Execution Status ---")
        if output["retry_needed"]:
            print("⚠️ Initial SQL failed. System performed exactly 1 Self-Correction Retry.")
            
        if output["status"] == "success":
            print(f"✅ Success! Retrieved {len(output['result'])} rows.")
            # Print the first few rows as a preview
            if output['result']:
                print("Preview of first 3 rows:")
                for row in output['result'][:3]:
                    print(f"  {row}")
        else:
            print(f"❌ Failed: {output['error']}")
            
        print("==================================================")

if __name__ == "__main__":
    main()