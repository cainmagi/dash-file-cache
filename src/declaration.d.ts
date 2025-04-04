declare module "*.css" {
  const content: {[className: string]: string};
  export default content;
}

declare module '*.scss' {
  const content: Record<string, string>;
  export default content;
}

interface Window {
  writer: any;
}
