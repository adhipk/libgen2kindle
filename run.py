from flask import Flask, request, jsonify, render_template
from helper import searchTitle,send2kindle
app = Flask(__name__)

@app.route('/')
def index():
    # Render the index.html template on accessing the root endpoint
    return render_template('index.html')

@app.route('/getBooks', methods=['GET'])
def get_books():
    title = request.args.get('title', '',type=str)
    if not title:
        return jsonify({'error': 'Missing book title'}), 400

    search_results = searchTitle(title)
    return render_template("booklist.html", books=search_results)
@app.route('/send2kindle', methods=['POST'])
def sendBooktoKindle():
	mirror = request.form.get("mirror",'',type=str)
	title = request.form.get("title",'',type=str)
	app.logger.info(f"{mirror},{title}")
	if not mirror:
		return jsonify({"error":"Missing mirror Link"}),400
	result = send2kindle(mirror,title)
	if result is False:
		return jsonify({"error":"Error sending title to kindle"}),400
	return jsonify({'status': 'success', 'message': f'Book "{title}" sent to Kindle'})
if __name__ == '__main__':
    app.run(debug=True)
