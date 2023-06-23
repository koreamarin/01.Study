import { useEffect, useState } from "react";      // useEffect는 컴포넌트가 마운트 됐을 때, 어떤 일을 수행하도록 해준다.
                                                  // useState는 컴포넌트에서 동적인 데이터를 다룰 때 사용한다.
import Movie from "../components/Movie";          // Movie.js에서 Movie함수를 불러다 쓴다.

function Home () {
  const [loading, setLoading] = useState(true);
  const [movies, setMovies] = useState([]);
  const getMovies = async () => {
    // const response = await fetch("https://yts.mx/api/v2/list_movies.json?minimum_rating=8.5&sort_by=year");
    // const json = await response.json();
    const json = await (await fetch("https://yts.mx/api/v2/list_movies.json?minimum_rating=9.5&sort_by=year")).json();
    setMovies(json.data.movies);
    setLoading(false);
  }

  useEffect(() => {
    getMovies();
  }, []);
  

  console.log(movies);

  return (
    <div>
      {loading ? (
        <h1>Loading...</h1>
          ) : (
            <div>
              {movies.map(movie => (
                <Movie
                  id={movie.id}
                  CoverImg={movie.medium_cover_image}
                  title={movie.title}
                  summary={movie.summary}
                  genres={movie.genres}
                />
              ))}
            </div>
          )
      }
    </div>
  ) 
}

export default Home;