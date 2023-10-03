import React from "react";
import { Stack } from "@chakra-ui/react";
import Header from "./Header";

const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <>
    <Stack spacing={8} mt={50} mr={50} mb={50} ml={50}>
      <Header />
      {children}
    </Stack>
  </>
);

export default Wrapper;
