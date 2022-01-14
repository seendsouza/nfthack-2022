import { Routes, Route} from "react-router-dom";
import LenderDashboard from "./components/LenderDashboard";
import Marketplace from "./components/Marketplace";
import Home from "./components/Home";
import Nav from "./components/Nav";
import './App.css'

function App() {

  return (
    <div className="App">
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/lender-dashboard" element={<LenderDashboard />} />
        <Route path="/marketplace" element={<Marketplace/>} />
      </Routes>
    </div>
  )
}

export default App
