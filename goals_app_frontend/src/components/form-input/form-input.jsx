import React from 'react'
import {callHandlers, capitalize, removeNonAlphaNumericHyphenated} from "../../utils";
import {FormContext, FormFieldValidationError} from "../form/form";
import classNames from "classnames";


export default class FormInput extends React.Component {
    static contextType = FormContext

    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this)
        this.validate = this.validate.bind(this)
        this.name = this.normalizeName()
    }

    normalizeName() {
        const name = this.props.name || removeNonAlphaNumericHyphenated(this.props.label.replace(' ', '-'))
        return name.toLowerCase()
    }

    handleChange(event) {
        const callbacks = this.props.onChange || this.context.onChange
        if (callbacks) {
            callHandlers(callbacks, event)
        } else {
            this.setState({[event.target.name]: event.target.value})
        }
    }

    validate() {
        const value = this.context.formValues[this.name]
        const status = {[this.name]: ''}
        const validators = this.props.validators

        if (!validators) {
            this.context.onValidation(status)
            return true
        }
        try {
            this.props.validators.forEach(validator => validator(value))
        } catch (err) {
            status[this.name] = err.message
            if (err instanceof FormFieldValidationError) {
                this.context.onValidation(status)
            } else {
                throw err
            }
            return false
        }
        this.context.onValidation(status)
        return true
    }

    render() {
        const value = this.context.formValues[this.name] || ''
        const error = this.context.fieldsErrors[this.name]

        return (
            <label className="form-field">
                {capitalize(this.props.label)}
                <input className={classNames(
                    "form-field__input",
                    {
                        "form-field__input_error": error
                    }
                )}
                       name={this.name}
                       type={this.props.type || 'text'}
                       value={value}
                       required={this.props.required}
                       onChange={this.handleChange}
                       onBlur={this.validate}
                />
                {!!error && <p className="form-field__error">{error}</p>}
            </label>
        )
    }
}