#------------------------------------------------------------------#
# SPG9000_EXPORTER_HTTP.py                                         #
#                                                                  #
# Author:        Mike Kurras                                       #
# Date:          2/27/2025                                         #
# Description:   OpenMetrics exporter for Telestream SPG9000 Sync  #
#                Pulse Generator.                                  #
#                Designed for use with Prometheus                  #
#------------------------------------------------------------------#

from flask import Flask, request
import SPG9000_Exporter

script_name = "SPG9000_Exporter.py"

app = Flask(__name__)

@app.route('/metrics')
def get_data():
    target_ip = request.args.get('target')
    api_key = request.args.get('api_key')
    data = SPG9000_Exporter.polldata(target_ip, api_key)
    #return f"<html><head><meta name=\"color-scheme\" content=\"light dark\"></head><body><pre style=\"word-wrap: break-word; white-space: pre-wrap;\">{data}</pre></body></html>"
    return data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')