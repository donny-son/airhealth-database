To download multiple files from KTDB one needs to login > synchronously click download and wait. Although there exists a batch download button, it does not work on data that contains information concerning the Metropolitan area(which is interesting). To overcome this difficulty,  simple scripts are required.

Please edit [card link] upon any updates.

The card currently contains the following content.
> [KTDB] async file downloader - python
>why: 일괄 다운로드 안됨
>how: https://www.ktdb.go.kr/ > login > 마이페이지 > 자료신청내역 > 데이터다운로드(버튼) > 데이터다운로드(버튼)
>
>input: uname, key(`./credentials/credentials.yml`)
>
>logic: open browser, login, move to download page, async download under `./KTDB-download/downloads/`.
>
>output: STATUS_CODE
>  STATUS_CODE = {'normal':1, 'error':-1, 'some_good_some_bad': 2, ... }

[card link]: https://github.com/ncc-airhealth/data-project/projects/1#card-72359110

