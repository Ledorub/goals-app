import React from "react";
import ReactDOM from "react-dom";
import Button from "../button/button";
import PopUp from "../pop-up/pop-up";


export default class ShowPopUpButton extends React.Component {
    state = {
        isPopUpActive: false
    }

    showPopUp = () => {
        this.setState({isPopUpActive: true})
    }

    hidePopUp = () => {
        this.setState({isPopUpActive: false})
    }

    render() {
        const isPopUpActive = this.state.isPopUpActive
        const PopUpContent = this.props.popUpContent
        return (
            <>
                <Button
                    {...(!isPopUpActive) && {onClick: this.showPopUp}}
                    className={this.props.className}
                >
                    {this.props.children}
                </Button>
                {isPopUpActive && ReactDOM.createPortal(
                    <PopUp isActive={isPopUpActive} onHide={this.hidePopUp}>
                        <PopUpContent />
                    </PopUp>,
                    document.querySelector('#modal-container')
                )}
            </>
        )
    }
}