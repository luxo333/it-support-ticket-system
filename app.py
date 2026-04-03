from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        status = request.form["status"]
        priority = request.form["priority"]

        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tickets (title, description, status, priority) VALUES (?, ?, ?, ?)",
            (title, description, status, priority)
        )

        conn.commit()
        conn.close()

        return "Ticket submitted successfully! <br><a href='/'>Go back</a> | <a href='/tickets'>View tickets</a>"

    return render_template("index.html")


@app.route("/tickets")
def view_tickets():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    conn.close()

    return render_template("tickets.html", tickets=tickets)


@app.route("/update_status/<int:ticket_id>", methods=["POST"])
def update_status(ticket_id):
    new_status = request.form["status"]

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (new_status, ticket_id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("view_tickets"))


@app.route("/delete_ticket/<int:ticket_id>", methods=["POST"])
def delete_ticket(ticket_id):
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("view_tickets"))

@app.route("/edit_ticket/<int:ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        status = request.form["status"]
        priority = request.form["priority"]

        cursor.execute(
            """
            UPDATE tickets
            SET title = ?, description = ?, status = ?, priority = ?
            WHERE id = ?
            """,
            (title, description, status, priority, ticket_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("view_tickets"))

    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    conn.close()

    return render_template("edit_ticket.html", ticket=ticket)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)