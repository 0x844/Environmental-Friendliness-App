import Message from './Message';


const pythonExec=()=>{
  const py_code = 'print("EW")';

  const pyodide = window.pyodide;
  pyodide.runPython(py_code);
}

function App(){
  return (
    <div className = "App">
      <header className = "App-Header">
        <h1>Run script</h1>
        <button onClick = {pythonExec}>CLICK TO START</button>
      </header>



    </div>
  
    

  );
}

export default App;