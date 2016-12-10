from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind= engine)
session = DBSession()

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body>"
				message += "Hello!"

				message +="</body></html>"

				self.wfile.write(message)
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1> The Restaurants in the Database are:</h1>"
				output += "<a href = '/restaurants/new' >Make a New Restaurant Here</a></br>"
				restros = session.query(Restaurant).all()
				for r in restros:
					output += r.name
					output += "</br>"
					output += "<a href = '/restaurants/%s/edit' >Edit</a></br>"% r.id
					output += "<a href = '/restaurants/%s/delete' >Delete</a></br>"% r.id
					output += "</br></br>"

				output +="</body></html>"

				self.wfile.write(output)
				return
			
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"

				output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'><input name = 'newRestaurantName' type = 'text'><input type = 'submit' value = 'Create'></form>"
			
				self.wfile.write(output)
				return

			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split('/')[2]
				restroQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if restroQuery != []:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()

					output = ""
					output += "<html></body>"
					output += "<h2>%s</h2>"% restroQuery.name
					output += "<form method = 'POST' enctype= 'multipart/form-data' action = '/restaurants/%s/edit'>"% restaurantIDPath
					output += "<input name = 'editRestaurantName' placeholder = '%s' type = 'text'><input type = 'submit' value = 'Post Edit'></form>"% restroQuery.name

					output += "</body></html>"
					self.wfile.write(output)
					return

			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split('/')[2]
				restroQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if restroQuery != []:
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "<h1> Are You Sure You Want To Delete - %s<h1>"% restroQuery.name
					output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete' >"% restaurantIDPath
					output += "<input type = 'submit' value = 'Delete'></form>"
					output += "</body></html>"
					self.wfile.write(output)

				return


			else:
				self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('editRestaurantName')

					restaurantIDPath = self.path.split("/")[2]
					myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
					if myRestaurantQuery != []:
						myRestaurantQuery.name = messagecontent[0]
						session.add(myRestaurantQuery)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

			if self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				restaurantIDPath = self.path.split("/")[2]
				restaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if restaurantQuery != []:
					session.delete(restaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type','text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()




			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

					newRestaurant = Restaurant(name=messagecontent[0])
					session.add(newRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
		except:
			pass

            


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s"  % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()