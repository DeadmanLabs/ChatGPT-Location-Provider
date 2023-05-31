import json, subprocess, time, quart, quart_cors, re
from geopy.geocoders import Nominatim
from quart import request
import requests
app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")
_globalVariable = {}

@app.get("/location")
async def getLocation():
    response = requests.get('http://ipinfo.io/json')
    if response.status_code == 200:
        data = response.json()
        result = {
            'Country': data['country'],
            'Region': data['region'],
            'City': data['city'],
            'Postal': data['postal'],
            'IP': data['ip'],
            'Hostname': data['hostname'],
            'Coordinates': list(map(lambda x: float(x), data['loc'].split(','))),
            'Organization': data['org'],
            'Timezone': data['timezone'],
        }
        return quart.Response(response=json.dumps(result), status=200)
    return quart.Response(response=json.dumps({ 'err': 'Failed to grab geolocation', 'response': {'status_code': response.status_code, 'body': response.content }}), status=403)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")
    
@app.get("/openapi.yaml")
async def openai_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")
    
def main():
    app.run(debug=True, host="0.0.0.0", port=3333)

if __name__ == "__main__":
    main()