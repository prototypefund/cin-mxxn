import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs'
import typescript from '@rollup/plugin-typescript';

export default {
  input: 'src/index.ts',
  output: {
    file: 'static/js/mxxn.js',
    format: 'esm'
  },
  plugins: [
    nodeResolve(),
    commonjs(),
    typescript()
  ]
};
