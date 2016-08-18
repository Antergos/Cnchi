


class LanguagePage extends CnchiPage {

	constructor( id ) {
		if ( null !== window._page ) {
			return window._page;
		}

		super( id );

		window._page = this;
		this.signals = JSON.parse('{{ signals }}');
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