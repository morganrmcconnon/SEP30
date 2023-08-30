import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import Search from "./pages/Search.jsx";
import { keywordAction } from "./components/KeywordSearch.jsx";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/search",
    element: <Search />,
    async action({ params, request }) {
      const formData = await request.formData();
      return Object.fromEntries(formData).keyword;
    },
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);
