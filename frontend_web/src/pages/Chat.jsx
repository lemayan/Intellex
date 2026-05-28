import { useState } from "react";
import { Send, Globe, FileText } from "lucide-react";
const API = "http://localhost:8000";
function Message({ role, content }) {
  const isUser = role === "user";
  return (
    <div style={{display:"flex",justifyContent: isUser ? "flex-end" : "flex-start",marginBottom:"1.5rem",animation:"fadeIn 0.3s ease"}}>
      <div style={{maxWidth:"72%",padding:"1rem 1.25rem",borderRadius: isUser ? "16px 16px 4px 16px" : "16px 16px 16px 4px",background: isUser ? "rgba(59,130,246,0.9)" : "rgba(30,30,30,0.8)",border: isUser ? "none" : "1px solid rgba(255,255,255,0.07)",backdropFilter:"blur(8px)",color:"#fff",lineHeight:1.65,fontSize:"0.95rem"}}>
        {content}
      </div>
    </div>
  );
}
export default function Chat() {
  const [messages, setMessages] = useState([{role:"assistant",content:"Welcome to DeepScholar. Ask me anything about your uploaded research documents, or enable web search for real-time information."}]);
  const [query, setQuery] = useState("");
  const [useDocs, setUseDocs] = useState(true);
  const [useWeb, setUseWeb] = useState(false);
  const [loading, setLoading] = useState(false);
  async function submit(e) {
    e.preventDefault();
    if (!query.trim() || loading) return;
    const q = query; setQuery(""); setLoading(true);
    setMessages(m => [...m, {role:"user",content:q}]);
    try {
      const res = await fetch(`${API}/api/chat`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query:q,use_documents:useDocs,use_web_search:useWeb})});
      const data = await res.json();
      setMessages(m => [...m, {role:"assistant",content:data.answer || "No response."}]);
    } catch {
      setMessages(m => [...m, {role:"assistant",content:"Could not reach the server. Ensure the FastAPI backend is running."}]);
    }
    setLoading(false);
  }
  return (
    <div style={{maxWidth:"820px",margin:"0 auto",display:"flex",flexDirection:"column",height:"calc(100vh - 6rem)"}}>
      <div style={{marginBottom:"2.5rem"}}>
        <div style={{fontSize:"0.75rem",letterSpacing:"0.12em",color:"#3b82f6",textTransform:"uppercase",marginBottom:"0.5rem"}}>AI Assistant</div>
        <h2 style={{fontSize:"2rem",fontWeight:300,letterSpacing:"-0.03em",color:"#fff"}}>Research Chat</h2>
      </div>
      <div style={{display:"flex",gap:"1.5rem",marginBottom:"1.5rem"}}>
        {[{label:"Document Search",val:useDocs,set:setUseDocs,icon:<FileText size={14}/>},{label:"Web Search",val:useWeb,set:setUseWeb,icon:<Globe size={14}/>}].map(({label,val,set,icon})=>(
          <button key={label} onClick={()=>set(v=>!v)} style={{display:"flex",alignItems:"center",gap:"0.5rem",padding:"0.5rem 1rem",borderRadius:"999px",border:`1px solid ${val?"rgba(59,130,246,0.5)":"rgba(255,255,255,0.1)"}`,background:val?"rgba(59,130,246,0.12)":"transparent",color:val?"#93c5fd":"#606060",fontSize:"0.82rem",fontWeight:500,cursor:"pointer",transition:"all 0.2s ease"}}>
            {icon}{label}
          </button>
        ))}
      </div>
      <div style={{flex:1,overflowY:"auto",padding:"1rem 0",marginBottom:"1.5rem"}}>
        {messages.map((m,i)=><Message key={i} {...m}/>)}
        {loading && <div style={{display:"flex",gap:"6px",padding:"1rem",justifyContent:"flex-start"}}>{[0,1,2].map(i=><div key={i} style={{width:"7px",height:"7px",borderRadius:"50%",background:"#3b82f6",animation:`pulse 1.2s ease ${i*0.2}s infinite`}}/>)}</div>}
      </div>
      <form onSubmit={submit} style={{display:"flex",gap:"0.75rem",alignItems:"flex-end",background:"rgba(20,20,20,0.6)",backdropFilter:"blur(12px)",border:"1px solid rgba(255,255,255,0.08)",borderRadius:"14px",padding:"0.75rem 0.75rem 0.75rem 1.25rem"}}>
        <textarea value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();submit(e)}}} placeholder="Ask a research question..." rows={1} style={{flex:1,resize:"none",background:"transparent",border:"none",outline:"none",color:"#fff",fontFamily:"inherit",fontSize:"0.95rem",lineHeight:1.5,padding:"0.3rem 0"}}/>
        <button type="submit" disabled={!query.trim()||loading} style={{padding:"0.65rem",borderRadius:"9px",background:"#3b82f6",border:"none",color:"#fff",cursor:"pointer",display:"flex",alignItems:"center",justifyContent:"center",transition:"all 0.2s ease",opacity:query.trim()&&!loading?1:0.4}}>
          <Send size={16}/>
        </button>
      </form>
      <style>{`@keyframes pulse{0%,100%{opacity:0.3;transform:scale(0.8)}50%{opacity:1;transform:scale(1.2}@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}`}</style>
    </div>
  );
}
