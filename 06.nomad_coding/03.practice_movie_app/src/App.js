import {
  BrowserRouter as Router,                    // BrowserRouter는 Router의 한 종류이다.
  Switch,                                     // Switch는 Router안에 들어가는 컴포넌트들을 관리해준다.
  Route,                                      // Route는 path에 따라 다른 컴포넌트를 보여준다.
} from "react-router-dom";
import Home from "./routes/Home";             // Home.js에서 Home함수를 불러다 쓴다.
import Detail from "./routes/Detail";         // Detail.js에서 Detail함수를 불러다 쓴다.


function App() {
  return (
    <Router>
      <Switch>
        <Route path="/hello">
          <h1>Hello</h1>
        </Route>
        <Route path="/movie/:id">
          <Detail />
        </Route>
        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;   // 다른곳에서 App함수를 불러다 쓸 수 있게 해준다.
