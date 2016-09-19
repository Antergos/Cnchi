const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const loaders = require('./webpack.loaders');
const ExtractTextPlugin = require('extract-text-webpack-plugin');


// Now create config for webpack
const config = {
	entry: './app/bootstrap.jsx',
	output: {
		filename: "bundle.js",
		path: path.join(__dirname, "dist"),
	},
	module: {
		loaders: loaders,
		noParse: [/\.min\.js$/]
	},
	resolve: { extensions: ['', '.js', '.jsx'] },
	plugins: [
		new webpack.NoErrorsPlugin(),
		//new webpack.HotModuleReplacementPlugin(),
		new webpack.ProvidePlugin({
			$: 'jquery',
			jQuery: 'jquery',
			'window.jQuery': 'jquery',
			'root.jQuery': 'jquery',
		}),
		new HtmlWebpackPlugin({
			template: './app/index.html'
		}),
		new ExtractTextPlugin('[name].css'),
	]
};


module.exports = config;