import './App.css';
import Search from "./components/Search";
import Navigation from "./components/Navigation";
import Result from "./components/Result";
import CodeViewer from "./components/CodeViewer"
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";


function App() {
      return (
          <div className="App">
        <Router>
            <Routes>
                <Route path="/" element={<Search />} />
                <Route path="/results" element={<Result />} />
                <Route path="/code_viewer" element={<CodeViewer />} />
            </Routes>
        </Router>
              </div>
    );
    // return (
    //     <div className="App">
    //         <Navigation/>
    //         {/*<div>*/}
    //             <Search/>
    //         {/*</div>*/}
    //         {/*<Result/>*/}
    //         {/*<CodeViewer />*/}
    //     </div>
    // );
}

export default App;
