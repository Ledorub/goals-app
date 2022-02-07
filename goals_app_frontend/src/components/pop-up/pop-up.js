import React from 'react'

export default class PopUp extends React.Component {
    state = {
        isActive: false
    }

    constructor(props) {
        super(props);
        this.hide = this.hide.bind(this)
        this.popUpContext = React.createContext(this.hide)
    }

    hide() {
        this.setState({isActive: false})
    }

    render() {
        const context = this.popUpContext
        const popUp = (
            <div className="pop-up">
                <div className="pop-up__content">
                    <context.Provider value={this.hide}>
                        {this.props.children}
                    </context.Provider>
                </div>
            </div>
        )
        return this.state.isActive ? popUp : null
    }
}