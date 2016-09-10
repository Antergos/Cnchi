/**
 * app.js
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

/* This is the entry file for the application, only contains
 * setup and boilerplate code.
 */

// 3rd-Party Libs
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { applyRouterMiddleware, Router, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import configureStore from './store';
import { install } from 'offline-plugin/runtime';

// This Application
import LanguageProvider from 'containers/LanguageProvider';
import { translationMessages } from '../i18n/i18n';
import { selectLocationState } from 'containers/App/selectors';
import App from 'containers/App';
import createRoutes from './routes';


// Create redux store with history
const initialState = {};
const store = configureStore( initialState, browserHistory );

/* Sync history and store, as the react-router-redux reducer is under the
 * non-default key ("routing"), selectLocationState must be provided for
 * resolving how to retrieve the "route" in the state
 */
const locationState = { selectLocationState: selectLocationState() };
const history = syncHistoryWithStore( browserHistory, store, locationState );

// Set up the router, wrapping all Routes in the App component
const rootRoute = { component: App, childRoutes: createRoutes( store ) };

const render = ( translatedMessages ) => {
	ReactDOM.render(
		<Provider store={store}>
			<LanguageProvider messages={translatedMessages}>
				<Router history={history} routes={rootRoute} render={} />
			</LanguageProvider>
		</Provider>,
		document.getElementById( 'app' )
	);
};

// Hot reloadable translation json files
if ( module.hot ) {
	// modules.hot.accept does not accept dynamic dependencies,
	// have to be constants at compile-time
	module.hot.accept( './i18n', () => {
		render( translationMessages );
	} );
}

render( translationMessages );

// Install ServiceWorker and AppCache last that way we don't install it if the app fails.
install();
