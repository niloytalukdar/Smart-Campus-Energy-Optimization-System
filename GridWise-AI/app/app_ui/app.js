async function postOptimize(payload){
  const res = await fetch('/optimize-energy',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  return res.json();
}

function buildDefaultHours(){
  const hours = [];
  for(let i=0;i<24;i++){
    hours.push({hour:i,demand_kwh:20.0,solar_kwh:(i>=8&&i<=17)?10.0:0.0,price:(i<12)?0.1:0.5});
  }
  return hours;
}

document.getElementById('sampleBtn').addEventListener('click',()=>{
  const sample = `Solar output will drop to 20% from 13:00 to 15:00\nDo not charge battery between 17 and 20`;
  document.getElementById('notes').value = sample;
});

document.getElementById('runBtn').addEventListener('click',async ()=>{
  const notes = document.getElementById('notes').value.split('\n').map(s=>s.trim()).filter(Boolean);
  const payload = {scenario_id:'UI-1',operator_notes:notes,battery:{capacity_kwh:100,initial_energy_kwh:50,max_charge_rate_kwh:25,max_discharge_rate_kwh:25,charge_efficiency:0.95,discharge_efficiency:0.95},hours:buildDefaultHours()};
  const out = document.getElementById('output');
  out.textContent = 'Loading...';
  try{
    const data = await postOptimize(payload);
    out.textContent = JSON.stringify(data,null,2);
  }catch(e){
    out.textContent = String(e);
  }
});

document.getElementById('runRawBtn').addEventListener('click', async ()=>{
  const raw = document.getElementById('rawInput').value.trim();
  const out = document.getElementById('output');
  if(!raw){ out.textContent = 'Please paste a valid OptimizeRequest JSON.'; return; }
  let payload;
  try{
    payload = JSON.parse(raw);
  }catch(e){ out.textContent = 'Invalid JSON: ' + e.message; return; }
  out.textContent = 'Loading...';
  try{
    const data = await postOptimize(payload);
    out.textContent = JSON.stringify(data,null,2);
  }catch(e){ out.textContent = String(e); }
});
