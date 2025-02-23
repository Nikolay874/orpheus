import {Container, Navbar} from 'react-bootstrap';
import React from "react";

function Navigation() {
    return <>
        {/* Навбар */}
        <Navbar bg="dark" variant="dark" expand="lg">
            <Container>
                <Navbar.Brand href="#">My Search App</Navbar.Brand>
            </Container>
        </Navbar>
    </>
}


export default Navigation