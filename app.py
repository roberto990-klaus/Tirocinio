<<<<<<< HEAD
import mysql.connector
=======
import mysql.connector 
>>>>>>> a545e1a21c545e275ccdd6ba8381568ed5bece41
from mysql.connector import Error
from flask import Flask, request, render_template, redirect, jsonify, url_for, session, flash , abort
from flask_mail import Mail, Message
import hashlib
from codicefiscale import codicefiscale
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
<<<<<<< HEAD
from model import classification_utils, load_model, predict, load_image
=======
>>>>>>> a545e1a21c545e275ccdd6ba8381568ed5bece41



app = Flask(__name__) #nome app che stiamo creando
<<<<<<< HEAD

app.secret_key = "chiave_segreta" #chiave segreta per gesitre la sessione in caso di login corretto
model_data = load_model()




@app.route('/predict', methods=['POST'])
def make_prediction():
    if 'file' not in request.files:
        return "Nessun file trovato"

    file = request.files['file']

    if file.filename == '':
        return "Nome file non valido"

    img = load_image(file, model_data['channels'], resize=model_data['img_dim'])
    prediction = predict(model_data['model'], img, model_data['class_names'])

    # Restituisci il risultato come JSON
    return jsonify({"prediction": prediction})



=======
app.secret_key = "chiave_segreta" #chiave segreta per gesitre la sessione in caso di login corretto
>>>>>>> a545e1a21c545e275ccdd6ba8381568ed5bece41


# Configurazione del database MySQL e prova di verifica della connessione riuscita
db_connessione = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tirociniosql"
)
print(db_connessione) #Stampa a video se mysql.connector si è connesso con successo al database

#Prova di connessione ulteriore, con stampa a video di tutti gli utenti presenti nel db
if db_connessione.is_connected():
    print("Connessione riuscita!!!")
    cursore = db_connessione.cursor()
    cursore.execute("SELECT * FROM utenti")
    risultato = cursore.fetchall()
    for x in risultato:
        print(x)


# Configurazione Flask-Mail per l'invio di email tramite Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'robertofalco990@gmail.com'
app.config['MAIL_PASSWORD'] = 'gfsieonfqhemtzhl'
app.config['MAIL_DEFAULT_SENDER'] = 'robertofalco990@gmail.com'

mail = Mail(app)


# Definizione di una route per la pagina principale
@app.route("/login.html")
def login_page():
    return render_template('login.html')

# Definizione di una route per la pagina dopo aver effettuato l'accesso
@app.route("/infopage.html")
def infopage():
    print("Accessing after_login page.")
    return render_template('infopage.html')

@app.route("/visualizzanalisi.html")
def visualizzanalisi():
    print("Accessing after_login page.")
    return render_template('visualizzanalisi.html')




@app.route("/after_login.html")
def after_login():
    print("Accessing after_login page.")
    return render_template('after_login.html')

#################################### FORM DI LOGIN ###########################


@app.route("/login", methods =  ["GET", "POST"]) #/login corrisponde all'action nel file html login.html
def login():
    if request.method == 'POST':
        email = request.form["email_login"] #nel form html "email" corrisponde al campo name=email
        password = request.form["password_login"]

        # Cifra la password inserita usando SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursore = db_connessione.cursor()
        verifica_credenziali = "SELECT * FROM utenti WHERE email = %s AND password = %s"
        dati = (email, hashed_password)
        
        cursore.execute(verifica_credenziali, dati)
        utente = cursore.fetchone()

        messaggio = None
        if utente and len(utente) >= 7 and utente[6] == '':
            session["logged_in"] = True
            #Print di verifica dal terminale
            print(f"Login effettuato per l'utente: {email}")
            return jsonify({"redirect": "/after_login.html"})
        else: 
            print("L'utente non è presente nel database.")
            messaggio = "Credenziali errate! Riprova."
            return jsonify({"error": messaggio})
    else:
        return render_template ('login.html')
    


#################################### FORM DI REGISTRAZIONE ###########################


###########Conferma email registrazione (presente nel form di login)

# Funzione per generare il token di conferma casuale
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt='email-confirm')

# Funzione per verificare il token di conferma
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
    except:
        return False
    return email

# Funzione per inviare l'email di conferma
def send_confirmation_email(email, token):
    confirmation_link = url_for('confirm_email', token=token, _external=True)
    subject = 'Conferma il tuo account'
    body = f'Clicca sul seguente link per confermare il tuo account: {confirmation_link}'

    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)


@app.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    if email:
        # Aggiorna il campo 'conferma_token' nel database per indicare che l'utente ha confermato l'account
        cursore = db_connessione.cursor()
        cursore.execute("UPDATE utenti SET conferma_token = '' WHERE email = %s", (email,))
        db_connessione.commit()
        cursore.close()

        return render_template("conferma_email.html", email=email)
    else:
        return render_template("conferma_email.html", error="Il link di conferma non è valido o è scaduto.")
    

