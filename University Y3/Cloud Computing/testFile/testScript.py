import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

FUNCTION_URLS = [
    'http://localhost:8080/function/mask-function',
    'http://localhost:8080/function/resize-function',
    'http://localhost:8080/function/poster-function'    
]

def make_sequential_requests():
    results = {url: {'success': 0, 'failures': []} for url in FUNCTION_URLS}
    for url in FUNCTION_URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results[url]['success'] += 1
            else:
                results[url]['failures'].append(f"Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            results[url]['failures'].append(str(e))
    return results

def run_load_test(requests_scale, concurrency_level):
    
    print(f"\n-------------------------------------------------")
    print(f"TEST: {concurrency_level} users, {requests_scale} requests")
    print(f"-------------------------------------------------")
    start_time = time.time()

    overall_results = {url: {'success': 0, 'failures': []} for url in FUNCTION_URLS}
    with ThreadPoolExecutor(max_workers=concurrency_level) as executor:
        futures = [executor.submit(make_sequential_requests) for _ in range(concurrency_level * requests_scale)]
        for future in as_completed(futures):
            result = future.result()
            for url in result:
                overall_results[url]['success'] += result[url]['success']
                overall_results[url]['failures'].extend(result[url]['failures'])

    for url, outcome in overall_results.items():
        total_requests = concurrency_level * requests_scale
        success_count = outcome['success']
        failure_count = len(outcome['failures'])
        print(f"- Function URL: {url}: {success_count}/{total_requests} successful")
        if failure_count > 0:
            print(f"    - Error: {outcome['failures'][0]}")

    end_time = time.time()
    print(f"Duration: {end_time - start_time:.2f} seconds")

    print("Waiting 30 seconds before the next test...")
    time.sleep(30)

if __name__ == "__main__":
    user_scale = [1, 10, 50, 100]
    request_scale = [1, 10, 50, 100]
    for concurrency_level in user_scale:
        for request_level in request_scale:
            run_load_test(request_level, concurrency_level)
