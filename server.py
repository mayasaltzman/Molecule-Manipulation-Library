import sys
import MolDisplay
import molecule
import molsql
import io
import requests
import json
import urllib
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler

#creating database
db = molsql.Database(reset=True)
db.create_tables()


class MyHandler(BaseHTTPRequestHandler):
    elementList = []
    elementList2 = []
    moleculeList = [] 
    message = ""
    elementsMessage = ""
    #presents a web-form to upload files with path is "/" and generates a 404 error otherwise
    def do_GET(self):
        #path to home page
        if self.path == "/":
            self.send_response(200)
            f = open("html/homePage.html")
            str_ = f.read()
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            
            f.close()

            self.wfile.write(bytes(str_, "utf-8"))
        #path to link JS for addRemove page
        elif self.path == "/scripts/addRemoveScript.js":
            self.send_response(200)
            f = open("scripts/addRemoveScript.js")
            str_ = f.read()
            self.send_header("Content-type", "text/javascript")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        #path to link JS for uploadSDf page
        elif self.path == "/scripts/uploadSDFScript.js":
            self.send_response(200)
            f = open("scripts/uploadSDFScript.js")
            str_ = f.read()
            self.send_header("Content-type", "text/javascript")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        #path to link JS for selectMolecules page
        elif self.path == "/scripts/selectMoleculesScript.js":
            self.send_response(200)
            f = open("scripts/selectMoleculesScript.js")
            str_ = f.read()
            self.send_header("Content-type", "text/javascript")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        #path to link style sheets for uploadFile page
        elif self.path == "/css/uploadFile.css":
            self.send_response(200)
            f = open("css/uploadFile.css")
            str_ = f.read()
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        #path to link style sheets for addRemove page
        elif self.path == "/css/addRemove.css":
            self.send_response(200)
            f = open("css/addRemove.css")
            str_ = f.read()
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        #path to link style sheets for homePage
        elif self.path == "/css/homePage.css":
            self.send_response(200)
            f = open("css/homePage.css")
            str_ = f.read()
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        #path to link style sheets for selecting molecules
        elif self.path == "/css/selectMolecules.css":
            self.send_response(200)
            f = open("css/selectMolecules.css")
            str_ = f.read()
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
            
        #path to display table after an element is removed
        elif self.path == "/removedData":
            #parsing table values so they can be sent back to JS
            myStr = db.conn.execute( "SELECT * FROM Elements;" ).fetchall()
            elementNum = []
            elementCode = []
            elementName = []
            color1 = []
            color2 = []
            color3 = []
            radius = []
            toWrite = []
            #contatanating all the data into a temp string to right
            for i in myStr:
                temp = "Element Number: "+ str(i[0]) + " - Element Code: " + i[1] + " - Element Name: " + i[2] + " - Colors: " + i[3] + " " + i[4] + " "+ i[5] + " - Radius: "+ str(i[6])
                toWrite.append(temp) #adding string to a list of strings

            #joining the list of strings to a comma seperated string
            my_string = ','.join(toWrite)
            
            #sending string back to js
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(my_string))
            self.end_headers()
            self.wfile.write(my_string.encode("utf-8"))
        
        #path to add and remove elements from the system
        elif self.path == "/addRemove?":
            self.send_response(200)
            f = open("html/addRemove.html")
            str_ = f.read()
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        
        #path to upload sdf files to the system
        elif self.path == "/uploadFile?":
            self.send_response(200)
            f = open("html/uploadSDF.html")
            str_ = f.read()
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        
        #path to select from a list of molecules
        elif self.path == "/selectMol?":
            self.send_response(200)
            f = open("html/selectMolecules.html")
            str_ = f.read()
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(str_))
            self.end_headers()
            f.close()
            self.wfile.write(bytes(str_, "utf-8"))
        
        #adding molecules to the data base
        elif self.path == "/addedMolecules":
            myMols = []
            atomNos = []
            bondNos = []
            molStrings = []
            cursor = db.conn
            #get all molecule names from the data base
            molNames = cursor.execute( "SELECT Molecules.NAME FROM Molecules;").fetchall()
            
            #loading molecules and adding each molecule to a list of molecules
            for i in molNames:
                myMols.append(db.load_mol(i[0]))
            
            #getting each molecules atom and bond numbers and adding them to a list of atom and bond numbers
            for i in myMols:
                atomNos.append(i.atom_no)
                bondNos.append(i.bond_no)
                
            
            #creating a temp string with the molecules name, atom nums, and bond nums, and adding them to a list of molecule strings
            for i in range(len(molNames)):
                temp = molNames[i][0] + " " + str(atomNos[i]) + " " + str(bondNos[i])
                molStrings.append(temp)
            
            #joining molecule strings to be one string
            my_string = ','.join(molStrings)
            
            #sending string to be used in JS
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(my_string))
            self.end_headers()
            self.wfile.write(my_string.encode("utf-8"))
        
        #path if user enters an invalid file, sends an error message
        elif self.path == "/invalidFile":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(MyHandler.message.encode('utf-8'))
        
        #path if user gives invalid element infor, sends an error message
        elif self.path == "/invalidElement":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(MyHandler.elementsMessage.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))
            
    def do_POST(self):
        #post request from addRemoveScript goes here when user wants to add an element
        if self.path == "/added":
            self.send_response(200)
            
            #reading data from JS
            content_length = int(self.headers.get("Content-Length")) 
            data = self.rfile.read(content_length) 
            
            #parsing JSON to a python dictonary
            dict = json.loads(data)
            
            #accessing values from dictonary
            elementNum = dict["elementNum"]
            elementCode = dict["elementCode"]
            elementName = dict["elementName"]
            color1 = dict["colors"][0]
            color2 = dict["colors"][1]
            color3 = dict["colors"][2]
            radius = dict["radius"]
            
            #adding to element to elements table
            try:
                db['Elements'] = (elementNum,elementCode,elementName,color1,color2,color3,radius)
                MyHandler.elementsMessage = ""
            except:
                MyHandler.elementsMessage = "invalid"
        
        #post request from addRemoveScript goes here when user wants to remove an element
        elif self.path == "/removed":
            self.send_response(200)
            #reading data from JS
            content_length = int(self.headers.get("Content-Length"))
            data = self.rfile.read(content_length) 
            
            #parsing JSON to a python dictonary
            dict = json.loads(data)
            
            #accessing values from dictonary
            elementNum = dict["elementNum"]
            elementCode = dict["elementCode"]
            elementName = dict["elementName"]
            color1 = dict["colors"][0]
            color2 = dict["colors"][1]
            color3 = dict["colors"][2]
            radius = dict["radius"]
            
            #removing element from table
            query = "DELETE FROM Elements WHERE ELEMENT_CODE = (?)"
            params = elementCode
            
            #making sure data to remove is not malicious
            db.conn.execute(query,params)
            
            db.conn.commit()
            
        
        #path when user has uploaded SDf file and given molecule a name
        elif self.path == "/uploadedSDF":
            
            #parsing form data
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {'REQUEST_METHOD':'POST'}
            )
            
            #getting file
            file_item = form['sdfFile'].file
            #getting mol name
            molName = form.getvalue('molName')
            #reading file
            asBytes = file_item.read()
            #turning file to bytes
            bytes_io = io.BytesIO(asBytes)
            #turning file to text io
            text_io = io.TextIOWrapper(bytes_io)

            #checking if data is malicious
            try:
                db.add_molecule(molName,text_io)
                MyHandler.message = ""
            except:
                MyHandler.message = "invalid"
            
            
            self.send_response(200)
        
        #path when user wants to display a molecule
        elif self.path == "/displayMol":
            content_length = int(self.headers.get("Content-Length"))
            data = self.rfile.read(content_length)   
            
            #parsing JSON to a python dictonary
            dict = json.loads(data)
            name = dict["molName"]
            #loading the molecules
            myMol = db.load_mol(name)
            #getting the radius elements and radial gradients
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()
            
            #getting the svg
            myMol.sort()
            svg = myMol.svg()
                
            message = svg
            
            #sending the svg back to the server
            self.send_response( 200 ); 
            self.send_header( "Content-type", "text/plain" )
            self.send_header( "Content-length", len(message) )
            self.end_headers()

            self.wfile.write( bytes( message, "utf-8" ) )
        
        #path for xrotation
        elif self.path == "/xRotation":
            #reading data from JS
            content_length = int(self.headers.get("Content-Length")) 
            data = self.rfile.read(content_length) 
            
            #parsing JSON to a python dictonary
            dict = json.loads(data)
            
            #getting molecule name and loading molecule
            molName = dict["name"]
            mol = db.load_mol(molName)
            
            #performing a rotation of that molecule 90 degress around the x axis
            mx = molecule.mx_wrapper(90,0,0)
            mol.xform(mx.xform_matrix)
            
            #getting the svg of the rotated molecule
            mol.sort()
            svg = mol.svg()
            message = svg

            self.send_response( 200 ); 
            self.send_response( 200 ); 
            self.send_header( "Content-type", "text/plain" )
            self.send_header( "Content-length", len(message) )
            self.end_headers()

            self.wfile.write( bytes( message, "utf-8" ) )
        
        #path for yrotation
        elif self.path == "/yRotation":
            #reading data from JS
            content_length = int(self.headers.get("Content-Length")) 
            data = self.rfile.read(content_length) 
            
            #parsing JSON to a python dictonary
            dict = json.loads(data)
            
            #getting the name of the molecule and loading the molecule
            molName = dict["name"]
            mol = db.load_mol(molName)
            
            #performing a rotation of the molecule 90 degrees around the y axis
            mx = molecule.mx_wrapper(0,90,0)
            mol.xform(mx.xform_matrix)
            
            #getting the svg of the rotated molecule
            mol.sort()
            svg = mol.svg()
            message = svg

            self.send_response( 200 ); 
            self.send_response( 200 ); 
            self.send_header( "Content-type", "text/plain" )
            self.send_header( "Content-length", len(message) )
            self.end_headers()

            self.wfile.write( bytes( message, "utf-8" ) )
        
        #path for zrotation
        elif self.path == "/zRotation":
            #reading data from JS
            content_length = int(self.headers.get("Content-Length")) 
            data = self.rfile.read(content_length) 
            
            #parsing JSON to a python dictonary
            dict = json.loads(data)
            
            #getting the molecule name and loading the molecule
            molName = dict["name"]
            mol = db.load_mol(molName)
            
            #perfoming a rotation of the molecule 90 degrees around the z axis
            mx = molecule.mx_wrapper(0,0,90)
            mol.xform(mx.xform_matrix)
            
            #getting the svg of the rotated molecule
            mol.sort()
            svg = mol.svg()
            message = svg

            self.send_response( 200 ); 
            self.send_response( 200 ); 
            self.send_header( "Content-type", "text/plain" )
            self.send_header( "Content-length", len(message) )
            self.end_headers()

            self.wfile.write( bytes( message, "utf-8" ) )

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

httpd = HTTPServer(("localhost", int(sys.argv[1])), MyHandler)
httpd.serve_forever()
