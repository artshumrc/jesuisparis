
from flask import Flask, render_template
from flask import request, jsonify
from py2neo import Graph, cypher
import json

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data")

@app.route('/')
def jesuisparis():
	return render_template('jesuisparis.html')

@app.route('/hashtag', methods=['POST'])
def hashtagSearch():
	parsed = []
	if request.method == 'POST':
		hashtag = request.json
		results = graph.cypher.execute("MATCH (n:Hashtag)-[r:TAGGED]-(q:Tweet) WHERE lower(n.text) ='"+hashtag+"' RETURN collect(q.webid) as webid")[0][0]
		return json.dumps(results)

@app.route('/text', methods=['POST'])
def clickedSearch():
	if request.method == 'POST':
		clicked = request.json
		results = graph.cypher.execute("MATCH (n:Tweet {webid:"+clicked+"}) RETURN n.text as text")[0][0]
		return json.dumps(results)

@app.route('/search', methods=['POST'])
def searchTweets():
	if request.method == 'POST':
		searched = request.json
		results = graph.cypher.execute("MATCH (n:Tweet) WHERE toLower(n.text) CONTAINS toLower('"+searched+"') RETURN collect(n.webid) as webid")[0][0]
		return json.dumps(results)
		
if __name__ == '__main__':
	app.debug = True
	app.run()
