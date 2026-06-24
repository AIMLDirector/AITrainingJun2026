from datetime import datetime
import time
time_now= datetime.now()
print("Current date and time:", time_now)

readable_format = time_now.strftime("%Y-%m-%d %H:%M:%S")
print("Current date and time in readable format:", readable_format) 
readable_format1 = time_now.strftime("%d/%m/%Y")
print("Current date and time in readable format:", readable_format1)

start_time = time_now.strftime("%H:%M:%S")  # string format time 

time.sleep(10)  # Sleep for 10 seconds
end_time = datetime.now().strftime("%H:%M:%S")

difference = datetime.strptime(end_time, "%H:%M:%S") - datetime.strptime(start_time, "%H:%M:%S")  # string parser time 
print("Time difference:", difference)


tick_start = time.perf_counter()  # Start the timer
time.sleep(10)
tick_end = time.perf_counter()  # End the timer 

elapsed_time = tick_end - tick_start  # Calculate elapsed time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

