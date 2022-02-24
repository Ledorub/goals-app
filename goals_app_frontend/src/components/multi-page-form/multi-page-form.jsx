import React from "react";
import {callHandlers} from "../../utils";
import deepmerge from "deepmerge";


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
            method: this.props.method
        }
    }

    handlePageSubmit(event, pageState) {
        this.setState(state => deepmerge(state, pageState))
        this.nextStage()
    }

    nextStage() {
        this.setState(state => (++state.stage, state))
    }

    handleSubmit(event, pageState) {
        this.handlePageSubmit(null, pageState)
        const data = deepmerge(this.state, pageState)
        callHandlers(this.props.onSubmit, event, data)
    }

    render() {
        const page = this.props.children[this.state.stage]
        const isLastPage = this.state.stage === this.props.children.length - 1
        this.contextValue.handleSubmit = isLastPage ? this.handleSubmit : this.handlePageSubmit

        return (
            <MultiPageFormContext.Provider value={this.contextValue}>
                {page}
            </MultiPageFormContext.Provider>
        )
    }
}