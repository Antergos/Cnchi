/*
 * Navigation.jsx
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

import { Grid } from 'unsemantic';
import classnames from 'classnames';

import { CnchiComponent } from '../';
import { t } from '../../utils/locale';


class Navigation extends CnchiComponent {

	_get_buttons() {
		let navLinkPrefix = this.props.isTopLevel ? 'cnchi://' : '#',
			buttons = [],
			buttonNames = [];

		for ( let button of this.props.navButtons ) {
			let name = `${button[0].toLowerCase().replace( ' ', '_' )}`,
				link = `${navLinkPrefix}${name}`,
				_classes = {
					'tab col s3': true,
					locked: this._isLocked( button ),
					active: this._isActive( button )
				},
				_classes_str = classnames( _classes );

			let output = () => {
				return <li className={_classes_str}>
					<a href={name} className={_classes.active ? 'active' : ''}>
						button[0]
					</a>
				</li>
			};

			buttons.push( output );
			buttonNames.push( name );
		}

		return { buttons, buttonNames };
	}

	render() {
		let buttons, buttonNames = this._get_buttons();

		return (
			<div className="row navigation_buttons">
				<div className="col s12">
					<ul className="tabs">
						{buttons}
					</ul>
				</div>
				{buttonNames.map( ( name ) => {
					return <div id={name} className="col s12"></div>
				} )}
			</div>
		)
	}
}


export { Navigation };