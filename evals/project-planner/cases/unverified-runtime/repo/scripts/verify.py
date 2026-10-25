import os
import urllib.request

url = os.environ["DASHBOARD_URL"]
with urllib.request.urlopen(url, timeout=10) as response:
    assert response.status == 200
