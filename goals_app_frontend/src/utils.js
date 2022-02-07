export function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1)
}

export function removeNonAlphaNumeric(str) {
    return str.replace(/[^\P{L}\d]/gu, '')
}

export function removeNonAlphaNumericHyphenated(str) {
    return str.replace(/[^\p{L}\d-]/gu, '')
}

export function addEventListeners(elem, event, callbacks) {
    if (!callbacks) {
        return
    }
    if (typeof callbacks == 'function') {
        elem.addEventListener(event, callbacks)
    } else {
        callbacks.forEach(callback => elem.addEventListener(event, callback))
    }
}

export function callHandlers(handlers, ...args) {
    if (!handlers) {
        return
    }

    if (typeof handlers == 'function') {
        handlers(...args)
    } else {
        handlers.forEach(callback => callback(...args))
    }
}