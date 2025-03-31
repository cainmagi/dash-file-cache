/**
 * Downloader (Implementation)
 *
 * The implementation of the real component.
 *
 * Author: Yuchen Jin (cainmagi)
 * GitHub: https://github.com/cainmagi/dash-file-cache
 * License: MIT
 */

import React, {useEffect} from "react";
import {type, is, isEmpty} from "ramda";
import streamSaver from "streamsaver";
import {WritableStream} from "web-streams-polyfill";

import LazyComponent, {ComponentTypes} from "../components/Downloader.react";

import {sanitizeHeaders, fileNameFromURL} from "../utils";

const downloadFile = (
  url: {url: string; file_name_fallback?: string},
  headers: Record<string, string> | undefined = undefined,
  allow_cross_origin: boolean = false,
  mitm: string | undefined = undefined
) => {
  let _headers = {Accept: "application/octet-stream"};
  if (headers) {
    _headers = Object.assign(_headers, headers);
  }
  return new Promise(
    (
      resolve: (value: {code: number; name: string}) => void,
      reject: (error: {code: number; text: string; exc: Error}) => void
    ) => {
      fetch(url.url, {
        method: "GET",
        headers: _headers,
        mode: allow_cross_origin ? "cors" : "same-origin",
      })
        .then((resp) => {
          if (!(resp.ok || resp.redirected)) {
            try {
              throw new Error(
                `Connection fails. The status code is ${resp.status}`
              );
            } catch (error) {
              reject({code: resp.status, text: "error-connect", exc: error});
              return;
            }
          }

          const contentDisposition = resp.headers.get("Content-Disposition");
          const fileNameContentDisp = contentDisposition
            ? contentDisposition.split("filename=")[1]
            : undefined;
          const fileName =
            is(String, fileNameContentDisp) && !isEmpty(fileNameContentDisp)
              ? fileNameContentDisp
              : url.file_name_fallback || fileNameFromURL(url.url);

          // Fix the writable stream.
          if (!streamSaver.WritableStream) {
            streamSaver.WritableStream = WritableStream;
          }
          if (!window.WritableStream) {
            window.WritableStream = streamSaver.WritableStream;
          }

          if (typeof mitm === "string" && !isEmpty(mitm)) {
            streamSaver.mitm = `${mitm}/mitm`;
          }

          const fileSize = resp.headers.get("Content-Length");
          const fileStream = streamSaver.createWriteStream(fileName, {
            size: fileSize ? parseInt(fileSize) || undefined : undefined,
          });
          const readableStream = resp.body;
          if (!readableStream) {
            try {
              throw new TypeError(
                `Fail to get readable stream. The status code is ${resp.status}`
              );
            } catch (error) {
              reject({code: resp.status, text: "error-config", exc: error});
              return;
            }
          }

          // Optimized for pipe
          if (streamSaver.WritableStream && readableStream.pipeTo) {
            return readableStream
              .pipeTo(fileStream)
              .then(() => resolve({code: resp.status, name: fileName}))
              .catch((error) =>
                reject({code: resp.status, text: "error-io", exc: error})
              );
          }

          const writer = fileStream.getWriter();
          window.writer = writer;
          const reader = readableStream.getReader();

          const pump = () => {
            reader
              .read()
              .then((res) =>
                res.done ? writer.close() : writer.write(res.value).then(pump)
              )
              .catch((error) =>
                reject({code: resp.status, text: "error-io", exc: error})
              );
          };

          pump();
          resolve({code: resp.status, name: fileName});
        })
        .catch((error) => {
          reject({code: 400, text: "error-unknown", exc: error});
        });
    }
  );
};

/**
 * Sanitize an input URL
 * @param {string | {url: string, file_name_fallback?: string}} url - The input URL.
 *   It can contain an optional fallback file name.
 * @returns {{url: string, file_name_fallback?: string}} The sanitized URL. It will
 *   be always an object or undefined.
 */
const santizeURL = (
  url: string | undefined | {url: string; file_name_fallback?: string}
): {url: string; file_name_fallback?: string} | undefined => {
  if (!url) {
    return undefined;
  }
  if (typeof url === "string") {
    if (isEmpty(url)) {
      return undefined;
    }
    return {url: url};
  }
  const _url = url.url;
  if (!_url) {
    return undefined;
  }
  const _file_name = url.file_name_fallback;
  if (_file_name && !isEmpty(_file_name)) {
    return {url: _url, file_name_fallback: _file_name};
  } else {
    return {url: _url};
  }
};

/**
 * Downloader is a React component based on StreamSaver.
 *
 * The StreamSaver.js project provides a customizable way to access and download
 * an online stream.
 *
 * This is the recommended downloader for practical uses. It has an optional children
 * argument. Any direct children supporting the property `value` will be specified
 * as the progress of downloading.
 */
const Downloader = (props: ComponentTypes) => {
  const {id, url, headers, allow_cross_origin, mitm, setProps, loading_state} =
    props;

  const sanitizedHeaders = sanitizeHeaders(headers);

  useEffect(() => {
    const sanitizedURL = santizeURL(url);

    if (type(sanitizedURL) != "Undefined") {
      downloadFile(sanitizedURL, sanitizedHeaders, allow_cross_origin, mitm)
        .then((value) => {
          console.log(`Download: ${value.name}`);
          setProps({url: "", status: {code: "success", http_code: value.code}});
        })
        .catch((error) => {
          console.error("Error:", error);
          setProps({
            url: "",
            status: {
              code: error.text || "error-unknown",
              http_code: error.code || 400,
            },
          });
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
    ></div>
  );
};

Downloader.defaultProps = LazyComponent.defaultProps;
Downloader.propTypes = LazyComponent.propTypes;

export default Downloader;
