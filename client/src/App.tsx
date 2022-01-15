import { Routes, Route } from "react-router-dom";
import Scholarships from "./components/Scholarships";
import Marketplace from "./components/Marketplace";
import Home from "./components/Home";
import Nav from "./components/Nav";
import "./App.css";

function App() {
  return (
    <div className="App font-inter text-base text-black bg-white antialiased font-feature-default">
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/scholarships" element={<Scholarships />} />
        <Route path="/marketplace" element={<Marketplace />} />
      </Routes>
    </div>
  );
}

export default App;
