import asyncio
import aiohttp
import aiofiles

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

    print("Enter URLs to download. Type 'done' when you are finished.")
    while True:
        url = input("Enter URL: ")
        if url.lower() == 'done':
            break
        use_default_filename = input("Do you want to use the default filename? (y/n): ").strip().lower()
        if use_default_filename == 'n':
            filename = input("Enter filename: ")
        else:
            filename = None
        urls.append(url)
        filenames.append(filename)

    tasks = [download(url, filename) for url, filename in zip(urls, filenames)]
    await asyncio.gather(*tasks)  # Wait for all downloads to finish concurrently

if __name__ == "__main__":
    asyncio.run(main())

        