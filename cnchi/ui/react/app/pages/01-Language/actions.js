/*
 * LanguagePage Actions
 *
 * Actions change things in our application. Since we use a uni-directional data flow,
 * specifically redux, we have these actions which are the only way our application interacts
 * with it's state. This guarantees that our state is up to date and nothing messes
 * it up weirdly somewhere.
 *
 * To add a new Action:
 *  1) Create and then import a constant for the action
 *  2) Add a function like this:
 *      export function yourAction(var) {
 *          return { type: YOUR_ACTION_CONSTANT, var: var }
 *      }
 */

import LANGUAGE_SELECTED from '../../constants';


export function languageSelected( language ) {
	return { type: LANGUAGE_SELECTED, language: language };
}

