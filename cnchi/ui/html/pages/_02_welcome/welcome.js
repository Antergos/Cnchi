/*
 * welcome.js
 *
 * Copyright 2016 Antergos
 *
 * This file is part of Cnchi.
 *
 * Cnchi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Cnchi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * The following additional terms are in effect as per Section 7 of the license:
 *
 * The preservation of all legal notices and author attributions in
 * the material or in the Appropriate Legal Notices displayed
 * by works containing it is required.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


class WelcomePage extends CnchiPage {

	constructor( id ) {
		if ( null !== window._page ) {
			return window._page;
		}

		super( id );

		window._page = this;
		this.signals = JSON.parse('{{ signals }}');
		this.$update_wrapper = $('.update_check_wrapper');
		this.$welcome_wrapper = $('.welcome_wrapper');
		this.$connection_wrapper = $('.no_internet_wrapper');
		this.has_connection = false;

		this.register_allowed_signals();
		// this.maybe_skip_to_next_page();
		this.register_event_handlers();
		this.initialize();
	}

	connection_check_result_cb( event, result ) {
		_page.has_connection = result;

		if ( false === result ) {
			_page.$connection_wrapper.fadeIn();
		}
	}

	do_has_connection_check() {
		if ( false === this.has_connection ) {
			cnchi.emit_signal('do-connection-check');
		}
	}

	do_update_check() {
		if ( false === this.has_connection ) {
			this.logger('An internet connection is required in order to check for installer update.');
			return;
		}

		if ( this.$connection_wrapper.is(':visible') ) {
			this.$connection_wrapper.fadeOut()
			.promise()
			.done(_show_update_wrapper);
		} else {
			_show_update_wrapper();
		}

		function _show_update_wrapper() {
			_page.$update_wrapper.fadeIn()
			.promise()
			.done(() => {
				cnchi.emit_signal('do-update-check');
			});
		}
	}

	initialize() {
		this.$welcome_wrapper.animateCss('magictime swashIn', () => {
			_page.$welcome_wrapper.addClass('showme');
		});
	}

	install_it_button_clicked_cb( event ) {
		console.log('clicked!');
		_page.$welcome_wrapper.animateCss('magictime swashOut', () => {
			console.log('callback!');
			let check, timer = 0;

			_page.$welcome_wrapper.hide(0);

			check = setInterval(() => {
				// Tell backend to do connection check every 10 seconds.
				if ( 0 === timer || timer % 10000 === 0 ) {
					_page.do_has_connection_check();
				}

				if ( true === _page.has_connection ) {
					clearInterval(check);
					_page.do_update_check();
				}

				timer += 500

			}, 250);
		});
	}

	maybe_skip_to_next_page() {
		let update_check_passed = localStorage.getItem('cnchi::welcome::update-check-passed');

		if ( null !== update_check_passed ) {
			cnchi.emit_signal('do-go-to-next-page');
		}
	}

	register_event_handlers() {
		$('.try_it button').on('click', this.try_it_button_clicked_cb);
		$('.install_it button').on('click', this.install_it_button_clicked_cb);
		$(window).on('update-available', this.update_available_cb);
		$(window).on('update-check-result', this.update_check_result_cb);
		$(window).on('connection-check-result', this.connection_check_result_cb)
	}

	try_it_button_clicked_cb( event ) {
		cnchi.emit_signal('do-try-it-selected');
	}

	update_available_cb() {
		let $heading = _page.$update_wrapper.find('h3');

		$heading.fadeOut()
		.promise()
		.done(() => {
			$heading.text("{{ _('An installer update is available. Please wait while the update is applied.') }}");
			$heading.fadeIn()
			.promise()
			.done(() => {
				$('.progress.active, .preloader-wrapper').toggleClass('active');
			});
		});
	}

	update_check_result_cb( event, data ) {
		let $headings = _page.$update_wrapper.find('h1, h3');

		$('.progress.active, .preloader-wrapper.active').toggleClass('hideme active');

		if ( true === data.result ) {
			localStorage.setItem('cnchi::welcome::update-check-passed', true);
		}

		if ( true === data.result && true === data.restart ) {
			// Update was installed successfully.
			$headings.fadeOut()
			.promise()
			.done(() => {
				$headings.filter('h1').text("{{ _('Update Complete.') }}");
				$headings.filter('h3').text("{{ _('Restarting the installer. One moment..') }}");
				$headings.fadeIn()
				.promise()
				.done(() => {
					setTimeout(() => {
						cnchi.emit_signal('do-restart');
					}, 4500);
				});
			});

		} else if ( true === data.result ) {
			// We already have the latest version.
			$headings.fadeOut()
			.promise()
			.done(() => {
				$headings.filter('h1').text("{{ _('Update Check Complete') }}");
				$headings.filter('h3').text("{{ _('You are using the latest version and can proceed with your installation!') }}");
				$headings.fadeIn()
				.promise()
				.done(() => {
					setTimeout(() => {
						_page.$update_wrapper.hide();
						cnchi.emit_signal('do-install-it-selected');
					}, 4500);
				});
			});

		} else {
			// Either the update check or the update itself failed.
		}
	}
}