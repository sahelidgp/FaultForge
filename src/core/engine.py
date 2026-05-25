import subprocess

def run_tests(test_file):
    result = subprocess.run(
        ["pytest", test_file, "--tb=short", "-q"], 
        capture_output=True, 
        text=True
    )
    return result.returncode == 0