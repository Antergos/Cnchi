/**
 * reducers.js
 *
 * Copyright © 2016 Antergos
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
 * Combine all reducers in this file and export the combined reducers.
 * If we were to do this in store.js, reducers wouldn't be hot reloadable.
 */

// 3rd-Party Libs
import { fromJS } from 'immutable';
import { combineReducers } from 'redux-immutable';
import { LOCATION_CHANGE } from 'react-router-redux';

// This Application
import globalReducer from 'containers/App/reducer';
import languageProviderReducer from 'containers/LanguageProvider/reducer';


// Initial routing state
const routeInitialState = fromJS( { locationBeforeTransitions: null } );

/**
 * Merge route into the global application state
 */
function routeReducer( state = routeInitialState, action ) {
	switch ( action.type ) {
		case LOCATION_CHANGE:
			return state.merge( { locationBeforeTransitions: action.payload, } );
		default:
			return state;
	}
}

/**
 * Creates the main reducer with the asynchronously loaded ones
 */
export default function createReducer( asyncReducers ) {
	return combineReducers( {
		route: routeReducer,
		global: globalReducer,
		language: languageProviderReducer,
		...asyncReducers,
	} );
}
