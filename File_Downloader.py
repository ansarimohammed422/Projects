import asyncio
import aiohttp
import aiofiles
from plyer import notification
import argparse

async def download(url,filename = None):
    print("downloading files")
    
    if filename == None:
        filename = url.split("/")[-1]
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(filename,"wb") as f:
                    async for chunk in response.content.iter_chunked(1024):
                        await f.write(chunk)
                print(f"Downloading file:- {filename}")
                notification.notify(
                    title="Download Complete",
                    message=f"{filename} downloaded successfully!",
                    app_name="File Downloader",
                    timeout=15   # Notification duration in seconds
                )
            else:
                print(f"Error URL not responding! - {response.status_code}")

async def main(urls,filename):
    """Asynchronously downloads multiple files from user input URLs and filenames."""

    tasks = [download(url, filename) for url, filename in zip(urls, filenames)]
    await asyncio.gather(*tasks)  # Wait for all downloads to finish concurrently

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asynchronously Download Multiple Files")
    parser.add_argument("urls",nargs="+",help="Urls of multiple files to download")
    parser.add_argument("-f","--filenames",nargs="*",help="File Names of files to download")

    args = parser.parse_args()

    urls = args.urls
    filenames = args.filenames

    if filenames is None:
        filenames = [None] * len(urls)
    elif len(filenames) < len(urls):
        filenames += [None] * (len(urls) - len(filenames))

    asyncio.run(main(urls,filenames))

        