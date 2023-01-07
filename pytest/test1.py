import time

start_time_1 = time.time()
start_time_2 = time.time()

# Print two more advanced progress bars that update at different rates
for i in range(100):
    # Calculate the elapsed time for the first progress bar
    elapsed_time_1 = time.time() - start_time_1

    # Calculate the estimated time remaining for the first progress bar
    time_remaining_1 = elapsed_time_1 / (i+1) * (100 - (i+1))

    # Format the string for the first progress bar
    progress_bar_1 = f"[{'#' * (i+1):<50}] {i+1}% (elapsed: {elapsed_time_1:.1f}s, remaining: {time_remaining_1:.1f}s)"

    # Calculate the elapsed time for the second progress bar
    elapsed_time_2 = time.time() - start_time_2

    # Calculate the estimated time remaining for the second progress bar
    time_remaining_2 = elapsed_time_2 / ((i+1) * 2) * (100 - ((i+1) * 2))

    # Format the string for the second progress bar
    progress_bar_2 = f"[{'#' * ((i+1) * 2):<50}] {(i+1) * 2}% (elapsed: {elapsed_time_2:.1f}s, remaining: {time_remaining_2:.1f}s)"

    # Print the progress bars
    print(f"{progress_bar_1}\n{progress_bar_2}", end="\r")

    # Wait 0.1 seconds before updating the progress bars
    time.sleep(0.1)
