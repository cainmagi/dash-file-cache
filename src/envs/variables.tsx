/**
 * Environmental variables of this side.
 * Yuchen Jin, mailto:cainmagi@gmail.com
 */

import React from "react";
import Link from "@docusaurus/Link";
import {useDocsVersion} from "@docusaurus/plugin-content-docs/client";
import IconExternalLink from "@theme/Icon/ExternalLink";

import InlineIcon from "../components/InlineIcon";
import mdiDot from "@iconify-icons/mdi/dot";
import {biSlashLg} from "../components/icons/BiSlashLg";

const docsPluginId = undefined; // Default docs plugin instance

const variables = {
  repoURL: "https://github.com/cainmagi/dash-file-cache",
  rawURL: "https://raw.githubusercontent.com/cainmagi/dash-file-cache",
  sourceVersion: {
    "0.2.0": "v0.2.0",
    "0.1.x": "v0.1.2",
    main: "c9d72d824d70274d2c931a98b1235de034cc5dd6",
  },
  dependencyVersion: {
    "0.2.0": "2.0.6",
    "0.1.x": undefined,
    main: "2.0.6",
  },
  sourceURIs: {
    "v0.2.0": {
      ".": "__init__.py",
      caches: "caches/__init__.py",
      "caches.abstract": "caches/abstract.py",
      "caches.abstract.CacheAbstract": "caches/abstract.py#L44",
      "caches.lrudict": "caches/lrudict.py",
      "caches.lrudict.LRUDict": "caches/lrudict.py#L107",
      "caches.memory": "caches/memory.py",
      "caches.memory.CachePlain": "caches/memory.py#L66",
      "caches.memory.CacheQueue": "caches/memory.py#L168",
      "caches.memory.CacheQueueMirror": "caches/memory.py#L207",
      "caches.tempfile": "caches/tempfile.py",
      "caches.tempfile.CacheFile": "caches/tempfile.py#L54",
      "caches.typehints": "caches/typehints.py",
      "caches.typehints.CachedBytesIO": "caches/typehints.py#L131",
      "caches.typehints.CachedData": "caches/typehints.py#L142",
      "caches.typehints.CachedFileInfo": "caches/typehints.py#L51",
      "caches.typehints.CachedPath": "caches/typehints.py#L81",
      "caches.typehints.CachedRequest": "caches/typehints.py#L95",
      "caches.typehints.CachedStringIO": "caches/typehints.py#L120",
      "caches.typehints.Deferred": "caches/typehints.py#L36",
      components: "components/__init__.py",
      "components.typehints": "components/typehints.py",
      "components.typehints.DownloaderURL": "components/typehints.py#L26",
      "components.typehints.DownloaderStatus": "components/typehints.py#L44",
      "components.PlainDownloader": "components/__init__.py#L31",
      "components.Downloader": "components/__init__.py#L31",
      services: "services/__init__.py",
      "services.data": "services/data.py",
      "services.data.ServiceData": "services/data.py#L57",
      "services.downloader": "services/downloader.py",
      "services.downloader.ServiceDownloader": "services/downloader.py#L38",
      "services.reqstream": "services/reqstream.py",
      "services.reqstream.ProtocolResponse": "services/reqstream.py#L45",
      "services.reqstream.DeferredRequestStream": "services/reqstream.py#L59",
      "services.utilities": "services/utilities.py",
      "services.utilities.get_server": "services/utilities.py#L61",
      "services.utilities.no_cache": "services/utilities.py#L40",
      utilities: "utilities.py",
      "utilities.is_in_main_process": "utilities.py#L52",
      "utilities.remove_temp_dir": "utilities.py#L63",
      "utilities.StreamFinalizer": "utilities.py#L120",
      "utilities.TempDir": "utilities.py#L76",
    },
    "v0.1.2": {
      ".": "__init__.py",
      caches: "caches/__init__.py",
      "caches.abstract": "caches/abstract.py",
      "caches.abstract.CacheAbstract": "caches/abstract.py#L44",
      "caches.lrudict": "caches/lrudict.py",
      "caches.lrudict.LRUDict": "caches/lrudict.py#L107",
      "caches.memory": "caches/memory.py",
      "caches.memory.CachePlain": "caches/memory.py#L66",
      "caches.memory.CacheQueue": "caches/memory.py#L168",
      "caches.memory.CacheQueueMirror": "caches/memory.py#L207",
      "caches.tempfile": "caches/tempfile.py",
      "caches.tempfile.CacheFile": "caches/tempfile.py#L54",
      "caches.typehints": "caches/typehints.py",
      "caches.typehints.CachedBytesIO": "caches/typehints.py#L104",
      "caches.typehints.CachedData": "caches/typehints.py#L115",
      "caches.typehints.CachedFileInfo": "caches/typehints.py#L49",
      "caches.typehints.CachedPath": "caches/typehints.py#L79",
      "caches.typehints.CachedStringIO": "caches/typehints.py#L93",
      "caches.typehints.Deferred": "caches/typehints.py#L34",
      components: "components/__init__.py",
      "components.downloader": "components/downloader.py",
      "components.downloader.Downloader": "components/downloader.py#L38",
      services: "services/__init__.py",
      "services.data": "services/data.py",
      "services.data.ServiceData": "services/data.py#L53",
      "services.utilities": "services/utilities.py",
      "services.utilities.get_server": "services/utilities.py#L61",
      "services.utilities.no_cache": "services/utilities.py#L40",
      utilities: "utilities.py",
      "utilities.is_in_main_process": "utilities.py#L52",
      "utilities.remove_temp_dir": "utilities.py#L63",
      "utilities.StreamFinalizer": "utilities.py#L120",
      "utilities.TempDir": "utilities.py#L76",
    },
    main: {
      ".": "__init__.py",
      caches: "caches/__init__.py",
      "caches.abstract": "caches/abstract.py",
      "caches.abstract.CacheAbstract": "caches/abstract.py#L44",
      "caches.lrudict": "caches/lrudict.py",
      "caches.lrudict.LRUDict": "caches/lrudict.py#L107",
      "caches.memory": "caches/memory.py",
      "caches.memory.CachePlain": "caches/memory.py#L66",
      "caches.memory.CacheQueue": "caches/memory.py#L168",
      "caches.memory.CacheQueueMirror": "caches/memory.py#L207",
      "caches.tempfile": "caches/tempfile.py",
      "caches.tempfile.CacheFile": "caches/tempfile.py#L54",
      "caches.typehints": "caches/typehints.py",
      "caches.typehints.CachedBytesIO": "caches/typehints.py#L131",
      "caches.typehints.CachedData": "caches/typehints.py#L142",
      "caches.typehints.CachedFileInfo": "caches/typehints.py#L51",
      "caches.typehints.CachedPath": "caches/typehints.py#L81",
      "caches.typehints.CachedRequest": "caches/typehints.py#L95",
      "caches.typehints.CachedStringIO": "caches/typehints.py#L120",
      "caches.typehints.Deferred": "caches/typehints.py#L36",
      components: "components/__init__.py",
      "components.typehints": "components/typehints.py",
      "components.typehints.DownloaderURL": "components/typehints.py#L26",
      "components.typehints.DownloaderStatus": "components/typehints.py#L44",
      "components.PlainDownloader": "components/__init__.py#L31",
      "components.Downloader": "components/__init__.py#L31",
      services: "services/__init__.py",
      "services.data": "services/data.py",
      "services.data.ServiceData": "services/data.py#L57",
      "services.downloader": "services/downloader.py",
      "services.downloader.ServiceDownloader": "services/downloader.py#L38",
      "services.reqstream": "services/reqstream.py",
      "services.reqstream.ProtocolResponse": "services/reqstream.py#L45",
      "services.reqstream.DeferredRequestStream": "services/reqstream.py#L59",
      "services.utilities": "services/utilities.py",
      "services.utilities.get_server": "services/utilities.py#L61",
      "services.utilities.no_cache": "services/utilities.py#L40",
      utilities: "utilities.py",
      "utilities.is_in_main_process": "utilities.py#L52",
      "utilities.remove_temp_dir": "utilities.py#L63",
      "utilities.StreamFinalizer": "utilities.py#L120",
      "utilities.TempDir": "utilities.py#L76",
    },
  },
};

