/*
 * saga.js
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

import { take, put, call, fork } from 'redux-saga/effects';
import { eventChannel } from 'redux-saga';

import * as actions from './actions';
import * as action_types from './constants';


function getTitleChangedChannel() {
	return eventChannel( ( emit ) => {
		$(document).on( 'title-changed.cnchi', emit );
		// return cleanup logic (called when chan.close() is invoked)
		return () => {
			$(document).off('title-changed.cnchi');
		};
	} );
}


function* titleChangedChannelWatcher() {
	const titleChangedChannel = yield call( getTitleChangedChannel );

	while ( true ) {
		const event = yield take( titleChangedChannel );

		if ( event ) {
			console.log('title changed!');
			yield put( actions.titleChanged( $(document).title ) );
		}
	}
}


function* titleChangedWatcher() {
	while ( yield take( action_types.TITLE_CHANGED ) ) {
		yield call()
	}
}

export function* rootSaga() {
	// Fork watchers so we can continue execution
	const titleChangedChannelWatcher = yield fork( titleChangedChannelWatcher );
	const titleChangedWatcher = yield fork( titleChangedWatcher );
}