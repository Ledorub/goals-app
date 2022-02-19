import React from 'react'
import {callHandlers} from "../../utils";

export const PopUpContext = React.createContext({})

const fallbackUi = (
    <>
        <img src="./error.png" alt="error" style={{width: "15%"}} />
        <p>Error happened. Please reload the page.</p>
    </>
)

class ErrorBoundary extends React.Component {
    state = {hasError: false}

    componentDidCatch(error, errorInfo) {
        this.setState({hasError: true})
    }

    render() {
        if (this.state.hasError) {
            return fallbackUi
        }
        return this.props.children
    }

}

export default class PopUp extends React.Component {
    popUpElement = React.createRef()
    state = {
        isActive: this.props.isActive || false,
        hasError: false
    }

    constructor(props) {
        super(props);
        this.hide = this.hide.bind(this)
        this.handleError = this.handleError.bind(this)
        this.hideOnOutsideClick = this.hideOnOutsideClick.bind(this)
        this.contextValue = {
            hide: this.hide,
            showError: this.handleError
        }
    }

    componentDidMount() {
        // Without timeout callback is fired on click that opens pop up (closes immediately).
        setTimeout(() => window.addEventListener('click', this.hideOnOutsideClick))
    }

    componentWillUnmount() {
        window.removeEventListener('click', this.hideOnOutsideClick)
    }

    hideOnOutsideClick({target}) {
        const popUpElement = this.popUpElement.current
        if (!(target === popUpElement || popUpElement.contains(target))) {
            this.hide()
        }
    }

    hide() {
        this.setState({isActive: false})
        callHandlers(this.props.onHide)
    }

    handleError(err) {
        this.setState({hasError: true})
    }

    render() {
        const popUp = (
            <div className="pop-up" ref={this.popUpElement}>
                <div className="pop-up__content">
                    <ErrorBoundary>
                        {this.state.hasError
                            ? fallbackUi
                            : <PopUpContext.Provider value={this.contextValue}>
                                {this.props.children}
                            </PopUpContext.Provider>
                        }
                    </ErrorBoundary>
                </div>
            </div>
        )
        return this.state.isActive ? popUp : null
    }
}