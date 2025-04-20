from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load only required CSVs
centrality_df = pd.read_csv("betweenness_centrality.csv", encoding="latin1")
top_5_df = pd.read_csv("top_5_recommendations_per_student.csv", encoding="latin1")

# Clean column names for consistency
centrality_df.columns = centrality_df.columns.str.strip().str.lower().str.replace(" ", "_")
top_5_df.columns = top_5_df.columns.str.strip().str.lower().str.replace(" ", "_")

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    centrality_score = None
    username = ""

    if request.method == "POST":
        username = request.form["name"]

        # Get centrality score
        match = centrality_df[centrality_df["student"].str.lower() == username.lower()]
        if not match.empty:
            centrality_score = round(float(match["centrality_score"].values[0]), 5)

        # Get top 5 recommendations
        filtered = top_5_df[top_5_df["student_a"].str.lower() == username.lower()]
        recommendations = filtered[["student_b", "mutual_connections"]].to_dict("records")

    return render_template("index.html",
                           username=username,
                           centrality_score=centrality_score,
                           recommendations=recommendations)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
