/*
 * cnchi_app.js
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


/**
 * This is used to access our classes from within jQuery callbacks.
 */
let _self = null;


/**
 * Capitalize a string.
 *
 * @returns {string}
 */
String.prototype.capitalize = function () {
	return this.charAt(0).toUpperCase() + this.slice(1);
};


/**
 * jQuery plugin to make using animate.css library more convenient.
 */
$.fn.extend({
	animateCss: function ( animationName, callback ) {
		let animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
		$(this).addClass(animationName).one(animationEnd, function () {
			setTimeout(() => {
				$(this).removeClass(animationName);
			}, 1000);

			if ( callback ) {
				callback();
			}
		});
	}
});


class CnchiApp {

	constructor() {
		if ( null !== _self ) {
			return _self;
		}

		_self = this;
		this.loaded = false;
		this.cmds = ['trigger_event'];
		this.signals = ['window-dragging-start', 'window-dragging-stop'];
		this._dragging = false;
		this.$header = $('.header');

		this._register_event_handlers();

		return _self
	}

	_get_log_message_prefix( caller ) {
		return `CnchiApp.${caller.name}:`;
	}

	_register_event_handlers() {
		$(window).on('page-loaded', this.page_loaded_handler);
		this.$header.on('mousedown', '*', this.header_mousedown_cb);
		this.$header.on('mouseup', '*', this.header_mouseup_cb);
	}

	emit_signal( ...args ) {
		let msg = JSON.stringify(args), log_prefix = this._get_log_message_prefix(this.emit_signal);

		if ( $.inArray(args[0], this.signals) < 0 ) {
			this.log(`${log_prefix} cmd: "${args[0]}" is not in the list of allowed signals!`);
			return;
		}

		this.log(`${log_prefix} Emitting signal: "${msg}" via python bridge...`);

		document.title = `_BR::${msg}`;
	}

	header_mousedown_cb( event ) {
		let $target = event.target ? $(event.target) : event.currentTarget ? $(event.currentTarget) : null;
		if (null === $target) {
			console.log('no target!');
			return;
		}
		if ( $target.closest('.no-drag').length || true === _self._dragging ) {
			console.log(`mousedown returning! ${_self._dragging}`);
			return;
		}
		_self._dragging = true;
		_self.emit_signal('window-dragging-start', 'window-dragging-start');
	}

	header_mouseup_cb( event ) {
		let $target = event.target ? $(event.target) : event.currentTarget ? $(event.currentTarget) : null;
		if ( null === $target ) {
			console.log('no target!');
			return;
		}
		if ( $target.closest('.no-drag').length || false === _self._dragging ) {
			console.log(`mouseup returning! ${_self._dragging}`);
			return;
		}
		_self._dragging = false;
		_self.emit_signal('window-dragging-stop', 'window-dragging-stop');
	}

	js_bridge_handler( args_var_name ) {
		let data, cmd, args, log_prefix = this._get_log_message_prefix(this.js_bridge_handler);

		args = window[args_var_name].args;
		cmd = window[args_var_name].cmd;

		if ( !cmd.length ) {
			this.log(`${log_prefix} "cmd" is required!`);
			return;
		}

		if ( $.inArray(cmd, this.cmds) < 0 ) {
			this.log(`${log_prefix} cmd: "${cmd}" is not in the list of allowed commands!`);
			return;
		}


		if ( args.length === 1 ) {
			args = args.pop();
		}

		this.log(`${log_prefix} Running command: ${cmd} with args: ${args}...`);

		this[cmd](args);
	}

	log( msg ) {
		console.log(msg)
	}

	page_loaded_handler( page ) {
		if ( false === _self.loaded ) {
			_self.loaded = true;
		}
	}

	trigger_event( event ) {
		let args = [];

		if ( Array.isArray(event) ) {
			args = event;
			event = args.shift();

			if ( args.length === 1 ) {
				args = args.pop();
			}
		}

		console.log(`triggering event: ${event} with args: ${args}`);

		$(window).trigger(event, args);
	}

}


/**
 * Manages a tab in the UI.
 * @prop {jQuery}   $tab   A jQuery object for the tab's HTML element in the DOM.
 * @prop {string}   id     The CSS ID for the tab.
 * @prop {string}   name   A name for this tab. It will be used in the navigation tab buttons.
 * @prop {CnchiTab} parent This tab's parent tab (the page this tab appears on).
 */
class CnchiTab {
	/**
	 * Creates a new {@link CnchiTab} object.
	 * @param {jQuery}   $tab     {@link CnchiTab.$tab}
	 * @param {string}   [id]     {@link CnchiTab.id}
	 * @param {CnchiTab} [parent] {@link CnchiTab.parent}
	 */
	constructor( $tab = null, id = '', parent = null ) {
		let log_prefix = cnchi._get_log_message_prefix(CnchiPageTab);

		if (null === $tab && '' === id) {
			cnchi.log(`${log_prefix} ERROR: One of [$tab, id] required!`);
			return;
		}

		this.$tab = ( null !== $tab ) ? $tab : $(`#${id}`);
		this.id = $tab.attr('id');
		this.name = $tab.attr('data-name');
		this.parent = parent;
	}
}


/**
 * Manages a page in the installation process. A page is actually a top-level tab in the UI that
 * can either house itself only or it can house itself and a number of other tabs. If a page
 * does not have more than one tab, no navigation tab buttons will be displayed on the page.
 * @extends CnchiTab
 */
class CnchiPage extends CnchiTab {
	constructor() {
		this.signals = [];
		this.tabs = [];
		this.current_tab = null;
		this.has_tabs = $('.page_tab').length ? true : false;

	}

	/**
	 * Calls prepare_tabs method if this page has tabs.
	 */
	maybe_prepare_tabs() {
		if ( true === this.has_tabs ) {
			this.prepare_tabs();
		}
	}

	/**
	 * Locates the tabs' containers in the DOM and uses them to create a `CnchiPageTab` object for each tab.
	 * Also ensures that `this.tabs`, `this.current_tab`, & `this.${tab_name}` are set properly.
	 */
	prepare_tabs() {
		$('.page_tab').each( (index, element) => {
			let tab_name =

			this[tab_name] = $(this);
			this.tabs.push(tab_name);
		});
	}

	/**
	 * Add this page's signals to `CnchiApp.signals` array.
	 */
	register_allowed_signals() {
		for ( let signal of this.signals ) {
			cnchi.signals.push(signal);
		}
	}

	/**
	 * Sets the current tab to
	 * @param identifier
	 */
	show_tab( identifier ) {
		let $tab = null;

		if ( identifier instanceof jQuery ) {
			$tab = identifier;
		} else if ('string' === typeof identifier) {
			$tab = $(identifier);
		} else if ('number' === typeof identifier) {
			$tab = $(this.tabs[identifier]);
		}

		if (null !== $tab) {
			$tab.fadeIn();
		} else {
			let log_prefix = cnchi._get_log_message_prefix(this.show_tab);
			cnchi.log(`${log_prefix} ERROR: Tab cannot be null!`)
		}
	}
}

window.CnchiPage = CnchiPage;
window.cnchi = new CnchiApp();
