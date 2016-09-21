const path = require( 'path' );
const fs = require( 'fs' );
const webpack = require( 'webpack' );
const HtmlWebpackPlugin = require( 'html-webpack-plugin' );
const loaders = require( './webpack.loaders' );
const ExtractTextPlugin = require( 'extract-text-webpack-plugin' );
const LiveReloadPlugin = require( 'webpack-livereload-plugin' );


// Now create config for webpack
const config = {
	devtool: 'source-map',
	entry: './app/bootstrap.jsx',
	output: {
		filename: "bundle.js",
		path: path.join( __dirname, "dist" ),
	},
	externals: ['cnchi', 'Materialize'],
	module: {
		loaders: loaders,
	},
	resolve: {
		alias: {
			jquery: 'jquery/src/jquery',
		},
		extensions: ['.js', '.jsx']
	},
	plugins: [
		new webpack.DefinePlugin( {
			'process.env': {
				NODE_ENV: JSON.stringify( 'development' ),
			},
		} ),
		new LiveReloadPlugin(),
		new webpack.NoErrorsPlugin(),
		new webpack.ProvidePlugin( {
			$: 'jquery',
			jQuery: 'jquery',
			_: 'underscore',
		} ),
		new HtmlWebpackPlugin( {
			template: './app/index.html'
		} ),
		new ExtractTextPlugin( '[name].css' ),
		new ExtractTextPlugin( '[name]__[local]___[hash:base64:5]' ),
	]
};


module.exports = config;