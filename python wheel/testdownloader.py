import requests
from contextlib import closing


def streamDownloadFile(url,filePath,openWay="w"):
	with closing(requests.get(url,stream = True)) as res:
		with open(filePath,openWay) as f:
			for chunk in res.iter_content(chunk_size = 1024):
				f.write(chunk)


if __name__ == '__main__':
	streamDownloadFile()

