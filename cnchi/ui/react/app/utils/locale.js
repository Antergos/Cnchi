/*
 * locale.js
 *
 * Copyright © 2016 Antergos
 * Copyright © 2016 Sentry (https://sentry.io)
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

import Jed from 'jed';
import React from 'react';
import { sprintf } from 'sprintf-js';
import _ from 'underscore';


let LOCALE_DEBUG = ( '1' === localStorage.getItem( 'localeDebug' ) ),
	i18n = null;

const t = gettext;
const tN = ngettext;
const tct = gettextComponentTemplate;


function argsInvolveReact( args ) {
	if ( args.some( React.isValidElement ) ) {
		return true;
	}
	if ( args.length == 1 && _.isObject( args[0] ) ) {
		return Object.keys( args[0] ).some( ( key ) => {
			return React.isValidElement( args[0][key] );
		} );
	}
	return false;
}


// zh-cn => zh_CN
function convertToPythonLocaleFormat( language ) {
	let [left, right] = language.split( '-' );
	return left + (
			right ? '_' + right.toUpperCase() : ''
		);
}


function format( formatString, args ) {
	if ( argsInvolveReact( args ) ) {
		return formatForReact( formatString, args );
	} else {
		return sprintf( formatString, ...args );
	}
}


function formatForReact( formatString, args ) {
	let rv = [];
	let cursor = 0;

	// always re-parse, do not cache, because we change the match
	sprintf.parse( formatString ).forEach( ( match, idx ) => {
		if ( _.isString( match ) ) {
			rv.push( match );
		} else {
			let arg = null;
			if ( match[2] ) {
				arg = args[0][match[2][0]];
			} else if ( match[1] ) {
				arg = args[parseInt( match[1], 10 ) - 1];
			} else {
				arg = args[cursor++];
			}

			// this points to a react element!
			if ( React.isValidElement( arg ) ) {
				rv.push( React.cloneElement( arg, { key: idx } ) );
				// not a react element, fuck around with it so that sprintf.format
				// can format it for us.  We make sure match[2] is null so that we
				// do not go down the object path, and we set match[1] to the first
				// index and then pass an array with two items in.
			} else {
				match[2] = null;
				match[1] = 1;
				rv.push( <span key={idx++}>
          {sprintf.format( [match], [null, arg] )}
        </span> );
			}
		}
	} );

	return rv;
}


function gettext( string, ...args ) {
	let rv = i18n.gettext( string );
	if ( args.length > 0 ) {
		rv = format( rv, args );
	}
	return mark( rv );
}


/**
 * special form of gettext where you can render nested react
 * components in template strings.  Example:
 *
 * gettextComponentTemplate('Welcome. Click [link:here]', {
 * root: <p/>,
 * link: <a href="#" />
 * });
 * the root string is always called "root", the rest is prefixed
 * with the name in the brackets
 */
function gettextComponentTemplate( template, components ) {
	let tmpl = parseComponentTemplate( i18n.gettext( template ) );
	return mark( renderComponentTemplate( tmpl, components ) );
}


function getTranslations( language ) {
	language = convertToPythonLocaleFormat( language );
	return require( `/usr/share/locale/${language}/LC_MESSAGES/cnchi.po` );
}


function localeSetup() {
	let selected_locale = localStorage.getItem( 'localeDebug' ),
		locale = null !== selected_locale ? selected_locale : 'en';

	setLocale( locale );
}


function mark( rv ) {
	if ( !LOCALE_DEBUG ) {
		return rv;
	}

	let proxy = {
		$$typeof: Symbol.for( 'react.element' ),
		type: 'span',
		key: null,
		ref: null,
		props: {
			className: 'translation-wrapper',
			children: _.isArray( rv ) ? rv : [rv]
		},
		_owner: null,
		_store: {}
	};

	proxy.toString = function () {
		return '🇦🇹' + rv + '🇦🇹';
	};

	return proxy;
}


function ngettext( singular, plural, ...args ) {
	return mark( format( i18n.ngettext( singular, plural, args[0] || 0 ), args ) );
}


function parseComponentTemplate( string ) {
	let rv = {};

	function process( startPos, group, inGroup ) {
		let regex = /\[(.*?)(:|\])|\]/g;
		let match;
		let buf = [];
		let satisfied = false;

		let pos = regex.lastIndex = startPos;
		while ( (match = regex.exec( string )) !== null ) { // eslint-disable-line no-cond-assign
			let substr = string.substr( pos, match.index - pos );
			if ( substr !== '' ) {
				buf.push( substr );
			}

			if ( match[0] == ']' ) {
				if ( inGroup ) {
					satisfied = true;
					break;
				} else {
					pos = regex.lastIndex;
					continue;
				}
			}

			if ( match[2] == ']' ) {
				pos = regex.lastIndex;
			} else {
				pos = regex.lastIndex = process( regex.lastIndex, match[1], true );
			}
			buf.push( { group: match[1] } );
		}

		let endPos = regex.lastIndex;
		if ( !satisfied ) {
			let rest = string.substr( pos );
			if ( rest ) {
				buf.push( rest );
			}
			endPos = string.length;
		}

		rv[group] = buf;
		return endPos;
	}

	process( 0, 'root', false );

	return rv;
}


function renderComponentTemplate( template, components ) {
	let idx = 0;

	function renderGroup( group ) {
		let children = [];

		(template[group] || []).forEach( ( item ) => {
			if ( _.isString( item ) ) {
				children.push( <span key={idx++}>{item}</span> );
			} else {
				children.push( renderGroup( item.group ) );
			}
		} );

		// in case we cannot find our component, we call back to an empty
		// span so that stuff shows up at least.
		let reference = components[group] || <span key={idx++}/>;
		if ( !React.isValidElement( reference ) ) {
			reference = <span key={idx++}>{reference}</span>;
		}

		if ( children.length > 0 ) {
			return React.cloneElement( reference, { key: idx++ }, children );
		} else {
			return React.cloneElement( reference, { key: idx++ } );
		}
	}

	return renderGroup( 'root' );
}


function setLocale( locale ) {
	let translations = getTranslations( locale );
	i18n = new Jed( {
		domain: 'cnchi',
		locale_data: {
			cnchi: translations
		},
		missing_key_callback( key ) {
			console.log( `[TRANSLATIONS ERROR] - Missing Key: ${key}` );
		},
	} );
}


function setLocaleDebug( value ) {
	sessionStorage.setItem( 'localeDebug', value ? '1' : '0' );
	/*eslint no-console:0*/
	console.log( 'Locale debug is: ', value ? 'on' : 'off', '. Reload page to apply changes!' );
}


function translationsExist( language ) {
	language = convertToPythonLocaleFormat( language );

	try {
		require( `/usr/share/locale/${language}/LC_MESSAGES/cnchi.po` );
	} catch ( err ) {
		return false;
	}
	return true;
}


export {
	argsInvolveReact,
	format,
	formatForReact,
	gettext,
	gettextComponentTemplate,
	localeSetup,
	mark,
	ngettext,
	parseComponentTemplate,
	renderComponentTemplate,
	setLocale,
	setLocaleDebug,
	t,
	tct,
	tN,
};
