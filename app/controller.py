from flask import Flask, jsonify, request, render_template
from data_handler import execute_query

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_query', methods=['GET'])
def start_query():
    query = request.args.get('query')
    result, query_time = execute_query(query)
    response_data = {
        'query_time': query_time,  # Add the query time to the response data
        'result': result
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
