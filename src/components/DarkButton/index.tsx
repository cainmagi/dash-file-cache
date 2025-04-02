/* DarkButton
 * Author: cainmagi@gmail.com
 */
import React, {useEffect, useState} from "react";

import Link from "@docusaurus/Link";
import {IconifyIcon, InlineIcon} from "@iconify/react";
// import useThemeContext from '@theme/hooks/useThemeContext'; //docs: https://v2.docusaurus.io/docs/2.0.0-alpha.69/theme-classic#usethemecontext
/* Refactor:
The original useThemeContext has been replaced by the new API useColorMode
https://github.com/facebook/docusaurus/pull/6289
*/
import {useColorMode} from "@docusaurus/theme-common";

const useButtonTheme = () => {
  const {colorMode, setColorMode} = useColorMode();
  const isDarkTheme = colorMode === "dark";
  if (isDarkTheme) {
    return `button--secondary button--outline`;
  } else {
    return "button--secondary";
  }
};

type DarkButtonProps = {
  index?: boolean;
  to?: string;
  href?: string;
  icon?: IconifyIcon | string;
  iconVspace?: number;
  children: React.ReactNode;
};

/**
 * DarkButton will render a different style when the dark mode is on.
 *
 * @param props - The properties of the button, similar to the usage of the properties of <Link/>.
 * @returns The <Link/> component with theme configured.
 */
const DarkButton = (props: DarkButtonProps): JSX.Element => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const curStyle = useButtonTheme();

  const className = props.index
    ? `button ${curStyle} button--lg button--index`
    : `button ${curStyle} button--lg`;

  const typeIconVspace = typeof props.iconVspace;
  const iconVspace =
    typeIconVspace === "undefined"
      ? "-0.3rem"
      : typeIconVspace === "number" && Math.abs(props.iconVspace) > 0.001
      ? `${props.iconVspace}rem`
      : "0";

  return (
    <Link
      key={String(mounted)}
      className={className}
      to={props.to}
      href={props.href}
    >
      {props.icon && (
        <InlineIcon
          icon={props.icon}
          width="1.35rem"
          style={{
            verticalAlign: iconVspace,
            marginRight: "1ex",
          }}
        />
      )}
      {props.children}
    </Link>
  );
};

export default DarkButton;
