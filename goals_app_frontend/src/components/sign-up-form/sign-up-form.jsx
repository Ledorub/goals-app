import React from 'react'
import FormInput from "../form-input/form-input";
import Button from "../button/button"
import MultiPageForm from "../multi-page-form/multi-page-form";
import FormPage from "../form-page/form-page";
import {formFieldValidator, formValidator} from "../form/form";
import Authenticator from "../../authenticator";
import {minLengthValidator} from "../../validators";
import {PopUpContext} from "../pop-up/pop-up";
import deepmerge from "deepmerge";


export default class SignUpForm extends React.Component {
    static contextType = PopUpContext

    constructor(props) {
        super(props);
        this.validators = this.getValidators()
        this.onSuccess = this.onSuccess.bind(this)
        this.onError = this.onError.bind(this)
        this.state = {}
    }

    handleSubmit = (event, data) => {
        new Authenticator().register(data)
            .then(({status}) => {
                if (status === 201) {
                    this.onSuccess()
                }
            })
            .catch(this.onError)
    }

    onSuccess() {
        this.setState({registrationWasSuccessful: true})
        setTimeout(this.context.hide, 3000)
    }

    onError(err) {
        this.context.showError(err)
    }

    getValidators() {
        return Object.entries(this).filter((...[[k, v]]) => k.startsWith('validate') && v)
    }

    validatePasswordsAreSame = formValidator('Provided passwords do not match.')(
        function (fields) {
            return fields['password'] === fields['confirm-password']
        }
    )

    validatePasswordMinLength = formFieldValidator('Password has to be at least 12 chars long.')(
        minLengthValidator(12)
    )

    render() {
        const nextPageButton = <Button>Continue</Button>
        const submitButton = <Button type="submit">Sign Up</Button>
        const registrationValidators = [this.validatePasswordsAreSame]
        const registrationWasSuccessful = this.state.registrationWasSuccessful

        return (
            <>
                {registrationWasSuccessful
                    ? <img src="./success.png" alt="success" style={{width: "15%"}} />
                    : (
                        <MultiPageForm name="Sign Up" method="post" onSubmit={this.handleSubmit}>
                            <FormPage key="registration-page" validators={registrationValidators}>
                                <FormInput type="email" label="email" required />
                                <FormInput type="password" label="password"
                                           validators={[this.validatePasswordMinLength]}
                                           required />
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
            </>
        )
    }
}