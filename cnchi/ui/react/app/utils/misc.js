/*
 * utils.js
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

import jQuery from 'jquery';


let _cn = {};


/**
 * Capitalizes a string.
 *
 * @returns {string}
 */
String.prototype.capitalise = function() {
	return this.charAt( 0 ).toUpperCase() + this.slice( 1 );
};


/**
 * Animate an element and once animation ends call callback if one is provided.
 *
 * @arg {String}   animation_name CSS class name for the animation.
 * @arg {function} [callback]     Function to call after the animation completes.
 */
/*jQuery.fn.animateCss = function( animation_name, callback ) {
	let animation_end = 'webkitAnimationEnd animationend';

	this.addClass( animation_name ).one( animation_end, () => {
		setTimeout( () => {
			this.removeClass( animation_name );
		}, 1000 );

		if ( callback ) {
			callback();
		}
	} );
};*/


_cn.inArray = ( item, array ) => {
	if ( ! array instanceof Array ) {
		console.log('[ERROR] inArray(): array must be of type Array!');
		return false;
	}
	return array.findIndex( i => i === item ) > -1;
};


export default _cn;

