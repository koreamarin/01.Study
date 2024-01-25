import { createBrowserRouter } from "react-router-dom";
import About from "./pages/About";
import Root from "./Root";
import NotFound from "./pages/NotFound";
import Home from "./pages/Home";
import ErrorComponents from "./component/ErrorComponents";
import User from "./pages/users/User";
import Followers from "./pages/users/Followers";

const router = createBrowserRouter([
  {
    path: "/", // 루트 경로
    element: <Root />, // 루트 컴포넌트
    children: [
      // 자식 라우터
      {
        path: "", // 자식 라우터의 경로
        element: <Home />, // 자식 라우터의 컴포넌트
        errorElement: <ErrorComponents />,
      },
      {
        // 자식 라우터의 경로, :userId(url prarmater) 는 User.tsx에서 useParams()를 통해 접근 가능하다.
        path: "users/:userId",
        element: <User />,
        children: [
          {
            path: "followers",
            element: <Followers />,
          },
        ],
      },
    ],
    errorElement: <NotFound />,
  },
]);

export default router;
