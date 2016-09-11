/*
 * Core constants
 *
 * Each action has a corresponding type, which the reducer knows and picks up on.
 * To avoid weird typos between the reducer and the actions, we save them as
 * constants here. We prefix them with 'cnchi/SomePage' so we avoid
 * reducers accidentally picking up actions they shouldn't.
 *
 * Follow this format:
 * export const YOUR_ACTION_CONSTANT = 'cnchi/SomePage/YOUR_ACTION_CONSTANT';
 */

export const TITLE_CHANGED = 'cnchi/core/TITLE_CHANGED';

