/* Themed Component
 * Author: cainmagi@gmail.com
 */
import React, { useEffect, useState } from "react";

// import useThemeContext from '@theme/hooks/useThemeContext'; //docs: https://v2.docusaurus.io/docs/2.0.0-alpha.69/theme-classic#usethemecontext
/* Refactor:
The original useThemeContext has been replaced by the new API useColorMode
https://github.com/facebook/docusaurus/pull/6289
*/
import { useColorMode } from "@docusaurus/theme-common";

type DarkButtonProps = {
  light: JSX.Element;
  dark: JSX.Element;
};

/**
 * ThemedComponent will render different components in different color modes.
 *
 * @param props - The components used in light and dark modes, respectively.
 * @returns The themed component that will render different components in different color modes.
 */
const ThemedComponent = (props: DarkButtonProps): JSX.Element => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const { colorMode, setColorMode } = useColorMode();
  const isDarkTheme = colorMode === "dark";

  return isDarkTheme ? props.dark : props.light;
};

export default ThemedComponent;
