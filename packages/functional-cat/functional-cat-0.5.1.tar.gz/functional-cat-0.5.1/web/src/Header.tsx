import { Link as ReactLink } from "react-router-dom";
import {
  Heading,
  Link,
  HStack,
  IconButton,
  Text,
  useColorMode,
  useColorModeValue,
} from "@chakra-ui/react";
import { FaGithub, FaMoon, FaSun } from "react-icons/fa";

export const logoText = "f(🐱)";

const Logo = () => (
  <Link as={ReactLink} style={{ textDecoration: "none" }} to="/">
    <Heading size="lg">{logoText}</Heading>
  </Link>
);

const Nav = () => (
  <HStack>
    <Link as={ReactLink} to="/models">
      models
    </Link>
    <Text opacity="50%">|</Text>
    <Link as={ReactLink} to="/tasks">
      tasks
    </Link>
    <Text opacity="50%">|</Text>
    <Link as={ReactLink} to="/types">
      types
    </Link>
    <Text opacity="50%">|</Text>
    <Link as={ReactLink} to="/about">
      about
    </Link>
  </HStack>
);

const ColorModeToggle = () => {
  const { toggleColorMode } = useColorMode();
  const Icon = useColorModeValue(FaMoon, FaSun);
  const text = useColorModeValue("dark", "light");
  return (
    <IconButton
      icon={<Icon />}
      onClick={toggleColorMode}
      aria-label={`switch to ${text} mode.`}
    />
  );
};

const RightButtons = () => (
  <HStack align="right">
    <IconButton
      as={Link}
      href={process.env.REACT_APP_GITHUB_URL}
      isExternal
      icon={<FaGithub />}
      aria-label="go to GitHub page"
    />
    <ColorModeToggle />
  </HStack>
);

const Header = () => (
  <HStack spacing={50}>
    <Logo />
    <Nav />
    <RightButtons />
  </HStack>
);

export default Header;
