from django.conf import settings
from hashids import Hashids

# ประสบการณ์วันนี้ เจอว่าพอย้ายไอ้โค้ดพวกนี้จากหน้า utils มาไว้ตรงนี้ เเมร่งดีขึ้นเลยหวะ อิหยังวะ !!! 
# หรือว่าจะเป็นที่ model เพราะมันเรียก import h_encode ซึ่งอยู่ข้างล่างเกินไป ทำให้มาที่หลังจากที่มันเรียกใช้ Cart model ทำให้ไม่เจอชื่อของ cart model
hashids = Hashids(settings.HASHIDS_SALT, min_length=10)



def h_encode(id):
	return hashids.encode(id)


def h_decode(h):
	z = hashids.decode(h)
	if z:
		return z[0]


class HashIdConverter:
	regex = '[a-zA-Z0-9]{10,}'

	def to_python(self, value):
		return h_decode(value)

	def to_url(self, value):
		return h_encode(value)

