from flask import Flask,render_template,url_for,jsonify,request,redirect
import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import check_password_hash,generate_password_hash 
from flask_jwt_extended import JWTManager
from functions import crear_token

app=Flask(__name__)


load_dotenv()

##Configuracion global del token
app.config["JWT_SECRET_KEY"] = "SECRETO"
jwt=JWTManager(app)

conexion=mysql.connector.connect(


    host="localhost",
    user="root",
    password="root",
    database="aplicacion"

)

@app.route("/",methods=["POST","GET"])

def redirigir():
    return redirect("register")


@app.route("/register",methods=["POST","GET"]) ## Ruta de registro de usuarios
def registro():

    if request.method=="GET":
        return render_template("register.html")
    
    correo=request.form.get("correo")
    password=request.form.get("password")

    if not correo or not password: ##Comprobacion de campos
        return jsonify({"message":"Faltan campos por completar","estado":False})
    
    cursor=conexion.cursor()

    cursor.execute("SELECT correo FROM usuarios WHERE correo=%s",(correo,))

    resultado=cursor.fetchone()

    if resultado: ##Comprobacion de si ya esta el correo registrado
        return jsonify({"message":"Este correo electronico ya esta registrado","estado":False})

    password_has=generate_password_hash(password)

    cursor.execute("INSERT INTO usuarios(correo,password) VALUES (%s,%s)",(correo,password_has))

    conexion.commit()

    return redirect("home")



@app.route("/login",methods=["POST","GET"]) ##Inicio de sesion

def login():

    if request.method=="GET":
        return render_template("login.html")

    correo=request.form.get("correo")
    password=request.form.get("password")

    if not correo or not password: ##Comprobacion de campos
        return jsonify({"message":"Faltan campos por completar","estado":False})
    
    cursor=conexion.cursor()


    cursor.execute("SELECT correo FROM usuarios WHERE correo=%s",(correo,))

    resultado_correo=cursor.fetchone()

    if not resultado_correo: ##Comprobacion de si el correo esta registrado
        return jsonify({"message":"El correo introducido no esta registrado","estado":False})
    

    cursor.execute("SELECT password FROM usuarios WHERE correo=%s",(correo,))

    resultado_pass=cursor.fetchone()

    if check_password_hash(resultado_pass[0],password):##Comprobacion de contraseñas haseadas
        token=crear_token(correo)
        return redirect("home")
    
    else:
        return jsonify({"message":"Las credenciales son incorrectas","estado":False})
    



@app.route("/home",methods=["POST","GET"])##Primera vista una vez logueado
def dashboard():
    if request.method=="GET":
        return render_template("home.html")
    
    favoritos=[]
    contador=5

    cursor=conexion.cursor()

    cursor.execute("SELECT nombre FROM FAVORITOS WHERE id")
   
    tiene_favoritos=cursor.fetchall()

    if not tiene_favoritos:


        while contador>0:
            contador-=1


            resultado=request.get_json("https://futuramaapi.com/api/random/character")##Peticion de la api

            personaje={

                "nombre":resultado.name,
                "genero":resultado.gender,
                "especie":resultado.species,
                "img":resultado.image

            }
                    
            favoritos.append(personaje)

        return favoritos

    else:
        return tiene_favoritos
        


if __name__=="__main__":
    app.run(debug=True)