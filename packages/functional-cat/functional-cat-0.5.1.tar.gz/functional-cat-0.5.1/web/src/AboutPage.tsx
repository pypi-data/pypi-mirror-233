import Wrapper from "./Wrapper";
import { Text, UnorderedList, ListItem } from "@chakra-ui/react";

const Content = () => (
  <>
    <br />
    <br />
    <Text>
      the machine learning research community does a great job of open-sourcing
      their models. many of these however are hard to use out-of-the-box for
      inference. common issues are:
      <br />
      <br />
      <UnorderedList style={{ textIndent: 20 }}>
        <ListItem>
          the code is optimized for training or bulk evaluation
        </ListItem>
        <ListItem>
          the input/output formats are opague or buried in documentation. e.g.
          it's unclear how to convert an image into the necessary input tensor.
          is it RGB or BGR? channel first or last? mean/std normalized? or its
          not clear what the output of say an object detection model is, or how
          to convert integer class labels to strings.
        </ListItem>
        <ListItem>
          the code is not organized as a package which makes it difficult to use
          in workflows with other packages.
        </ListItem>
        <ListItem>dependency and install hell.</ListItem>
        <ListItem>
          model weights are behind a broken link, or something like google drive
          which is hard to get programatically.
        </ListItem>
      </UnorderedList>
      <br />
      the goal of functional-cat is to address these problems by providing a
      simple wrapper on top of the models it supports. All models take in PIL
      images, handling all of the necessary pre- and post-processing interally.
      it also provides unified data classes for objects such as detections,
      instance segmentations, and keypoints, which makes the models
      interoperable and their outputs easier to understand and use.
    </Text>
  </>
);

const AboutPage = () => <Wrapper children={<Content />} />;

export default AboutPage;
