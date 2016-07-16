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
 * Whether or not the {@link CnchiApp} object has been created.
 */
let _cnchi_exists = false;


/**
 * Capitalizes a string.
 *
 * @returns {string}
 */
String.prototype.capitalise = function() {
	return this.charAt(0).toUpperCase() + this.slice(1);
};


/**
 * jQuery plugin to make using animate.css library more convenient.
 */
$.fn.extend({
	/**
	 * Animate an element and once animation ends call callback if one is provided.
	 *
	 * @arg {String}   animation_name CSS class name for the animation.
	 * @arg {function} [callback]     Function to call after the animation completes.
	 */
	animateCss: function( animation_name, callback ) {
		let animation_end = 'webkitAnimationEnd animationend';

		$(this).addClass(animation_name).one(animation_end, function() {
			setTimeout(function() {
				$(this).removeClass(animation_name);
			}, 1000);

			if ( 'function' === typeof callback ) {
				callback();
			}
		});
	}
});

/**
 * The main application object. It follows the Singleton pattern.
 *
 * @prop {jQuery}   $header  A jQuery object corresponding to the app's header in the DOM.
 * @prop {boolean}  loaded   Whether or not the `page-loaded` event has fired.
 * @prop {String[]} cmds     The commands the app will accept from Python -> JS Bridge.
 * @prop {String[]} signals  The signals the app will allow to be sent via JS Bridge -> Python.
 * @prop {boolean}  dragging Whether or not the window is currently being dragged.
 */
class CnchiApp {

	constructor() {
		if ( false !== _cnchi_exists ) {
			return cnchi;
		}

		this.loaded = false;
		this.cmds = ['trigger_event'];
		this.signals = ['window-dragging-start', 'window-dragging-stop'];
		this.dragging = false;
		this.$header = $('.header');

		this.register_event_handlers();
	}

	/**
	 * Sends an allowed signal and optional arguments to the backend via the Python<->JS Bridge.
	 *
	 * @arg {...String|Array|Object} args The first arg should always be the name of the signal.
	 *
	 * @example
	 * emit_signal( 'do-some-action' );
	 * @example
	 * emit_signal( 'do-some-action', arg1, arg2 );
	 */
	emit_signal( ...args ) {
		let msg = '[', _args = [], log_prefix = this.get_log_message_prefix(this.emit_signal);

		if ( $.inArray(args[0], this.signals) < 0 ) {
			this.log(`${log_prefix} cmd: "${args[0]}" is not in the list of allowed signals!`);
			return;
		}

		// Convert any non-string args to JSON strings so that we have a single string to send.
		for ( let _arg of args ) {
			if ( Array === typeof _arg || _arg instanceof Object ) {
				_arg = JSON.stringify(_arg);
			} else if ('string' === typeof _arg) {
				_arg = `"${_arg}"`;
			}

			msg = `${msg}${_arg}, `;
		}

		msg = msg.replace(/, $/, '');
		msg = `${msg}]`;

		this.log(`${log_prefix} Emitting signal: "${msg}" via python bridge...`);

		document.title = `_BR::${msg}`;
	}

	/**
	 * Returns a string in the form of `CnchiApp.${caller.name}` for use in log messages.
	 *
	 * @arg {function} caller Reference to the calling function.
	 *
	 * @example
	 * // returns "CnchiApp.emit_js:"
	 * get_log_message_prefix( this.emit_js );
	 *
	 * @returns {string}
	 */
	get_log_message_prefix( caller ) {
		return `CnchiApp.${caller.name}:`;
	}

	/**
	 * Header `mousedown` event callback. Intended to be used to implement window dragging.
	 * However, dragging doesn't work at the moment (probably because of some bug in GTK)
	 *
	 * @arg {jQuery.Event} event
	 *
	 * @todo Find a way to make this work.
	 */
	header_mousedown_cb( event ) {
		let $target = event.target ? $(event.target) : event.currentTarget ? $(event.currentTarget) : null;

		if ( null === $target ) {
			console.log('no target!');
			return;
		}

		if ( $target.closest('.no-drag').length || true === cnchi._dragging ) {
			console.log(`mousedown returning! ${cnchi._dragging}`);
			return;
		}

		cnchi._dragging = true;
		cnchi.emit_signal('window-dragging-start', 'window-dragging-start');
	}

	/**
	 * Header `mouseup` event callback.
	 *
	 * @see CnchiApp.header_mousedown_cb
	 */
	header_mouseup_cb( event ) {
		let $target = event.target ? $(event.target) : event.currentTarget ? $(event.currentTarget) : null;

		if ( null === $target ) {
			console.log('no target!');
			return;
		}

		if ( $target.closest('.no-drag').length || false === cnchi._dragging ) {
			console.log(`mouseup returning! ${cnchi._dragging}`);
			return;
		}

		cnchi._dragging = false;

		cnchi.emit_signal('window-dragging-stop', 'window-dragging-stop');
	}

