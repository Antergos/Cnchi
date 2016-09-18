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
import { Navigation } from '../';
import { Grid } from '../';
import { t } from '../../utils/locale';

import logo from '../../assets/images/overlay.png'


class Header extends CnchiComponent {
	getShowNavigation() {
		let excluded = ['language', 'welcome'];
		return false === _cn.inArray(this.props.currentPage, excluded);
	}
	render() {

		return (
			<Grid size="100" className="grid-parent header">

				{/* ---->>> HEADER TOP ---->>> */}
				<Grid size="100" className="header_top">
					<Grid size="25" suffix="25" className="logo_container">
						<Grid size="25">
							<img src={logo} alt="Antergos logo" className="logo" />
						</Grid>
						<Grid size="75" className="cnchi_title">Cnchi { t( 'Installer' ) }</Grid>
					</Grid>
					<Grid size="25" prefix="25" className="window_buttons">
						<a className="waves-effect waves-light waves-circle btn-flat no-drag">
							<i className="material-icons">remove</i>
						</a>
						<a className="waves-effect waves-light waves-circle btn-flat no-drag">
							<i className="material-icons">fullscreen</i>
						</a>
						<a className="waves-effect waves-light waves-circle btn-flat no-drag">
							<i className="material-icons">close</i>
						</a>
					</Grid>
				</Grid> {/* <<<---- HEADER TOP <<<---- */}

				{/* ---->>> HEADER BOTTOM ---->>> */}
				<Grid size="100" className="header_bottom no-drag">
					{this.props.showNavigation
						? <Navigation currentPage={this.props.currentPage} isTopLevel={ true } />
						: ''}
					<div className="progress">
						<div className="determinate" style={ { width: '8%' } }></div>
					</div>
				</Grid> {/* <<<---- HEADER BOTTOM <<<---- */}

			</Grid>
		)
	}
}


export { Header };