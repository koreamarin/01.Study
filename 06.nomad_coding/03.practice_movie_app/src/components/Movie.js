import PropTypes from "prop-types";
import { Link } from "react-router-dom";

function Movie({id, CoverImg, title, summary, genres}){
    return (<div>
    <img src={CoverImg} alt={title} />
    <h2>
      <Link to={`/movie/${id}`}>
        {title}
      </Link>
    </h2>
    <p>{summary}</p>
    <ul>
      {genres.map(g => (
        <li key={g}>{g}</li>
      ))}
    </ul>
    
  </div>);

}

//Movie함수를 다른곳에서 불러다 쓸 떄, Movie함수의 인자로 들어오는 값들의 타입을 지정해준다.
//isRequired는 필수값이라는 뜻이다.
Movie.propTypes = {
    id:PropTypes.number.isRequired,
    coverImg: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    summary: PropTypes.string.isRequired,                       // string으로 이루어진 변수가 들어가야함. 필수값.
    genres: PropTypes.arrayOf(PropTypes.string).isRequired,     // string으로 이루어진 배열이 들어가야함. 필수값.
}


export default Movie;