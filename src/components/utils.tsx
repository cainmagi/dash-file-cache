import Heading, {Props as HeadingProps} from "@theme/Heading";

type HeadingSafeProps = HeadingProps & JSX.IntrinsicElements["h1"];

/**
 * Heading component with the issue caused by the absence of `props.children` gets
 * fixed.
 * @param props - The properties of a <h*> tag, where the tag name is specified by
 *   the property `as`.
 * @returns The <h*> component.
 */
export const HeadingSafe = (props: HeadingSafeProps): JSX.Element => {
  return <Heading {...props} />;
};
