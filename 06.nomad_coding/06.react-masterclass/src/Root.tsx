import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./component/Header";

function Root() {
  return (
    <div>
      <Header />
      <Outlet /> {/* 자식 라우터를 렌더링하는 역할을 합니다 */}
    </div>
  );
}

export default Root;
