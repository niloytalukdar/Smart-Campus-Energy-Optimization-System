import urllib.request, json, sys

def main():
    payload={'scenario_id':'TEST-REALTIME','operator_notes':['Solar output will drop to 20% from 13 to 15','Do not charge battery between 17 and 20'],'battery':{'capacity_kwh':2400,'initial_energy_kwh':1200,'max_charge_rate_kwh':500,'max_discharge_rate_kwh':500,'charge_efficiency':0.95,'discharge_efficiency':0.95},'hours':[{'hour':i,'demand_kwh':200,'solar_kwh':100 if 8<=i<=17 else 0,'price':7 if i<12 else 12} for i in range(24)]}
    url='http://127.0.0.1:8000/optimize-energy'
    req=urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            obj=json.load(resp)
    except Exception as e:
        print('ERROR', e)
        sys.exit(1)
    out={
        'total_cost': obj.get('total_cost'),
        'directive_interpretation': obj.get('directive_interpretation'),
        'hourly_plan_sample': obj.get('hourly_plan',[])[:3],
        'solar_curtailment': next((d.get('factor') for d in obj.get('directive_interpretation',[]) if d.get('directive_type')=='solar_reduction'), None),
        'peak_cost_delta': obj.get('peak_cost_delta') if 'peak_cost_delta' in obj else None,
    }
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