	/**
	 * Handles messages sent from the backend via the Python<->JS Bridge. Messages are
	 * injected into the global scope as an `Object` referenced by a unique variable. The
	 * variable name is then passed to this method so it can access the message.
	 *
	 * @arg msg_obj_var_name
	 */
	js_bridge_handler( msg_obj_var_name ) {
		let data, cmd, args, log_prefix = this.get_log_message_prefix(this.js_bridge_handler);

		args = window[msg_obj_var_name].args;
		cmd = window[msg_obj_var_name].cmd;

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

	/**
	 * Outputs a log message.
	 *
	 * @arg msg
	 *
	 * @todo Finish implementing JS->Python logging facility so we can stop using console.log()
	 */
	log( msg ) {
		console.log(msg)
	}

	page_loaded_handler( event, page ) {
		if ( false === cnchi.loaded ) {
			cnchi.loaded = true;
		}
	}

	register_event_handlers() {
		$(window).on('page-loaded', this.page_loaded_handler);
		this.$header.on('mousedown', '*', this.header_mousedown_cb);
		this.$header.on('mouseup', '*', this.header_mouseup_cb);
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
 *
 * @prop {jQuery}   $tab   A jQuery object for the tab's HTML element in the DOM.
 * @prop {string}   id     The CSS ID for the tab.
 * @prop {string}   name   A name for this tab. It will be used in the navigation tab buttons.
 * @prop {CnchiTab} parent This tab's parent tab (the page this tab appears on).
 */
class CnchiTab {
	/**
	 * Creates a new {@link CnchiTab} object.
	 *
	 * @arg {jQuery}   $tab     {@link CnchiTab.$tab}
	 * @arg {string}   [id]     {@link CnchiTab.id}
	 * @arg {CnchiTab} [parent] {@link CnchiTab.parent}
	 */
	constructor( $tab, id, parent ) {
		let log_prefix = cnchi.get_log_message_prefix(CnchiTab);

		if ( null === $tab && '' === id ) {
			cnchi.log(`${log_prefix} ERROR: One of [$tab, id] required!`);
			return;
		}

		this.$tab = ( $tab instanceof jQuery ) ? $tab : $(`#${id}`);
		this.id = this.$tab.attr('id');
		this.name = this.$tab.attr('data-name');
		this.parent = parent;
	}
}


/**
 * Manages a page in the installation process. A page is actually a top-level tab in the UI that
 * can optionally house a number of other tabs in addition to itself (a page is also a tab).
 * If a page does not have any other (than itself) tabs, no navigation buttons will
 * be displayed on the page.
 *
 * @extends CnchiTab
 *
 * @prop {CnchiTab}   current_tab The tab that is currently visible on the page.
 * @prop {boolean}    has_tabs    Whether or not this page has mulitple tabs.
 * @prop {string[]}   signals     Names of signals used by the page to communicate with backend.
 * @prop {CnchiTab[]} tabs        This page's tabs. One tab is always implied (the page itself).
 *
 */
class CnchiPage extends CnchiTab {

	constructor( $tab, id ) {
		super($tab, id, null);
		this.signals = [];
		this.tabs = [];
		this.current_tab = null;
		this.has_tabs = $('.page_tab').length ? true : false;

		if ( true === this.has_tabs ) {
			this.prepare_tabs();
		}

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
			$tab = $(identifier);

		} else if ( 'number' === typeof identifier ) {
			let tab_name = this.tabs[identifier];
			$tab = this[tab_name].$tab;
		}

		return $tab;
	}

	/**
	 * Locates the tabs' containers in the DOM and uses them to create `CnchiTab` objects for
	 * the tabs. Also ensures that `this.tabs`, `this.current_tab`, and `this.<tab_name>_tab`(s)
	 * are properly set.
	 */
	prepare_tabs() {
		$('.page_tab').each(( index, element ) => {
			let tab_name = $(element).attr('id'),
				prop_name = `${tab_name}_tab`,
				$tab = $(tab_name);

			this[prop_name] = new CnchiTab($tab, tab_name, this);
			this.tabs.push(tab_name);
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
	 * Sets the current tab to the tab represented by `identifier`.
	 *
	 * @arg {CnchiTab|jQuery|string|number} identifier See {@link CnchiPage#get_tab_jquery_object}.
	 */
	show_tab( identifier ) {
		let $tab = this.get_tab_jquery_object(identifier);

		if ( null !== $tab ) {
			$tab.fadeIn();
		} else {
			let log_prefix = cnchi.get_log_message_prefix(this.show_tab);
			cnchi.log(`${log_prefix} ERROR: Tab cannot be null!`)
		}
	}
}


if ( false === _cnchi_exists ) {
	window.cnchi = new CnchiApp();
	window.CnchiPage = CnchiPage;
	window.CnchiTab = CnchiTab;
	_cnchi_exists = true;
}

