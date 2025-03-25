import React from "react";

export const PlainDownloader = React.lazy(() =>
  import(
    /* webpackChunkName: "PlainDownloader" */ "./fragments/PlainDownloader.react"
  )
);
