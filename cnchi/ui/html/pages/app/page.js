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
		super();

		this.signals = [];
		this.tabs = [];
		this.current_tab = null;
		this.previous_tab = null;
		this.next_tab = null;
		this.$page = $( '.main_content' );
		this.next_tab_animation_interval = null;

		this._prepare_tabs();
		this._register_event_handlers();
		this._set_current_tab( 0 );

	}

	_assign_next_and_previous_tab_props() {
		this.next_tab = ( this.tabs.length > 1 ) ? this.tabs[1] : null;

		for ( let [index, value] of this.tabs.entries() ) {
			value.previous_tab = ( index > 0 ) ? this.tabs[index - 1] : null;
			value.next_tab = ( index < (this.tabs.length - 1) ) ? this.tabs[index + 1] : null;
		}
	}

	/**
	 * Locates the page's tabs in the DOM and creates `CnchiTab` objects for them. Also ensures
	 * that `this.tabs`, `this.current_tab`, and `this.<tab_name>_tab`(s) are properly set.
	 */
	_prepare_tabs() {
		let $page_tabs = $( '.page_tab' );
		this.$tab.fadeIn();
		this.$tab_button.removeClass( 'locked' ).addClass( 'active' );

		$page_tabs.each( ( index, element ) => {
			let tab_name = $( element ).attr( 'id' ),
				property_name = `${tab_name}_tab`;

			this[property_name] = new CnchiTab( $( element ), tab_name, this );

			this.tabs.push( this[property_name] );
			this[property_name].$tab_button.on( 'click', this.tab_button_clicked_cb );

			if ( index === ( $page_tabs.length - 1 ) ) {
				this._assign_next_and_previous_tab_props();
			}
		} );
	}

	/**
	 * Adds this page's signals to {@link CnchiApp.signals} array.
	 */
	_register_allowed_signals() {
		for ( let signal of this.signals ) {
			cnchi.signals.push( signal );
		}
	}

	_register_event_handlers() {

	}

	_set_current_tab( identifier ) {
		let tab;

		if ( Number.isInteger( identifier ) ) {
			tab = this.tabs[identifier];
		} else {
			tab = this.get_tab_by_name( identifier );
		}

		this._show_tab( tab );
	}

	_show_tab( tab ) {
		let _prepare = () => {
			this.current_tab = tab;
			this.current_tab.prepare( 'show' );
		};

		if ( null !== this.current_tab ) {
			this.current_tab.prepare( 'hide' )
				.done( () => {
					_prepare();
				} );
		} else {
			_prepare();
		}
	}

	_unlock_next_tab_animated() {
		let $tab_button = this._get_next_tab_button();

		if ( $tab_button.hasClass( 'locked' ) ) {
			$tab_button.on( 'click', this.tab_button_clicked_cb ).removeClass( 'locked' );
		}

		$tab_button.animateCss( 'animated tada' );
	}

	change_current_tab_cb( event, id ) {
		console.log( 'change current tab fired!' );
		this.logger.debug( 'change current tab fired!' );
		clearInterval( this.next_tab_animation_interval );
		this.reload_element( `#${id}`, this.show_tab );
	}

	get_tab_by_name( tab_name ) {
		let property_name = `${tab_name}_tab`;
		return this[property_name];
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
			$old_el = this.$page.find( selector ),
			$new_el;

		console.log( [url, $old_el] );
		this.logger.debug( [url, $old_el] );

		$old_el.hide( 0 )
			   .promise()
			   .done( () => {
				   $.get( url, ( data ) => {
					   $new_el = $( data ).find( selector );
					   console.log( $new_el );

					   $old_el.replaceWith( $new_el );
					   $new_el.show( 0 )
							  .promise()
							  .done( () => {
								  if ( callback ) {
									  callback( selector );
								  }
							  } );
				   } );
			   } );
	}

	/**
	 * Sets the current tab to the tab represented by `identifier`.
	 *
	 * @arg {CnchiTab|jQuery|string|number} identifier See {@link CnchiPage#get_tab_jquery_object}.
	 */
	show_tab( identifier ) {
		let tab = this.get_tab_by_id( identifier.replace( '#', '' ) );
		console.log( [tab, this.current_tab] );

		if ( null !== tab.$tab ) {
			this.current_tab.$tab.fadeOut()
				.promise()
				.done( () => {
					this.current_tab.$tab_button.removeClass( 'active' );

					tab.$tab_button.addClass( 'active' );
					tab.$tab.fadeIn()
					   .promise()
					   .done( () => {
						   $( window ).trigger( 'page-change-current-tab-done' );
						   this.current_tab = tab;
					   } );

				} );
		} else {
			this.logger.debug( 'Tab cannot be null!', this.show_tab )
		}
	}

	tab_button_clicked_cb( event ) {
		let $target = $( event.currentTarget ),
			$tab_button = $target.closest( '.tab' );

		event.preventDefault();
		_page.tab_button_clicked_handler( $tab_button );
	}

	unlock_next_tab() {
		this._unlock_next_tab_animated();
		this.next_tab_animation_interval = setInterval( () => {
			this._unlock_next_tab_animated();
		}, 4000 );
	}
}

window.CnchiPage = CnchiPage;
