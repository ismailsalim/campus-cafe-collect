const merge = require('webpack-merge');
const common = require('./webpack.common.js');


module.exports = merge(common, {
   mode: 'development',
   devtool: 'sourcemap',
   devServer: {
     contentBase: './dist',
     historyApiFallback: true
   },
 });
