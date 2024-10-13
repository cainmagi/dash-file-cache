import vsiSymbolClass from "@iconify-icons/codicon/symbol-class";
import vsiPackage from "@iconify-icons/codicon/package";
import vsiSymbolNamespace from "@iconify-icons/codicon/symbol-namespace";
import vsiSymbolParameter from "@iconify-icons/codicon/symbol-parameter";
import vsiSymbolOperator from "@iconify-icons/codicon/symbol-operator";
import vsiSymbolMethod from "@iconify-icons/codicon/symbol-method";
import vsiSymbolField from "@iconify-icons/codicon/symbol-field";
import vsiTerminalIcon from "@iconify-icons/codicon/terminal";
import mdiAlphaTBoxOutline from '@iconify-icons/mdi/alpha-t-box-outline';
import mdiAt from "@iconify-icons/mdi/at";
import mdiAbc from "@iconify-icons/mdi/abc";
import mdiFunctionVariant from "@iconify-icons/mdi/function-variant";
import mdiLockOutline from "@iconify-icons/mdi/lock-outline";
import mdiLockOpenVariantOutline from "@iconify-icons/mdi/lock-open-variant-outline";
import octFileCode16 from "@iconify-icons/octicon/file-code-16";
import octUnverified16 from "@iconify-icons/octicon/unverified-16";

import InlineIcon from "../InlineIcon";
import { SourceLink, Splitter } from "@site/src/envs/variables";

export type IconObjTypeProps = {
  type:
    | "class"
    | "func"
    | "package"
    | "module"
    | "param"
    | "op"
    | "method"
    | "ctx"
    | "deco"
    | "abc"
    | "type"
    | "term"
    | "private"
    | "public"
    | "src";
  vspace?: number;
  hasText?: boolean;
  text?: string;
};

export const IconObjType = ({
  type,
  vspace,
  hasText = false,
  text,
}: IconObjTypeProps): JSX.Element => {
  switch (type) {
    case "class":
      return (
        <InlineIcon
          icon={vsiSymbolClass}
          vspace={vspace}
          text={hasText ? text || "Class" : undefined}
        />
      );
    case "func":
      return (
        <InlineIcon
          icon={mdiFunctionVariant}
          vspace={vspace}
          text={hasText ? text || "Function" : undefined}
        />
      );
    case "type":
      return (
        <InlineIcon
          icon={mdiAlphaTBoxOutline}
          vspace={vspace || -0.3}
          text={hasText ? text || "Type" : undefined}
        />
      );
    case "package":
      return (
        <InlineIcon
          icon={vsiPackage}
          vspace={vspace}
          text={hasText ? text || "Package" : undefined}
        />
      );
    case "module":
      return (
        <InlineIcon
          icon={vsiSymbolNamespace}
          vspace={vspace}
          text={hasText ? text || "Module" : undefined}
        />
      );
    case "param":
      return (
        <InlineIcon
          icon={vsiSymbolParameter}
          vspace={vspace}
          text={hasText ? text || "Parameter" : undefined}
        />
      );
    case "op":
      return (
        <InlineIcon
          icon={vsiSymbolOperator}
          vspace={vspace}
          text={hasText ? text || "Operator" : undefined}
        />
      );
    case "method":
      return (
        <InlineIcon
          icon={vsiSymbolMethod}
          vspace={vspace}
          text={hasText ? text || "Method" : undefined}
        />
      );
    case "ctx":
      return (
        <InlineIcon
          icon={vsiSymbolField}
          vspace={vspace}
          text={hasText ? text || "Context" : undefined}
        />
      );
    case "deco":
      return (
        <InlineIcon
          icon={mdiAt}
          vspace={vspace}
          text={hasText ? text || "Decorator" : undefined}
        />
      );
    case "abc":
      return (
        <InlineIcon
          icon={mdiAbc}
          vspace={vspace}
          text={hasText ? text || "Abstract" : undefined}
        />
      );
    case "term":
      return (
        <InlineIcon
          icon={vsiTerminalIcon}
          vspace={vspace || -0.2}
          text={hasText ? text || "Terminal" : undefined}
        />
      );
    case "private":
      return (
        <InlineIcon
          icon={mdiLockOutline}
          vspace={vspace}
          text={hasText ? text || "Private" : undefined}
        />
      );
    case "public":
      return (
        <InlineIcon
          icon={mdiLockOpenVariantOutline}
          vspace={vspace}
          text={hasText ? text || "Public" : undefined}
        />
      );
    case "src":
      return (
        <InlineIcon
          icon={octFileCode16}
          vspace={vspace}
          text={hasText ? text || "Source" : undefined}
        />
      );
    default:
      return (
        <InlineIcon
          icon={octUnverified16}
          vspace={vspace}
          text={hasText ? text || "Unknown" : undefined}
        />
      );
  }
};

export type APITopBarProps = {
  type: "class" | "func" | "module" | "type";
  isPrivate?: boolean;
  isAbstract?: boolean;
  isContext?: boolean;
  isDecorator?: boolean;
  source_ver?: string;
  source?: string;
};

/**
 * Render a top bar showing the API information.
 * @param props - Basic information shown on the top bar.
 * @returns The one line <p> component with top bar information.
 */
const APITopBar = (props: APITopBarProps): JSX.Element => {
  return (
    <p>
      <IconObjType type={props.type} hasText={true} />
      {props.isPrivate && (
        <>
          <Splitter />
          <IconObjType type={"private"} hasText={true} />
        </>
      )}
      {props.isAbstract && (
        <>
          <Splitter />
          <IconObjType type={"abc"} hasText={true} />
        </>
      )}
      {props.isContext && (
        <>
          <Splitter />
          <IconObjType type={"ctx"} hasText={true} />
        </>
      )}
      {props.isDecorator && (
        <>
          <Splitter />
          <IconObjType type={"deco"} hasText={true} />
        </>
      )}
      {props.source && (
        <>
          <Splitter />
          <SourceLink url={props.source}>
            <IconObjType type={"src"} hasText={true} />
          </SourceLink>
        </>
      )}
    </p>
  );
};

export default APITopBar;
