import {themes as prismThemes} from "prism-react-renderer";
import type {Config} from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

// import remarkMath from "remark-math";
// import rehypeKatex from 'rehype-katex';

const config: Config = {
  title: "Dash File Cache",
  tagline:
    "Utilities for providing convenient methods to serve cached data in Plotly-Dash or Flask.",
  favicon: "img/favicon.ico",

  // Set the production url of your site here
  url: "https://cainmagi.github.io/",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/dash-file-cache/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "cainmagi", // Usually your GitHub org/user name.
  projectName: "dash-file-cache", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  trailingSlash: false,

  // Use mermaid. (not working on 3.5.2)
  // themes: ["@docusaurus/theme-mermaid"],
  // markdown: {
  //   format: "detect",
  //   mermaid: true,
  // },

  plugins: [
    [
      // Use SASS/SCSS.
      "docusaurus-plugin-sass",
      {
        // options
        // api: "modern-compiler",
      },
    ],
  ],

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en", "zh-cn"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          // remarkPlugins: [remarkMath],
          // rehypePlugins: [rehypeKatex],
          sidebarPath: "./sidebars.ts",
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/cainmagi/dash-file-cache/edit/docs/",
          editLocalizedFiles: true,
        },
        theme: {
          customCss: "./src/css/custom.scss",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: "img/social-card.webp",
    navbar: {
      title: "DashFileCache",
      logo: {
        alt: "Dash File Cache",
        src: "img/logo.svg",
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorial",
          position: "left",
          label: "Tutorial",
        },
        {
          type: "docSidebar",
          sidebarId: "apis",
          position: "left",
          label: "APIs",
        },
        {
          type: "localeDropdown",
          position: "right",
        },
        {
          href: "https://github.com/cainmagi/dash-file-cache",
          position: "right",
          className: "header-github-link",
          "aria-label": "GitHub repository",
        },
        {
          href: "https://pypi.org/project/dash-file-cache",
          position: "right",
          className: "header-pypi-link",
          "aria-label": "PyPI repository",
        },
      ],
      hideOnScroll: false,
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            {
              label: "Tutorial",
              to: "/docs/",
            },
            {
              label: "APIs",
              to: "/docs/apis/",
            },
          ],
        },
        {
          title: "Contact the author",
          items: [
            {
              label: "Website",
              href: "https://cainmagi.github.io/",
            },
            {
              label: "Email",
              href: "mailto:cainmagi@gmail.com",
            },
            {
              label: "GitHub",
              href: "https://github.com/cainmagi",
            },
          ],
        },
        {
          title: "Community",
          items: [
            {
              label: "GitHub of Aramco AIT",
              href: "https://github.com/aschrc-ait-team",
            },
            {
              label: "UH MODAL Lab",
              href: "https://modal.ece.uh.edu/",
            },
            {
              label: "University of Houston",
              href: "https://www.uh.edu/",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Dash File Cache, Yuchen Jin. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.vsDark,
      additionalLanguages: ["bash", "python"],
      magicComments: [
        // Remember to extend the default highlight class name as well!
        {
          className: "theme-code-block-highlighted-line",
          line: "highlight-next-line",
          block: {start: "highlight-start", end: "highlight-end"},
        },
        {
          className: "code-block-error-line",
          line: "This will error",
        },
      ],
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
