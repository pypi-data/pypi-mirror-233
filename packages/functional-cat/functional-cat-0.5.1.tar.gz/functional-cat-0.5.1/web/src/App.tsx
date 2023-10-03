import "./App.css";
import { BrowserRouter, Route, Routes, useLocation } from "react-router-dom";
import "@fontsource/roboto-mono";
import {
  ChakraProvider,
  extendTheme,
  type ThemeConfig,
} from "@chakra-ui/react";

import { FuncDetails } from "./func";
import AboutPage from "./AboutPage";
import HomePage from "./HomePage";
import FuncGrid from "./FuncGrid";
import Wrapper from "./Wrapper";
import TasksPage from "./TasksPage";
import TypesPage from "./TypesPage";
import { useEffect } from "react";

const config: ThemeConfig = {
  initialColorMode: "light",
  useSystemColorMode: true,
};

// 3. extend the theme
const theme = extendTheme({
  config,
  fonts: {
    heading: "Roboto Mono",
    body: "Roboto Mono",
  },
});

const ModelsPage = () => <Wrapper children={<FuncGrid />} />;

const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

const App = () => (
  <ChakraProvider theme={theme}>
    <BrowserRouter>
      <ScrollToTop /> {/* https://stackoverflow.com/a/70652876/398171 */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/types" element={<TypesPage />} />
        <Route path="/models" element={<ModelsPage />} />
        <Route
          path="/func/:name"
          element={<Wrapper children={<FuncDetails />} />}
        />
      </Routes>
    </BrowserRouter>
  </ChakraProvider>
);

export default App;
