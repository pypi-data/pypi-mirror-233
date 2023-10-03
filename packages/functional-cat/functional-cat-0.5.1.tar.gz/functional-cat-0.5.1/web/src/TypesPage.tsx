import _types from "./types.json";
import Wrapper from "./Wrapper";
import { PythonClassComponent, PythonClassMeta } from "./pythonClassMeta";

const types = _types as PythonClassMeta[];

const TypesList = () => (
  <>
    {types.map((x) => (
      <PythonClassComponent pythonClassMeta={x} />
    ))}
  </>
);

const TypesPage = () => <Wrapper children={<TypesList />} />;

export default TypesPage;
