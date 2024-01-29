import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './routes/Home';
import Detail from './routes/Detail';


function Router() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/detail" element={<Detail />} />
            </Routes>
        </BrowserRouter>
    )
}

export default Router;