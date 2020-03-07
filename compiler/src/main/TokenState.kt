/**
 * OcellusScript Tokenizer States
 * (C) 2020 Marquis Kurt.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

enum class TokenizerState {
    START,
    IN_ID,
    MAYBE_DOCSTRING,
    FINISH,
    ERROR
}