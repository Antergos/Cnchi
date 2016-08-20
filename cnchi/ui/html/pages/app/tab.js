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
	 * @arg {string}    [name]     {@link CnchiTab.name}
	 * @arg {CnchiPage} [parent] {@link CnchiTab.parent}
	 */
	constructor( $tab, name, page ) {
		super();

		let result = this._check_args( $tab, name, page );

		if ( true !== result ) {
			this.logger.error( result, this.constructor );
		}

		this.$tab = ( $tab instanceof jQuery ) ? $tab : $( `#${name}` );
		this.$tab_button = this._get_tab_button();
		this.locked = true;
		this.loaded = false;
		this.lock_key = `unlocked_tabs::${this.id}`;
		this.name = name;
		this.next_tab = null;
		this.page = page;
		this.previous_tab = null;

		this._maybe_unlock();

	}

	_check_args( $tab, name, page ) {
		let result = true;

		if ( 'undefined' === typeof $tab && '' === name ) {
			result = 'One of [$tab, name] required!';

		} else if ( 'undefined' === typeof page ) {
			result = 'page is required to create a new CnchiTab!';
		}

		return result;
	}

	_get_tab_button() {
		let selector = `[href\$="${this.name}"]`,
			$container = $( '.main_content' );

		return $container.find( '.navigation_buttons' ).find( selector ).parent();
	}

	_hide() {
		return this.$tab.fadeOut().promise();
	}

	_load_and_show() {
		return this.page.reload_element( `#${this.name}` ).then( this.$tab.fadeIn().promise() )
	}

	_maybe_unlock() {
		let unlocked = ( null !== localStorage.getItem( this.lock_key ) );

		if ( true === unlocked ) {
			this._unlock();
		}
	}

	_show() {
		let deferred;

		if ( this.page.tabs[0] === this || this.loaded ) {
			deferred = this.$tab.fadeIn().promise();
		} else {
			deferred = this._load_and_show();
		}

		return deferred;
	}

	_unlock() {
		this.$tab_button.removeClass( 'locked' );
		this.$tab_button.on( 'click', this.page.tab_button_clicked_cb );
		localStorage.setItem( this.lock_key, 'true' );
	}

	prepare( prepare_to ) {
	}
}

window.CnchiTab = CnchiTab;
