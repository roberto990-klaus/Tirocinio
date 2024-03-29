from mysql.connector import Error
import mysql.connector
from flask import Flask, request, render_template, redirect, jsonify, url_for, session, flash, send_from_directory, request, send_file, make_response
from flask_mail import Mail, Message
from codicefiscale import codicefiscale
from itsdangerous import URLSafeTimedSerializer
from model.classification_utils import load_model
import os, hashlib, base64, random, string, pdfkit, json
from werkzeug.utils import secure_filename
from heatmap import generate_heatmap, get_image_info
from datetime import datetime
from flask_caching import Cache
import threading
import tkinter as tk


cache = Cache()

app = Flask(__name__) # Inizializza l'app Flask
app.secret_key = "chiave_segreta" # Imposta la chiave segreta per la sessione
app.config['CACHE_TYPE'] = 'simple'  # Usa una cache semplice per scopi di sviluppo
cache.init_app(app)

# Funzione per creare la finestra Tkinter
def create_window():
    root = tk.Tk()
    root.mainloop()

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



#Rotta per gestire la traduzione
@app.route('/translation/<lang>.json')
def get_translation(lang):
    return send_from_directory('translation', lang + '.json')



# Configurazione Flask-Mail per l'invio di email tramite Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'robertofalco990@gmail.com'
app.config['MAIL_PASSWORD'] = 'gfsieonfqhemtzhl'
app.config['MAIL_DEFAULT_SENDER'] = 'robertofalco990@gmail.com'

mail = Mail(app)

@app.route('/')
def index():
    # Esegui il redirect a /login
    return redirect(url_for('login'))


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
        messaggio = None
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



#Rotta per la generazione del codice fiscale tramite la libreria
@app.route("/generate_codice_fiscale", methods=["POST"])
def generate_codice_fiscale_endpoint():
    try:
        nome = request.form["nome"]
        cognome = request.form["cognome"]
        data_di_nascita = request.form["data"]
        sesso = request.form["sesso"]
        luogo_di_nascita = request.form["luogo_di_nascita"]

        codice_fiscale = generate_codice_fiscale(nome, cognome, data_di_nascita, sesso, luogo_di_nascita)
        print(codice_fiscale)

        return jsonify({"codice_fiscale": codice_fiscale})

    except Exception as e:
        print(f"Errore nella generazione del codice fiscale: {str(e)}")
        return jsonify({"error": "Errore durante la generazione del codice fiscale."})


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
        
        
        # Converte la data di nascita nel formato corretto
        data_di_nascita = datetime.strptime(data_di_nascita, '%d/%m/%Y').strftime('%Y-%m-%d')



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




######################################## FORM PER IL CARICAMENTO DELL'IMMAGINE DOPO IL LOGIN #######################################


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
            plot_path, previsione = generate_heatmap(temp_file_path)

            # Rimuovi il file temporaneo dopo l'elaborazione
            os.remove(temp_file_path)

            # Ottiene la previsione dalla funzione get_image_info
            predicted_class_name = get_image_info(plot_path, previsione)
            classe_predetta = predicted_class_name
            previsione = str(classe_predetta[1])
            print("#####################################################", previsione)

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
        
    # Aggiorna la cache solo la prima volta che la pagina viene visitata dopo il login
    if 'visited_after_login' not in session:
        cache.clear()  # Cancella la cache
        session['visited_after_login'] = True  # Imposta la variabile di sessione

    return render_template('after_login.html')



######################################## FORM VISUALIZZA IMMAGINE #######################################


