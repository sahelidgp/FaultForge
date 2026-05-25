import argparse
import sys
import os
import ast
import shutil

from src.core.ast_hacker import MutationDiscoverer, OperatorMutator
from src.core.engine import run_tests
from src.reporters.console import print_success, print_failure, print_info
from src.reporters.html_report import generate_report

def main():
    parser = argparse.ArgumentParser(description="Automated Mutation Testing CLI")
    parser.add_argument("--target", required=True, help="Python source file to mutate")
    parser.add_argument("--tests", required=True, help="Test file to run")
    args = parser.parse_args()

    if not os.path.exists(args.target) or not os.path.exists(args.tests):
        print_failure("Error: Target or Test file not found.")
        sys.exit(1)

    print_info(f"Starting Mutation Engine v2.0 (Isolated Execution)...")
    backup_file = args.target + ".bak"
    shutil.copy(args.target, backup_file)

    try:
        # 1. DISCOVERY PHASE
        with open(args.target, "r") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        discoverer = MutationDiscoverer()
        discoverer.visit(tree)
        
        total_mutations = discoverer.total_targets
        if total_mutations == 0:
            print_info("No mutations could be applied. File is clean.")
            sys.exit(0)
            
        print_info(f"Discovery complete. Found {total_mutations} potential mutation targets.")

        # 2. ISOLATED EXECUTION LOOP
        results = []
        for i in range(total_mutations):
            print_info(f"Injecting Mutant #{i+1}...")
            
            # Parse a fresh, clean tree for each loop
            clean_tree = ast.parse(source_code)
            mutator = OperatorMutator(target_index=i)
            mutated_tree = mutator.visit(clean_tree)
            ast.fix_missing_locations(mutated_tree)

            # Write the isolated mutation to the file
            with open(args.target, "w") as f:
                f.write(ast.unparse(mutated_tree))
                
            # Run the test suite against this single mutant
            tests_passed = run_tests(args.tests)
            status = "KILLED" if not tests_passed else "SURVIVED"
            
            # Log the result
            results.append({
                "id": i + 1,
                "name": mutator.mutation_name,
                "status": status
            })

            # Restore the clean code before the next loop
            shutil.copy(backup_file, args.target)

        # 3. GENERATE REPORT
        print_success("Execution complete. Generating dashboard...")
        report_file = generate_report(args.target, results)
        print_success(f"Report generated successfully: {report_file}")

    finally:
        shutil.move(backup_file, args.target)
        print_info("Restored original code and cleaned up.")

if __name__ == "__main__":
    main()