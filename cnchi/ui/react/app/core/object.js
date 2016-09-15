/*
 * object.js
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

import CnchiLogger from './logger'


/**
 * A base object for all Cnchi* objects. It sets up the logger and
 * binds `this` to the class for all class methods.
 *
 * @prop {CnchiLogger} logger The logger object.
 */
class CnchiObject {

	constructor() {
		this.logger = new CnchiLogger( this.constructor.name );
		this._bind_this();
	}

	/**
	 * Binds `this` to the class for all class methods.
	 *
	 * @private
	 */
	_bind_this() {
		let excluded = ['constructor', '_bind_this', 'not_excluded'];

		function not_excluded( method, context ) {
			let _excluded = excluded.findIndex( excluded_method => method === excluded_method ) > - 1,
				is_method = 'function' === typeof context[method];

			return is_method && ! _excluded;
		}

		for ( let obj = this; obj; obj = Object.getPrototypeOf( obj ) ) {
			for ( let method of Object.getOwnPropertyNames( obj ) ) {
				if ( not_excluded( method, this ) ) {
					this[method] = this[method].bind( this );
				}
			}
		}
	}
}


export default CnchiObject;
