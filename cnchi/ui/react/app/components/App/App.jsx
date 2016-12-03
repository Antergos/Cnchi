/*
 * Container.jsx
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

import CnchiComponent from '../CnchiComponent';
import Header from '../Header/Header';
import Grid from '../Grid/Grid';
import all_pages from '../../pages';
import _cn from '../../utils/misc';

// import '../../assets/js/materialize.min.js';
// import '../../assets/css/vendor/materialize.css';
import '../../assets/css/vendor/unsemantic-grid.css';
import '../../assets/css/style.css';
import '../../core/global.scss'


class App extends CnchiComponent {

	constructor( props ) {
		super( props );

		this.state = this.props.initialState;
	}

	_getShowNavigation() {
		let excluded = ['Language', 'Welcome'];
		return false === _cn.inArray(this.state.currentPage, excluded);
	}

	updateState( key, value ) {
		let oldState = this.state[this.state.currentPage],
			newState = Object.assign( {}, oldState, {key: value} );

		this.setState(newState);
	}

	render() {
		let page_class_name = `${this.state.currentPage.capitalise()}Page`,
			CurrentPage = all_pages[page_class_name];

		return (
			<Grid isContainer={true} className="grid-parent cnchi_app">
				{this._getShowNavigation()
					? <Header currentPage={this.state.currentPage} />
					: ''}
				<CurrentPage updateState={this.updateState} {...this.state} />
			</Grid>
		)
	}
}


export default App;