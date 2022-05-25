import ShowPopUpButton from "./components/show-pop-up-button/show-pop-up-button";
import SignInForm from "./components/sign-in-form/sign-in-form";
import ButtonAnchor from "./components/button-anchor/button-anchor";
import Home from "./components/home/home";
import AppHeader from "./components/app-header/app-header";
import {BrowserRouter, Route, Routes, Outlet} from "react-router-dom";
import React from "react";

const modalContainer = document.createElement('div')
modalContainer.id = 'modal-container'
document.body.append(modalContainer)

const AppLayout = () => (
    <div id="content">
        <Outlet />
    </div>
)

export default function App() {
    return (
        <BrowserRouter>
            <AppHeader
                logoSrc="/logo.png"
                actionButton={
                    <ShowPopUpButton popUpContent={SignInForm}>
                        Sign In
                    </ShowPopUpButton>
                }
            >
                <ButtonAnchor href="some-url" backgroundImage="/archive.png" />
            </AppHeader>
            <Routes>
                <Route element={<AppLayout />}>
                    <Route path="/" element={<Home />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}