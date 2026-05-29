import React, { useState } from 'react'
import "./Home.css";
import { FiUpload } from "react-icons/fi";
import { useNavigate } from 'react-router-dom'

export default function Home() {

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [image, setImage] = useState(null);

  const handleFileChange = async (event) => {

    const file = event.target.files[0];

    if (file) {

      setLoading(true);

      setImage(URL.createObjectURL(file));

      const formData = new FormData();

      formData.append("image", file);

      try {

        const response = await fetch(
          "https://face2fameai.onrender.com/upload",
          {
            method: "POST",
            body: formData
          }
        );

        const data = await response.json();

        console.log(data);

        console.log("NAVIGATING", data);

        navigate("/result", {
          state: {
            match: data.match,
            distance: data.distance,
            image: data.celebrity_image,
            movies: data.movies
          }
        });

      }

      catch (error) {

        console.log(error);

      }

      finally {

        setLoading(false);

      }

    }
  };

  return (

    <div className="div1">

      <h1 className="heading1">
        Face2FameAI
      </h1>

      <p className="heading2">
        Discover movies based on your celebrity lookalike
      </p>

      <label className="uploadBox">

        <input
          type="file"
          hidden
          onChange={handleFileChange}
        />

        {
          loading ? (

            <div className="loader"></div>

          ) : image ? (

            <img
              src={image}
              alt="preview"
              className="previewImage"
            />

          ) : (

            <>
              <div className="iconCircle">
                <FiUpload className="uploadIcon" />
              </div>

              <h2 className="uploadHeading">
                Upload Your Photo
              </h2>

              <p className="uploadText">
                Click to browse or drag and drop
              </p>
            </>
          )
        }

      </label>

      <footer className="footer">
        Built by Aafia © 2026
      </footer>

    </div>
  )
}