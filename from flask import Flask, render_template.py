from flask import Flask, render_template, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

OPENROUTER_API_KEY = "" \
"" \
"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"  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/kesesuaian")
def get_kesesuaian():
    keyword = request.args.get("keyword", "")
    conn = sqlite3.connect("data/kesesuaian.db")
    c = conn.cursor()
    c.execute("SELECT * FROM kesesuaian WHERE nama_lokasi LIKE ?", ('%' + keyword + '%',))
    rows = c.fetchall()
    conn.close()
    data = [{"id": r[0], "nama_lokasi": r[1], "kelas": r[2]} for r in rows]
    return jsonify(data)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    # Step 1: Coba jawab pertanyaan pakai SQLite
    conn = sqlite3.connect("data/kesesuaian.db")
    c = conn.cursor()
    if "sangat sesuai" in user_input.lower():
        c.execute("SELECT nama_lokasi FROM kesesuaian WHERE kelas = 'Sangat Sesuai'")
        rows = c.fetchall()
        conn.close()
        lokasi = [r[0] for r in rows]
        answer = f"Lokasi yang sangat sesuai: {', '.join(lokasi)}"
        return jsonify({"reply": answer})

    # Step 2: Kirim ke model via OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral:instruct",  # bisa diganti dengan model lain
            "messages": [
                {"role": "system", "content": "Kamu adalah asisten GIS yang menjawab pertanyaan tentang kesesuaian lahan berdasarkan data SQLite yang berisi nama lokasi dan kelas kesesuaian (Sangat Sesuai, Cukup Sesuai, Tidak Sesuai)."},
                {"role": "user", "content": user_input}
            ]
        }
    )

    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
