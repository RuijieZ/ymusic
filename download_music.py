import os
import sys
import subprocess
from argparse import ArgumentParser
from multiprocessing import Pool, cpu_count

from mp4tomp3 import transform_dir
#pool = mp.Pool(processes=2)


def read_all_urls(path):
	try:
		with open(path, "r") as f:
			return [line.strip() for line in f if line[0] != "#"]
	except Exception as e:
		print(e)
		print("Exception happens when reading urls")
		sys.exit()

def transform(path):
	isDirectory = os.path.isdir(path)
	if not isDirectory:
		print("Target directory is not directory, exiting now")
		sys.exit()


	try:
		transform_dir(path, path)   # input
	except Exception as e:
		print("error in calling the mp4tomp3 function")
		print(e)

def download_video(url, path):
	try:
		print("".format(url))
		cmd = "youtube-dl -i -f mp4 --yes-playlist '{}' -o '{}/%(title)s.%(ext)s'".format(url, path)
		returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
		print('downloaded {}, returned value: {}'.format(url, returned_value))
		return 0
	except Exception as e:
		print("download url: {} failed".format(url))
		print(e)
		return -1
	

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-pl", "--playlist", dest="playlist",
                        help="path to the playlist for all the songs you want to download from youtube...should be in the format of one row per url")
    parser.add_argument("-dp", "--download_path", dest="download_path",
                        help="folder path to store both the viedoes and mp3 file")
    args = parser.parse_args()

    print("Step 1, read all urls......")
    urls = read_all_urls(args.playlist)

    print("Step 2, using multiprocess to download the urls")
    pool = Pool(processes=23)
    results = [pool.apply(download_video, (url,args.download_path,)) for url in urls]

    print("Step 3, transform the viedoes....")
    transform(args.download_path)

    print("Exiting...")