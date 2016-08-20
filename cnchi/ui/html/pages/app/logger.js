/*
 * logger.js
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
 * Sends log messages through the Python<->JS Bridge to our Python logging handler.
 *
 * @prop {String} log_prefix      A string that will be prepended to log messages.
 * @prop {String} _unknown_method A string used for the calling method name when one isn't
 *     provided.
 */
class CnchiLogger {

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
		return `[${this.log_prefix}.${this._get_caller_name( caller )}]: ${msg}`;
	}

	/**
	 * Sends a message to the Python logging facility.
	 *
	 * @arg {String} msg   The message to be sent.
	 * @arg {String} level The logging level to use for the message.
	 * @private
	 */
	_write_log( msg, level ) {
		let esc_msg = msg.replace( /"/g, '\\"' );
		msg = `_BR::["do-log-message", "${level}", "${esc_msg}"]`;

		cnchi._bridge_message_queue.push( msg );
		console.log( msg );
	}

	/**
	 * Sends a message to Python logging facility where logging level == method name.
	 *
	 * @arg {String}          msg         The message to be logged.
	 * @arg {Function|String} [caller=''] The method calling this log method.
	 */
	info( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'info' );
	}

	/**
	 * @see Logger.info
	 */
	debug( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'debug' );
	}

	/**
	 * @see Logger.info
	 */
	warning( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'warning' );
	}

	/**
	 * @see Logger.info
	 */
	error( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'error' );
	}
}


window.CnchiLogger = CnchiLogger;
