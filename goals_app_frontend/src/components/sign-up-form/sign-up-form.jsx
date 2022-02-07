import React from 'react'
import FormInput from "../formInput/form-input";
import Button from "../button/button"
import MultiPageForm from "../multi-page-form/multi-page-form";
import FormPage from "../form-page/form-page";
import {formValidator, formFieldValidator} from "../form/form";


export default class SignUpForm extends React.Component {
    constructor(props) {
        super(props);
        this.validators = this.getValidators()
    }

    handleSubmit = () => {}

    getValidators() {
        return Object.entries(this).filter((...[[k, v]]) => k.startsWith('validate') && v)
    }

    validatePasswordsAreSame = formValidator('Provided passwords do not match.')(
        function (fields) {
            return fields['password'] === fields['confirm-password']
        }
    )

    validatePasswordMinLength = formFieldValidator('Password has to be at least 12 chars long.')(
        function (value) {
            return value.length >= 12
        }
    )

    render() {
        const nextPageButton = <Button>Continue</Button>
        const submitButton = <Button type="submit">Sign Up</Button>
        const registrationValidators = [this.validatePasswordsAreSame]

        return (
            <MultiPageForm name="Sign Up" method="post" onSubmit={this.handleSubmit}>
                <FormPage key="registration-page" validators={registrationValidators}>
                    <FormInput type="email" label="email" required />
                    <FormInput type="password" label="password" validators={[this.validatePasswordMinLength]} required />
                    <FormInput type="password" label="confirm password" required />
                    {nextPageButton}
                </FormPage>
                <FormPage key="profile-page">
                    <FormInput label="username" required />
                    <FormInput label="first name?" />
                    <FormInput label="last name?" />
                    {submitButton}
                </FormPage>
            </MultiPageForm>
        )
    }
}