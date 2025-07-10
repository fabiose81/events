import React from 'react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { validateToken } from '../utils/Validade'
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Image from 'react-bootstrap/Image';

const Main = ({ children }) => {

    const navigate = useNavigate();
    const [username, setUsername] = useState();

    const loadUser = () => {
        const token = validateToken();
        if (token) {
            setUsername(token.username);
        } else {
            navigate("/");
        }
    }

    useEffect(() => {
        loadUser();
    });

    return (
        <>
            {
                username
                &&
                <div>
                    <Navbar className="bg-body-tertiary">

                        <Navbar.Brand>{username}</Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav" />
                        <Nav className="justify-content-end">
                            <Nav.Link href="/" onClick={() => {
                                localStorage.setItem("token", "");
                            }}><Image src="logout.png" style={{ width: "30px", height: "40px" }} />
                            </Nav.Link>
                        </Nav>
                    </Navbar>
                    <React.Fragment>
                        <main className="app-content">
                            {children}
                        </main>
                    </React.Fragment>
                </div>
            }
        </>
    );
}

export default Main