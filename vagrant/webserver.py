from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi 
import re


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                output = "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name + "<br>"
                    
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" %restaurant.id
                    output += "<br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a> <br><br>" %restaurant.id

                output += "<a href='/restaurants/new'>Make a New Restaurant</a>" 
                output += "</body></html>"    


                self.wfile.write(str.encode(output))
                print(output)
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = "<html><body><h1>Make a New Restaurant</h1></body></html>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'><input name='newrestaurant' type = 'text'><input type = 'submit' value='Create'></form>"
                
                self.wfile.write(str.encode(output))
                print(output)
                return

            if self.path.endswith("/delete") | self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #get id from the url & assign to variable
                restaurantid = re.sub('[a-z]*|/*', '', self.path)
                
                #get restaurant name from id
                restaurant = session.query(Restaurant).filter_by(id = restaurantid).one()
                print(restaurant.name)
                
                if self.path.endswith("/delete"):
                    output = "<html><body><h1>Are you sure you want to delete this restaurant? %s</h1></body></html>" %restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data'><input name='restaurantidd' type = 'hidden' value = '%s'><input type = 'submit' value='Delete Restaurant'></form>" %restaurantid
                if self.path.endswith("/edit"):
                    output = "<html><body><h1>Update this restaurant? %s</h1></body></html>" %restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data'><input name='restaurantidu' type = 'hidden' value = '%s'><input type = 'text' name = 'updaterestaurant'><input type = 'submit' value='Update Restaurant'></form>" %restaurantid    
                
                self.wfile.write(str.encode(output))
                print(output)
                return    

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = "<html><body>Hello!</body></html>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type = 'text'><input type = 'submit' value='Submit'></form>"
                
                self.wfile.write(str.encode(output))
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = b"<html><body>&#161Ola! <a href= '/hello' >Back to Hello<a/></body></html>"
                self.wfile.write(output)
                print(output)
                return    
            else:
                self.send_error(404, "File Not Found: %s" % self.path)

    def do_POST(self):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                newrestaurantname = fields.get('newrestaurant')
                restaurantidd = fields.get('restaurantidd')
                restaurantidu = fields.get('restaurantidu')
                
            if restaurantidd != None:  
                print("begin delete")
                restaurant = session.query(Restaurant).filter_by(id = int(restaurantidd[0])).one()
                session.delete(restaurant)
                session.commit()
                print("end delete")
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                

            if restaurantidu != None:
                print("begin update")
                newname = fields.get('updaterestaurant')
                restaurantupdate = session.query(Restaurant).filter_by(id = int(restaurantidu[0])).one()
                restaurantupdate.name = newname[0]
                session.commit()
                print("end update")
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                   
            
            
            if newrestaurantname != None:  
                newrestaurant = Restaurant(name = newrestaurantname[0])  
                session.add(newrestaurant)
                session.commit()
                print("saved to db")

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                

            if messagecontent != None:
                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += "<form method='POST' enctype='multipart/form-data' action='deleteRestaurant'><h2>What would you like me to say?</h2><input name='message' type = 'text'><input type = 'submit' value='Submit'></form>"

                output += "</body></html>"
                self.wfile.write(str.encode(output))
                print(output)



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()   
    except KeyboardInterrupt:
        print(" pressed. Shutting down server...")
        server.socket.close()

if __name__ == '__main__':
    main()