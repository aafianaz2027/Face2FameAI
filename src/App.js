import React from 'react'

import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./Home";
import Result from "./Result";

export default function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/result"
          element={<Result />}
        />

      </Routes>

    </BrowserRouter>

  )
}