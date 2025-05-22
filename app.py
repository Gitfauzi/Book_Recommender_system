from flask import Flask, render_template, request
import pickle
import numpy as np

popularity_df = pickle.load(open('popularity.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books= pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popularity_df['Book-Title'].values),
                           author=list(popularity_df['Book-Author'].values),
    image= list(popularity_df['Image-URL-M'].values),
    votes= list(popularity_df['Number_of_rating'].values),
    ratings= list(popularity_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books',methods = ['post']) # because we are asking data from form
def recommend():
    user_input = request.form.get('user_input')
    if user_input not in pt.index:
        return render_template('recommend.html', data=[])

    index = np.where(pt.index == user_input)[0][0]

    # distances = similarity_score[index]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[
                    1:6]  # 1984 ka 1984 ke saath similarity, similarly with all books

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[
            i[0]]]  # this will give the indexes of most similar 5 items, its like pt.index[46]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    return render_template('recommend.html', data = data)

if __name__=='__main__':
    app.run(debug = True)