import subprocess

def run():
    print("--- LINUX SYSTEM INFORMATION ---")
    print("\n[Hostname]")
    subprocess.run(["hostname"])
    print("\n[Current Date and Time]")
    subprocess.run(["date"])
