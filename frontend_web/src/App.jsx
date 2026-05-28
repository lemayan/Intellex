import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { MessageSquare, FolderSearch } from "lucide-react";
import Chat from "./pages/Chat";
import Documents from "./pages/Documents";
const navStyle = (isActive) => ({
  display:"flex",alignItems:"center",gap:"0.8rem",padding:"0.75rem 1rem",
  borderRadius:"6px",textDecoration:"none",fontSize:"0.9rem",fontWeight:500,
  color: isActive ? "#ffffff" : "#a0a0a0",
  background: isActive ? "rgba(59,130,246,0.15)" : "transparent",
  border: isActive ? "1px solid rgba(59,130,246,0.3)" : "1px solid transparent",
  transition:"all 0.2s ease"
});
export default function App() {
  return (
    <Router>
      <div style={{display:"flex",height:"100vh",width:"100vw",overflow:"hidden"}}>
        <aside style={{width:"240px",flexShrink:0,padding:"2rem 1.25rem",display:"flex",flexDirection:"column",gap:"2rem",background:"rgba(10,10,10,0.8)",backdropFilter:"blur(12px)",borderRight:"1px solid rgba(255,255,255,0.07)"}}>
          <div>
            <div style={{fontSize:"0.7rem",letterSpacing:"0.15em",color:"#606060",textTransform:"uppercase",marginBottom:"0.4rem"}}>Research Platform</div>
            <h1 style={{fontSize:"1.3rem",fontWeight:600,letterSpacing:"-0.02em",color:"#fff"}}>DeepScholar</h1>
          </div>
          <nav style={{display:"flex",flexDirection:"column",gap:"0.3rem"}}>
            <NavLink to="/" end style={({isActive})=>navStyle(isActive)}><MessageSquare size={16}/>Research Chat</NavLink>
            <NavLink to="/documents" style={({isActive})=>navStyle(isActive)}><FolderSearch size={16}/>Documents</NavLink>
          </nav>
          <div style={{marginTop:"auto",padding:"1rem",background:"rgba(59,130,246,0.06)",borderRadius:"8px",border:"1px solid rgba(59,130,246,0.12)"}}>
            <div style={{fontSize:"0.75rem",color:"#606060",marginBottom:"0.25rem"}}>Status</div>
            <div style={{fontSize:"0.85rem",color:"#a0a0a0"}}>System ready</div>
          </div>
          <div style={{paddingTop:"1rem",borderTop:"1px solid rgba(59,130,246,0.2)",textAlign:"center"}}>
            <div style={{fontSize:"0.7rem",color:"#606060",letterSpacing:"0.08em",textTransform:"uppercase",marginBottom:"0.3rem"}}>Created by</div>
            <div style={{
              fontSize:"0.9rem",
              fontWeight:600,
              color:"#93c5fd",
              letterSpacing:"0.04em",
              textShadow:"0 0 12px rgba(59,130,246,0.8), 0 0 24px rgba(59,130,246,0.4)"
            }}>Nikita Simiyu</div>
          </div>
        </aside>
        <main style={{flex:1,overflowY:"auto",padding:"3rem 4rem"}}>
          <Routes>
            <Route path="/" element={<Chat />} />
            <Route path="/documents" element={<Documents />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
