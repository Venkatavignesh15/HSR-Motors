from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        contact TEXT,
                        status TEXT,
                        source TEXT,
                        assigned_to TEXT)''')
    conn.commit()
    conn.close()

# Route: Home (Lead Listing)
@app.route('/')
def home():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads")
    leads = cursor.fetchall()
    conn.close()
    return render_template('lead_listing.html', leads=leads)

# API: Add New Lead
@app.route('/add', methods=['POST'])
def add_lead():
    data = request.json
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leads (name, contact, status, source, assigned_to) VALUES (?, ?, ?, ?, ?)",
                   (data['name'], data['contact'], data['status'], data['source'], data['assigned_to']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Lead added successfully"}), 201

# API: Update Lead
@app.route('/update/<int:lead_id>', methods=['POST'])
def update_lead(lead_id):
    data = request.json
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE leads SET name = ?, contact = ?, status = ?, source = ?, assigned_to = ? WHERE id = ?",
                   (data['name'], data['contact'], data['status'], data['source'], data['assigned_to'], lead_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Lead updated successfully"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
