/*
 * page.js
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

'use strict';


/**
 * Manages a page in the installation process. A page contains one or more tabs. When
 * a page contains only one tab, the page-level tab buttons will not be shown.
 *
 * @extends CnchiObject
 *
 * @prop {CnchiTab}   current_tab The tab that is currently visible on the page.
 * @prop {boolean}    has_tabs    Whether or not this page has mulitple tabs.
 * @prop {string[]}   signals     Names of signals used by the page to communicate with backend.
 * @prop {CnchiTab[]} tabs        This page's tabs. One tab is always implied (the page itself).
 *
 */
class CnchiPage extends CnchiObject {

	constructor( id ) {
		let $page_tabs = $('.page_tab'),
			has_tabs = $page_tabs.length ? true : false,
			$tab = ( true === has_tabs ) ? $page_tabs.first() : $(`#${id}`);

		super();

		this.signals = [];
		this.tabs = [];
		this.has_tabs = has_tabs;
		this.current_tab = null;
		this.$page = (true === this.is_page) ? $('.main_content') : this.parent.$page;
		this.$tab = $tab;
		this.$top_navigation_buttons = $('.header_bottom .navigation_buttons .tabs');
		this.next_tab_animation_interval = null;

		if ( true === this.has_tabs ) {
			this.prepare_tabs();
		}

		this.maybe_unlock_top_level_tabs();
		$(window).on('page-change-current-tab', this.change_current_tab_cb)

	}

	_assign_next_and_previous_tab_props() {
		this.previous = null;
		this.next = this.tabs[0];

		for ( let [index, value] of this.tabs.entries() ) {
			value.previous = ( index > 0 ) ? this.tabs[index - 1] : this;
			value.next = ( index < (this.tabs.length - 1) ) ? this.tabs[index + 1] : null;
		}
	}

	_get_next_tab_button() {
		console.log([this.current_tab]);
		let $tab_button,
			on_last_tab_for_page = ( true === this.has_tabs && null === this.current_tab.next );

		if ( false === this.has_tabs || on_last_tab_for_page ) {
			$tab_button = this.$tab_button.next();
		} else {
			$tab_button = this.current_tab.$tab_button.filter('.main_content li').next();
		}

		return $tab_button;
	}

	_unlock_next_tab_animated() {
		let $tab_button = this._get_next_tab_button();

		if ( $tab_button.hasClass('locked') ) {
			$tab_button.on('click', this.tab_button_clicked_cb).removeClass('locked');
		}

		$tab_button.animateCss('animated tada');
	}

	change_current_tab_cb( event, id ) {
		console.log('change current tab fired!');
		this.logger.debug('change current tab fired!');
		clearInterval(this.next_tab_animation_interval);
		this.reload_element(`#${id}`, this.show_tab);
	}

	get_tab_by_id( id ) {
		let tab;

		for ( let tab_obj of this.tabs ) {
			if ( tab_obj.id === id ) {
				tab = tab_obj;
				break;
			}
		}

		return tab;
	}

	/**
	 * Returns a jQuery object for the tab represented by `identifier`.
	 *
	 * @arg {CnchiTab|jQuery|string|number} An identifier by which to locate the tab.
	 *
	 * @returns {jQuery|null}
	 */
	get_tab_jquery_object( identifier ) {
		let $tab = null;

		if ( identifier instanceof CnchiTab ) {
			$tab = identifier.$tab;

		} else if ( identifier instanceof jQuery ) {
			$tab = identifier;

		} else if ( 'string' === typeof identifier ) {
			$tab = $(`#${identifier}`);

		} else if ( 'number' === typeof identifier ) {
			let tab_name = this.tabs[identifier];
			$tab = this[tab_name].$tab;
		}

		return $tab;
	}

	maybe_unlock_top_level_tabs() {
		this.$top_navigation_buttons.children().each(( index, element ) => {
			let $tab_button = $(element);

			$tab_button.removeClass('locked');

			if ( $tab_button.hasClass('active') ) {
				// This button is for the current page. Don't unlock anymore buttons.
				return false;
			}
		});
	}

	/**
	 * Locates the tabs' collapsibles in the DOM and uses them to create `CnchiTab` objects for
	 * the tabs. Also ensures that `this.tabs`, `this.current_tab`, and `this.<tab_name>_tab`(s)
	 * are properly set.
	 */
	prepare_tabs() {
		let $page_tabs = $('.page_tab');
		this.current_tab = this;

		this.$tab.fadeIn();
		this.$tab_button.removeClass('locked').addClass('active');

		$page_tabs.each(( index, element ) => {
			// Don't create a `CnchiTab` object for the first tab since it is the current page.
			if ( 0 === index ) {
				return;
			}

			let tab_name = $(element).attr('id'),
				prop_name = `${tab_name}_tab`;

			this[prop_name] = new CnchiTab($(element), tab_name, this);
			this.tabs.push(this[prop_name]);

			if ( index === ($page_tabs.length - 1) ) {
				this._assign_next_and_previous_tab_props();
			}
		});
	}

	/**
	 * Adds this page's signals to {@link CnchiApp.signals} array.
	 */
	register_allowed_signals() {
		for ( let signal of this.signals ) {
			cnchi.signals.push(signal);
		}
	}

	/**
	 * Reloads a single element on the page. The result is the same as if the entire page
	 * had been reloaded, except only that single element will actually change.
	 *
	 * @arg {String}   selector A CSS selector that matches only one element on the page.
	 * @arg {Function} callback An optional callback to be called after element is reloaded.
	 */
	reload_element( selector, callback ) {
		let url = `cnchi://${this.id}`,
			$old_el = this.$page.find(selector),
			$new_el;

		console.log([url, $old_el]);
		this.logger.debug([url, $old_el]);

		$old_el.hide(0)
		.promise()
		.done(() => {
			$.get(url, ( data ) => {
				$new_el = $(data).find(selector);
				console.log($new_el);

				$old_el.replaceWith($new_el);
				$new_el.show(0)
				.promise()
				.done(() => {
					if ( callback ) {
						callback(selector);
					}
				});
			});
		});
	}

	/**
	 * Sets the current tab to the tab represented by `identifier`.
	 *
	 * @arg {CnchiTab|jQuery|string|number} identifier See {@link CnchiPage#get_tab_jquery_object}.
	 */
	show_tab( identifier ) {
		let tab = this.get_tab_by_id(identifier.replace('#', ''));
		console.log([tab, this.current_tab]);

		if ( null !== tab.$tab ) {
			this.current_tab.$tab.fadeOut()
			.promise()
			.done(() => {
				this.current_tab.$tab_button.removeClass('active');

				tab.$tab_button.addClass('active');
				tab.$tab.fadeIn()
				.promise()
				.done(() => {
					$(window).trigger('page-change-current-tab-done');
					this.current_tab = tab;
				});

			});
		} else {
			this.logger.debug('Tab cannot be null!', this.show_tab)
		}
	}

	unlock_next_tab() {
		this._unlock_next_tab_animated();
		this.next_tab_animation_interval = setInterval(() => {
			this._unlock_next_tab_animated();
		}, 4000);
	}
}

window.CnchiPage = CnchiPage;
