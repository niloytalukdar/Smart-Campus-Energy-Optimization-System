import json
import urllib.request


def main():
    payload = {
        'scenario_id': 'TEST-RAW',
        'operator_notes': ['Solar output will drop to 20% from 13 to 15', 'Do not charge battery between 17 and 20'],
        'battery': {
            'capacity_kwh': 100,
            'initial_energy_kwh': 50,
            'max_charge_rate_kwh': 25,
            'max_discharge_rate_kwh': 25,
            'charge_efficiency': 0.95,
            'discharge_efficiency': 0.95
        },
        'hours': [
            {'hour': i, 'demand_kwh': 20.0, 'solar_kwh': 10.0 if 8 <= i <= 17 else 0.0, 'price': 0.1 if i < 12 else 0.5}
            for i in range(24)
        ]
    }
    url = 'http://127.0.0.1:8000/optimize-energy'
    print('Posting to', url)
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8')
            print('Status:', resp.status)
            try:
                obj = json.loads(body)
                print(json.dumps(obj, indent=2))
            except Exception as e:
                print('Failed to parse JSON:', e)
                print(body)
    except Exception as e:
        print('Request failed:', e)

if __name__ == '__main__':
    main()
