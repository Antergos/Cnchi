/*
 * tab.js
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
 * Manages a tab in the UI. Tabs make up pages. All pages contain at least one tab.
 *
 * @prop {jQuery}    $tab    A jQuery object for the tab's HTML element in the DOM.
 * @prop {string}    id      The CSS ID for the tab.
 * @prop {string}    name    A name for this tab. It will be used in the navigation tab buttons.
 * @prop {CnchiPage} parent  This tab's parent tab (the page this tab appears on).
 */
class CnchiTab extends CnchiObject {
	/**
	 * Creates a new {@link CnchiTab} object.
	 *
	 * @arg {jQuery}    $tab     {@link CnchiTab.$tab}
	 * @arg {string}    [id]     {@link CnchiTab.id}
	 * @arg {CnchiPage} [parent] {@link CnchiTab.parent}
	 */
	constructor( $tab, id, page ) {
		super();

		let result = this._check_args( $tab, id, page );

		if ( true !== result ) {
			this.logger.error( result, this.constructor );
		}

		this.$tab = ( $tab instanceof jQuery ) ? $tab : $(`#${id}`);
		this.$tab_button = this.get_tab_button();
		this.id = id;
		this.locked = true;
		this.lock_key = `unlocked_tabs::${this.id}`;
		this.name = this.$tab.attr('data-name');
		this.next = null;
		this.page = page;
		this.previous = null;

		this._maybe_unlock();

	}

	_check_args( $tab, id, page ) {
		let result = true;

		if ( 'undefined' === typeof $tab && '' === id ) {
			result = 'One of [$tab, id] required!';

		} else if ( 'undefined' === typeof page ) {
			result = 'page is required to create a new CnchiTab!';
		}

		return result;
	}

	_do_unlock() {
		this.$tab_button.removeClass( 'locked' );
		this.$tab_button.on( 'click', this.tab_button_clicked_cb );
		localStorage.setItem( this.lock_key, 'true' );
	}

	_maybe_unlock() {
		let unlocked = ( null !== localStorage.getItem( this.lock_key ) );

		if ( true === unlocked ) {
			this._do_unlock();
		}
	}

	_tab_button_clicked_handler( $tab_button ) {
		if ( $tab_button.hasClass('locked') ) {
			this.logger.debug('is locked!');
			console.log('is locked!');
			return;
		}

		let id = $tab_button.children('a').attr('href');

		$(window).trigger('page-change-current-tab', [id.replace('#', '')]);
	}

	get_tab_button() {
		let selector = `[href\$="${this.id}"]`,
			$container = $('.main_content');

		return $container.find('.navigation_buttons').find(selector).parent();
	}

	tab_button_clicked_cb( event ) {
		let $target = $(event.currentTarget),
			$tab_button = $target.closest('.tab');
		console.log(event);
		this.logger.debug(event);

		if ( !$('.header_bottom').has($tab_button).length ) {
			event.preventDefault();
			console.log('clicked!');
			console.log(event);
			_page._tab_button_clicked_handler($tab_button);
		}
	}
}

window.CnchiTab = CnchiTab;
