from flask import Flask, render_template, request
import pickle
import numpy as np

final_popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

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


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_inputs = request.form.get('user_input')
    index = np.where(pt.index == user_inputs)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        tempt_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(tempt_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(tempt_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(tempt_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)

# @app.route('/recommend', methods = ['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#     return str(user_input)

if __name__ == '__main__':
    app.run(debug=True)
