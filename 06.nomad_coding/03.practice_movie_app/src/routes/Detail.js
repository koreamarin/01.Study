import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Detail() {
    const id = useParams().id
    const [movie, setMovie] = useState(); // useState는 컴포넌트에서 동적인 데이터를 다룰 때 사용한다.
    const getMovie = async () => {
        const json = await (await fetch(`https://yts.mx/api/v2/movie_details.json?movie_id=${id}`)).json();
        console.log(json);
        console.log(json.data.movie);
        setMovie(json.data.movie);
    }
    useEffect(() => {
        getMovie();
    }, []);
    return (
        <div>
            <h1>Detail</h1>
            <div>
                {movie && (
                    <div>
                        <h1>{movie.title}</h1>
                        <img src={movie.medium_cover_image}></img>
                    </div>
                )}
            </div>
        </div>
    );
}


export default Detail;