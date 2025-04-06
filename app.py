print("🧠 App.py is running...")

from flask import Flask, render_template, request, send_file, session, redirect, url_for, flash
import os
from utils.analyzer import analyze_data, generate_proposal, generate_summary
import pandas as pd
from export import export_summary_to_pdf
import random


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'


def generate_ai_suggestions(villages):
    suggestions = []
    for v in villages:
        msg = f"📍 <strong>{v['Village Name']} ({v['Region']})</strong> – "
        if v["Literacy Rate"] < 50 and v["Connectivity Score"] < 5:
            msg += "Launch a <em>Literacy & Digital Access Program</em> due to low literacy and poor connectivity."
        elif v["Literacy Rate"] < 50:
            msg += "Initiate <em>Basic Education Scheme</em> to uplift low literacy rates."
        elif v["Connectivity Score"] < 5:
            msg += "Improve digital and road connectivity through <em>Smart Village Initiative</em>."
        else:
            msg += "This village is well-performing. Consider <em>Model Village Pilot Project</em> here."
        suggestions.append(msg)
    return suggestions


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'datafile' not in request.files:
            flash('No file part in the request')
            return redirect(request.url)

        file = request.files['datafile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Run analysis
            stats = analyze_data(filepath)
            df = pd.read_csv(filepath)
            proposals_df = stats['proposals']
            proposals = proposals_df.to_dict(orient='records')

            # Convert villages for suggestions
            village_list = df.to_dict(orient='records')
            suggestions = generate_ai_suggestions(village_list)

            # Generate summary text
            summary = generate_summary(village_list)
            session['summary'] = summary

            return render_template(
                'index.html',
                stats={
                    'total_villages': len(df),
                    'avg_literacy': round(df['Literacy Rate'].mean(), 2),
                    'avg_connectivity': round(df['Connectivity Score'].mean(), 2),
                    'weakest_area': df.loc[df['Connectivity Score'].idxmin()]['Village Name'],
                    'chart_regions': df['Region'].tolist(),
                    'chart_literacy': df['Literacy Rate'].tolist(),
                    'chart_connectivity': df['Connectivity Score'].tolist()
                },
                proposals=proposals,
                summary=summary.split('\n'),
                filepath=filepath,
                suggestions=suggestions
            )

    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    filepath = request.form.get('filepath')
    print("🧾 Received filepath:", filepath)

    if not filepath or not os.path.exists(filepath):
        return 'File path is invalid or missing', 400

    df = pd.read_csv(filepath)
    stats = analyze_data(filepath)
    proposals_df = stats['proposals']
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'proposals_output.csv')
    proposals_df.to_csv(output_path, index=False)

    return send_file(output_path, as_attachment=True)


@app.route('/export/pdf')
def download_pdf():
    summary_text = session.get("summary", "No summary available")
    filepath = export_summary_to_pdf(summary_text)
    return send_file(filepath, as_attachment=True)
def _bless_creator():
    return "Made by Sarim Saudagar"
_bless_creator()


if __name__ == '__main__':
    print("🚀 Starting Flask Server...")
    app.run(debug=True)
