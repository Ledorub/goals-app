import React from 'react';
import {callHandlers} from "../../utils";


class FormValidationError extends Error {
    constructor(msg='Unknown form error occurred.') {
        super(msg);
        this.name = this.constructor.name
    }
}

export class FormFieldValidationError extends Error {
    constructor(msg) {
        super(msg);
        this.name = this.constructor.name
    }
}

export const FormContext = React.createContext('')

function genericFormValidator(msg, error) {
    return function (fn) {
        return function (...args) {
            const isValid = fn(...args)
            if (!isValid) {
                throw new error(msg)
            }
            return true
        }
    }
}

export function formValidator(msg) {
    return genericFormValidator(msg, FormValidationError)
}

export function formFieldValidator(msg) {
    return genericFormValidator(msg, FormFieldValidationError)
}


// TODO: Fix fields never get valid after error.
// Better to rewrite all error handling from scratch.
export default class Form extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this)
        this.handleFieldValidation = this.handleFieldValidation.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.state = {
            formValues: {},
            formError: '',
            fieldsErrors: {},
            handleChange: this.handleChange
        }
    }

    handleChange(event) {
        const {name: field, value} = event.target
        this.setState(state => (state.formValues[field] = value, state))
    }

    handleFieldValidation(err) {
        const [[field, msg]] = Object.entries(err)
        this.setState(state => (state.fieldsErrors[field] = msg, state))
    }

    validateForm() {
        let formError = ''

        const validators = this.props.validators
        if (validators) {
            try {
                validators.forEach(v => v(this.state.formValues))
            } catch (err) {
                if (err instanceof FormValidationError) {
                    formError = err.message
                } else {
                    throw err
                }
            }
        }
        this.setState({formError})
        const hasFieldsErrors = Object.values(this.state.fieldsErrors).some(Boolean)
        return !(hasFieldsErrors || formError)
    }

    handleSubmit(event) {
        event.preventDefault()
        const isValid = this.validateForm()
        if (isValid) {
            callHandlers(this.props.onSubmit, event, this.state)
        }
    }

    render() {
        const contextValue = {
            formValues: this.state.formValues,
            fieldsErrors: this.state.fieldsErrors,
            onChange: this.handleChange,
            onValidation: this.handleFieldValidation
        }
        const formError = this.state.formError
        return (
            <FormContext.Provider value={contextValue}>
                <form className="form" method={this.props.method} onSubmit={this.handleSubmit}>
                    <fieldset className="form__fields">
                        <legend className="form__name">{this.props.name}</legend>
                        {!!formError && <p>{formError}</p>}
                        {this.props.children}
                    </fieldset>
                </form>
            </FormContext.Provider>
        )
    }
}