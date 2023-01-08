import application_main

def main():
    # Pass command line arguments to the other file
    for m1 in range(100, 1000+1, 300):
        for parition in range(500, 2000, 500):
            application_main.function_for_test('addition', m1, m1, m1, m1, parition)

if __name__ == "__main__":
    main()