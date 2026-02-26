import { createHashRouter } from "react-router-dom";
import { Root } from "./components/Root";
import { Home } from "./components/pages/Home";
import { Experience } from "./components/pages/Experience";
import { Projects } from "./components/pages/Projects";
import { Skills } from "./components/pages/Skills";
import { Contact } from "./components/pages/Contact";
import { SecureVigilProject } from "./components/pages/SecureVigilProject";

export const router = createHashRouter([
  {
    path: "/",
    Component: Root,
    children: [
      { index: true, Component: Home },
      { path: "experience", Component: Experience },
      { path: "projects", Component: Projects },
      { path: "projects/securevigil", Component: SecureVigilProject },
      { path: "skills", Component: Skills },
      { path: "contact", Component: Contact },
    ],
  },
]);