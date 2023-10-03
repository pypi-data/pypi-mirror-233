import _tasks from "./tasks.json";
import Wrapper from "./Wrapper";
import { PythonClassComponent, PythonClassMeta } from "./pythonClassMeta";

const tasks = _tasks as PythonClassMeta[];

const TasksList = () => (
  <>
    {tasks.map((x) => (
      <PythonClassComponent pythonClassMeta={x} />
    ))}
  </>
);

const TasksPage = () => <Wrapper children={<TasksList />} />;

export default TasksPage;
