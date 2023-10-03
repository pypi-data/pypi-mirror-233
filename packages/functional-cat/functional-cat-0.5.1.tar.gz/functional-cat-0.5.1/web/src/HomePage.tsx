import Wrapper from "./Wrapper";
import { Link } from "react-router-dom";
import {
  Button,
  Container,
  Center,
  Text,
  Heading,
  VStack,
  HStack,
} from "@chakra-ui/react";

const Main = () => {
  return (
    <>
      <br />
      <br />
      <br />
      <Center>
        <VStack spacing={50}>
          <Heading size="2xl">functional cat</Heading>
          <Container>
            <Text align="center">
              a catalog and Python library of easy-to-use computer vision
              models.
            </Text>
          </Container>
          <HStack>
            <Button as={Link} to="/models" style={{ textDecoration: "none" }}>
              Browse the models
            </Button>
            <Button as={Link} to="/about" style={{ textDecoration: "none" }}>
              About
            </Button>
          </HStack>
        </VStack>
      </Center>
    </>
  );
};

const HomePage = () => <Wrapper children={<Main />} />;

export default HomePage;
