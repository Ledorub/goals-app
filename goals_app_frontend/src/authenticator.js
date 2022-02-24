import axios from 'axios'
import {baseURL} from "./settings";
import {objToFormData, isObjEmpty} from "./utils";

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

    postForm(url, data) {
        if (!url) {
            throw new Error('"url" value is required to post form.')
        }

        if (isObjEmpty(data)) {
            throw new Error('"data" value is required to post form.')
        }

        const formData = objToFormData(data)
        return axios.post(
            url,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        ).then(response => ({
            status: response.status,
            headers: response.headers,
            data: response.data
        }))
    }

    #saveCSRFWrapper(func) {
        return function (...args) {
            return func.apply(this, args)
                .then(response => {
                    const csrfToken = response.headers['x-xsrf-token']
                    csrfToken && localStorage.setItem('csrf_token', csrfToken)
                    return response
                })
                .then(v => {
                    console.log(v)
                    return v
                })
        }
    }

    register(data) {
        const url = new URL('sign-up/', baseAuthURL)
        return this.postForm(url, data)
    }

    login(data) {
        const url = new URL('sign-in/', baseAuthURL)
        return this.postForm(url, data)
    }

    refreshToken() {
        const url = new URL('refresh-token/', baseAuthURL)
        return axios.get(url).then(response => response.data)
    }
}