const useCurrentSourceVersion = (): string => {
  const versionHook = useDocsVersion();
  const versionLabel = versionHook?.label;
  return (
    variables.sourceVersion[versionLabel] || variables.sourceVersion["main"]
  );
};

export type DependencyTagProps = {
  ver: string;
};

export const DependencyTag = ({
  ver = "main",
}: DependencyTagProps): JSX.Element => {
  const _ver = ver?.toLowerCase() === "next" ? "main" : ver;
  const versionDeps = variables.dependencyVersion[_ver];
  return versionDeps ? (
    <Link
      href={`https://github.com/jimmywarting/StreamSaver.js/tree/${versionDeps}`}
    >
      <code>{`streamsaver@${versionDeps}`}</code>
      <IconExternalLink />
    </Link>
  ) : (
    <InlineIcon icon={biSlashLg} />
  );
};

export const rawURL = (url: string): string => {
  return variables.rawURL + "/" + url;
};

export const repoURL = (url: string | undefined = undefined): string => {
  return url ? variables.repoURL + "/" + url : variables.repoURL;
};

export const releaseURL = (ver: string | undefined = undefined): string => {
  const _ver = ver?.toLowerCase() === "next" ? "main" : ver;
  const version = variables.sourceVersion[_ver] || useCurrentSourceVersion();
  if (version === "main" || _ver === "main") {
    return variables.repoURL + "/releases/latest";
  }
  return variables.repoURL + "/releases/tag/" + version;
};

export const rootURL = (url: string): string => {
  const currentSourceVersion = useCurrentSourceVersion();
  return variables.repoURL + "/blob/" + currentSourceVersion + "/" + url;
};

const getURIByVersionPath = (path: string, ver: string): string => {
  const routes = typeof path === "string" ? path.trim() : "";
  if (routes.length === 0) {
    return path;
  }
  const currentURI = variables.sourceURIs[ver] || variables.sourceURIs["main"];
  return currentURI[path] || path;
};

export const sourceURL = (url: string): string => {
  const currentSourceVersion = useCurrentSourceVersion();
  return (
    variables.repoURL +
    "/blob/" +
    currentSourceVersion +
    "/dash_file_cache/" +
    getURIByVersionPath(url, currentSourceVersion)
  );
};

export const demoURL = (url: string): string => {
  const currentSourceVersion = useCurrentSourceVersion();
  return (
    variables.repoURL + "/blob/" + currentSourceVersion + "/examples/" + url
  );
};

export type SourceLinkProps = {
  url: string;
  children: React.ReactNode;
};

export const SourceLink = ({url, children}: SourceLinkProps): JSX.Element => {
  return (
    <Link to={sourceURL(url)} className="noline">
      {children}
    </Link>
  );
};

export type SplitterProps = {
  padx?: string;
};

export const Splitter = ({padx = "0"}: SplitterProps): JSX.Element => {
  return (
    <span style={{padding: "0 " + padx}}>
      <InlineIcon icon={mdiDot} />
    </span>
  );
};
