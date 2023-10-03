import { Heading, Link, Text } from "@chakra-ui/react";

export interface PythonClassMeta {
  class: string;
  description: string;
  lineOfDef: number;
  filePath: string;
}

export const PythonClassComponent: React.FC<{
  pythonClassMeta: PythonClassMeta;
}> = ({ pythonClassMeta }) => (
  <>
    <Link
      href={`${process.env.REACT_APP_GITHUB_URL}/blob/${process.env.REACT_APP_BRANCH}/${pythonClassMeta.filePath}#L${pythonClassMeta.lineOfDef}`}
    >
      <Heading size="md">{pythonClassMeta.class}</Heading>
    </Link>
    <Text>{pythonClassMeta.description}</Text>
  </>
);
