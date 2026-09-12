/// <reference types="vitest" />
/// <reference types="@testing-library/jest-dom" />

declare module 'vitest' {
  interface Assertion<T = any> {
    toBeInTheDocument(): T
    toHaveAttribute(name: string, value?: string | RegExp): T
    toHaveClass(className: string | string[]): T
    toHaveStyle(css: string | Record<string, any>): T
    toHaveTextContent(text: string | RegExp): T
  }
  interface AsymmetricMatchersContaining {
    toBeInTheDocument(): any
    toHaveAttribute(name: string, value?: string | RegExp): any
    toHaveClass(className: string | string[]): any
    toHaveStyle(css: string | Record<string, any>): any
    toHaveTextContent(text: string | RegExp): any
  }
}

export {}

