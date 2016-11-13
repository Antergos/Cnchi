/**
 * bootstrap.js
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

// 3rd-Party Libs
import React from 'react'
import ReactDOM from 'react-dom';


// This Application
import CnchiApp from './core/app';
import App from './components/App/App';
import { localeSetup } from './utils/locale';



const render = ( initalState ) => {
	localeSetup();
	ReactDOM.render(
		<App initialState={initalState} />,
		document.getElementById( 'cnchi_app' )
	);
};


new CnchiApp( render );
