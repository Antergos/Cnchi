module.exports = function(grunt) {

	grunt.initConfig({
		concat: {
			options: {
				separator: '\n\n',
				sourceMap: true
			},
			default: {
				files: {
					'pages/app/dist/bundle.js': [
						'pages/resources/js/jquery-3.1.0.min.js',
						'pages/resources/js/jquery-migrate-3.0.0.js',
						'pages/resources/js/jquery.waypoints.min.js',
						'pages/resources/js/jquery.waypoints.inview.min.js',
						'pages/resources/js/materialize.min.js',
						'pages/resources/js/moment-timezone-meta.js',
						'pages/resources/js/moment-with-locales.min.js',
						'pages/resources/js/moment-timezone-with-data-2010-2020.min.js',
						'pages/app/utils.js',
						'pages/app/logger.js',
						'pages/app/object.js',
						'pages/app/app.js',
						'pages/app/tab.js',
						'pages/app/page.js'
					],
					'pages/app/dist/all_styles.css': [
						'pages/resources/css/vendor/*.css',
						'pages/resources/css/style.css'
					],
				},
			},
		},
	});

	grunt.loadNpmTasks('grunt-contrib-concat');

	grunt.registerTask('default', ['concat']);
};