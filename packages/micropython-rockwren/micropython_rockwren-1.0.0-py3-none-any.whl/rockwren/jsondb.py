' Simple database: JSON file backed dictionary'
_A='db.json'
import ujson
class JsonDB(dict):
	'\n    Simple database with dict interface that stores key value pairs in a json formed text file.\n    ';_db_file=_A
	def __init__(A,file=_A):A._db_file=file;super().__init__(())
	def load(A):
		' Load database file into dictionary. ';B={}
		try:
			with open(A._db_file,'r')as C:B=ujson.load(C)
		except OSError:
			with open(A._db_file,'w+')as C:ujson.dump(B,C)
		A.clear();A.update(B)
	def save(A):
		' Save dictionary state to database file. '
		with open(A._db_file,'w+')as B:ujson.dump(A,B)