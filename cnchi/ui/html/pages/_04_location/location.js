/*
 * location.js
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


class LocationPage extends CnchiPage {

	constructor( id ) {
		if ( null !== window._page ) {
			return window._page;
		}

		super( id );

		window._page = this;
		this.location = null;
		this.layout = null;
		this.variant = null;
		this.kbd_widget = null;
		this.lang_name = null;
		this.collapsible_containers = new CollapsibleContainers();

		this.$show_all_locations = $( '#show_all_locations' );
		this.show_all_locations = this.$show_all_locations.prop( 'checked' );
		this.$locations_list = $( 'ul.collapsible:not(#keyboard_layout ul)' );
		this.$kbd_layouts_list = $( '#keyboard_layout ul.collapsible' );
		this.timezone_map = null;

		this.register_event_handlers();
		this.initialize();
	}

	initialize() {
		cnchi.emit_signal( 'do-load-keyboard-layouts' );
	}

	keyboard_layout_selected_cb( event, original_event ) {
		let $variant = $( original_event.target ),
			variant = $variant.attr( 'id' );

		$variant.addClass( 'active' );

		if ( null !== this.variant ) {
			$( `#${this.variant}` ).removeClass( 'active' );
		}

		this.variant = variant;
		this.unlock_next_tab();
	}

	location_selected_cb( event, original_event ) {
		let $location = $( original_event.target ),
			location = $location.attr( 'id' ),
			location_name = $location.text();

		this.lang_name = location_name.split( ' ' )[ 0 ];

		$location.addClass( 'active' );

		if ( null !== this.location ) {
			$( `#${this.location}` ).removeClass( 'active' );
		}

		this.location = location;
		this.unlock_next_tab();
	}

	current_tab_changed_cb() {
		console.log( `current_tab_changed_cb(): current_tab is: ${this.current_tab.id}` );

		if ( 'keyboard_layout' === this.current_tab.id ) {
			this.$kbd_layouts_list = $( '#keyboard_layout ul.collapsible' );
			this.collapsible_containers.initialize();
			this.$kbd_layouts_list.on( 'collection-item-selected.keyboard_layout', this.keyboard_layout_selected_cb );
			this.kbd_widget = new window.KeyboardWidget( this.location, this.lang_name );

			cnchi.emit_signal( 'do-enable-timezone-map' );

		} else if ( 'timezone' === this.current_tab.id ) {
			this.timezone_map = new window.TimezoneMap( this.location );
		}
	}

	register_event_handlers() {
		this.$show_all_locations.on( 'click', this.show_all_locations_clicked_cb );
		this.$locations_list.on( 'collection-item-selected.location', this.location_selected_cb );
		$( window ).on( 'page-change-current-tab-done', this.current_tab_changed_cb );
	}

	show_all_locations_clicked_cb( event ) {
		cnchi.emit_signal( 'do-show-all-locations' );
		setTimeout( () => {
			this.reload_element( '.collection_wrapper', this.init_collapsable_list );
		}, 250 )
	}
}

window.LocationPage = LocationPage;