# Funzione per generare il codice fiscale
def generate_codice_fiscale(nome, cognome, data_di_nascita, sesso, luogo_di_nascita):

    codice_fiscale = codicefiscale.encode(
        firstname=nome,
        lastname=cognome,
        gender=sesso,  
        birthdate=data_di_nascita,
        birthplace=luogo_di_nascita 
        )

    return str(codice_fiscale)

<<<<<<< HEAD

=======
>>>>>>> a545e1a21c545e275ccdd6ba8381568ed5bece41
########### Route per la generazione del codice fiscale tramite la libreria

@app.route("/generate_codice_fiscale", methods=["POST"])
def generate_codice_fiscale_endpoint():
    nome = request.form["nome"]
    cognome = request.form["cognome"]
    data_di_nascita = request.form["data"]
    sesso = request.form["sesso"]
    luogo_di_nascita = request.form["luogo_di_nascita"]

    codice_fiscale = generate_codice_fiscale(nome, cognome, data_di_nascita, sesso, luogo_di_nascita)

    return jsonify({"codice_fiscale": codice_fiscale}) #invia il codice fiscale generato sia al db che al form html per la visualizzazione


####### Route form di registrazione

@app.route("/register", methods = ["GET", "POST"])
def register():  
    if request.method == 'POST':
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        data_di_nascita = request.form["data"]
        sesso = request.form["sesso"]
        luogo_di_nascita = request.form["luogo_di_nascita"]
        email = request.form["email"]
        password = request.form["password"]

        # Genera il codice fiscale
        codice_fiscale = generate_codice_fiscale(nome, cognome, data_di_nascita, sesso, luogo_di_nascita)


        # Cifratura della password usando SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        #controlla se l'email è già presente nel database
        cursore = db_connessione.cursor()
        cursore.execute("SELECT * FROM utenti WHERE email = %s", (email,))
        utente_esistente = cursore.fetchone()
        cursore.close()

        messaggio = None
        if utente_esistente:
            messaggio = "Questo indirizzo email è già registrato."
            return jsonify({"error": messaggio})
        else:
            cursore = db_connessione.cursor()
            conferma_token = generate_confirmation_token(email)
            cursore.execute("INSERT INTO utenti (nome, cognome, data_di_nascita, email, cf, password, conferma_token) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (nome, cognome, data_di_nascita, email, codice_fiscale, hashed_password, conferma_token)) 
            db_connessione.commit()
            cursore.close()
             # Invia l'email di conferma
            send_confirmation_email(email, conferma_token)

            messaggio = "Registrazione completata con successo!  Controlla la tua email per confermare l'account."
            return jsonify({"success": messaggio})  
        
    return render_template("login.html", messaggio=messaggio, codice_fiscale=codice_fiscale)




######################################## FORM MODIFICA DATI #######################################


# Funzione per generare il token di conferma per la modifica dei dati
def generate_modifica_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt='modifica-confirm')


# Funzione per inviare l'email di conferma per la modifica dei dati
def send_modifica_confirmation_email(email, token):
    confirmation_link = url_for('confirm_modifica', token=token, _external=True)
    subject = 'Conferma la modifica dei tuoi dati'
    body = f'Clicca sul seguente link per confermare la modifica dei tuoi dati: {confirmation_link}'

    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)


# Funzione per la conferma del token di modifica
@app.route("/confirm_modifica/<token>")
def confirm_modifica(token):
    email = confirm_token(token, expiration=3600)
    if email:
        # Recupera lo stato di conferma dell'email dal database
        cursore = db_connessione.cursor()
        cursore.execute("UPDATE utenti SET conferma_token = '' WHERE email = %s", (email,))
        db_connessione.commit()
        cursore.close() 

        return render_template("conferma_modifica.html", email=email)
   
    else:
         # Gestisce il caso in cui il token non è valido o è scaduto
        return render_template("conferma_modifica.html", error="Il link di conferma non è valido o è scaduto.")



###### Route per il form di modifica dati

