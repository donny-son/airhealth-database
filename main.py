import asyncio
import argparse
from KTDB.downloader import KTDBDownloader


async def main(*args, **kwargs):
    if kwargs["subject"] == "KTDB":
        ktdb_downloader = KTDBDownloader()
        if kwargs["download"]:
            await ktdb_downloader.download()
        if kwargs["clean"]:
            ktdb_downloader.clean()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Data processor for geographic data.")
    parser.add_argument('subject', metavar='S',help="subject for data processing")
    parser.add_argument('-d','--download', action="store_true", help="download subject data")
    parser.add_argument('-c','--clean', action="store_true", help="clean subject data")
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
