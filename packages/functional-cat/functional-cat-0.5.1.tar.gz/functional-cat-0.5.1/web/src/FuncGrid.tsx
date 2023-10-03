import {
  SimpleGrid,
  Grid,
  GridItem,
  Checkbox,
  Stack,
  VStack,
  Heading,
  Input,
  Text,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { funcs } from "./func";
import { FuncCard } from "./func";

const frameworks: string[] = Array.from(
  new Set(Object.values(funcs).map((x) => x.framework))
);

const tasks: string[] = Array.from(
  new Set(Object.values(funcs).map((x) => x.task))
);

const SelectionFilter: React.FC<{
  title: string;
  allOptions: string[];
  selectedOptions: string[];
  setSelectedOptions: React.Dispatch<React.SetStateAction<string[]>>;
}> = ({ title, allOptions, selectedOptions, setSelectedOptions }) => {
  const handleChange = (option: string, e: any) => {
    if (e.target.checked) {
      if (!selectedOptions.includes(option)) {
        setSelectedOptions(selectedOptions.concat([option]));
      }
    } else {
      if (selectedOptions.includes(option)) {
        setSelectedOptions(selectedOptions.filter((f) => f !== option));
      }
    }
  };
  return (
    <Stack spacing={5} direction="column">
      <Heading size="sm">{title}</Heading>
      {allOptions.map((x) =>
        selectedOptions.includes(x) ? (
          <Checkbox onChange={(e) => handleChange(x, e)} defaultChecked key={x}>
            {x}
          </Checkbox>
        ) : (
          <Checkbox onChange={(e) => handleChange(x, e)} key={x}>
            {x}
          </Checkbox>
        )
      )}
    </Stack>
  );
};

const Search: React.FC<{
  currentQuery: string;
  setCurrentQuery: React.Dispatch<React.SetStateAction<string>>;
  placeholder: string;
}> = ({ currentQuery, setCurrentQuery, placeholder }) => {
  const handleChange = (e: any) => setCurrentQuery(e.target.value);
  return (
    <Input
      placeholder={placeholder}
      value={currentQuery}
      // width={350}
      onChange={handleChange}
    />
  );
};

const descAndTitleSearchFilter = (query: string, funcKey: string): boolean => {
  const lowerCaseQuery = query.toLowerCase();
  return (
    funcs[funcKey].description.toLowerCase().includes(lowerCaseQuery) ||
    funcKey.includes(lowerCaseQuery)
  );
};

const classLabelSearchFilter = (query: string, funcKey: string): boolean => {
  if (!query) {
    return true;
  }

  const lowerCaseQuery = query.toLowerCase();
  const func = funcs[funcKey];
  if (!func.classLabels) {
    return false;
  }

  for (const label of func.classLabels) {
    if (label.includes(lowerCaseQuery)) {
      return true;
    }
  }
  return false;
};

const FuncGrid = () => {
  let funcKeys = Object.keys(funcs);
  const [selectedFrameworks, setSelectedFrameworks] = useState(frameworks);
  const [selectedTasks, setSelectedTasks] = useState(tasks);
  const [currentDTQuery, setCurrentDTQuery] = useState("");
  const [currentLabelQuery, setCurrentLabelQuery] = useState("");
  const nCols = 7;

  funcKeys = funcKeys.filter((funcKey) =>
    selectedFrameworks.includes(funcs[funcKey].framework)
  );
  funcKeys = funcKeys.filter((funcKey) =>
    selectedTasks.includes(funcs[funcKey].task)
  );
  funcKeys = funcKeys.filter((funcKey) =>
    descAndTitleSearchFilter(currentDTQuery, funcKey)
  );
  funcKeys = funcKeys.filter((funcKey) =>
    classLabelSearchFilter(currentLabelQuery, funcKey)
  );

  return (
    <Grid
      templateColumns={`repeat(${nCols}, 1fr)`}
      templateRows={"25px 1fr"}
      gap={10}
    >
      <GridItem colSpan={1} rowSpan={2}>
        <VStack spacing="50px" align="left">
          <SelectionFilter
            title="Framework"
            allOptions={frameworks}
            selectedOptions={selectedFrameworks}
            setSelectedOptions={setSelectedFrameworks}
          />
          <SelectionFilter
            title="Task"
            allOptions={tasks}
            selectedOptions={selectedTasks}
            setSelectedOptions={setSelectedTasks}
          />
        </VStack>
      </GridItem>
      <GridItem colSpan={2}>
        <Search
          currentQuery={currentDTQuery}
          setCurrentQuery={setCurrentDTQuery}
          placeholder="Search name and description"
        />
      </GridItem>
      <GridItem colSpan={2}>
        <Search
          currentQuery={currentLabelQuery}
          setCurrentQuery={setCurrentLabelQuery}
          placeholder="Search by class label"
        />
      </GridItem>
      <GridItem colSpan={nCols - 5}>
        <Text fontSize="3xl" align="center">{`${funcKeys.length} models`}</Text>
      </GridItem>
      <GridItem colSpan={nCols - 1}>
        <SimpleGrid minChildWidth="290px" spacing="20px">
          {funcKeys.map((x) => (
            <FuncCard name={x} func={funcs[x]} key={x} />
          ))}
        </SimpleGrid>
      </GridItem>
    </Grid>
  );
};

export default FuncGrid;
