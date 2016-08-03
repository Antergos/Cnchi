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

'use strict';

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
 * Animate an element and once animation ends call callback if one is provided.
 *
 * @arg {String}   animation_name CSS class name for the animation.
 * @arg {function} [callback]     Function to call after the animation completes.
 */
$.fn.animateCss = function( animation_name, callback ) {
	let animation_end = 'webkitAnimationEnd animationend';

	this.addClass(animation_name).one(animation_end, () => {
		setTimeout(() => {
			this.removeClass(animation_name);
		}, 1000);

		if ( callback ) {
			callback();
		}
	});
};


/**
 * Sends log messages via the Python<->JS Bridge to our Python logging handler.
 *
 * @prop {String} log_prefix      A string that will be prepended to log messages.
 * @prop {String} _unknown_method A string used for calling method name when one isn't provided.
 */
class Logger {

	/**
	 * Creates a new Logger instance.
	 *
	 * @arg {String} log_prefix {@link Logger.log_prefix}
	 */
	constructor( log_prefix ) {
		this.log_prefix = log_prefix;
		this._unknown_method = '@unknown@';
	}

	/**
	 * Determines and returns the caller name based on value of `caller` argument
	 *
	 * @arg {Function|String} caller
	 * @returns {String}
	 * @private
	 */
	_get_caller_name( caller ) {
		return ( '' !== caller ) ? caller.name : this._unknown_method;
	}

	/**
	 * Prepares a message to be sent to Python logging facility.
	 *
	 * @arg {String} msg    The message to be logged.
	 * @arg {String} caller The name of the caller or an empty string.
	 * @returns {string}
	 * @private
	 */
	_process_message( msg, caller ) {
		return `[${this.log_prefix}.${this._get_caller_name(caller)}]: ${msg}`;
	}

	/**
	 * Sends a message to the Python logging facility.
	 *
	 * @arg {String} msg   The message to be sent.
	 * @arg {String} level The logging level to use for the message.
	 * @private
	 */
	_write_log( msg, level ) {
		let esc_msg = msg.replace(/"/g, '\\"');
		msg = `_BR::["do-log-message", "${level}", "${esc_msg}"]`;

		cnchi._bridge_message_queue.push(msg);
		console.log(msg);
	}

	/**
	 * Sends a message to Python logging facility where logging level == method name.
	 *
	 * @arg {String}          msg         The message to be logged.
	 * @arg {Function|String} [caller=''] The method calling this log method.
	 */
	info( msg, caller = '' ) {
		msg = this._process_message(msg, caller);
		this._write_log(msg, 'info');
	}

	/**
	 * @see Logger.info
	 */
	debug( msg, caller = '' ) {
		msg = this._process_message(msg, caller);
		this._write_log(msg, 'debug');
	}

	/**
	 * @see Logger.info
	 */
	warning( msg, caller = '' ) {
		msg = this._process_message(msg, caller);
		this._write_log(msg, 'warning');
	}

	/**
	 * @see Logger.info
	 */
	error( msg, caller = '' ) {
		msg = this._process_message(msg, caller);
		this._write_log(msg, 'error');
	}
}


/**
 * A base object for all Cnchi* objects. It sets up the logger and
 * binds `this` to the class for all class methods.
 *
 * @prop {Logger} logger The logger object.
 */
class CnchiObject {

	constructor() {
		this.logger = new Logger(this.constructor.name);
		this._bind_this();
	}

	/**
	 * Binds `this` to the class for all class methods.
	 *
	 * @private
	 */
	_bind_this() {
		let excluded = ['constructor', '_bind_this', 'not_excluded'];

		function not_excluded(method, context) {
			let _excluded = excluded.findIndex(excluded_method => method === excluded_method) > -1,
				is_method = 'function' === typeof context[method];

			return is_method && ! _excluded;
		}

		for ( let obj = this; obj; obj = Object.getPrototypeOf(obj) ) {
			for ( let method of Object.getOwnPropertyNames(obj) ) {
				if ( not_excluded(method, this) ) {
					this[method] = this[method].bind(this);
				}
			}
		}
	}
}


/**
 * The main application object. It follows the Singleton pattern.
 *
 * @prop {jQuery}   $header  A jQuery object corresponding to the app's header in the DOM.
 * @prop {boolean}  loaded   Whether or not the `page-loaded` event has fired.
 * @prop {String[]} cmds     The commands the app will accept from Python -> JS Bridge.
 * @prop {String[]} signals  The signals the app will allow to be sent via JS Bridge -> Python.
 * @prop {boolean}  dragging Whether or not the window is currently being dragged.
 */
class CnchiApp extends CnchiObject {

