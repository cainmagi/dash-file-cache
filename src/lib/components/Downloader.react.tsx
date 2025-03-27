/**
 * Downloader (Signature)
 *
 * The lazy-loaded version with the property definition.
 *
 * Author: Yuchen Jin (cainmagi)
 * GitHub: https://github.com/cainmagi/dash-file-cache
 * License: MIT
 */

import React from "react";
import PropTypes, {InferProps} from "prop-types";
import {Downloader as RealComponent} from "../LazyLoader";

/**
 * Default values of Downloader.
 */
const defaultProps = {
  url: "",
  allow_cross_origin: false,
};

/**
 * Property types of Downloader.
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
  url: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.exact({
      /**
       * The URL used to access the data to be downloaded.
       */
      url: PropTypes.string.isRequired,

      /**
       * A maunally configured file name. If this file name is configured, it will
       * be used when the file name cannot be parsed in the headers. This configuration
       * is useful when the URL is from a cross-origin site.
       */
      file_name_fallback: PropTypes.string,
    }),
  ]),

  /**
   * The extra headers to be used when submitting the request of the downloading
   * event.
   *
   * This property may need to be configured when the downloading event needs to
   * add authentication information.
   */
  headers: PropTypes.object,

  /**
   * A flag determineing whether the cross-origin downloading link can be used.
   *
   * If the data to be downloaded is from a cross-domain site, need to configure this
   * value as `True` while the remote site needs to configure the headers
   * Access-Control-Allow-Origin
   */
  allow_cross_origin: PropTypes.bool,

  /**
   * The status code when a downloading event is finalized.
   *
   * If multiple downloading events are triggered by the same downloader, the later
   * event will overwrite the status from the former events.
   */
  status: PropTypes.exact({
    /**
     * The status code of the event. If the event is successful, this value should
     * be "success" once the downloading event is finalized.
     */
    code: PropTypes.oneOf([
      "success",
      "error-connect",
      "error-config",
      "error-io",
      "error-unknown",
    ]),

    /**
     * The HTTP code from the response. If the event is successful, this value should
     * be in the range of 200-299.
     */
    http_code: PropTypes.number,
  }),

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
 * Downloader is a React component based on StreamSaver.
 *
 * The StreamSaver.js project provides a customizable way to access and download
 * an online stream. This is the recommended downloader for practical uses. It has
 * the optimized performance for triggering multiple downloading events.
 */
const Downloader = (props: ComponentTypes = defaultProps): JSX.Element => {
  return (
    <React.Suspense fallback={null}>
      <RealComponent {...props} />
    </React.Suspense>
  );
};

Downloader.propTypes = propTypes;
Downloader.defaultProps = defaultProps;

export default Downloader;
