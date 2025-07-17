from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'same_random_data'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'phone_inventory'

mysql = MySQL(app)

@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM designed_phones_tbl")
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('index.html', phones=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name_of_phone']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_no = request.form['batch_no']
        phone_subtype = request.form['phone_subtype']

        cursor = mysql.connection.cursor()
        cursor.execute("""INSERT INTO designed_phones_tbl(name_of_phone, price, quantity, expiry_date, batch_no, phone_subtype)
                        VALUES(%s, %s, %s, %s, %s, %s)
        """,(name, price, quantity, expiry_date, batch_no, phone_subtype))
        mysql.connection.commit()
        flash("Successfully Added Phone")
        return redirect(url_for('Index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name_of_phone']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_no = request.form['batch_no']
        phone_subtype = request.form['phone_subtype']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE designed_phones_tbl
            SET name_of_phone=%s, price=%s, quantity=%s, expiry_date=%s, batch_no=%s, phone_subtype=%s
            WHERE id=%s
        """, (name, price, quantity, expiry_date, batch_no, phone_subtype, id_data))
        mysql.connection.commit()
        flash("Phone Updated Successfully!")
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM designed_phones_tbl WHERE id = %s", (id_data,))
    mysql.connection.commit()
    flash("Phone Deleted Successfully!")
    return redirect(url_for('Index'))

    if __name__ == '__main__':
        app(debug=True,port=5000)