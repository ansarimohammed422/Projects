import asyncio
import aiohttp
import aiofiles
import plyer
import os

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
                plyer.notification.notify(
                    title="Download Complete",
                    message=f"{filename} downloaded successfully!",
                    app_name="File Downloader",
                    timeout=10  # Notification duration in seconds
                )
            else:
                print(f"Error URL not responding! - {response.status_code}")




# async def main():
#     # fchoice = input("if you wanna enter filename press (y/n):- ")
#     # if fchoice == "y":
#     #     url = input("Enter file url you want to download:- ")
#     #     filename = input("Enter file name you wanna save:- ")
#     #     download(url,filename)
#     # elif fchoice == "n":
#     #     url = input("Enter file url you want to download:- ")
#     #     download(url)
async def main():
    """Asynchronously downloads multiple files from user input URLs and filenames."""
    urls = []
    filenames = []

    urls_input = input("Enter URLs separated by spaces: ")
    filenames_input = input("Enter filenames separated by spaces (or leave blank for default filenames): ")

    urls = urls_input.split()
    filenames = filenames_input.split() if filenames_input else [None] * len(urls)

    num_urls = len(urls)
    num_filenames = len(filenames)

    if num_filenames < num_urls:
        filenames += [None] * (num_urls - num_filenames)
    


    tasks = [download(url, filename) for url, filename in zip(urls, filenames)]
    await asyncio.gather(*tasks)  # Wait for all downloads to finish concurrently

if __name__ == "__main__":
    asyncio.run(main())

        