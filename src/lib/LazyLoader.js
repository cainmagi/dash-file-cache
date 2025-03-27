import React from "react";

export const PlainDownloader = React.lazy(() =>
  import(
    /* webpackChunkName: "PlainDownloader" */ "./fragments/PlainDownloader.react"
  )
);

export const Downloader = React.lazy(() =>
  import(/* webpackChunkName: "Downloader" */ "./fragments/Downloader.react")
);
