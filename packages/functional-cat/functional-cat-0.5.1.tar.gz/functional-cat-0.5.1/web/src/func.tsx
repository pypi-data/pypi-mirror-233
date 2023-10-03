import {
  Badge,
  Box,
  Image,
  Link,
  Text,
  Heading,
  useColorModeValue,
  HStack,
  VStack,
  Stack,
  SimpleGrid,
  Table,
  Thead,
  Th,
  Tr,
  Td,
} from "@chakra-ui/react";
import React from "react";
import { Link as ReactLink, useParams } from "react-router-dom";
import SyntaxHighlighter from "react-syntax-highlighter";
import {
  atomOneDark,
  atomOneLight,
} from "react-syntax-highlighter/dist/esm/styles/hljs";
import _funcs from "./funcs.json";

export interface Example {
  outputImage: string; // base64-encoded string for output image
  output: string; // string representation of output
}

export interface Func {
  class: string;
  constructorArgs: Object;
  description: string;
  example: Example;
  task: string;
  framework: string;
  installSnippet: string;
  devices: { cpu: boolean; gpu: boolean };
  colabLink?: string | null;
  classLabels?: string[] | null;
  keyPointLabels?: string[] | null;
}

export interface FuncCatalog {
  string: Func;
}

export const funcs = _funcs as { [key: string]: Func };

export interface FuncProps {
  name: string;
  func: Func;
}

const smallDescription = (description: string) => {
  const length = 75;
  if (description.length <= length) {
    return description;
  }
  return description.slice(0, length) + "...";
};

const FuncTitle: React.FC<{ name: string; size: string }> = ({
  name,
  size,
}) => (
  <Heading
    textTransform="uppercase"
    size={size}
    fontWeight="bold"
    color="#ED6A5A"
  >
    {name}
  </Heading>
);

export const FuncCard: React.FC<FuncProps> = ({ name, func }) => (
  <ReactLink to={`/func/${name}`} style={{ textDecoration: "none" }}>
    <Box
      p="5"
      maxW="320px"
      height="250px"
      borderWidth="1px"
      opacity="80%"
      borderRadius="lg"
      boxShadow="dark-lg"
      overflow="hidden"
    >
      <FuncTitle name={name} size="md" />
      <VStack align="stretch" spacing="10px">
        <Text mt={2} fontSize="medium" lineHeight="short">
          {smallDescription(func.description)}
        </Text>
        <Stack direction="row">
          <Badge colorScheme="pink">{func.task}</Badge>
          <Badge colorScheme="purple">{func.framework}</Badge>
        </Stack>
      </VStack>
    </Box>
  </ReactLink>
);

const funcToSnippet = (func: Func) => {
  const name = func.class.split(".");
  const package_name = name.slice(0, name.length - 1).join(".");
  const class_name = name[name.length - 1];

  let constructor_args = "";
  for (const [key, value] of Object.entries(func.constructorArgs)) {
    constructor_args += `${key}=${JSON.stringify(value)}`;
    constructor_args += ", ";
  }
  constructor_args = constructor_args.slice(0, -2);

  const ret = `from ${package_name} import ${class_name}\nfrom PIL import Image\n\nmodel = ${class_name}(${constructor_args})\nimg = Image.open("/path/to/image")\nmodel([img], score_thres=0.5)`;
  return ret;
};

// makes links out of any urls in text, from https://stackoverflow.com/a/61157860/398171
const URL_REGEX =
  /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)/;
const renderText = (txt: string) =>
  txt
    .split(" ")
    .map((part) =>
      URL_REGEX.test(part) ? <a href={part}>{part} </a> : part + " "
    );

const InstallSection: React.FC<{ func: Func }> = ({ func }) => {
  const syntaxStyle = useColorModeValue(atomOneLight, atomOneDark);

  return (
    <>
      <Heading size="md">Install</Heading>
      <SyntaxHighlighter language="bash" style={syntaxStyle}>
        {func.installSnippet}
      </SyntaxHighlighter>
    </>
  );
};

const ExampleSection: React.FC<{ func: Func }> = ({ func }) => {
  const syntaxStyle = useColorModeValue(atomOneLight, atomOneDark);
  const snippet = funcToSnippet(func);

  return (
    <>
      <Heading size="md">Example</Heading>
      <Heading size="sm">Code snippet</Heading>
      <SyntaxHighlighter language="python" style={syntaxStyle}>
        {snippet}
      </SyntaxHighlighter>
      <Heading size="sm">Output</Heading>
      <SyntaxHighlighter language="python" style={syntaxStyle}>
        {func.example.output}
      </SyntaxHighlighter>
      <Box>
        <Image src={func.example.outputImage} />
      </Box>
    </>
  );
};

const DeviceSection: React.FC<{ func: Func }> = ({ func }) => (
  <>
    <Heading size="md">Device support</Heading>
    <Table>
      <Thead>
        <Tr>
          <Th>cpu</Th>
          <Th>gpu</Th>
        </Tr>
      </Thead>
      <Tr>
        <Td>{func.devices.cpu ? "✅ " : "❌"}</Td>
        <Td>{func.devices.gpu ? "✅ " : "❌"}</Td>
      </Tr>
    </Table>
  </>
);

const ColabLink: React.FC<{ func: Func }> = ({ func }) =>
  func.colabLink ? (
    <>
      <Link href={func.colabLink} isExternal>
        <Image
          src="https://colab.research.google.com/assets/colab-badge.svg"
          width="10%"
          height="10%"
        />
      </Link>
    </>
  ) : (
    <></>
  );

const LabelsSection: React.FC<{ labels: string[]; title: string }> = ({
  labels,
  title,
}) => (
  <>
    <Heading size="md">{title}</Heading>
    <SimpleGrid minChildWidth="100px" spacing={2}>
      {labels.map((x) => (
        <Badge
          variant="outline"
          colorScheme="orange"
          fontSize="xs"
          overflowWrap="break-word"
          overflow="scroll"
          maxWidth={100}
          textAlign="center"
        >
          {x}
        </Badge>
      ))}
    </SimpleGrid>
  </>
);

const ClassLabelsSection: React.FC<{ func: Func }> = ({ func }) =>
  func.classLabels ? (
    <LabelsSection labels={func.classLabels} title="Classes" />
  ) : (
    <></>
  );

const KeyPointLabelsSection: React.FC<{ func: Func }> = ({ func }) =>
  func.keyPointLabels ? (
    <LabelsSection labels={func.keyPointLabels} title="Key points" />
  ) : (
    <></>
  );

export const FuncDetails = () => {
  let { name } = useParams();
  let func = null;
  if (name != null) {
    func = funcs[name];
  } else {
    return <></>;
  }

  return (
    <>
      <FuncTitle name={name || ""} size="lg" />
      <Text fontSize="xl">{renderText(func.description)}</Text>
      <ColabLink func={func} />
      <HStack spacing="100px" align="top">
        <VStack width="55%" align="left" spacing="4">
          <InstallSection func={func} />
          <ExampleSection func={func} />
        </VStack>
        <VStack width="35%" align="left" spacing="4">
          <DeviceSection func={func} />
          <ClassLabelsSection func={func} />
          <KeyPointLabelsSection func={func} />
        </VStack>
      </HStack>
    </>
  );
};
