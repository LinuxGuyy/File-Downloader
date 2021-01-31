try:
	print("❱ Initialising Everything")
	import requests
	import re
	from os.path import isfile

	def get_filename(cd):
		if not cd:
			return False
		fname = re.findall('filename=(.+)', cd)
		if len(fname) == 0:
			return False
		return fname[0]

	def is_downloadable(url):
		h = requests.head(url, allow_redirects=True)
		header = h.headers
		content_type = header.get('content-type')
		if 'text' in content_type.lower():
			return True
		if 'html' in content_type.lower():
			return False
		return True

	print("✔ Everything Initialised")
	url = str(input("❱ URL: "))

	if is_downloadable(url):
		print("✔ URL Checked - File is Downloadable")
	else:
		print("✖ URL Checked - File Can't Be Downloaded")
		exit(1)

	print("✔ Getting The File")
	r = requests.get(url, stream=True, allow_redirects=True)

	print("❱ Retrieving Filename")
	if url.find('/'):
		filename = url.rsplit('/', 1)[1]
	else:
		filename = get_filename(r.headers.get('content-disposition'))
		if not filename:
			print("✖ Filename Can't Be Fetched")
			filename = str(input("❱ Filename: "))

	if isfile(filename):
		print(f"✖ File With The Name '{filename}' Already Exist")
		filename = str(input("❱ Unique Filename: "))

	print("❱ Making The File")
	with open(filename, "wb") as file:
		print("❱ Writing Data To The File")
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				file.write(chunk)
			else:
				print("✖ Unknown Error Occured")
				exit(1)

		print("✔ File Written Sucessfully")
		exit(0)
except KeyboardInterrupt:
	print("\n✖ Ctrl + C Detected")
except ImportError:
	print("\n✖ 'Requests' Module Not Found")
except Exception as e:
	print(f"\n✖ {e}")