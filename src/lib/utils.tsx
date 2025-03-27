/**
 * Utilities
 *
 * Shared utilities used by different components.
 *
 * Author: Yuchen Jin (cainmagi)
 * GitHub: https://github.com/cainmagi/dash-file-cache
 * License: MIT
 */

import normalizeHeaderCase from "header-case-normalizer";
import {type, is, isEmpty} from "ramda";

/**
 * Wait until the property of an object is available.
 * @param {object} obj - The object containing the property.
 * @param {object} prop - The name of the property to be accessed.
 * @param {object} interval - The waiting interval. The unit is ms.
 * @returns {Promise<any>} A promise returning the property of `obj`.
 */
export const waitForProperty = (
  obj: object,
  prop: string,
  interval: number = 100
) => {
  return new Promise(
    (resolve: (value: any) => any, reject: (error: Error) => void) => {
      const checkProperty = () => {
        if (obj[prop] !== undefined) {
          resolve(obj[prop]);
        } else {
          setTimeout(checkProperty, interval);
        }
      };
      checkProperty();
    }
  );
};

/**
 * Convert a value to string. Different from `JSON.stringify`, this method only
 * performs the conversion at the first level.
 * @param {any} val - The value to be converted.
 * @returns {string} The converted value.
 */
export const toString = (val: any): string => {
  if (type(val) === "Object") {
    return JSON.stringify(
      Object.fromEntries(
        Object.entries(val).map(([key, val]) => [`${key}`, `${val}`])
      )
    );
  }
  if (type(val) === "Array") {
    return JSON.stringify(val.map((ele) => `${ele}`));
  }
  return `${val}`;
};

/**
 * Convert a value to array. If it is an array, return it. Otherwise, return an
 * array with only one element.
 * @param {T | Array[T]} val - The value to be converted.
 * @returns {Array[T]} The converted value.
 */
export const toArray = <T extends {}>(val: T | Array<T>): Array<T> => {
  if (is(Array, val)) {
    return val;
  }
  return [val];
};

/**
 * Sanitize headers
 * @param {Record<string,any>|null|undefined} headers - The headers to be sanitized.
 * @returns {Record<string,string>|undefined} The normalized headers. Will return `undefined` if the
 * given headers are invalid.
 */
export const sanitizeHeaders = (
  headers: Record<string, any> | undefined | null
): Record<string, string> | undefined => {
  if (!is(Object, headers) || isEmpty(headers)) {
    return undefined;
  }

  return Object.fromEntries(
    Object.entries(headers).map(([key, val]) => [
      normalizeHeaderCase(
        key
          .replace(/[_\s]/g, "-")
          .replace(/(?<=[a-z])([A-Z])/g, "-$1")
          .replace(/-{2,}/g, "-")
      ),
      toString(val),
    ])
  );
};

/**
 * Parse the file name from an URL.
 * @param {string} url - The URL containing the file name.
 * @returns {string} The parsed file name. If the parsing fails, return "Unknown".
 */
export const fileNameFromURL = (url: string): string => {
  const pathname = URL.parse(url).pathname;
  const res = pathname.substring(pathname.lastIndexOf("/") + 1);
  return isEmpty(res) ? "Unknown" : res;
};
