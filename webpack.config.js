const path = require("path");
const webpack = require("webpack");
const WebpackDashDynamicImport = require("@plotly/webpack-dash-dynamic-import");
const packagejson = require("./package.json");

const dashLibraryName = packagejson.name.replace(/-/g, "_");

const tempLibraryName = `${dashLibraryName}_components`;

module.exports = (env, argv) => {
  let mode;

  const overrides = module.exports || {};

  // if user specified mode flag take that value
  if (argv && argv.mode) {
    mode = argv.mode;
  }

  // else if configuration object is already set (module.exports) use that value
  else if (overrides.mode) {
    mode = overrides.mode;
  }

  // else take webpack default (production)
  else {
    mode = "production";
  }

  let filename = (overrides.output || {}).filename;
  if (!filename) {
    const modeSuffix = mode === "development" ? "dev" : "min";
    filename = `${dashLibraryName}.${modeSuffix}.js`;
  }

  const entry = overrides.entry || {main: "./src/lib/index.tsx"};

  const devtool = overrides.devtool || "source-map";

  const externals =
    "externals" in overrides
      ? overrides.externals
      : {
          react: "React",
          "react-dom": "ReactDOM",
          "plotly.js": "Plotly",
          "prop-types": "PropTypes",
        };

  return {
    mode,
    entry,
    output: {
      path: path.resolve(__dirname, tempLibraryName),
      chunkFilename: "[name].js",
      filename,
      library: dashLibraryName,
      libraryTarget: "window",
    },
    devtool,
    devServer: {
      static: {
        directory: path.join(__dirname, "/"),
      },
    },
    externals,
    resolve: {
      // Add `.ts` and `.tsx` as a resolvable extension.
      extensions: [".ts", ".tsx", ".js", ".jsx", ".json"],
      // Add support for TypeScripts fully qualified ESM imports.
      extensionAlias: {
        ".js": [".js", ".ts"],
        ".cjs": [".cjs", ".cts"],
        ".mjs": [".mjs", ".mts"],
      },
    },
    module: {
      rules: [
        {
          test: /\.([cm]?ts|tsx)$/,
          use: "ts-loader",
          exclude: /node_modules/,
        },
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
          },
        },
        {
          test: /\.css$/,
          use: [
            {
              loader: "style-loader",
            },
            {
              loader: "css-loader",
              options: {
                modules: {
                  localIdentHashSalt: "dash-file-cache",
                  localIdentName: "dfc-[local]__[hash:base64:8]",
                },
              },
            },
          ],
        },
        {
          test: /\.s[ac]ss$/i,
          use: [
            {
              loader: "style-loader",
            },
            {
              loader: "css-loader",
              options: {
                modules: {
                  localIdentHashSalt: "dash-file-cache",
                  localIdentName: "dfc-[local]__[hash:base64:8]",
                },
              },
            },
            // Compiles Sass to CSS
            {
              loader: "sass-loader",
            },
          ],
        },
      ],
    },
    optimization: {
      splitChunks: {
        name: "[name].js",
        cacheGroups: {
          async: {
            chunks: "async",
            minSize: 0,
            name(module, chunks, cacheGroupKey) {
              return `${cacheGroupKey}-${chunks[0].name}`;
            },
          },
          shared: {
            chunks: "all",
            minSize: 0,
            minChunks: 2,
            name: "dash_file_cache-shared",
          },
        },
      },
    },
    plugins: [
      new WebpackDashDynamicImport(),
      new webpack.SourceMapDevToolPlugin({
        filename: "[file].map",
        exclude: ["async-plotlyjs"],
      }),
    ],
  };
};
