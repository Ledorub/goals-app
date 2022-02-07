import React from "react";
import {callHandlers} from "../../utils";


export const MultiPageFormContext = React.createContext('')

export default class MultiPageForm extends React.Component {
    state = {
        stage: 0
    }

    constructor(props) {
        super(props);
        this.handlePageSubmit = this.handlePageSubmit.bind(this)
        this.nextStage = this.nextStage.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.contextValue = {
            formName: this.props.name,
            method: this.props.method,
            handleSubmit: this.handlePageSubmit
        }
    }

    handlePageSubmit(event, pageState) {
        this.setState(pageState)
        this.nextStage()
    }

    nextStage() {
        this.setState(state => (++state.stage, state))
    }

    handleSubmit(event) {
        callHandlers(this.props.onSubmit, event)
    }

    render() {
        const page = this.props.children[this.state.stage]
        return (
            <MultiPageFormContext.Provider value={this.contextValue}>
                {page}
            </MultiPageFormContext.Provider>
        )
    }
}