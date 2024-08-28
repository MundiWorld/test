import os
from waitress import serve
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask("MundiWorld_Schoolpage")

# API Key de SerpAPI
SERPAPI_KEY = os.environ.get('c6b302e6d546f1e7592d93d1617c4feb170b5f615d5291d75bcd6f0a968b8098')

def get_papers(query, num_results=5):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_scholar",
        "q": query,
        "num": num_results,
        "api_key": "c6b302e6d546f1e7592d93d1617c4feb170b5f615d5291d75bcd6f0a968b8098"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()["organic_results"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

@app.route('/search_papers', methods=['GET'])
def search_papers():
    query = request.args.get('query')
    num_results = request.args.get('num_results', 5)
    
    try:
        papers = get_papers(query, num_results)
        informal_response = "¡Aquí tienes algunos papers interesantes!\n\n"
        
        for i, paper in enumerate(papers[:num_results], start=1):
            title = paper.get("title")
            link = paper.get("link")
            snippet = paper.get("snippet")
            
            informal_response += f"{i}. {title}\n"
            informal_response += f"Resumen: {snippet}\n"
            informal_response += f"Enlace: {link}\n\n"
        
        return jsonify({"response": informal_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

if __name__ == '__main__':
  serve(app, host="0.0.0.0", port=8080)
