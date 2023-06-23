import React from 'react';                      // React는 컴포넌트를 만들기 위해 필요한 모델이다.
import ReactDOM from 'react-dom/client';        // ReactDOM은 React를 웹사이트에 출력(render)하는 것을 도와주는 모델이다.
import App from './App';                        // App.js에서 App함수를 불러다 쓴다.

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <App />
);