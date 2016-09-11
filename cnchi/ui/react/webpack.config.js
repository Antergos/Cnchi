/*eslint-env node*/
/*eslint no-var:0*/
let path = require( 'path' ),
	fs = require( 'fs' ),
	webpack = require( 'webpack' ),
	fs_utils = require( './utils/filesystem.js'),
	page_dirs = fs_utils.dirlist( path.join( __dirname, 'app', 'pages' ) );
	entry = {};


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


// Determine entry points (pages) and add them to the entry object.
if ( page_dirs.length ) {
	page_dirs.forEach( (page_dir) => {
		let page = page_dir.split('-').pop();
		entry[ page_dir ] = path.join( __dirname, 'app', 'pages', page_dir, `${page}Page` );
	} );
}


// Now create config for webpack
const config = {
	entry: entry,
	output: {
		chunkFilename: "[id].chunk.js",
		filename: "[name].bundle.js",
		path: path.join(__dirname, "dist"),
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				loader: 'babel',
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
		resolve: { extensions: ['', '.js', '.jsx'] }
	},
};


module.exports = config;