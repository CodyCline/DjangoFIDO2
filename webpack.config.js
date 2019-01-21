const path = require("path");
const autoprefixer = require('autoprefixer');
const BundleTracker  = require('webpack-bundle-tracker');
const ExtractText = require('extract-text-webpack-plugin');

module.exports = {
  entry: ['./static/src/layout.scss', './static/src/app.js'],
  output: {
    path: path.join(__dirname, './static/dist/'),
    filename: "[name]-[hash].js",
  },
  plugins: [
    new BundleTracker({
      path: __dirname, 
      filename: './webpack-stats.json'
    })
  ],
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: 'main.css',
            },
          },
          {loader: 'extract-loader'},
          {loader: 'css-loader'},
          {loader: 'postcss-loader',
            options: {
              plugins: () => [autoprefixer()],
            },
          },
          {
            loader: 'sass-loader',
            options: {
              includePaths: ['./node_modules'],
            },
          }
        ],
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015'],
          plugins: ['transform-object-assign']
        },
      }
    ],
  },
};