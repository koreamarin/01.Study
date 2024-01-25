import { Link, useSearchParams } from "react-router-dom";
import { users } from "../db";

function Home() {
  // readSearchParams는 url query parameter를 가져오는 역할이고, setReadSearchParams는 url query parameter를 수정하는 역할을 한다. useState와 매우 유사하다.
  const [readSearchParams, setReadSearchParams] = useSearchParams();
  console.log(readSearchParams.get("asd")); // url query parameter에 있는 asd의 value를 가져온다.
  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <Link to={`/users/${user.id}`}>{user.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
export default Home;
