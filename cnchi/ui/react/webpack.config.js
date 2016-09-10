module.exports = {
	entry: './app/bootstrap.jsx',
	output: {
		filename: 'bundle.js',
		path: './dist',
		publicPath: '/',
	},
	module: {
		loaders:[
			{
				test: /\.jsx?$/,
				exclude: /node_modules/,
				loader: 'babel',
				query: {
					presets: ['react']
				}
			},
			{
				test: /\.json$/,
				exclude: /node_modules/,
				loader: 'json',
			},
		],
	},
};