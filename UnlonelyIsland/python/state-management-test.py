import datetime

time = datetime.datetime.now()
with open("./log.txt", "a") as f:
    f.write(f"Session started at {time}\n")

  
def current_time():
    print("Current time is", time.strftime("%H:%M:%S"))
    return time.strftime("%H:%M:%S")