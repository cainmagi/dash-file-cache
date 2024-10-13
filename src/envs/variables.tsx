/**
 * Environmental variables of this side.
 * Yuchen Jin, mailto:cainmagi@gmail.com
 */

import React from "react";
import Link from "@docusaurus/Link";

import InlineIcon from "../components/InlineIcon";
import mdiDot from "@iconify-icons/mdi/dot";

const variables = {
  sourceURL:
    "https://github.com/cainmagi/dash-file-cache/blob/90214d58c0610976d7af1c583a35f83784c0c80c",
};

export const demoURL = (url: string): string => {
  return variables.sourceURL + "/examples/" + url;
};

export const SourceURL = (url: string): string => {
  return variables.sourceURL + "/dash_file_cache/" + url;
};

export type SourceLinkProps = {
  url: string;
  children: React.ReactNode;
};

export const SourceLink = ({ url, children }: SourceLinkProps): JSX.Element => {
  return (
    <Link to={SourceURL(url)} className="noline">
      {children}
    </Link>
  );
};

export type SplitterProps = {
  padx?: string;
};

export const Splitter = ({ padx = "0" }: SplitterProps): JSX.Element => {
  return (
    <span style={{ padding: "0 " + padx }}>
      <InlineIcon icon={mdiDot} />
    </span>
  );
};
