/*
 * LanguagePage.jsx
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

// 3rd-Party Libs
import React from 'react'
import { Input, Button } from 'react-materialize';

import CnchiComponent from '../../components/CnchiComponent';
import Grid from '../../components/Grid/Grid';
import { t } from '../../utils/locale';

import '../../assets/css/vendor/magic.css';
import './style.css';
import logo from '../../assets/images/overlay.png'


class LanguagePage extends CnchiComponent {

	constructor( props ) {
		super( props );
	}

	onLanguageSelected( event ) {
		this.props.updateState( 'selectedLanguage', event.target.value );
	}

	render() {
		return (
			<Grid size="100" className="content_wrapper">
				<Grid size="100" className="heading">
					<img src={logo} alt="Antergos logo"/>
					<h1>{ t( 'Welcome To Antergos!' ) }</h1>
					<h3>{ t( 'Please select a language to continue.' ) }</h3>
				</Grid>
				<Grid size="30" prefix="35" suffix="35" className="language_selection">
					<Grid size="100">
						<form>
							<Input
								id="language_select"
								s={12}
								type="select"
								label={ t( 'Installer Language' ) }
								value={ this.props.selectedLanguage ? this.props.selectedLanguage : 'default' }
								onChange={ this.onLanguageSelected }>
								<option key="default" value="default">{ t( 'Choose a language' ) }</option>
								{ this.props.languages.map( ( language ) => {
									return <option key={ language } value={ language }>{ language }</option>
								} )}
							</Input>
						</form>
					</Grid>
					<Grid size="100" className="button_wrapper">
						<Button id="continue_btn" waves="light" floating large className="pink accent-2" icon="forward"/>
					</Grid>
				</Grid>
			</Grid>
		);
	}

}


export default LanguagePage;