# Rotta per gestire la visualizzazione delle immagini analizzate prese dal db
@app.route("/visualizzanalisi.html")
def visualizza_analisi():
    # Recupera l'email dell'utente loggato
    email_utente = session.get('email_utente')
    
    # Query per recuperare le informazioni sull'immagine per l'utente loggato
    cursore.execute("SELECT id, immagine, data, previsione FROM immagini_utenti WHERE email_utente = %s", (email_utente,))
    result = cursore.fetchall()

    # Lista per memorizzare le informazioni sull'immagine
    image_infos = []

    # Itera attraverso ogni risultato per ottenere le informazioni sull'immagine
    for row in result:

        # ID dell'immagine
        image_id = row[0]
        print("ID -->", image_id)
        # Codifica i dati binari dell'immagine in Base64
        img_base64 = base64.b64encode(row[1]).decode("utf-8")

        # Ottieni la data come stringa nel formato desiderato
        date_str = row[2].strftime("%d-%m-%Y %H:%M:%S")

        # Aggiungi le informazioni sull'immagine alla lista
        image_infos.append({"id": image_id, "image_data": img_base64, "date": date_str, "prediction": row[3]})




    # Passa la lista di informazioni sull'immagine all'HTML
    return render_template('visualizzanalisi.html', image_infos=image_infos)


# Rotta per eliminare un'immagine dal database
@app.route("/elimina_immagine", methods=['POST'])
def elimina_immagine():
    # Ottieni l'ID dell'immagine dalla richiesta POST
    immagine_id = request.form.get('immagine_id')
    print("ID dell'immagine ottenuto:", immagine_id)

    # Esegui la query per eliminare l'immagine dal database
    cursore = db_connessione.cursor()
    cursore.execute("DELETE FROM immagini_utenti WHERE id = %s", (immagine_id,))
    db_connessione.commit()
    cursore.close()
    # Ritorna una risposta di conferma
    return "Immagine eliminata con successo"



########### STAMPA PDF ################

# Funzione per generare un nome casuale di 10 caratteri alfanumerici
def generate_random_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Imposta il percorso di wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    image_data = data.get('image_data')
    prediction = data.get('prediction')
    
    # Debug: stampa il valore del parametro della lingua ricevuto
    lingua = request.args.get('lingua', 'en')  # Predefinito: inglese
    print('Lingua selezionata:', lingua)

    # Seleziona il template HTML corretto in base alla lingua selezionata
    if lingua == 'it':
        template_name = 'stampa_pdf_it.html'
    else:
        template_name = 'stampa_pdf_en.html'

    # Genera un nome casuale per il PDF
    pdf_name = generate_random_name() + '.pdf'

    # Leggi l'immagine del logo come dati binari
    logo_path = os.path.join(app.root_path, 'static', 'Unimol-logo.png')
    with open(logo_path, 'rb') as f:
        logo_data = f.read()

    # Converti i dati binari dell'immagine del logo in base64
    logo_base64 = base64.b64encode(logo_data).decode('utf-8')

    # Passa i dati all'interno del template HTML
    html_content = render_template(template_name, image_data=image_data, prediction=prediction, unimol_logo_base64=logo_base64)

    # Genera il PDF
    pdf_data = pdfkit.from_string(html_content, False, configuration=config)

    # Crea una risposta HTTP con il PDF come dati
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={pdf_name}'

    return response



@app.route('/download/<filename>', methods=['GET'])
def download_pdf(filename):
    pdf_dir = os.path.join(app.root_path, 'pdf')
    return send_from_directory(pdf_dir, filename)



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
        cursore.execute("UPDATE utenti SET conferma_token_modifica = '' WHERE email = %s", (email,))
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
                cursore.execute("UPDATE utenti SET conferma_token_modifica = %s WHERE email = %s", (modifica_token, email))

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

                messaggio = "I tuoi dati sono stati modificati con successo. Controlla la tua email per confermare la modifica dei dati"
                return jsonify({"success": messaggio})
            else:
                messaggio = "Email o password errate. Riprovare !!!"
                return jsonify({"error": messaggio})
        else:
            messaggio = "Email o password errate. Riprovare !!!"
            return jsonify({"error": messaggio})

    return render_template("modifica_dati.html")


