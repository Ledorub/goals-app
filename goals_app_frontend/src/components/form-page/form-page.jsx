import React from "react";
import Form from "../form/form";
import {MultiPageFormContext} from "../multi-page-form/multi-page-form";
import {callHandlers} from "../../utils";


export default class FormPage extends React.Component {
    static contextType = MultiPageFormContext

    handleSubmit = (event, ...args) => {
        callHandlers(this.context.handleSubmit, event, ...args)
    }

    render() {
        const context = this.context
        return (
            <Form name={context.formName} method={context.method} onSubmit={this.handleSubmit} {...this.props}>
                {this.props.children}
            </Form>
        )
    }
}