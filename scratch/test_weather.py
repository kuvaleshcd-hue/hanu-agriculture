import urllib.request
import json
import urllib.parse

def test_wttr(city):
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            current = data['current_condition'][0]
            area = data['nearest_area'][0]
            print(f"City: {city}")
            print(f"Location: {area['areaName'][0]['value']}, {area['region'][0]['value']}")
            print(f"Temp: {current['temp_C']}°C")
            print(f"Humidity: {current['humidity']}%")
            print(f"Desc: {current['weatherDesc'][0]['value']}")
    except Exception as e:
        print(f"Error for {city}: {e}")

if __name__ == '__main__':
    test_wttr("Pandavapura")
    test_wttr("Mandya")