# Aggiungiamo una nuova route per recuperare e visualizzare i dati dell'utente loggato
@app.route("/dati_utente", methods=["GET"])
def dati_utente():
    # Verifica se l'utente è loggato
    if 'email_utente' not in session:
        return jsonify({"error": "Utente non autenticato"})

    # Recupera l'email dell'utente dalla sessione
    email_utente = session["email_utente"]

    # Query per recuperare i dati dell'utente dal database
    cursore = db_connessione.cursor()
    cursore.execute("SELECT nome, cognome, data_di_nascita, cf FROM utenti WHERE email = %s", (email_utente,))
    utente = cursore.fetchone()
    cursore.close()

    # Verifica se l'utente è stato trovato nel database
    if utente:
        # Converte la data di nascita in formato stringa
        data_di_nascita = utente[2].strftime("%d-%m-%Y")

        # Costruisce il dizionario con i dati dell'utente
        dati_utente = {
            "nome": utente[0],
            "cognome": utente[1],
            "data_di_nascita": data_di_nascita,
            "cf": utente[3]
        }

        # Restituisce i dati dell'utente come JSON
        return jsonify(dati_utente)
    else:
        return jsonify({"error": "Utente non trovato"})







######################################## FORM INFO PAGE #######################################


# Definizione di una route per la pagina dopo aver effettuato l'accesso
@app.route("/infopage.html")
def infopage():
    print("Accessing after_login page.")
    return render_template('infopage.html')




######################################## FORM ELIMINA DATI #######################################

# Funzione per inviare l'email di conferma per l'eliminazione
def send_elimina_confirmation_email(email):
    subject = 'Conferma eliminazione account'
    body = 'Il tuo account è stato eliminato con successo.'
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

# Rotta per il form di eliminazione del profilo
@app.route("/elimina_dati.html", methods=["GET", "POST"])
def elimina_dati():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password: 
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            try:
                # Controllo della password
                with db_connessione.cursor() as cursore_controllo:
                    verifica_password = "SELECT * FROM utenti WHERE email = %s AND password = %s"
                    dati_verifica_password = (email, hashed_password)
                    cursore_controllo.execute(verifica_password, dati_verifica_password)
                    utente = cursore_controllo.fetchone()

                    if utente:
                        # Eliminazione delle righe correlate nella tabella "immagini_utenti"
                        with db_connessione.cursor() as cursore_elimina_immagini:
                            elimina_immagini = "DELETE FROM immagini_utenti WHERE email_utente = %s"
                            cursore_elimina_immagini.execute(elimina_immagini, (email,))

                        # Eliminazione dell'utente dalla tabella "utenti"
                        with db_connessione.cursor() as cursore_elimina_utente:
                            elimina_utente = "DELETE FROM utenti WHERE email = %s"
                            cursore_elimina_utente.execute(elimina_utente, (email,))

                        # Commit della transazione
                        db_connessione.commit()

                        # Invia l'email di conferma per l'eliminazione
                        send_elimina_confirmation_email(email)

                        # Restituzione del messaggio di successo
                        messaggio = "Il tuo account è stato eliminato con successo !!! Tra qualche istante verrai riportato alla pagina principale"
                        return jsonify({"success": messaggio})
                    else:
                        # Se la password non corrisponde, restituisci un errore
                        return jsonify({"error": "Email o password errata. Riprovare !!!"})

            except mysql.connector.Error as error:
                # Rollback della transazione in caso di errore
                db_connessione.rollback()
                return jsonify({"error": str(error)})

    return render_template("elimina_dati.html")



# Definizione di una route per la pagina dopo aver effettuato l'accesso
@app.route("/error")
def errorpage():
    print("Accessing error page.")
    return render_template('error.html')


@app.route("/logout")
def logout():
    if not session.get('logged_in'):
        # L'utente non è loggato, reindirizzalo alla pagina di errore personalizzata
        return render_template('login.html')

    # Rimuovi la chiave 'logged_in' dalla sessione
    session.pop("logged_in", None)
    # Reindirizza l'utente alla pagina di login o alla pagina principale
    return render_template('login.html')


#elimina la richiesta favicon.ico del sito web, ossia l'icona personalizzata
@app.route("/favicon.ico") 
def no_favicon():
    return "", 204


if __name__ == "__main__":
    # Avvia la finestra Tkinter nel thread principale
    create_window_thread = threading.Thread(target=create_window)
    create_window_thread.start()

    # Avvia il server Flask nel thread principale
    app.run(host='0.0.0.0', port=5000, debug=True)

