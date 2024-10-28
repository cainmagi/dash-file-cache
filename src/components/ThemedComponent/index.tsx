/* Themed Component
 * Author: cainmagi@gmail.com
 */
import React, {CSSProperties, useEffect, useState} from "react";

// import useThemeContext from '@theme/hooks/useThemeContext'; //docs: https://v2.docusaurus.io/docs/2.0.0-alpha.69/theme-classic#usethemecontext
/* Refactor:
The original useThemeContext has been replaced by the new API useColorMode
https://github.com/facebook/docusaurus/pull/6289
*/
import {useColorMode} from "@docusaurus/theme-common";

type ThemedComponentProps = {
  light: JSX.Element;
  dark: JSX.Element;
  className?: string;
  style?: React.CSSProperties;
};

/**
 * ThemedComponent will render different components in different color modes.
 * 
 * Note that the top level of this component is a `<div>` which cannot be used in `<p>`
 *
 * @param props - The components used in light and dark modes, respectively.
 * @returns The themed component that will render different components in different
 *   color modes.
 */
const ThemedComponent = (props: ThemedComponentProps): JSX.Element => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const {colorMode, setColorMode} = useColorMode();
  const isDarkTheme = colorMode === "dark";

  return (
    <div key={String(mounted)} className={props.className} style={props.style}>
      {isDarkTheme ? props.dark : props.light}
    </div>
  );
};

export default ThemedComponent;
