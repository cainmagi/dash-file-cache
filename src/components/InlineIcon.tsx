import React from "react";

import { IconifyIcon, InlineIcon } from "@iconify/react";

export type InlineIconMProps = {
  icon: IconifyIcon | string;
  vspace?: number;
  text?: string;
};

/**
 * InlineIconM is a modified InlineIcon.
 *
 * @param props - The properties of the icon, it only supports the customizations of
 *   the icon content and the vertical space.
 * @returns The <InlineIcon/> component with the customization.
 */
const InlineIconM = (props: InlineIconMProps): JSX.Element => {
  return props.text ? (
    <>
      <InlineIcon
        icon={props.icon}
        width="1.35rem"
        style={{ verticalAlign: `${props.vspace || -0.4}rem` }}
      />
      <span style={{ marginLeft: "0.3rem" }}>{props.text}</span>
    </>
  ) : (
    <InlineIcon
      icon={props.icon}
      width="1.35rem"
      style={{ verticalAlign: `${props.vspace || -0.4}rem` }}
    />
  );
};

export default InlineIconM;
