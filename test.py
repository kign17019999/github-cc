import subprocess

def main():
    # Pass command line arguments to the other file
    for m1 in range(100, 1000+1, 100):
        for parition in range(500, 10000, 500):
            subprocess.run(["python", "application_main.py"] + ['addition', m1, m1, m1, m1, parition])

if __name__ == "__main__":
    main()