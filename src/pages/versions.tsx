/**
 * Modified from Docusaurus official versions.js
 * Copyright (c) Yuchen Jin and its affiliates.
 * Original author: Facebook, Inc. and its affiliates.
 */

import React from "react";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Link from "@docusaurus/Link";
import Layout from "@theme/Layout";

import InlineIcon from "@site/src/components/InlineIcon";
import mdiFileDocumentMultipleOutline from "@iconify-icons/mdi/file-document-multiple-outline";
import octTag16 from "@iconify-icons/octicon/tag-16";

// import { useVersions, useLatestVersion } from '@theme/hooks/useDocs';
/* Refactor:
The original useVersions / useLatestVersion have been moved to the plugin
https://github.com/facebook/docusaurus/pull/6287
*/
import {
  useVersions,
  useLatestVersion,
} from "@docusaurus/plugin-content-docs/client";

import Translate from "@docusaurus/Translate";

import {DependencyTag, releaseURL} from "../envs/variables";

const docsPluginId = undefined; // Default docs plugin instance

function Version() {
  const {siteConfig} = useDocusaurusContext();
  const versions = useVersions(docsPluginId);
  const latestVersion = useLatestVersion(docsPluginId);
  const currentVersion = versions.find(
    (version) => version.name === "current"
  )!;
  const pastVersions = versions.filter(
    (version) => version !== latestVersion && version.name !== "current"
  );

  return (
    <Layout
      title="Versions"
      description="Versions page listing all documented site versions."
    >
      <main className="container margin-vert--lg">
        <h1>
          <Translate
            id="versions.title"
            description="Title text in the version page."
            values={{title: <code>{siteConfig.title}</code>}}
          >
            {"{title} documentation versions"}
          </Translate>
        </h1>

        {latestVersion && (
          <div className="margin-bottom--lg">
            <h3 id="next">
              <Translate
                id="versions.current.head"
                description="Head of the current version."
              >
                {`Current version (Stable)`}
              </Translate>
            </h3>
            <p>
              <Translate
                id="versions.current.descr"
                description="Description of the current version."
              >
                Here you can find the documentation for current released
                version.
              </Translate>
            </p>
            <table>
              <thead>
                <tr>
                  <th>
                    <Translate
                      id="versions.table.version"
                      description="Table item: version."
                    >
                      Version
                    </Translate>
                  </th>
                  <th>
                    <Translate
                      id="versions.table.docs"
                      description="Table item: documentation."
                    >
                      Documentation
                    </Translate>
                  </th>
                  <th>
                    <Translate
                      id="versions.table.rel"
                      description="Table item: release number."
                    >
                      Release
                    </Translate>
                  </th>
                  <th>
                    <Translate
                      id="versions.table.dep"
                      description="Table item: dependency number."
                    >
                      Core dependency
                    </Translate>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>{latestVersion.label}</th>
                  <td align="center">
                    <Link to={latestVersion.path}>
                      <InlineIcon icon={mdiFileDocumentMultipleOutline} />
                    </Link>
                  </td>
                  <td align="center">
                    <Link href={releaseURL(latestVersion.label || "main")}>
                      <InlineIcon icon={octTag16} />
                    </Link>
                  </td>
                  <td align="center">
                    <DependencyTag ver={latestVersion.label} />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

        {pastVersions.length > 0 && (
          <div className="margin-bottom--lg">
            <h3 id="archive">
              <Translate
                id="versions.prev.head"
                description="Head of the previous version."
              >
                Past versions (Not maintained anymore)
              </Translate>
            </h3>
            <p>
              <Translate
                id="versions.prev.descr"
                description="Description of the previous version."
                values={{title: <code>{siteConfig.title}</code>}}
              >
                {
                  "Here you can find documentation for previous versions of {title}."
                }
              </Translate>
            </p>
            <table>
              <thead>
                <tr>
                  <th>
                    <Translate
                      id="versions.table.version"
                      description="Table item: version."
                    >
                      Version
                    </Translate>
                  </th>
                  <th>
                    <Translate
                      id="versions.table.docs"
                      description="Table item: version."
                    >
                      Documentation
                    </Translate>
                  </th>
                  <th>
                    <Translate
                      id="versions.table.rel"
                      description="Table item: release number."
                    >
                      Release
                    </Translate>
                  </th>
                  <th>
                    <Translate
                      id="versions.table.dep"
                      description="Table item: dependency number."
                    >
                      Core dependency
                    </Translate>
                  </th>
                </tr>
              </thead>
              <tbody>
                {pastVersions.map((version) => (
                  <tr key={version.name}>
                    <th>{version.label}</th>
                    <td align="center">
                      <Link to={version.path}>
                        <InlineIcon icon={mdiFileDocumentMultipleOutline} />
                      </Link>
                    </td>
                    <td align="center">
                      <Link href={releaseURL(version.label || "main")}>
                        <InlineIcon icon={octTag16} />
                      </Link>
                    </td>
                    <td align="center">
                      <DependencyTag ver={version.label} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {currentVersion !== latestVersion && (
          <div className="margin-bottom--lg">
            <h3 id="latest">
              <Translate
                id="versions.next.head"
                description="Head of the next version."
              >
                Next version (Unreleased)
              </Translate>
            </h3>
            <p>
              <Translate
                id="versions.next.descr"
                description="Description of the next version."
              >
                Here you can find the documentation for work-in-process
                unreleased version.
              </Translate>
            </p>
            <table>
              <thead>
                <tr>
                  <th>
                    <Translate
                      id="versions.table.version"
                      description="Table item: version."
                    >
                      Version
                    </Translate>
                  </th>
                  <th>
                    <Translate
                      id="versions.table.docs"
                      description="Table item: version."
                    >
                      Documentation
                    </Translate>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>{currentVersion.label}</th>
                  <td align="center">
                    <Link to={currentVersion.path}>
                      <InlineIcon icon={mdiFileDocumentMultipleOutline} />
                    </Link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        )}
      </main>
    </Layout>
  );
}

export default Version;
