from pathlib import Path
import asyncio
import shutil

from yaml import safe_load
from bs4 import BeautifulSoup, element
from tqdm import tqdm
import aiohttp


class KTDBDownloader:
    BASE_URL = 'https://www.ktdb.go.kr'
    LOGIN_URL = BASE_URL + '/loginProcess.do'
    DATA_REQUEST_HISTORY_URL = BASE_URL + '/www/selectMyPbldataReqstWebList.do?key=159'

    CREDENTIAL_PATH = Path(".") / "credentials" / "credentials.yml"
    DOWNLOAD_DIR = Path(".") / 'KTDB' / 'downloads'

    async def login(self) -> aiohttp.ClientSession:
        # Get credential
        with open(self.CREDENTIAL_PATH) as stream:
            credential = safe_load(stream)

        ktdb_id = credential['ktdb']['uname']
        ktdb_pw = credential['ktdb']['key']

        # Login
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        form_data = {
            'userId': ktdb_id,
            'passwd': ktdb_pw,
        }

        try:
            timeout = aiohttp.ClientTimeout(total=None)
            session = aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(verify_ssl=False))
            await session.post(
                url=self.LOGIN_URL,
                data=form_data,
                headers=headers,
            )
            print('Login success')
            return session
        except Exception as e:
            print(f'Failed to login. Reason: {e}')

    async def download(self, batch_size=5):
        # Login
        session = await self.login()
        assert session is not None, f"session failed"

        # Get data page url
        async with session.get(self.DATA_REQUEST_HISTORY_URL) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            table = soup.find('table', class_='board_t1')
            data_page_url = table.find('a')['href']
            data_page_url = self.BASE_URL + data_page_url.replace('./', '/www/')

        # Download files from data page url
        async with session.get(data_page_url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            table = soup.find('table', class_='board_t1')
            rows = table.find('tbody').find_all('tr')

            print(f'Start Download in {self.DOWNLOAD_DIR}')
            print('---------------------------')

            # metadata
            self._download_metadata(self.DOWNLOAD_DIR / "metadata.html", table)

            # data
            batch_list = [rows[i:i+batch_size] for i in range(0, len(rows), batch_size)]
            for batch in batch_list:
                tasks = []
                for row in batch:
                    filename = row.find('td', {'data-cell-header': '자료코드 : '}).string
                    download_a_tag = row.find('a', class_="sbtn wgreen")
                    download_url = self.BASE_URL + download_a_tag['href']
                    file_path = self.DOWNLOAD_DIR / f'{filename}.zip'

                    if not file_path.is_file():
                        tasks.append(self._download(session, file_path, download_url))

                if tasks:
                    await asyncio.wait(tasks)

            print('---------------------------')
            print('Download complete')

        await session.close()

    def _download_metadata(self, file_path: Path, table: element.Tag):
        """
        inputs bs4.element.Tag and writes a human-readable html file
        """
        if not file_path.exists():
            with open(file_path, "w") as f:
                print(BeautifulSoup(str(table), "html.parser"), file=f)

    @staticmethod
    async def _download(session, file_path: Path, url):
        async with session.get(url) as response:
            chunk_size = 1024
            progress_bar = tqdm(desc=str(file_path), unit='B', unit_scale=True)
            with open(file_path, 'wb') as f:
                async for chunk in response.content.iter_chunked(chunk_size):
                    f.write(chunk)
                    progress_bar.update(len(chunk))
                progress_bar.close()

    def clean(self):
        no_remove_list = ['README.md']
        print(f'Remove downloads in {self.DOWNLOAD_DIR}')
        for f in tqdm(self.DOWNLOAD_DIR.iterdir()):
            if f.name in no_remove_list:
                continue
            try:
                if f.is_file() or f.is_symlink():
                    f.unlink()
                elif f.is_dir():
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
