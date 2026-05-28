import { useState, useRef } from "react";
import { UploadCloud, FileText, CheckCircle } from "lucide-react";
const API = "http://localhost:8000";
export default function Documents() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [done, setDone] = useState([]);
  const [drag, setDrag] = useState(false);
  const ref = useRef();
  function onDrop(e) { e.preventDefault(); setDrag(false); setFiles([...e.dataTransfer.files]); }
  async function upload() {
    if (!files.length) return; setUploading(true);
    const fd = new FormData(); files.forEach(f=>fd.append("files",f));
    try {
      const res = await fetch(`${API}/api/documents`, {method:"POST",body:fd});
      const data = await res.json(); setDone(data.results || []); setFiles([]);
    } catch { setDone([{filename:"Error",status:"failed"}]); }
    setUploading(false);
  }
  return (
    <div style={{maxWidth:"720px",margin:"0 auto"}}>
      <div style={{marginBottom:"2.5rem"}}>
        <div style={{fontSize:"0.75rem",letterSpacing:"0.12em",color:"#3b82f6",textTransform:"uppercase",marginBottom:"0.5rem"}}>Knowledge Base</div>
        <h2 style={{fontSize:"2rem",fontWeight:300,letterSpacing:"-0.03em",color:"#fff"}}>Document Management</h2>
        <p style={{color:"#606060",marginTop:"0.5rem",fontSize:"0.9rem"}}>Upload PDF, DOCX, or TXT files to build your searchable knowledge base.</p>
      </div>
      <div onDragOver={e=>{e.preventDefault();setDrag(true)}} onDragLeave={()=>setDrag(false)} onDrop={onDrop} onClick={()=>ref.current.click()} style={{border:`2px dashed ${drag?"#3b82f6":"rgba(255,255,255,0.1)"}`,borderRadius:"16px",padding:"4rem 2rem",textAlign:"center",cursor:"pointer",background:drag?"rgba(59,130,246,0.06)":"rgba(20,20,20,0.4)",backdropFilter:"blur(8px)",transition:"all 0.2s ease",marginBottom:"1.5rem"}}>
        <input ref={ref} type="file" multiple accept=".pdf,.docx,.txt" style={{display:"none"}} onChange={e=>setFiles([...e.target.files])}/>
        <UploadCloud size={40} color={drag?"#3b82f6":"#404040"} style={{marginBottom:"1rem"}}/>
        <p style={{color:"#a0a0a0",fontSize:"0.95rem"}}>Drag and drop files here, or click to browse</p>
        <p style={{color:"#404040",fontSize:"0.8rem",marginTop:"0.4rem"}}>PDF, DOCX, TXT supported</p>
      </div>
      {files.length > 0 && (
        <div style={{marginBottom:"1.5rem",padding:"1.25rem",background:"rgba(20,20,20,0.6)",borderRadius:"10px",border:"1px solid rgba(255,255,255,0.07)"}}>
          {[...files].map((f,i)=>(
            <div key={i} style={{display:"flex",alignItems:"center",gap:"0.75rem",padding:"0.6rem 0",borderBottom:"1px solid rgba(255,255,255,0.05)"}}>
              <FileText size={15} color="#3b82f6"/>
              <span style={{color:"#e0e0e0",fontSize:"0.9rem"}}>{f.name}</span>
              <span style={{marginLeft:"auto",color:"#606060",fontSize:"0.8rem"}}>{(f.size/1024).toFixed(1)} KB</span>
            </div>
          ))}
          <button onClick={upload} disabled={uploading} style={{marginTop:"1rem",width:"100%",padding:"0.75rem",borderRadius:"8px",background:uploading?"#1d4ed8":"#3b82f6",border:"none",color:"#fff",fontWeight:500,fontSize:"0.9rem",cursor:"pointer",transition:"all 0.2s ease"}}>
            {uploading ? "Processing..." : `Upload ${files.length} file${files.length>1?"s":""}`}
          </button>
        </div>
      )}
      {done.length > 0 && (
        <div style={{padding:"1.25rem",background:"rgba(16,185,129,0.06)",border:"1px solid rgba(16,185,129,0.2)",borderRadius:"10px"}}>
          {done.map((d,i)=>(
            <div key={i} style={{display:"flex",alignItems:"center",gap:"0.75rem",padding:"0.5rem 0"}}>
              <CheckCircle size={15} color="#10b981"/>
              <span style={{color:"#a0a0a0",fontSize:"0.9rem"}}>{d.filename}</span>
              <span style={{marginLeft:"auto",color:"#10b981",fontSize:"0.8rem",textTransform:"capitalize"}}>{d.status}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
