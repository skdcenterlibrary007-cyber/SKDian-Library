
import React, {useState,useEffect} from 'react';
import {createRoot} from 'react-dom/client';

function App(){
  const [token,setToken]=useState(localStorage.getItem('lib_token')||'');
  const [students,setStudents]=useState([]);
  const login=async()=>{
    const username=prompt('Username');
    const password=prompt('Password');
    const res=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});
    if(res.ok){let j=await res.json(); localStorage.setItem('lib_token',j.token); setToken(j.token);}
  };
  const load=async()=>{
    const res=await fetch('/api/students',{headers:{Authorization:'Bearer '+token}});
    if(res.ok){setStudents(await res.json());}
  };
  return <div>
    <h1>लाइब्रेरी ऐप</h1>
    {token?<button onClick={load}>Load Students</button>:<button onClick={login}>Login</button>}
    <ul>{students.map(s=><li key={s.id}>{s.name} ({s.roll_no})</li>)}</ul>
  </div>;
}

const root=createRoot(document.getElementById('root'));
root.render(<App/>);
