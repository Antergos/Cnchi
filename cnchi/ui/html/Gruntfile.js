module.exports = function(grunt) {

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		rollup: {
			options: {
				entry: 'pages/resources/js/cnchi_app.js',
				globals: {
					jQuery: '$'
				},
				plugins: [
					nodeResolve({
						jsnext: true,
						browser: true
					})
				]
			},
			files: {
				'pages/resources/dist/js/bundle.js': ['pages/resources/js/cnchi_app.js'], // Only one source file is permitted
			},
		},
		uglify: {
			options: {
				banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
			},
			dist: {
				files: {
					'dist/bundle.min.js': ['pages/resources/dist/js/bundle.js']
				}
			}
		},
		jshint: {
			files: ['Gruntfile.js', 'pages/resources/js/*.js'],
			options: {
				// options here to override JSHint defaults
				globals: {
					jQuery: true,
					console: true,
					module: true,
					document: true
				}
			}
		},
		watch: {
			files: ['<%= jshint.files %>'],
			tasks: ['jshint']
		}
	});

	//grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-jshint');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-rollup');

	grunt.registerTask('test', ['jshint']);

	grunt.registerTask('default', ['rollup']);

};