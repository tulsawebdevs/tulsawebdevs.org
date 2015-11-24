// Production build configuration
var path = require('path');

var root = __dirname;
var project_root = path.resolve(root, '../../');
var output_path = path.resolve(root, '../static/bundles/');
var js_dir = path.resolve('js');
var css_dir = path.resolve('css');

// Webpack
var webpack = require('webpack');
// plugins
var CleanPlugin = require('clean-webpack-plugin');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

// debug
// console.log(output_path, js_dir, css_dir);

module.exports = {
  cache: true,
  context: __dirname,
  entry: './js/bootstrap.js',
  output: {
    path: output_path,
    filename: '[name].js',
    chunkFilename: '[id].js'
  },
  module: {
    preLoaders: [
      {
        test: /\.js$/,
        loader: 'eslint',
        include: js_dir
      }
    ],
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel',
        // include: /js/,
        exclude: /node_modules/,
        query: {
          // presets: ['react', 'es2015'],
          plugins: ['transform-runtime']
        }
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader'),
        include: css_dir
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader?sourceMap', 'sass-loader?sourceMap')
      },
      // SASS Currently not working :(
      {
        test: /\.sass$/,
        // Passing indentedSyntax query param to node-sass
        loader: ExtractTextPlugin.extract("style-loader', 'css-loader?sourceMap', 'sass-loader?indentedSyntax")
      }
    ]
  },
  eslint: {
    configFile: '.eslintrc',
    emitError: true,
    emitWarning: true,
    failOnWarning: true,
    failOnError: true
  },
  resolve: {
    root: root,
    modulesDirectories: [path.resolve(project_root, './node_modules')]
  },
  plugins: [
    new CleanPlugin(['../static/bundles']),
    new webpack.optimize.OccurenceOrderPlugin(true), // preferEntry true
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({ output: {comments: false} }),
    // new webpack.optimize.CommonsChunkPlugin("commons.chunk-[hash].js"),
    new ExtractTextPlugin('[name].css', {allChunks: true}),
    new BundleTracker({path: __dirname, filename: 'webpack.stats.json'})
  ]
}
