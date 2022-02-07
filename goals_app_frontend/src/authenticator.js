import axios from 'axios'
import {BASE_URL} from "./index";

const BASE_AUTH_URL = `${BASE_URL}/auth/`


export default class Authenticator {
    constructor() {
        this.login = this.#saveCSRFWrapper(this.login)
        this.refreshToken = this.#saveCSRFWrapper(this.refreshToken)
    }

    #saveCSRFWrapper(func) {
        return function (...args) {
            func(args).then(response => localStorage.setItem('csrf_token', response.headers['X-XSRF-TOKEN']))
        }
    }

    register() {
        const url = `${BASE_AUTH_URL}/sign-up/`
        return axios.get(url).then(response => response.data)
    }

    login() {
        const url = `${BASE_AUTH_URL}/sign-in/`
        return axios.get(url).then(response => response.data)
    }

    refreshToken() {
        const url = `${BASE_AUTH_URL}/refresh-token/`
        return axios.get(url).then(response => response.data)
    }
}