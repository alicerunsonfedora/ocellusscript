/**
 * This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */
function mobileMenu() {
    let menuElement = document.getElementById("nav-mobile-menu");
    menuElement.classList.contains("nav-mobile-open") ? menuElement.classList.replace("nav-mobile-open", "nav-mobile-closed") : menuElement.classList.replace("nav-mobile-closed", "nav-mobile-open")
}