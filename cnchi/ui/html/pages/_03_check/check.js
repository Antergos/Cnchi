/*
 * check.js
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


class CheckPage extends CnchiPage {

	constructor( id ) {
		if ( null !== window._page ) {
			return window._page;
		}

		super(id);

		window._page = this;
		this.signals = JSON.parse(window[`${this.constructor.name}_signals`]);

		this.register_allowed_signals();
		this.register_event_handlers();
		this.initialize();
	}

	initialize() {
		Materialize.showStaggeredList('.checked_items');

		for ( let signal of this.signals ) {
			if ( signal.indexOf('do-') > -1 ) {
				cnchi.emit_signal(signal);
			}
		}
	}

	checks_results_cb( event, result ) {
		let color = ( true === result ) ? 'green' : 'red',
			icon = ( true === result ) ? 'check' : 'close',
			signal = event.type.replace('-result', ''),
			css_id = signal.replace(/-/g, '_'),
			selector = `#${css_id}`;

		$(selector).find('i').removeClass('gray red green').addClass(color).text(icon);
		_page.maybe_unlock_next_tab();
	}

	maybe_unlock_next_tab() {
		if ( ! $('.content_wrapper').find('.red, .gray').length ) {
			_page.unlock_next_tab();
		}
	}

	register_event_handlers() {
		for ( let signal of this.signals ) {
			if ( signal.indexOf('-result') > -1 ) {
				$(window).on(signal, this.checks_results_cb);
			}
		}
	}
}

window.CheckPage = CheckPage;