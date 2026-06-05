import React, { useState } from 'react'
import "./Home.css";
import { FiUpload } from "react-icons/fi";
import { useNavigate } from 'react-router-dom'

export default function Home() {

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [image, setImage] = useState(null);

  const compressImage = (file, maxSize = 1024, quality = 0.75) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = () => {
        const img = new Image();

        img.onload = () => {
          const scale = Math.min(
            1,
            maxSize / Math.max(img.width, img.height)
          );

          const canvas = document.createElement("canvas");
          canvas.width = Math.round(img.width * scale);
          canvas.height = Math.round(img.height * scale);

          const ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

          canvas.toBlob(
            (blob) => {
              if (!blob) {
                reject(new Error("Could not compress image"));
                return;
              }

              resolve(
                new File(
                  [blob],
                  file.name.replace(/\.[^.]+$/, ".jpg"),
                  { type: "image/jpeg" }
                )
              );
            },
            "image/jpeg",
            quality
          );
        };

        img.onerror = reject;
        img.src = reader.result;
      };

      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const handleFileChange = async (event) => {

    const file = event.target.files[0];

    if (file) {

      setLoading(true);

      try {

        const compressedFile = await compressImage(file);

        setImage(URL.createObjectURL(compressedFile));

        const formData = new FormData();

        formData.append("image", compressedFile);

        const response = await fetch(
          "/api/upload",
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
          accept="image/*"
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