	constructor() {
		if ( false !== _cnchi_exists ) {
			return cnchi;
		}

		super();

		this.loaded = false;
		this.cmds = ['trigger_event'];
		this.signals = ['window-dragging-start', 'window-dragging-stop'];
		this.dragging = false;
		this.$header = $('.header');
		this._logger = null;
		this._bridge_message_queue = [];
		this.bmq_worker = null;

		this.register_event_handlers();
		this._start_bridge_message_queue_worker();
	}


	_start_bridge_message_queue_worker() {
		this.bmq_worker = setInterval(() => {
			if ( this._bridge_message_queue.length === 0 ) {
				return;
			}

			document.title = this._bridge_message_queue.shift();
		}, 100);
	}

	/**
	 * Sends an allowed signal and optional arguments to the backend via the Python<->JS Bridge.
	 *
	 * @arg {...String|Array|Object} args The first arg should always be the name of the signal.
	 *
	 * @example
	 * emit_signal( 'do-some-action' );
	 * emit_signal( 'do-some-action', arg1, arg2 );
	 */
	emit_signal( ...args ) {
		let msg = '[', _args = [];

		if ( $.inArray(args[0], this.signals) < 0 ) {
			this.logger.error(`cmd: "${args[0]}" is not in the list of allowed signals!`);
			return;
		}

		// Convert any non-string args to JSON strings so that we have a single string to send.
		for ( let _arg of args ) {
			if ( Array === typeof _arg || _arg instanceof Object ) {
				_arg = JSON.stringify(_arg);
			} else if ( 'string' === typeof _arg ) {
				_arg = `"${_arg}"`;
			}

			msg = `${msg}${_arg}, `;
		}

		msg = msg.replace(/, $/, '');
		msg = `${msg}]`;

		this.logger.debug(`Emitting signal: "${msg}" via python bridge...`);

		this._bridge_message_queue.push(`_BR::${msg}`);
	}


	/**
	 * Header `mousedown` event callback. Intended to be used to implement window dragging.
	 * There is no official api for our use-case. Still, it appears to be possible. However,
	 * it doesn't work at the moment (probably because of some bug in GTK).
	 *
	 * @arg {jQuery.Event} event
	 *
	 * @todo Find a way to make this work.
	 */
	header_mousedown_cb( event ) {
		let $target = event.target ? $(event.target) : event.currentTarget ? $(event.currentTarget) : null;

		if ( null === $target ) {
			this.logger.debug('no target!');
			return;
		}

		if ( $target.closest('.no-drag').length || true === cnchi._dragging ) {
			this.logger.debug(`mousedown returning! ${cnchi._dragging}`);
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
			this.logger.debug('no target!');
			return;
		}

		if ( $target.closest('.no-drag').length || false === cnchi._dragging ) {
			this.logger.debug(`mouseup returning! ${cnchi._dragging}`);
			return;
		}

		cnchi._dragging = false;

		cnchi.emit_signal('window-dragging-stop', 'window-dragging-stop');
	}

	/**
	 * Handles messages sent from the backend via the Python<->JS Bridge. Messages are
	 * injected into the global scope as an `Object` referenced by a unique variable. The
	 * variable name is then passed to this method as a string so it can access the message.
	 *
	 * @arg msg_obj_var_name
	 */
	js_bridge_handler( msg_obj_var_name ) {
		let data, cmd, args;

		args = window[msg_obj_var_name].args;
		cmd = window[msg_obj_var_name].cmd;

		if ( !cmd.length ) {
			this.logger.error('"cmd" is required!', this.js_bridge_handler);
			return;
		}

		if ( $.inArray(cmd, this.cmds) < 0 ) {
			this.logger.error(
				`cmd: "${cmd}" is not in the list of allowed commands!`, this.js_bridge_handler
			);
			return;
		}

		if ( args.length === 1 ) {
			args = args.pop();
		}

		this.logger.debug(`Running command: ${cmd} with args: ${args}...`, this.js_bridge_handler);

		this[cmd](args);
	}

	page_loaded_handler( event, page ) {
		if ( false === cnchi.loaded ) {
			cnchi.loaded = true;
		}
	}

	register_event_handlers() {
		//$(window).on('page-loaded', (event) => this.page_loaded_handler(event));
		//this.$header.on('mousedown', '*', this.header_mousedown_cb);
		//this.$header.on('mouseup', '*', this.header_mouseup_cb);
	}

