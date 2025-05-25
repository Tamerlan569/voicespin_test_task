import aiohttp
import asyncio
import time
import json

async def fetch(session, url):
    async with session.get(url) as response:
        return url, response.status

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

def main():
    with open('urls.json') as f:
        urls = json.load(f)['urls']

    start_time = time.time()
    results = asyncio.run(fetch_all(urls))
    total_time = time.time() - start_time

    successful_responses = sum(1 for _, status in results if status == 200)
    response_times = [status for _, status in results]

    print(f"Number of successful responses: {successful_responses}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Fastest response time: {min(response_times)}")
    print(f"Slowest response time: {max(response_times)}")

if __name__ == "__main__":
    main()
