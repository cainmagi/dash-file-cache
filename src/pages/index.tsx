import clsx from "clsx";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import { HeadingSafe as Heading } from "../components/utils";
import Translate, { translate } from "@docusaurus/Translate";

import styles from "./index.module.scss";

import DarkButton from "@site/src/components/DarkButton";

import LogoSVG from "../../static/img/logo.svg";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          <span>
            <LogoSVG className={styles["title-logo"]} />
          </span>{" "}
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">
          <Translate
            id="index.sub-title"
            description="Sub-title text in the cover."
            values={{ subtitle: siteConfig.tagline }}
          >
            {"{subtitle}"}
          </Translate>
        </p>
        <div className={styles.buttons}>
          <DarkButton index={true} to="/docs">
            <Translate
              id="index.button.start"
              description="Text of the index button: Get started"
            >
              Getting started
            </Translate>
          </DarkButton>
          <DarkButton
            index={true}
            to="https://pypi.org/project/dash-file-cache/"
          >
            <Translate
              id="index.button.pypi"
              description="Text of the index button: PYPI Project"
            >
              PyPI Project
            </Translate>
          </DarkButton>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={translate(
        {
          id: "index.layout.title",
          description: "The title displayed in the website head.",
          message: "Hello from {title}",
        },
        { title: siteConfig.title }
      )}
      description={translate(
        {
          id: "index.layout.descr",
          description: "The description displayed in the website head.",
          message: "{descr}",
        },
        { descr: siteConfig.tagline }
      )}
    >
      <HomepageHeader />
      <main>
      </main>
    </Layout>
  );
}
