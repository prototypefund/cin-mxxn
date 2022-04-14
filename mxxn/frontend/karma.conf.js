const {nodeResolve} = require('@rollup/plugin-node-resolve');
const typescript = require('rollup-plugin-typescript2');
const riot = require('rollup-plugin-riot');


module.exports = function(config) {
  config.set({
    basePath: __dirname,

    frameworks: ['jasmine'],

    files: [
      {
        pattern: 'tests/**/*.test.ts',
        watched: false,
        type: 'js'
      },
      {
        pattern: 'src/index.ts',
        watched: false ,
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
          riot(),
          typescript({
			include: [
				'src/**/*.ts',
				'src/**/*.riot',
                'tests/**/*.ts',
			]
          })
        ],
        output: {
            dir: 'tests/build',
            format: 'iife',
            name: 'mxxn'
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
