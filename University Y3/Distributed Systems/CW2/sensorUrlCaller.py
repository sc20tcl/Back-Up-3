import requests
import time

def repeatedly_call_url(url, interval_seconds, max_calls):
    start_time = time.time()
    call_count = 0

    while max_calls is None or call_count < max_calls:
        try:
            response = requests.get(url)
            
            # Process the response here if needed

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

        time.sleep(interval_seconds)
        call_count += 1
    
    end_time = time.time() 
    total_duration = end_time - start_time
    # print(f"Total duration: {total_duration:.2f} seconds")
    return total_duration

repeatedly_call_url("http://localhost:7071/api/hello", 5, 20)


# timestamp = []

# maxCalls = 0
# while maxCalls <= 1000:
#     maxCalls += 100
#     time1 = repeatedly_call_url("http://localhost:7071/api/hello", 0, maxCalls)
#     time2 = repeatedly_call_url("http://localhost:7071/api/hello", 0, maxCalls)
#     time3 = repeatedly_call_url("http://localhost:7071/api/hello", 0, maxCalls)
#     averageTime = (time1 + time2 + time3)/3
#     timestampString = str(maxCalls) + ': ' + str(averageTime)
#     timestamp.append(timestampString)
#     print(maxCalls)

# for x in timestamp:
#     print(x)
