from google.appengine.ext import db

class Image(db.Model):
	image = db.BlobProperty()
	
class ImageKeyRel(db.Model):
	key_ = db.StringProperty()
	short = db.IntegerProperty()