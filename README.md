# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

### Installation

The dependencies are maintained by `yarn>=4`. Therefore, please do not use `npm` to install packages or run commands.

The following commands show steps for preparing the dependencies with VSCode. Please run the following commands,

```sh
yarn install
yarn dlx @yarnpkg/sdks vscode
```

Remember to do the following steps:

1. Install the VSCode extensions recommended by the workspace;
2. Open the command menu by <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>
3. Search `Select TypeScript Version`, and select the workspace version.
4. If the typescript still does not work properly, try to search and select the `TypeScript: Reload Project` command by using <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>.

### Local Development

Run the following command to check whether there are any typescript errors:

```sh
yarn tsc
```

Run the following command to check all `.mdx` files.

```sh
npx docusaurus-mdx-checker
```

Run the following command to start a local development server.

```sh
yarn start
```

This command will automatically open up a browser window. Most changes are reflected live without having to restart the server.

### Build

```sh
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

> [!CAUTION]
> Users do not and should not use the following commands to deploy the project.
>
> The correct way to deploy the project is simply commit and push the changes, the deployment is delegated to the GitHub workflow.

Using SSH:

```sh
USE_SSH=true yarn deploy
```

Not using SSH:

```sh
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
