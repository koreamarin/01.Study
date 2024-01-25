import React from "react";
import ReactDOM from "react-dom/client";
import router from "./Router";
import { RouterProvider } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
    {/* RouterProvider를 통해 라우터를 제공합니다. router는 src/Router.tsx에서 만든 라우터입니다. */}
  </React.StrictMode>
);