@app.route("/modifica_dati.html", methods=["GET", "POST"])
def modifica_dati():
    messaggio = None
    if request.method == "POST":
        #prendiamo in memoria email e password inseriti nel form html
        email = request.form.get("email")
        password = request.form.get("password")

        
        if email and password: #verifichiamo che questi campi sono stati inseriti
            cursore = db_connessione.cursor()
            verifica = "SELECT * FROM utenti WHERE email = %s AND password = %s"
            dati_verifica = (email, password)
            cursore.execute(verifica, dati_verifica) #cerca nel db un utente con email e password salvati sopra
            utente_esistente = cursore.fetchone() #va a memorizzare la prima riga trovata
        

            if utente_esistente:
                # Genera il token e salvalo nel database
                modifica_token = generate_modifica_token(email)
                cursore.execute("UPDATE utenti SET conferma_token = %s WHERE email = %s", (modifica_token, email))


                # Costruisci la query di aggiornamento
                query = "UPDATE utenti SET "                
                nuovo_nome = request.form.get("nuovo_nome")
                nuovo_cognome = request.form.get("nuovo_cognome")
                nuova_data = request.form.get("nuova_data")
                nuovo_codice_fiscale = request.form.get("nuovo_codice_fiscale")
                nuova_password = request.form.get("nuova_password")

                # Costruisci una query di aggiornamento dinamica senza segnaposto %s
                query = "UPDATE utenti SET "

                aggiornamenti = [] #lista in cui memorizziamo tutti i dati che devono essere modificati

                if nuovo_nome:
                    aggiornamenti.append(f"nome = '{nuovo_nome}'") #la f indica una stringa formattata
                if nuovo_cognome:
                    aggiornamenti.append(f"cognome = '{nuovo_cognome}'")
                if nuova_data:
                    aggiornamenti.append(f"data_di_nascita = '{nuova_data}'")
                if nuovo_codice_fiscale:
                    aggiornamenti.append(f"cf = '{nuovo_codice_fiscale}'")
                if nuova_password:
                    aggiornamenti.append(f"password = '{nuova_password}'")

                query += ", ".join(aggiornamenti) #concateniamo gli aggiornamenti in una unica stringa
                query += f" WHERE email = '{email}' AND password = '{password}'"

                # Esegui la query di aggiornamento
                cursore.execute(query)
                db_connessione.commit()
                cursore.close()
                
                # Invia l'email di conferma
                send_modifica_confirmation_email(email, modifica_token)

                messaggio = "I tuoi dati sono stati modificati con successo !!!"
                return jsonify({"success": messaggio})
                    
            else:
                messaggio = "Email o password errate. Riprovare !!!"
                return jsonify({"error": messaggio})


    return render_template("modifica_dati.html")



######################################## FORM ELIMINA DATI #######################################


# Funzione per generare il token di eliminazione
def generate_elimina_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt='elimina-confirm')


# Funzione per inviare l'email di conferma per l'eliminazione
def send_elimina_confirmation_email(email, token):
    confirmation_link = url_for('confirm_elimina', token=token, _external=True)
    subject = 'Conferma l\'eliminazione del tuo account'
    body = f'Clicca sul seguente link per confermare l\'eliminazione del tuo account: {confirmation_link}'

    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)


# Funzione per la conferma del token di modifica
@app.route("/confirm_elimina/<token>")
def confirm_elimina(token):
    email = confirm_token(token, expiration=3600)
    if email:
       # Invia l'email di conferma
        send_elimina_confirmation_email(email, token)


        return render_template("conferma_elimina.html", email=email)
    else:
        return render_template("conferma_elimina.html", error="Il link di conferma non è valido o è scaduto.")




####### Route per il form di eliminazione del profilo

@app.route("/elimina_dati.html", methods = ["GET", "POST"])
def elimina_dati():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password: 
            cursore = db_connessione.cursor()
            verifica = "DELETE FROM utenti WHERE email = %s AND password = %s"
            dati_verifica = (email, password)
            cursore.execute(verifica, dati_verifica)
            db_connessione.commit()
            print("Numero di righe cancellate:", cursore.rowcount)

            messaggio = None
            if cursore.rowcount > 0:
                cursore.close()
                messaggio = "Il tuo account è stato eliminato con successo !!! Tra qualche istante verrai riportato alla pagina principale"
                return jsonify({"success": messaggio})
            else:
                cursore.close()
                messaggio = "Email o password errata. Riprovare !!!"
                return jsonify({"error": messaggio})
            
            
    return render_template("elimina_dati.html")



#elimina la richiesta favicon.ico del sito web, ossia l'icona personalizzata
@app.route("/favicon.ico") 
def no_favicon():
    return "", 204





<<<<<<< HEAD


@app.route('/predict', methods=['POST'])
def make_prediction():
    if 'file' not in request.files:
        return "Nessun file trovato"

    file = request.files['file']

    if file.filename == '':
        return "Nome file non valido"

    img = load_image(file, model_data['channels'], resize=model_data['img_dim'])
    prediction = predict(model_data['model'], img, model_data['class_names'])

    # Restituisci il risultato come JSON
    return jsonify({"prediction": prediction})



=======
>>>>>>> a545e1a21c545e275ccdd6ba8381568ed5bece41
if __name__ == "__main__":
    app.run(port=5000, debug= True)
