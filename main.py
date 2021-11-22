import asyncio
import argparse
from KTDB.downloader import KTDBDownloader


async def main(*args, **kwargs):
    if kwargs["Subject"] == "KTDB":
        ktdb_downloader = KTDBDownloader()
        if kwargs["cmd"] == "download":
            await ktdb_downloader.download(kwargs["batch_size"])
        if kwargs["cmd"] == "clean":
            ktdb_downloader.clean()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Data processor for geographic data.")
    parser.add_argument('Subject', help="Subject for data processing.")
    subparser = parser.add_subparsers(dest="cmd", help="Commands to perform on subject.")
    subparser.required = True

    p_download = subparser.add_parser("download")
    p_download.add_argument("batch_size", nargs="?", type=int, default=5, help="Batch size of async download. Default is 5.")

    p_clean = subparser.add_parser("clean")

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
