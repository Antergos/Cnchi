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

import { CnchiComponent } from '../';
import { Header } from '../';
import { Grid } from '../';
import Pages from '../../pages'

import '../../assets/css/vendor/materialize.css'
import '../../assets/css/vendor/unsemantic-grid.css'
import '../../assets/css/style.css'


class App extends CnchiComponent {

	constructor( props ) {
		super( props );

		this.state = cnchi.app_state;
	}

	render() {
		let page_class_name = `${this.state.current_page.capitalise()}Page`,
			CurrentPage = pages[page_class_name];

		return (
			<Grid isContainer={true} className="grid-parent cnchi_app">
				<Header currentPage={this.state.current_page} />
				<CurrentPage />
			</Grid>
		)
	}
}


export { App };