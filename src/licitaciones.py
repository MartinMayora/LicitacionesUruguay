import time
from collections import deque
from prompt import intrested_in_licitacion
def process_licitaciones(parsedCSV):

    list_intresting = []
    request_times = deque(maxlen=10)  # Track last 10 requests
    min_interval = 5.8  # 10 requests/60 seconds = 6 seconds each, but we use 5.8 for safety
    
    for i, parse in enumerate(parsedCSV):
        current_time = time.time()
        if len(request_times) == 10:
            time_since_oldest = current_time - request_times[0]
            if time_since_oldest < 60:
                wait_time = 60 - time_since_oldest + 0.1
                print(f"Waiting {wait_time:.1f}s to respect rate limit...")
                time.sleep(wait_time)
                current_time = time.time()
        
        result = intrested_in_licitacion(parse[0])
        request_times.append(current_time)
        
        if result == "SI":
            list_intresting.append((parse[1], parse[2]))
            print(f"{i+1}/{len(parsedCSV)}: Interesting - {parse[1]}")
        else:
            print(f"{i+1}/{len(parsedCSV)}: Not interesting - {parse[1]}")
        
        if len(request_times) >= 1:
            time_since_last = current_time - request_times[-1] if len(request_times) > 1 else 0
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)
    
    return list_intresting