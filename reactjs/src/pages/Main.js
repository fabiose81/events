import React from 'react';
import { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { validateToken } from '../utils/Validade'
import { MyContext } from '../utils/MyContext';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Image from 'react-bootstrap/Image';
import './Main.css'

const Main = ({ children }) => {

    const contextValue = useContext(MyContext);
    const navigate = useNavigate();
    const [username, setUsername] = useState();
    
    const loadUser = () => {
        const token = validateToken();
        if (token) {
            contextValue.token = token;
            setUsername(token.username);
        } else {
            navigate("/");
        }
    }

    useEffect(() => {
        loadUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <>
            {
                username
                &&
                <div>
                    <Navbar className="bg-body-tertiary justify-content-end">
                        <Navbar.Brand>{username}</Navbar.Brand>
                        <Nav>
                            <Nav.Link href="/" onClick={() => {
                                localStorage.setItem("token", "");
                            }}>
                                <Image src="logout.png" style={{ width: "30px", height: "40px" }} />
                            </Nav.Link>
                        </Nav>
                    </Navbar>
                    <React.Fragment>
                        <main className="main-content">
                            {children}
                        </main>
                    </React.Fragment>
                </div>
            }
        </>
    );
}

export default Main