	/**
	 * Triggers an event for signal received from backend with optional arguments.
	 *
	 * @arg {String|Array} event Either the event name or an Array where the first item is
	 *                           the event name and remaining items are args to pass to callback.
	 */
	trigger_event( event ) {
		let args = [];

		if ( Array.isArray(event) ) {
			args = event;
			event = args.shift();

			if ( args.length === 1 ) {
				args = args.pop();
			}
		}

		this.logger.debug(`triggering event: ${event} with args: ${args}`, this.trigger_event);

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
class CnchiTab extends CnchiObject {
	/**
	 * Creates a new {@link CnchiTab} object.
	 *
	 * @arg {jQuery}   $tab     {@link CnchiTab.$tab}
	 * @arg {string}   [id]     {@link CnchiTab.id}
	 * @arg {CnchiTab} [parent] {@link CnchiTab.parent}
	 */
	constructor( $tab, id, parent ) {
		super();

		if ( null === $tab && '' === id ) {
			this.logger.error('One of [$tab, id] required!', this.constructor);
			return;
		}

		this.logger.debug([$tab, id, parent]);
		this.$tab = ( $tab instanceof jQuery ) ? $tab : $(`#${id}`);
		this.id = id;
		this.name = this.$tab.attr('data-name');
		this.parent = parent;
		this.is_page = ( null === this.parent );
		this.locked = true;
		this.$tab_button = this.get_tab_button();
		this.previous = null;
		this.next = null;

		this._maybe_unlock();

	}

	_do_unlock() {
		let key = `unlocked_tabs::${this.id}`;

		this.$tab_button.removeClass('locked');
		this.$tab_button.on('click', this.tab_button_clicked_cb);
		localStorage.setItem(key, 'true');
	}

	_maybe_unlock() {
		let key = `unlocked_tabs::${this.id}`,
			unlocked = ( null !== localStorage.getItem(key) );

		if ( true === unlocked || true === this.is_page ) {
			this._do_unlock();
		}
	}

	_tab_button_clicked_handler( $tab_button ) {
		if ( $tab_button.hasClass('locked') ) {
			return;
		}

		let id = $tab_button.children('a').attr('href');

		$(window).trigger('page-change-current-tab', [id.replace('#', '')]);
	}

	get_tab_button() {
		let selector = `[href\$="${this.id}"]`,
			$container = ( true === this.is_page ) ? $('.cnchi_app') : $('.main_content');

		return $container.find('.navigation_buttons').find(selector).parent();
	}

	tab_button_clicked_cb( event ) {
		let $target = $(event.currentTarget),
			$tab_button = $target.closest('.tab');
		console.log(event);

		if ( !$('.header_bottom').has($tab_button).length ) {
			event.preventDefault();
			console.log('clicked!');
			console.log(event);
			_page._tab_button_clicked_handler($tab_button);
		}
	}
}


/**
 * Manages a page in the installation process. A page is actually a top-level tab in the UI that
 * can optionally house a number of other tabs in addition to itself (since a page is also a tab).
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

	constructor( id ) {
		let $page_tabs = $('.page_tab'),
			has_tabs = $page_tabs.length ? true : false,
			$tab = (true === has_tabs) ? $page_tabs.first() : $(`#${id}`);

		super($tab, id, null);

		this.signals = [];
		this.tabs = [];
		this.has_tabs = has_tabs;
		this.current_tab = null;
		this.$page = (true === this.is_page) ? $tab : this.parent.$page;
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
		for ( let [index, value] of this.tabs.entries() ) {
			value.previous = (index > 0) ? this.tabs[index - 1] : this;
			value.next = (index < (this.tabs.length - 1)) ? this.tabs[index + 1] : null;
		}
	}

	_unlock_next_tab_animated() {
		let _this = ( this instanceof CnchiTab ) ? this : this.current_tab,
			$tab_button = _this.$tab_button.next();

		if ( true === _this.has_tabs && _this.current_tab !== _this.tabs[_this.tabs.length + 1] ) {
			$tab_button = this.$tab_button.filter('.main_content .navigation_buttons li').next();
		}

		if ( $tab_button.hasClass('locked') ) {
			$tab_button.on('click', _page.tab_button_clicked_cb).removeClass('locked');
		}

		$tab_button.animateCss('animated tada');
	}

	change_current_tab_cb( event, id ) {
		console.log('change current tab fired!');
		clearInterval(this.next_tab_animation_interval);
		this.reload_element(`#${id}`, this.show_tab);
	}

	get_tab_by_id( id ) {
		let tab;

		for ( let tab_obj of _page.tabs ) {
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
		})
	}

	/**
	 * Locates the tabs' containers in the DOM and uses them to create `CnchiTab` objects for
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

		console.log([url, selector]);

		$old_el.hide(0)
			.promise()
			.done(() => {
				$.get(url, function( data ) {
					$new_el = $(data).find(selector);
					console.log($new_el);

					$old_el.replaceWith($new_el).show(0)
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
						});

					this.current_tab = tab;
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


if ( false === _cnchi_exists ) {
	window.cnchi = new CnchiApp();
	window.Logger = Logger;
	window.CnchiObject = CnchiObject;
	window.CnchiPage = CnchiPage;
	window.CnchiTab = CnchiTab;
	_cnchi_exists = true;
}

