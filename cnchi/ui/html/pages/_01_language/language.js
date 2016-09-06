/*
 * language.js
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


class LanguagePage extends CnchiPage {

	constructor( id ) {
		if ( null !== window._page ) {
			return window._page;
		}

		super( id );

		window._page = this;
		this.signals = JSON.parse(window[`${this.constructor.name}_signals`]);
		this.cache_key = 'cnchi::language::selected';

		this.register_allowed_signals();
		// this.maybe_skip_to_next_page();
		this.initialize();
	}

	initialize() {
		$('html, body').css({'background': '#383A41', 'opacity': 1});
		$('select').material_select();

		this.register_event_handlers();
	}

	maybe_skip_to_next_page() {
		let selected_language = localStorage.getItem(this.cache_key);

		if (null !== selected_language) {
			cnchi.emit_signal('do-go-to-next-page');
		}
	}

	register_event_handlers() {
		$('.btn_wrapper button').on('click', () => {
			let lang = $('select').val();

			/* Changing the language will mean needing to restart Cnchi. Save this key in cache
			 * temporarily so we don't show this page after being restarted once.
			 */
			localStorage.setItem(_page.cache_key, true);

			this.logger.debug(`${lang} language was selected`);

			$('.content_wrapper').animateCss('magictime holeOut', () => {
				$('.content_wrapper').hide(0);
				cnchi.emit_signal('do-language-selected', lang);
			});
		});
	}
}

window.LanguagePage = LanguagePage;