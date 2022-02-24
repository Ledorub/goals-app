import React from "react";
import {PopUpContext} from "../pop-up/pop-up";
import Authenticator from "../../authenticator";
import Form from "../form/form";
import FormInput from "../form-input/form-input";
import Button from "../button/button";


export default class SignInForm extends React.Component {
    static contextType = PopUpContext
    state = {}

    constructor(props) {
        super(props);
        this.onSuccess = this.onSuccess.bind(this)
        this.onError = this.onError.bind(this)
    }

    handleSubmit = (event, data) => {
        new Authenticator().login(data)
            .then(({status}) => {
                if (status === 200) {
                    this.onSuccess()
                }
            })
            .catch(this.onError)
    }

    onSuccess() {
        this.setState({signInWasSuccessful: true})
        setTimeout(this.context.hide, 3000)
    }

    onError(err) {
        this.context.showError(err)
    }

    render() {
        const signInWasSuccessful = this.state.signInWasSuccessful

        return (
            <>
                {signInWasSuccessful
                    ? <img src="./success.png" alt="success" style={{width: "15%"}} />
                    : (
                        <Form name="Sign In" method="post" onSubmit={this.handleSubmit}>
                            <FormInput type="email" label="email" required />
                            <FormInput type="password" label="password" required />
                            <Button type="submit">Sign In</Button>
                        </Form>
                    )
                }
            </>

        )
    }
}