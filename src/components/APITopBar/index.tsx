import {translate} from "@docusaurus/Translate";

import vsiSymbolClass from "@iconify-icons/codicon/symbol-class";
import vsiPackage from "@iconify-icons/codicon/package";
import vsiSymbolNamespace from "@iconify-icons/codicon/symbol-namespace";
import vsiSymbolParameter from "@iconify-icons/codicon/symbol-parameter";
import vsiSymbolOperator from "@iconify-icons/codicon/symbol-operator";
import vsiSymbolMethod from "@iconify-icons/codicon/symbol-method";
import vsiSymbolField from "@iconify-icons/codicon/symbol-field";
import vsiExtensions from "@iconify-icons/codicon/extensions";
import vsiTerminalIcon from "@iconify-icons/codicon/terminal";
import mdiAlphaTBoxOutline from "@iconify-icons/mdi/alpha-t-box-outline";
import mdiAt from "@iconify-icons/mdi/at";
import mdiAbc from "@iconify-icons/mdi/abc";
import mdiFunctionVariant from "@iconify-icons/mdi/function-variant";
import mdiLockOutline from "@iconify-icons/mdi/lock-outline";
import mdiLockOpenVariantOutline from "@iconify-icons/mdi/lock-open-variant-outline";
import octFileCode16 from "@iconify-icons/octicon/file-code-16";
import octUnverified16 from "@iconify-icons/octicon/unverified-16";

import {iconoirComponentSolid} from "../icons/IconoirComponentSolid";

import InlineIcon from "../InlineIcon";
import {SourceLink, Splitter} from "@site/src/envs/variables";

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
    | "ext"
    | "comp"
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
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.class",
                    description:
                      "The text displayed for the APITopBar icon: Class.",
                    message: "Class",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "func":
      return (
        <InlineIcon
          icon={mdiFunctionVariant}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.func",
                    description:
                      "The text displayed for the APITopBar icon: Function.",
                    message: "Function",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "type":
      return (
        <InlineIcon
          icon={mdiAlphaTBoxOutline}
          vspace={vspace || -0.3}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.type",
                    description:
                      "The text displayed for the APITopBar icon: Type.",
                    message: "Type",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "package":
      return (
        <InlineIcon
          icon={vsiPackage}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.package",
                    description:
                      "The text displayed for the APITopBar icon: Package.",
                    message: "Package",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "module":
      return (
        <InlineIcon
          icon={vsiSymbolNamespace}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.module",
                    description:
                      "The text displayed for the APITopBar icon: Module.",
                    message: "Module",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "param":
      return (
        <InlineIcon
          icon={vsiSymbolParameter}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.param",
                    description:
                      "The text displayed for the APITopBar icon: Parameter.",
                    message: "Parameter",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "op":
      return (
        <InlineIcon
          icon={vsiSymbolOperator}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.op",
                    description:
                      "The text displayed for the APITopBar icon: Operator.",
                    message: "Operator",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "method":
      return (
        <InlineIcon
          icon={vsiSymbolMethod}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.method",
                    description:
                      "The text displayed for the APITopBar icon: Method.",
                    message: "Method",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "ctx":
      return (
        <InlineIcon
          icon={vsiSymbolField}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.ctx",
                    description:
                      "The text displayed for the APITopBar icon: Context.",
                    message: "Context",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "deco":
      return (
        <InlineIcon
          icon={mdiAt}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.deco",
                    description:
                      "The text displayed for the APITopBar icon: Decorator.",
                    message: "Decorator",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "abc":
      return (
        <InlineIcon
          icon={mdiAbc}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.abc",
                    description:
                      "The text displayed for the APITopBar icon: Abstract.",
                    message: "Abstract",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "ext":
      return (
        <InlineIcon
          icon={vsiExtensions}
          vspace={vspace || -0.3}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.ext",
                    description:
                      "The text displayed for the APITopBar icon: Extension.",
                    message: "Extension",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "comp":
      return (
        <InlineIcon
          icon={iconoirComponentSolid}
          vspace={vspace || -0.3}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.comp",
                    description:
                      "The text displayed for the APITopBar icon: Component.",
                    message: "Component",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "term":
      return (
        <InlineIcon
          icon={vsiTerminalIcon}
          vspace={vspace || -0.2}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.term",
                    description:
                      "The text displayed for the APITopBar icon: Terminal.",
                    message: "Terminal",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "private":
      return (
        <InlineIcon
          icon={mdiLockOutline}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.private",
                    description:
                      "The text displayed for the APITopBar icon: Private.",
                    message: "Private",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "public":
      return (
        <InlineIcon
          icon={mdiLockOpenVariantOutline}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.public",
                    description:
                      "The text displayed for the APITopBar icon: Public.",
                    message: "Public",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    case "src":
      return (
        <InlineIcon
          icon={octFileCode16}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.src",
                    description:
                      "The text displayed for the APITopBar icon: Source.",
                    message: "Source",
                  },
                  {}
                )
              : undefined
          }
        />
      );
    default:
      return (
        <InlineIcon
          icon={octUnverified16}
          vspace={vspace}
          text={
            hasText
              ? text ||
                translate(
                  {
                    id: "components.apitopbar.icon.default",
                    description:
                      "The text displayed for the APITopBar icon: Unknown.",
                    message: "Unknown",
                  },
                  {}
                )
              : undefined
          }
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
  isMixin?: boolean;
  isComponent?: boolean;
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
      {props.isMixin && (
        <>
          <Splitter />
          <IconObjType type={"ext"} hasText={true} />
        </>
      )}
      {props.isComponent && (
        <>
          <Splitter />
          <IconObjType type={"comp"} hasText={true} />
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
