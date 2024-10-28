import Link from "@docusaurus/Link";
import IconExternalLink from "@theme/Icon/ExternalLink";

import {IconifyIcon} from "@iconify/react";
import InlineIcon from "./InlineIcon";

export type IconLinkProps = {
  href: string;
  icon?: IconifyIcon | string;
  text?: string;
};

/**
 * Render a link with an Icon.
 * @param props - text, href, and icon of the link. If the icon is not specified, will
 *   use the external link icon to render it.
 * @returns The <link/> component with `href` configured.
 */
const IconLink = (props: IconLinkProps): JSX.Element => {
  const text = props.text || props.href;
  const icon = props.icon ? (
    <InlineIcon icon={props.icon} />
  ) : (
    <IconExternalLink />
  );

  return (
    <p>
      <Link href={props.href}>
        <span>{text}</span>
        {icon}
      </Link>
    </p>
  );
};

export default IconLink;
