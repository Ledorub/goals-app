import axios from 'axios'
import {baseURL} from "./settings";
import {objToFormData} from "./utils";

const baseAuthURL = new URL('auth/', baseURL)


export default class Authenticator {
    constructor() {
        if (Authenticator._instance) {
            return Authenticator._instance
        }
        Authenticator._instance = this

        this.login = this.#saveCSRFWrapper(this.login)
        this.refreshToken = this.#saveCSRFWrapper(this.refreshToken)
    }

    #saveCSRFWrapper(func) {
        return function (...args) {
            func(args).then(response => localStorage.setItem('csrf_token', response.headers['X-XSRF-TOKEN']))
        }
    }

    register(data) {
        const url = new URL('sign-up/', baseAuthURL)
        const formData = objToFormData(data)
        return axios.post(
            url,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        ).then(response => ({status: response.status, data: response.data}))
    }

    login() {
        const url = new URL('sign-in/', baseAuthURL)
        return axios.get(url).then(response => response.data)
    }

    refreshToken() {
        const url = new URL('refresh-token/', baseAuthURL)
        return axios.get(url).then(response => response.data)
    }
}