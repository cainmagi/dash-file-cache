/**
 * PlainDownloader (Implementation)
 *
 * The implementation of the real component.
 *
 * Author: Yuchen Jin (cainmagi)
 * GitHub: https://github.com/cainmagi/dash-file-cache
 * License: MIT
 */

import React, {useRef, useEffect} from "react";
import {type, isEmpty} from "ramda";

import LazyComponent, {
  ComponentTypes,
} from "../components/PlainDownloader.react";

import {waitForProperty} from "../utils";

/**
 * PlainDownloader is a plain and native React component.
 *
 * This component is implemented by a temporarily created magic link referring to a
 * given URL.
 *
 * Since the implementation of this PlainDownloader is simply based on the HTML `<a>`
 * tag, the request headers and authentication of this downloader is not customizable.
 */
const PlainDownloader = (props: ComponentTypes) => {
  const {id, url, setProps, loading_state} = props;

  const ref = useRef();

  useEffect(() => {
    if (type(url) === "String" && !isEmpty(url)) {
      waitForProperty(ref, "current")
        .then((value) => {
          value.click();
          return Promise.resolve();
        })
        .catch((error) => {
          console.error("Error:", error);
          setProps({url: ""});
        })
        .then(() => {
          setProps({url: ""});
        })
        .catch((error) => {
          console.error("Error:", error);
          setProps({url: ""});
        });
    }
    return () => {};
  }, [url]);

  return (
    <div
      id={id}
      data-dash-is-loading={
        (loading_state && loading_state.is_loading) || undefined
      }
    >
      {type(url) === "String" && !isEmpty(url) ? (
        <a ref={ref} href={url} download target="_blank" rel="no-refresh"></a>
      ) : (
        <></>
      )}
    </div>
  );
};

PlainDownloader.defaultProps = LazyComponent.defaultProps;
PlainDownloader.propTypes = LazyComponent.propTypes;

export default PlainDownloader;
