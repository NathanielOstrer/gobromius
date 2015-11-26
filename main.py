#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import models
from google.appengine.ext import db
from google.appengine.api import mail
from os import environ
import captcha
import base36

class MainHandler(webapp2.RequestHandler):
	def get(self):
		chtml = captcha.displayhtml(
		public_key = "6LcfNesSAAAAALpz578J4CXiHk3hwgPZIWSAvtVe",
		use_ssl = False,
		error = None)

		template_values = {
		'captchahtml': chtml
		}

		
		#self.response.write(template_values)

		self.response.write("""

<html> 
<h1> Go Bromius Image Sharer </h1>
</br>
<p> Share an image! </p>

<form name="post_image_form" action="post_image" method="post" enctype="multipart/form-data">

File name:<input type="file" name="imgfile"> <br>
		""")

		self.response.write(chtml)
		self.response.write("""
<input type="submit" value="Submit"</br>

</form>

</html>

		""")

class PostImage(webapp2.RequestHandler):
	def post(self):
		img = self.request.get("imgfile")
		if not img:
			self.response.write("error!")
		else:
			image = models.Image(image=db.Blob(img))
			image.put()
			num = 0
			short = models.ImageKeyRel.gql("WHERE short != -1 ORDER BY short DESC").fetch(limit=1)
			if short:
				num = short[0].short + 1
			rel = models.ImageKeyRel(key_=str(image.key()), short=num)
			rel.put()
			self.response.out.write('<meta http-equiv="refresh" content=".5;URL=/' + base36.base36encode(num) + '">')

class Image(webapp2.RequestHandler):
	def get(self):
		url = str(self.request.url)
		split = url.split('/')
		base36short = split[len(split)-1]
		short = base36.base36decode(base36short)
		print short
		key_ = models.ImageKeyRel.gql("WHERE short = :1", short).get()
		img = db.get(key_.key_)
		if img.image:
			self.response.headers['Content-Type'] = 'image/png'
			self.response.out.write(img.image)
		else:
			self.error(404)


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/post_image', PostImage),
	(r'/.*.*.*.*.*', Image),

], debug=True)
