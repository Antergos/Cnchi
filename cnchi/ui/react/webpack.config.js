/*eslint-env node*/
/*eslint no-var:0*/
let path = require( 'path' ),
	fs = require( 'fs' ),
	webpack = require( 'webpack' ),
	ExtractTextPlugin = require( 'extract-text-webpack-plugin' );


let babelQuery = {
	plugins: ['react'],
	extra: {},
};


// only extract po files if we need to
if ( 'True' === process.env.CN_EXTRACT_TRANSLATIONS ) {
	babelQuery.plugins.push( 'babel-gettext-extractor' );
	babelQuery.plugins.extra = {
		gettext: {
			fileName: 'en.po',
			baseDirectory: path.join( __dirname, 'app' ),
			functionNames: {
				gettext: ['msgid'],
				ngettext: ['msgid', 'msgid_plural', 'count'],
				gettextComponentTemplate: ['msgid'],
				t: ['msgid'],
				tN: ['msgid', 'msgid_plural', 'count'],
				tct: ['msgid']
			},
		},
	};
}


const config = {
	entry: './app/bootstrap.jsx',
	output: {
		filename: 'bundle.js',
		path: './dist',
		publicPath: '/',
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				loader: 'babel-loader',
				include: path.join( __dirname, 'app' ),
				exclude: /(vendor|node_modules|dist)/,
				query: babelQuery
			},
			{
				test: /\.po$/,
				loader: 'po-catalog-loader',
				query: {
					referenceExtensions: ['.js', '.jsx'],
					domain: 'cnchi'
				}
			},
			{
				test: /\.json$/,
				loader: 'json-loader'
			},
		],
		noParse: [
			// don't parse known, pre-built javascript files (improves webpack perf)
			path.join(__dirname, 'node_modules', 'jquery', 'dist', 'jquery.js'),
			path.join(__dirname, 'node_modules', 'jed', 'jed.js'),
			path.join(__dirname, 'node_modules', 'marked', 'lib', 'marked.js')
		],
	},
};


module.exports = config;