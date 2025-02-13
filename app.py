#imports
import sqlite3
import os
from flask import Flask, session, render_template, request, g, redirect, url_for

app = Flask(__name__)
app.secret_key = "TeamTurtles@123456789"#secret key




#create the database if it does not yet exist
connection = sqlite3.connect("part.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS parts (
        idd INTEGER,
        name TEXT,
        amnt INTEGER
    )
""")

DATABASE = 'part.db'


#function that establishes connection to database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('part.db')
        
    return db

#close database connection when app context ends
@app.teardown_appcontext
def close_connection(exception):
    #print("teardown")
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        

#renders homepage
@app.route('/')
def index():
#    data = get_db()
    return render_template('index.html')

#adds a new part to the database
@app.route('/add', methods=['POST'])
def add_part():
    #takes in input from website
    idd = request.form['id']
    name = request.form['name']
    amnt = request.form['amnt']

    #checks if ID and Amount are numbers, and if not, gives an alert
    if not idd.isdigit() or not amnt.isdigit():
        return """
            <script>
                alert("ID and Amount must be valid numbers.");
                window.location.href = "/";
            </script>
        """

    #checks if part name is empty, and if not, gives an alert
    if not name:
        return """
            <script>
                alert("Part name cannot be empty.");
                window.location.href = "/";
            </script>
        """

    idd = int(idd)
    amnt = int(amnt)

    #checks if a part with the same ID already exists, and if so, increments the amount rather than creating a duplicate
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT amnt FROM parts WHERE idd = ?", (idd,))
    existing_part = cursor.fetchone()
    if existing_part:
        new_amnt = existing_part[0] + amnt
        cursor.execute("UPDATE parts SET amnt = ? WHERE idd = ?", (new_amnt, idd))
        message = f"Part ID {idd} already exists. Added {amnt} to the existing amount."
        db.commit()
        return f"""
            <script>
                alert("{message}");
                window.location.href = "/";
            </script>
        """
    else:
        cursor.execute("INSERT INTO parts (idd, name, amnt) VALUES (?, ?, ?)", (idd, name, amnt))
    
        db.commit()
        return redirect(url_for('index')) 
    

@app.route('/edit', methods=['POST'])
def edit_part():
    #function to edit the amount of an existing part in the database
    idd = request.form['id']
    amnt = request.form['amnt']

    if not idd.isdigit() or not amnt.isdigit():
        return """
            <script>
                alert("ID and Amount must be valid numbers.");
                window.location.href = "/";
            </script>
        """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE parts SET amnt = ? WHERE idd = ?", (amnt, idd))
    db.commit()
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_part():
    #function to delete a part with a given ID in database
    idd = request.form['id']

    if not idd.isdigit():
        return """
            <script>
                alert("ID must be valid numbers.");
                window.location.href = "/";
            </script>
        """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM parts WHERE idd = ?", (idd,))
    db.commit()
    return redirect(url_for('index'))
    

@app.route('/view', methods=['GET'])
def view_parts():
    #function that retrieves and displays all parts (ID, name, and amount)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM parts")
    parts = cursor.fetchall()
    return render_template('view.html', parts=parts)


@app.route('/deleteall', methods=['GET'])
def delete_all():
    #deletes everything from table
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM parts")
    db.commit()
    return redirect(url_for('view_parts'))

    
    
    
if __name__ == '__main__':
    app.run()
