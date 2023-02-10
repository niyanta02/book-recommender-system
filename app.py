from flask import Flask, render_template
import pickle

final_popular_df = pickle.load(open('popular.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(final_popular_df['Book-Title'].values),
                           author=list(final_popular_df['Book-Author'].values),
                           image=list(final_popular_df['Image-URL-M'].values),
                           votes=list(final_popular_df['num_ratings'].values),
                           rating=list(final_popular_df['avg_ratings'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template(('recommend.html'))

if __name__ == '__main__':
    app.run(debug=True)
