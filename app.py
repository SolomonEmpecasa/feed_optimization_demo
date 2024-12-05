from flask import Flask, render_template, send_from_directory, session
from model import load_data, generate_fake_data, optimize_feed

app = Flask(__name__)

app.secret_key = 'your_secret_key'

df = load_data("houses.csv")

@app.route('/')
def index():
    # Load data
    df = load_data("houses.csv")

    # Ensure DataFrame is not empty
    if df.empty:
        return "Error: DataFrame is empty."

    clicked_house_id = session.get('clicked_house_id', None)
    

    # Optimize feed
    optimized_df = optimize_feed(df, clicked_house_id)

    return render_template('index.html', houses=optimized_df.to_dict('records'))

@app.route('/house/<int:house_id>')
def house_detail(house_id):
    session['clicked_house_id'] = house_id

    # Retrieve specific house details based on the house_id
    house_details = df.loc[df['id'] == house_id].to_dict('records')[0]

    # Ensure the house exists (optional)
    if not house_details:
        return "Error: House not found."

    return render_template('house_detail.html', house=house_details)

@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True)