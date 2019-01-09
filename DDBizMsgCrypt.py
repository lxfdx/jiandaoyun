import base64
import string
import random
import hashlib
import time
import struct
from Crypot.Cipher import AES
import socket
from binascii import a2b_hex,b2a_hex
import json
import requests

class SHA1():
	def getSHA1(self,token,timestamp,nonce,cncrypt):
		sortlist = [token,timestamp,nonce,encrypt]
		sortlist.sort()
		sha = hashlib.sha1()
		sha.update(''.join(sortlist))
		return sha.hexdigest()

class PKCS7Encoder():
	block_size = 32
	def encode(self,text):
		text_length = len(text)
		amount_to_pad = self.block_size - (text_length % self.block_size)
		if amount_to_pad == 0:
			amount_to_pad = self.block_size
		pad = chr(amount_to_pad)
		print(chr(amount_to_pad))
		return text + pad * amount_to_pad

	def decode(self,decrypted):
		pad = ord(decrypted[-1])
		if pad<1 or pad>32:
			pad = 0
		return decrypted[:-pad]


class Prpcrypt():
	def __init__(self,key):
		self.key = key
		self.MODE = AES.MODE_CBC

	def encrypt(self,text,appid):
		text = self.get_random_str()+struct.pack('I',socket.htonl(len(text))) + text +appid
		pkcs7 = PKCS7Encoder()
		text = pkcs7.encode(text)
		
		cryptor = AES.new(self.key,self.mode,self.key[:16])
		ciphertext = cryptor.encrypt(text)
		return base64.b64encode(ciphertext)
	def decrypt(self,text,appid):
		cryptor = AES.new(self.key,self.mode,self.key[:16])
		plain_text = cryptor.decrypt(base64.b64decode(text))

		pad = ord(plain_text[-1])
		content = plain_text[16:-pad]
		json_len = socket.ntohl(struct.unpack("I",content[:4])[0])
		json_content = content[4:json_len+4]
		from_appdi = content[json_len+4:]
		return json_content

	def get_random_str(self):
		rule = string.ascii_letters + string.digits
		str = random.sample(rule, 16)
		return ''.join(str)



class DDBizMsgCrypt():
	def __init__(self,sToken,sEncodingAESKey,sAppId):
		self.key = base64.b64decode(sEncodingAESKey + '=')
		self.token = sToken
		self.appid = sAppId


	def EncryptMsg(self,sReplyMsg,sNonce,timestamp=None):
		pc = Prpcrypt()
		sha1 = SHA1()
		encrypt = pc.encrypt(sReplyMsg,self.appid)
		signature = sha1.getSHA1(self.token,timestamp,sNonce,encrypt)
		return self.generate(encrypt,signature,timestamp,sNonce)
	def generate(self,encrypt,signature,timestamp,nonce):
		resp_dict = {'msg_signature':signature,
			     'timestamp':timestamp,
			     'nonce':nonce,
			     'encrypt':encrypt}
		return json.dumps(resp_dict)

	def DecryptMsg(self,sPostData,sMsgSignature,sTimeStamp,sNonce):
		sha1= SHA1()
		signature = sha1.getSHA1(self.token,sTimeStamp,sNonce,encrypt)
		
