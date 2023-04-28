from flask import Flask, render_template, request, url_for, flash, redirect, Response
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect
import cv2
import numpy as np
import tensorflow
import math
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
from tensorflow import keras
import re

from config import config

#Models
from models.ModelUser import ModelUser

#Entities
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(ID):
    return ModelUser.get_by_ID(db,ID)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user = User(1, "", "", request.form['email'], request.form['password'], None, None)
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('dashboard'))
            else:
                flash("Revise la contraseña")
                return render_template('login.html')
        else:
            flash("Usuario no existe")
            return render_template('login.html')
    else:
        return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Validar los datos del formulario
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        document = request.form['document']
        super_user = 0
        if not name or not last_name or not email or not password or not confirm_password or not document:
            flash("Falta información requerida para el registro.")
            return render_template('registro.html')
        
        # Verificar si el email ya está en uso
        existing_user = ModelUser.login(db, User(None, None, None, email, password, None, None))
        if existing_user is not None:
            flash("El correo electrónico ya está registrado.")
            return render_template('registro.html')

        # Verificar que las contraseñas ingresadas cumplan con los requisitos
        if password != confirm_password:
            flash("Las contraseñas no coinciden.")
            return render_template('registro.html')
        elif len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.")
            return render_template('registro.html')
        elif not re.search("[@_!#$%^&*()<>?/\|}{~:.]", password):
            flash("La contraseña debe contener al menos un caracter especial.")
            return render_template('registro.html')


        #Validacion del Correo misena
        pattern = r"@(misena.edu.co|soy.sena.edu.co)$"
        if not re.search(pattern, email):
            flash("El correo electrónico debe ser de dominio @misena.edu.co o @soy.sena.edu.co")
            return render_template('registro.html')

        # Crear un objeto User con los datos del formulario
        new_user = User(None, name, last_name, email, password, document, super_user)
        
        # Guardar el nuevo usuario en la base de datos
        success = ModelUser.create(db, new_user)
        if success:
            flash("Registro exitoso. Inicia sesión para continuar.")
            return redirect(url_for('signin'))
        else:
            flash("Ha ocurrido un error al registrar al usuario. Intenta nuevamente.")
            return render_template('registro.html')
    else:
        return render_template('registro.html')


@app.route('/traductor')
@login_required
def traductor():
    return render_template('traductor.html')

# Realizamos la Videocaptura
cap = cv2.VideoCapture(0)

detector = HandDetector(maxHands=1)

classifier = Classifier("Model\keras_model7.h5", "Model\labels7.txt")

offset = 20
imgSize = 300

labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
          "V", "W", "X", "Y", "Z", "Hola"]

# Mostramos el video en RT
def gen_frame():

    while True:
        success, img = cap.read()
        frame = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            if not imgCrop.size:  # Si la imagen es vacía, salta a la siguiente iteración del bucle
                continue

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                print(prediction, index)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

            cv2.rectangle(frame, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (18, 218, 157), cv2.FILLED)
            cv2.putText(frame, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(frame, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (18, 167, 118), 4)

            # cv2.imshow("ImageCrop", imgCrop)
            # cv2.imshow("ImageWhite", imgWhite)




        suc, encode = cv2.imencode('.jpg', frame)
        frame = encode.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



# Ruta del video
# Ruta del video
@app.route('/video')
@login_required
def video():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/home')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



def status_401(error):
    return redirect(url_for('signin'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>"


@app.route('/reset_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('recuperar_contras.html')
    else:
         # Validar los datos del formulario
        email = request.form['email']
        return render_template('recuperar_contras.html')



if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(debug=True, port=2505)
