import Navbar from "./components/navbar/navbar";
import ShowPopUpButton from "./components/show-pop-up-button/show-pop-up-button";
import SignUpForm from "./components/sign-up-form/sign-up-form";
import ButtonAnchor from "./components/button-anchor/button-anchor";

const modalContainer = document.createElement('div')
modalContainer.id = 'modal-container'
document.body.append(modalContainer)

export default function App() {
    return (
        <Navbar
            logoSrc="./logo.png"
            actionButton={
                <ShowPopUpButton popUpContent={SignUpForm}>
                    Sign Up
                </ShowPopUpButton>
            }
        >
            <ButtonAnchor href="some-url" backgroundImage="./archive.png" />
        </Navbar>
    )
}