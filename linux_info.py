import subprocess

def run():
    print("--- LINUX SYSTEM INFORMATION ---")
    print("\n[Hostname]")
    subprocess.run(["hostname"])
    print("\n[Current Date and Time]")
    subprocess.run(["date"])
    print("\n[CPU Information]")
    subprocess.run(["lscpu"])
    print("\n[Memory Usage]")
    subprocess.run(["free", "-h"])
