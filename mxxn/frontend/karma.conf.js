const {nodeResolve} = require('@rollup/plugin-node-resolve');
const typescript = require('@rollup/plugin-typescript');


module.exports = function(config) {
  config.set({
    basePath: __dirname,

    frameworks: ['jasmine'],

    files: [
      {
        pattern: 'tests/**/*.test.ts',
        watched: false,
        type: 'js'
      }
    ],

    exclude: [
    ],

    preprocessors: {
      '**/*.ts': ['rollup']
    },

    rollupPreprocessor: {
        plugins: [
          nodeResolve(),
          typescript()
        ],
        output: {
            dir: 'tests/build',
            format: 'iife',
        },
    },

    reporters: ['progress'],

    port: 8888,

    colors: true,

    logLevel: config.LOG_ERROR,

    autoWatch: true,

    browsers: ['ChromeHeadless'],

    singleRun: false,

    concurrency: Infinity
  })
}
