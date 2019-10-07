import os
from Crypto.Cipher import AES
from Crypto import Random

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = "(enc)"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:#rb means read in binary
		with open(outputFile, 'wb') as outfile:#wb means write in the binary mode
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk)%16 != 0:
					chunk += b' '*(16-(len(chunk)%16))

				outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor= AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(filesize)

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

def Main():
	choice = input("Would you like to (E)encrypt or (D)Decrypt ")

	if choice == 'E':
		filename = input("File to encrypt: ")
		password = input("Password: ")
		encrypt(getKey(password), filename)
		print('Done.')
	elif choice == 'D':
		filename = input("File to decrypt: ")
		password = input("Password: ")
		decrypt(getKey(password),filename)
		print("Done.")

	else:
		print("No option selected, closing...")


Main()