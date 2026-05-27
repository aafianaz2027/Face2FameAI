import React from 'react';
import { useLocation } from 'react-router-dom';
import "./Result.css";

export default function Result() {

  const location = useLocation();

  const data = location.state;

  if (!data) {
    return <h1>No Result Found</h1>;
  }

  const movies = data.movies || [];


  return (

    <div className="diva1">

      <h1 className="head1">
        Celebrity Match
      </h1>

      <div className="resultCard">

        <img
          src={data.image}
          alt="celebrity"
          className="resultImage"
        />

        <p className="matchText">
          You look like
        </p>

        <h2 className="celebName">
          {data.match}
        </h2>

        <div className="moviesBox">

          <h3 className="movieHeading">
            Recommended Movies
          </h3>

          {
            movies.map((movie, index) => (

              <div
                key={index}
                className="movieCard"
              >
                {movie}
              </div>

            ))
          }

        </div>

      </div>
      <footer className="footer">
        Built by Aafia © 2026
      </footer>

    </div>

  )
}