/**
 * PlainDownloader (Signature)
 *
 * The lazy-loaded version with the property definition.
 *
 * Author: Yuchen Jin (cainmagi)
 * GitHub: https://github.com/cainmagi/dash-file-cache
 * License: MIT
 */

import React from "react";
import PropTypes, {InferProps} from "prop-types";
import {PlainDownloader as RealComponent} from "../LazyLoader";

/**
 * Default values of PlainDownloader.
 */
const defaultProps = {
  url: "",
};

/**
 * Property types of PlainDownloader.
 */
const propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks.
   */
  id: PropTypes.string,

  /**
   * The URL used to access the data to be downloaded.
   * 
   * Each time when this value is set, a download event will be triggered. After
   * triggering the download event, this value will be reset by a blank string.
   */
  url: PropTypes.string,

  /**
   * Dash-assigned callback that should be called to report property changes
   * to Dash, to make them available for callbacks.
   */
  setProps: PropTypes.func,

  /**
   * Object that holds the loading state object coming from dash-renderer
   */
  loading_state: PropTypes.shape({
    /**
     * Determines if the component is loading or not
     */
    is_loading: PropTypes.bool,
    /**
     * Holds which property is loading
     */
    prop_name: PropTypes.string,
    /**
     * Holds the name of the component that is loading
     */
    component_name: PropTypes.string,
  }),
};

export type ComponentTypes = InferProps<typeof propTypes>;

/**
 * PlainDownloader is a plain and native React component.
 *
 * This component is implemented by a temporarily created magic link referring to a
 * given URL.
 *
 * Since the implementation of this PlainDownloader is simply based on the HTML `<a>`
 * tag, the request headers and authentication of this downloader is not customizable.
 */
const PlainDownloader = (props: ComponentTypes = defaultProps): JSX.Element => {
  return (
    <React.Suspense fallback={null}>
      <RealComponent {...props} />
    </React.Suspense>
  );
};

PlainDownloader.propTypes = propTypes;
PlainDownloader.defaultProps = defaultProps;

export default PlainDownloader;
