import mysql.connector
from mysql.connector import Error
from flask import Flask, request, render_template, redirect, jsonify, url_for, session, flash , abort, send_from_directory, request, send_file, make_response, render_template_string
from flask_mail import Mail, Message
import hashlib
from hashlib import sha1
from codicefiscale import codicefiscale
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from model.classification_utils import load_model
import os
from werkzeug.utils import secure_filename
from heatmap import generate_heatmap, get_image_info
import base64
import random, string
import pdfkit
import imgkit



# Inizializza l'app Flask
app = Flask(__name__)
# Imposta la chiave segreta per la sessione
app.secret_key = "chiave_segreta"



 # Carica i dati del modello
model_data = load_model()
# Estrae il modello dal dizionario model_data
model = model_data['model']
# Estrae i nomi delle classi dal dizionario model_data
class_names = model_data['class_names']



@app.route('/translation/<lang>.json')
def get_translation(lang):
    return send_from_directory('translation', lang + '.json')




@app.route("/after_login.html", methods=["GET", "POST"])
def after_login():
    if request.method == "POST":
        # Controlla se l'utente è loggato
        if 'email_utente' not in session:
            flash('Effettua il login prima di caricare un\'immagine')
            return redirect(url_for('login_page'))

        if 'file' not in request.files:
            flash('Nessun file selezionato')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Nessun file selezionato')
            return redirect(request.url)

        try:
            # Salva il file temporaneo
            temp_dir = os.path.join(app.root_path, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.join(temp_dir, secure_filename(file.filename))
            file.save(temp_file_path)

            # Genera il plot e ottieni il percorso del file di plot
            plot_path = generate_heatmap(temp_file_path)

            # Rimuovi il file temporaneo dopo l'elaborazione
            os.remove(temp_file_path)

            # Ottieni la previsione dalla funzione get_image_info
            predicted_class_name = get_image_info(plot_path)
            classe_predetta = predicted_class_name
            previsione = str(classe_predetta[1])
 

            # Leggi l'immagine come dati binari
            with open(plot_path, "rb") as img_file:
                img_data = img_file.read()

            # Recupera l'email dell'utente loggato
            email_utente = session.get('email_utente')

            # Salva l'immagine convertita nel database associata all'utente loggato
            cursore.execute("INSERT INTO immagini_utenti (immagine, email_utente, previsione) VALUES (%s, %s, %s)", (img_data, email_utente, previsione))
            db_connessione.commit()
            db_connessione.close

            print("Immagine salvata nel database per l'utente:", email_utente)

            return send_file(plot_path, mimetype='image/jpeg')

        except Exception as e:
            flash(f'Errore durante l\'analisi dell\'immagine: {str(e)}')
            print("Errore durante l'analisi dell'immagine:", str(e))
            return redirect(request.url)

    return render_template('after_login.html')





@app.route("/visualizzanalisi.html")
def visualizza_analisi():
    # Recupera l'email dell'utente loggato
    email_utente = session.get('email_utente')
    
    # Query per recuperare le informazioni sull'immagine per l'utente loggato
    cursore.execute("SELECT immagine, data, previsione FROM immagini_utenti WHERE email_utente = %s", (email_utente,))
    result = cursore.fetchall()

    # Lista per memorizzare le informazioni sull'immagine
    image_infos = []

    # Itera attraverso ogni risultato per ottenere le informazioni sull'immagine
    for row in result:
        # Codifica i dati binari dell'immagine in Base64
        img_base64 = base64.b64encode(row[0]).decode("utf-8")

        # Ottieni la data come stringa nel formato desiderato
        date_str = row[1].strftime("%d-%m-%Y %H:%M:%S")

        # Aggiungi le informazioni sull'immagine alla lista
        image_infos.append({"image_data": img_base64, "date": date_str, "prediction": row[2]})

    # Passa la lista di informazioni sull'immagine all'HTML
    return render_template('visualizzanalisi.html', image_infos=image_infos)






# Imposta il percorso di wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    image_data = data.get('image_data')
    prediction = data.get('prediction')
    # Percorso dell'immagine del logo
    logo_path = 'unimol_logo.png'

    # Genera il PDF come stringa HTML
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Analisi Immagine</title>
        </head>
        <body>
            
            <h1 style="text-align: center;">Titolo del progetto: Progettazione e sviluppo di un portale web per la diagnosi automatica di patologie attraverso il deep learning</h1>
            
            <h1>Studente: Roberto Falcone</h1>
            <h1>Relatore: Francesco Mercaldo</h1>
            <h1>Correlatore: Giovanni Ciaramella</h1>
            <br>
            
            <h1 style="text-align: center;">Immagine Analizzata</h1>
            <img src="data:image/jpeg;base64,{image_data}" alt="Immagine Analizzata" style="display: block; margin: 0 auto;">
            <h1>Previsione: {prediction}</h1>
            <br>
            <h1>
                Informazioni Progetto
                <br>
                1	Dataset
                <br>
                Il dataset1 utilizzato in questo progetto contiene 25.000 immagini a colori in formato .jpeg, di cui 10.000 relative ad adenocarcinomi e tessuti benigni del colon e 15.000 relative ad adenocarcinomi polmonari, carcinomi polmonari a cellule squamose e tessuti polmonari benigni.

                Nel dettaglio nel dataset sono presenti 750 immagini di tessuto polmonare, in particolare, 250 di tessuto polmonare sano, 250 di adenocarcinomi polmonari e 250 di carcinomi a cellule squamose, rispettando la norma HIPAA.

                Tutte le immagini sono state in seguito ritagliate, utilizzando il linguaggio di programmazione Python, ottenendo dimensioni quadrate di 768x768 pixel dai 1024x768 pixel originali.

                Successivamente, le immagini sono state aumentate utilizzando il pacchetto software Augmentor, che ha permesso un ampliamento del set di dati a 15.000 immagini, mediante i seguenti aumenti: rotazioni sinistra e destra (fino a 25 gradi) e capovolgimenti orizzontali e verticali.
                <br>
                2	Classificazione
                <br>
                Per effettuare la classificazione e’ stata utilizzata un’architettura di Deep Learning denominata Standard CNN composta da uno strato convoluzionale, uno strato di pooling e uno strato completamente connesso.
                <br>
                2.1	Training phase
                <br>
                Il modello e’ stato addestrato con i seguenti iper-parametri:
                <br>
                epochs = 50; batch_size = 32; learning_rate = 0.0001; size_img = 110x3; Execution time = 1:00:17 (HH:MM:SS)
                Divisione del dataset in 80-10-10 (training-validation-test)
                <br>
                lung aca : 4000-499-500 -> 4999
                <br>
                lung_n : 4000-499-500 -> 4999
                <br>
                lung_scc : 4000-499-500 -> 4999
                <br>
                1 https://arxiv.org/pdf/1912.12142.pdf
                <br>
                Immagini relative alla loss e all’accuracy durante la fase di addestramento sono all’interno del file zip.
                <br>
                2.2	Test phase
                <br>
                L’immagine relativa alla matrice di confusione ottenuta durante la fase di test e’ presente all’interno del file zip.
                <br>
                test loss: 0.0818919986486435;
                <br>
                test accuracy:0.9819999933242798 Prec:0.9819999933242798 Recall:0.9819999933242798
                <br>
                F-Measure:0.9819999933242798 AUC:0.9951958656311035
                <br>
                Approssima tutto alla terza cifra decimale
                <br>
                3	Grad-CAM
                <br>
                Inserire informazioni descritte nell’articolo inviata tramite email. Inoltre aggiungere:
                Le aree significative sono rappresentate da colori come il giallo e le aree meno significative con colori come il blu o il verde.
            </h1>

        </body>
        </html>
    """



    # Genera il PDF utilizzando pdfkit e ottieni i dati binari del PDF
    pdf_data = pdfkit.from_string(html_content, False, configuration=config)

    # Crea una risposta con il PDF come allegato
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

    return response



@app.route('/download/<filename>', methods=['GET'])
def download_pdf(filename):
    pdf_dir = os.path.join(app.root_path, 'pdf')
    return send_from_directory(pdf_dir, filename)




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


# Configurazione Flask-Mail per l'invio di email tramite Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''

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








#################################### FORM DI LOGIN ###########################


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form["email_login"]
        password = request.form["password_login"]

        # Cifra la password inserita usando SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursore = db_connessione.cursor()
        verifica_credenziali = "SELECT * FROM utenti WHERE email = %s AND password = %s"
        dati = (email, hashed_password)
        
        cursore.execute(verifica_credenziali, dati)
        utente = cursore.fetchone()

        if utente and len(utente) >= 7 and utente[6] == '':
            # Memorizza l'accesso dell'utente nella sessione
            session["logged_in"] = True
            session["email_utente"] = email
            # Print di verifica nel terminale
            print(f"Login effettuato per l'utente: {email}")
            # Ritorna un messaggio di reindirizzamento come JSON
            return jsonify({"redirect": "/after_login.html"})
        else: 
            # Se le credenziali non corrispondono, ritorna un messaggio di errore come JSON
            print("L'utente non è presente nel database.")
            messaggio = "Credenziali errate! Riprova."
            return jsonify({"error": messaggio})

    return render_template('login.html')
    


##### FORM DI RECUPERO PASSWORD #############


@app.route("/recupera_password", methods=["POST"])
def recupera_password():
    if request.method == 'POST':
        email = request.form.get("email_recupero_password")
        
        # Controlla se l'email è presente nel database
        cursore = db_connessione.cursor()
        cursore.execute("SELECT * FROM utenti WHERE email = %s", (email,))
        utente = cursore.fetchone()
        cursore.close()

        if utente:
            # Se l'email è presente, genera una nuova password casuale
            nuova_password = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

            # Aggiorna la nuova password nel database per l'utente corrispondente all'email
            hashed_password = hashlib.sha256(nuova_password.encode()).hexdigest()
            cursore = db_connessione.cursor()
            cursore.execute("UPDATE utenti SET password = %s WHERE email = %s", (hashed_password, email))
            db_connessione.commit()
            cursore.close()

            # Invia l'email con la nuova password
            msg = Message("Nuova Password", recipients=[email])
            msg.body = f"Ecco la tua nuova password: {nuova_password}. Ti consigliamo di cambiarla dopo il login."
            mail.send(msg)

            # Restituisci un JSON con un messaggio di successo
            return jsonify({"success": "Una nuova password è stata inviata al tuo indirizzo email. Controlla la tua casella di posta."})
        else:
            # Se l'email non è presente, restituisci un JSON con un messaggio di errore
            return jsonify({"error": "L'indirizzo email fornito non è registrato nel nostro sistema."})

    return redirect(url_for('login_page'))



    


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



########### Route per la generazione del codice fiscale tramite la libreria

@app.route("/generate_codice_fiscale", methods=["POST"])
def generate_codice_fiscale_endpoint():
    nome = request.form["nome"]
    cognome = request.form["cognome"]
    data_di_nascita = request.form["data"]
    sesso = request.form["sesso"]
    luogo_di_nascita = request.form["luogo_di_nascita"]

    codice_fiscale = generate_codice_fiscale(nome, cognome, data_di_nascita, sesso, luogo_di_nascita)
    print(codice_fiscale)

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


# Funzione per verificare il token di conferma
def modifica_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(token, salt='modifica-confirm', max_age=expiration)
    except:
        return False
    return email


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
    email = modifica_token(token, expiration=3600)
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

        if email and password: #verifichiamo che questi campi siano stati inseriti
            # Cifra la password inserita usando SHA-256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursore = db_connessione.cursor()
            verifica = "SELECT * FROM utenti WHERE email = %s AND password = %s"
            dati_verifica = (email, hashed_password)
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

                aggiornamenti = [] 

                if nuovo_nome:
                    aggiornamenti.append(f"nome = '{nuovo_nome}'") 
                if nuovo_cognome:
                    aggiornamenti.append(f"cognome = '{nuovo_cognome}'")
                if nuova_data:
                    aggiornamenti.append(f"data_di_nascita = '{nuova_data}'")
                if nuovo_codice_fiscale:
                    aggiornamenti.append(f"cf = '{nuovo_codice_fiscale}'")
                if nuova_password:
                    hashed_nuova_password = hashlib.sha256(nuova_password.encode()).hexdigest()
                    aggiornamenti.append(f"password = '{hashed_nuova_password}'")

                query += ", ".join(aggiornamenti) 
                query += f" WHERE email = '{email}'"

                cursore = db_connessione.cursor()
                cursore.execute(query)
                db_connessione.commit()
                cursore.close()
                
                send_modifica_confirmation_email(email, modifica_token)

                messaggio = "I tuoi dati sono stati modificati con successo. Controlla la tua email per confermare l'account."
                return jsonify({"success": messaggio})
            else:
                print("Le password non corrispondono.")
                messaggio = "Email o password errate. Riprovare !!!"
                return jsonify({"error": messaggio})
        else:
            print("Nessuna password trovata per l'email specificata.")
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






if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=5000, debug= True)
